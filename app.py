#!/usr/bin/env python3

import logging
import os

import requests

from thoth.common import init_logging
from thoth.storages import __version__
from thoth.storages import GraphDatabase


init_logging()


def _get_api_token():
    """Get token to Kubernetes master."""
    try:
        with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as token_file:
            return token_file.read()
    except FileNotFoundError as exc:
        raise FileNotFoundError("Unable to get service account token, please check that service has "
                                "service account assigned with exposed token") from exc


_LOGGER = logging.getLogger('thoth.graph_refresh_job')

KUBERNETES_API_URL = os.getenv('KUBERNETES_API_URL', 'https://kubernetes.default.svc.cluster.local')
KUBERNETES_API_TOKEN = os.getenv('KUBERNETES_API_TOKEN') or _get_api_token()
KUBERNETES_VERIFY_TLS = bool(int(os.getenv('KUBERNETES_VERIFY_TLS', "1")))
THOTH_MIDDLETIER_NAMESPACE = os.environ['THOTH_MIDDLETIER_NAMESPACE']
THOTH_SOLVER_OUTPUT = os.environ['THOTH_SOLVER_OUTPUT']


# TODO: we should move this this hardcoded thing away - one approach is documented in https://trello.com/c/XmxmtOyW
SOLVERS = frozenset({
    'fridex/thoth-solver-fc27',
    'fridex/thoth-solver-fc26'
})


def _do_run_pod(template: dict) -> str:
    """Run defined template in Kubernetes."""
    # We don't care about secret as we run inside the cluster. All builds should hard-code it to secret.
    endpoint = "{}/api/v1/namespaces/{}/pods".format(KUBERNETES_API_URL, THOTH_MIDDLETIER_NAMESPACE)
    _LOGGER.debug("Sending POST request to Kubernetes master %r", KUBERNETES_API_URL)
    response = requests.post(
        endpoint,
        headers={
            'Authorization': 'Bearer {}'.format(KUBERNETES_API_TOKEN),
            'Content-Type': 'application/json'
        },
        json=template,
        verify=KUBERNETES_VERIFY_TLS
    )
    _LOGGER.debug("Kubernetes master response (%d) from %r: %r",
                  response.status_code, KUBERNETES_API_URL, response.text)
    if response.status_code / 100 != 2:
        _LOGGER.error(response.text)
    response.raise_for_status()

    return response.json()['metadata']['name']


def run_solver(solver: str, packages: str) -> str:
    """Run a solver for the given packages."""
    name_prefix = "{}-{}".format(solver, solver.rsplit('/', maxsplit=1)[-1]).replace(':', '-').replace('/', '-')
    template = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "generateName": name_prefix + '-',
            "namespace": THOTH_MIDDLETIER_NAMESPACE,
            "labels": {
                "thothtype": "userpod",
                "thothpod": "analyzer"
            }
        },
        "spec": {
            "restartPolicy": "Never",
            "automountServiceAccountToken": False,
            "containers": [{
                "name": solver.rsplit('/', maxsplit=1)[-1],
                "image": solver,
                "livenessProbe": {
                    "tcpSocket": {
                        "port": 80
                    },
                    "initialDelaySeconds": 100,
                    "failureThreshold": 1,
                    "periodSeconds": 10
                },
                "env": [
                    {"name": "THOTH_SOLVER", "value": str(solver)},
                    # No need to run transitive again
                    {"name": "THOTH_SOLVER_NO_TRANSITIVE", "value": "1"},
                    {"name": "THOTH_SOLVER_PACKAGES", "value": str(packages.replace('\n', '\\n'))},
                    {"name": "THOTH_SOLVER_DEBUG", "value": "1"},  # TODO: hardcoded now
                    {"name": "THOTH_SOLVER_OUTPUT", "value": THOTH_SOLVER_OUTPUT}
                ]
                # TODO resource limits and requests
            }]
        }
    }

    _LOGGER.debug("Requesting to run solver %r with payload %s", solver, template)
    return _do_run_pod(template)


def graph_refresh(graph_hosts=None, graph_port=None):
    """Schedule refresh for packages that are not yet analyzed by solver."""
    graph = GraphDatabase(hosts=graph_hosts, port=graph_port)
    graph.connect()

    packages = ""
    for package, versions in graph.retrieve_unsolved_pypi_packages().items():
        for version in versions:
            packages += f"{package}=={version}\n"

        for dependent_package, dependent_versions in graph.retrieve_dependent_packages(package).items():
            for dependent_version in versions:
                packages += f"{dependent_package}=={dependent_version}\n"

    for solver in SOLVERS:
        pod_id = run_solver(solver, packages)
        _LOGGER.info("Scheduled solver %r for packages %r, pod id is %r", solver, packages, pod_id)


def main():
    _LOGGER.debug("Debug mode is on")
    _LOGGER.info("Version of thoth-storages: %r", __version__)
    graph_refresh()


if __name__ == '__main__':
    main()
