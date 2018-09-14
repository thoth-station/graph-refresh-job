#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# graph-refresh-job
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


__version__ = '0.5.0-dev'
__git_commit_id__ = os.getenv('OPENSHIFT_BUILD_COMMIT', '')

init_logging()


_LOGGER = logging.getLogger('thoth.graph_refresh_job')

_SOLVER_OUTPUT = os.environ['THOTH_SOLVER_OUTPUT']
_LOG_SOLVER = os.environ.get('THOTH_LOG_SOLVER') == 'DEBUG'
_OPENSHIFT = OpenShift()

prometheus_registry = CollectorRegistry()
_METRIC_SECONDS = Gauge(
    'graph_refresh_job_runtime_seconds', 'Runtime of graph refresh job in seconds.',
    registry=prometheus_registry)

_METRIC_UNSOLVED_PYPI_PACKAGES_TOTAL = Counter(
    'graph_refresh_unsolved_pypi_packages', 'Number of unsolved PyPi packages found in Graph Database.',
    registry=prometheus_registry)
_METRIC_SOLVERS_RUN_TOTAL = Counter(
    'graph_refresh_solvers_run', 'Solvers run to solve PyPi packages.',
    registry=prometheus_registry)
_METRIC_PYPI_PACKAGES_HANDLED_BY_SOLVERS_TOTAL = Counter(
    'graph_refresh_pypi_packages_handled_by_solvers', 'PyPi packages handled per solver.',
    registry=prometheus_registry)


def graph_refresh(graph_hosts: str = None, graph_port: int = None) -> None:
    """Schedule refresh for packages that are not yet analyzed by solver."""
    graph = GraphDatabase(hosts=graph_hosts, port=graph_port)
    graph.connect()

    packages = ""
    for package, versions in graph.retrieve_unsolved_pypi_packages().items():
        _METRIC_UNSOLVED_PYPI_PACKAGES_TOTAL.inc()

        for version in versions:
            _LOGGER.info(f"Adding new package {package} in version {version}")
            packages += f"{package}=={version}\n"

        for dependent_package, dependent_versions in graph.retrieve_dependent_packages(package).items():
            for dependent_version in versions:
                _LOGGER.info(f"Adding dependency refresh  {dependent_version!r}=={dependent_version!r} "
                             f"from {package}=={version}")
                packages += f"{dependent_package}=={dependent_version}\n"

    if not packages:
        return

    for solver in _OPENSHIFT.get_solver_names():
        _METRIC_SOLVERS_RUN_TOTAL.inc()

        pod_id = _OPENSHIFT.run_solver(
            solver=solver, debug=_LOG_SOLVER, packages=packages, output=_SOLVER_OUTPUT)
        _LOGGER.info(
            "Scheduled solver %r for packages %r, pod id is %r", solver, packages, pod_id)

    _METRIC_PYPI_PACKAGES_HANDLED_BY_SOLVERS_TOTAL.inc(len(packages))


def main():
    """Perform graph refresh job."""
    _LOGGER.debug("Debug mode is on")

    _LOGGER.info(
        f"Version v{__version__}+{__git_commit_id__}.thoth_storages-{__storage_version__}")

    _THOTH_METRICS_PUSHGATEWAY_URL = os.getenv('THOTH_METRICS_PUSHGATEWAY_URL')

    with _METRIC_SECONDS.time():
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
