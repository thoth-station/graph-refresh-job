#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# thoth-graph-refresh-job
# Copyright(C) 2018 Fridolin Pokorny
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import logging
import os

import requests

from thoth.common import init_logging
from thoth.storages import __version__ as __storage_version__
from thoth.storages import GraphDatabase


__version__ = '0.1.0'
__git_commit_id__ = os.getenv('OPENSHIFT_BUILD_COMMIT', '')

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

KUBERNETES_API_URL = os.getenv(
    'KUBERNETES_API_URL', 'https://kubernetes.default.svc.cluster.local')
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
    endpoint = "{}/api/v1/namespaces/{}/pods".format(
        KUBERNETES_API_URL, THOTH_MIDDLETIER_NAMESPACE)
    _LOGGER.debug("Sending POST request to Kubernetes master %r",
                  KUBERNETES_API_URL)
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
    response.raise_for_status()

    return response.json()['metadata']['name']


def run_solver(solver: str, packages: str) -> str:
    """Run a solver for the given packages."""
    name_prefix = "{}-{}".format(solver, solver.rsplit('/',
                                                       maxsplit=1)[-1]).replace(':', '-').replace('/', '-')
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
                    {"name": "THOTH_SOLVER_PACKAGES", "value": packages},
                    {"name": "THOTH_LOG_SOLVER", "value": "DEBUG"},  # TODO: hardcoded now
                    {"name": "THOTH_SOLVER_OUTPUT", "value": THOTH_SOLVER_OUTPUT}
                ]
                # TODO resource limits and requests
            }]
        }
    }

    _LOGGER.debug("Requesting to run solver %r with payload %s",
                  solver, template)
    return _do_run_pod(template)


def graph_refresh(graph_hosts=None, graph_port=None):
    """Schedule refresh for packages that are not yet analyzed by solver."""
    graph = GraphDatabase(hosts=graph_hosts, port=graph_port)
    graph.connect()

    packages = ""
    for package, versions in graph.retrieve_unsolved_pypi_packages().items():
        for version in versions:
            _LOGGER.info(f"Adding new package {package} in version {version}")
            packages += f"{package}=={version}\n"

        for dependent_package, dependent_versions in graph.retrieve_dependent_packages(package).items():
            for dependent_version in versions:
                _LOGGER.info(f"Adding dependency refresh  {dependent_version!r}=={dependent_version!r} "
                             f"from {package}=={version}")
                packages += f"{dependent_package}=={dependent_version}\n"

    for solver in SOLVERS:
        pod_id = run_solver(solver, packages)
        _LOGGER.info(
            "Scheduled solver %r for packages %r, pod id is %r", solver, packages, pod_id)


def main():
    _LOGGER.debug("Debug mode is on and hardcoded!")

    _LOGGER.info(
        f"Version v{__version__}+{__git_commit_id__}.thoth_storages-{__storage_version__}")

    graph_refresh()


if __name__ == '__main__':
    main()
