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
"""Refresh data stored in the graph database."""

import logging
import os

from prometheus_client import CollectorRegistry, Gauge, Counter, push_to_gateway

from thoth.common import init_logging
from thoth.common import OpenShift
from thoth.storages import __version__ as __storage_version__
from thoth.storages import GraphDatabase


__version__ = '0.6.0'
__git_commit_id__ = os.getenv('OPENSHIFT_BUILD_COMMIT', '')

init_logging()
prometheus_registry = CollectorRegistry()


_LOGGER = logging.getLogger('thoth.graph_refresh_job')

_SOLVER_OUTPUT = os.environ['THOTH_SOLVER_OUTPUT']
_LOG_SOLVER = os.environ.get('THOTH_LOG_SOLVER') == 'DEBUG'

_THOTH_METRICS_PUSHGATEWAY_URL = os.getenv('THOTH_METRICS_PUSHGATEWAY_URL')
_METRIC_RUNTIME = Gauge(
    'graph_refresh_job_runtime_seconds', 'Runtime of graph refresh job in seconds.', [],
    registry=prometheus_registry)
_METRIC_PACKAGES_ADDED = Counter(
    'graph_refresh_job_packages_added_total', 'Number of new and unsolved package-version added.', [],
    registry=prometheus_registry)
_METRIC_DEPENDENT_PACKAGES_ADDED = Counter(
    'graph_refresh_job_dependent_packages_added_total', 'Number package-version to be solved based on a package-version added.', [],
    registry=prometheus_registry)
_METRIC_SOLVERS_SCHEDULED = Counter(
    'graph_refresh_job_solvers_scheduler_total', 'Number of Solvers scheduled.', ['solver'],
    registry=prometheus_registry)


def graph_refresh(graph_hosts: str = None, graph_port: int = None) -> None:
    """Schedule refresh for packages that are not yet analyzed by solver."""
    graph = GraphDatabase(hosts=graph_hosts, port=graph_port)
    graph.connect()

    packages = []
    for package, versions in graph.retrieve_unsolved_pypi_packages().items():
        for version in versions:
            _LOGGER.info(f"Adding new package {package} in version {version}")
            _METRIC_PACKAGES_ADDED.inc()

            packages.append(f"{package}=={version}\n")

        for dependent_package, dependent_versions in graph.retrieve_dependent_packages(package).items():
            for dependent_version in versions:
                _LOGGER.info(f"Adding dependency refresh {dependent_version!r}=={dependent_version!r} "
                             f"from {package}=={version}")
                _METRIC_DEPENDENT_PACKAGES_ADDED.inc()

                packages.append(f"{dependent_package}=={dependent_version}\n")

    if not packages:
        return

    _OPENSHIFT = OpenShift()

    for solver in _OPENSHIFT.get_solver_names():
        for package in packages:
            pod_id = _OPENSHIFT.run_solver(
                solver=solver, debug=_LOG_SOLVER, packages=package, output=_SOLVER_OUTPUT
            )
            _LOGGER.info("Scheduled solver %r for package %r, pod id is %r", solver, package, pod_id)
            _METRIC_SOLVERS_SCHEDULED.labels(solver).inc()


def main():
    """Perform graph refresh job."""
    _LOGGER.debug("Debug mode is on")

    _LOGGER.info(
        f"Version v{__version__}+{__git_commit_id__}.thoth_storages-{__storage_version__}")

    with _METRIC_RUNTIME.time():
        graph_refresh()

    if _THOTH_METRICS_PUSHGATEWAY_URL:
        try:
            _LOGGER.debug(
                f"Submitting metrics to Prometheus pushgateway {_THOTH_METRICS_PUSHGATEWAY_URL}")
            push_to_gateway(_THOTH_METRICS_PUSHGATEWAY_URL, job='graph-refresh',
                            registry=prometheus_registry)
        except Exception as e:
            _LOGGER.exception(
                f'An error occurred pushing the metrics: {str(e)}')


if __name__ == '__main__':
    main()
