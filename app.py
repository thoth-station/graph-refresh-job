#!/usr/bin/env python3
# thoth-graph-refresh-job
# Copyright(C) 2018, 2019 Fridolin Pokorny
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
from thoth.common import __version__ as __common__version__

from thoth.storages import __version__ as __storage__version__
from thoth.storages import GraphDatabase


__version__ = f"0.6.1+storage.{__storage__version__}.common.{__common__version__}"

init_logging()
prometheus_registry = CollectorRegistry()

_GRAPH_DB = GraphDatabase()
_GRAPH_DB.connect()

_LOGGER = logging.getLogger("thoth.graph_refresh_job")

_SOLVER_OUTPUT = os.getenv("THOTH_SOLVER_OUTPUT", "http://result-api/api/v1/solver-result")
_PACKAGE_ANALYZER_OUTPUT = os.getenv(
    "THOTH_PACKAGE_ANALYZER_OUTPUT",
    "http://result-api/api/v1/package-analysis-result"
)
_SUBGRAPH_CHECK_API = os.getenv("THOTH_SUBGRAPH_CHECK_API", "http://result-api/api/v1/subgraph-check")

_LOG_SOLVER = os.environ.get("THOTH_LOG_SOLVER") == "DEBUG"
THOTH_MY_NAMESPACE = os.getenv("NAMESPACE", "thoth-test-core")

_THOTH_METRICS_PUSHGATEWAY_URL = os.getenv("PROMETHEUS_PUSHGATEWAY_URL")
_METRIC_RUNTIME = Gauge(
    "graph_refresh_job_runtime_seconds",
    "Runtime of graph refresh job in seconds.",
    [],
    registry=prometheus_registry,
)

# Metrics Exporter Metrics
_METRIC_INFO = Gauge(
    "thoth_graph_refresh_job_info",
    "Thoth Graph Refresh Job information",
    ["env", "version"],
    registry=prometheus_registry,
)
_METRIC_INFO.labels(THOTH_MY_NAMESPACE, __version__).inc()

_METRIC_PACKAGES_ADDED = Counter(
    "graph_refresh_job_packages_added_total",
    "Number of new and unsolved package-version added.",
    [],
    registry=prometheus_registry,
)
_METRIC_SOLVERS_SCHEDULED = Counter(
    "graph_refresh_job_solvers_scheduler_total",
    "Number of Solvers scheduled.",
    ["solver"],
    registry=prometheus_registry,
)
_METRIC_SOLVERS_UNSCHEDULED = Counter(
    "graph_refresh_job_solvers_unscheduled_total",
    "Number of Solvers failed to schedule.",
    ["solver"],
    registry=prometheus_registry,
)
_METRIC_PACKAGE_ANALYZERS_SCHEDULED = Counter(
    "graph_refresh_job_package_analyzers_scheduled_total",
    "Number of Package Analyzers scheduled.",
    ["package-analyzer"],
    registry=prometheus_registry,
)
_METRIC_PACKAGE_ANALYZERS_UNSCHEDULED = Counter(
    "graph_refresh_job_package_analyzers_unscheduled_total",
    "Number of Package Analyzers failed to schedule.",
    ["package-analyzer"],
    registry=prometheus_registry,
)
# If set to non-zero value, the graph-refresh will be scheduled for only first N unsolved package-versions.
_THOTH_GRAPH_REFRESH_EAGER_STOP = int(os.getenv("THOTH_GRAPH_REFRESH_EAGER_STOP") or 0)


def graph_refresh_solver() -> None:
    """Schedule refresh for packages that are not yet analyzed by solver."""
    indexes = list(_GRAPH_DB.get_python_package_index_urls())

    openshift = OpenShift()

    packages = []
    # Iterate over all registered solvers and gather packages which were not solved by them.
    for solver_name in openshift.get_solver_names():
        _LOGGER.info("Checking unsolved packages for solver %r", solver_name)
        for package, versions in _GRAPH_DB.retrieve_unsolved_python_packages(
            solver_name
        ).items():
            for version in versions:
                _LOGGER.info(f"Adding new package {package} in version {version}")
                _METRIC_PACKAGES_ADDED.inc()

                packages.append((f"{package}=={version}", solver_name))

    if not packages:
        _LOGGER.info("No unsolved packages found")
        return

    count = 0
    for package, solver in packages:
        try:
            analysis_id = openshift.schedule_solver(
                solver=solver,
                debug=_LOG_SOLVER,
                packages=package,
                indexes=indexes,
                output=_SOLVER_OUTPUT,
                subgraph_check_api=_SUBGRAPH_CHECK_API,
            )
        except Exception as ecx:
            # If we get some errors from OpenShift master - do not retry. Rather schedule the remaining
            # ones and try to schedule the given package in the next run.
            _LOGGER.exception(
                f"Failed to schedule new solver to solve package {package}, the graph refresh job will not "
                "fail but will try to reschedule this in next run"
            )
            _METRIC_SOLVERS_UNSCHEDULED.labels(solver).inc()
            continue

        _LOGGER.info(
            "Scheduled solver %r for package %r, analysis is %r",
            solver,
            package,
            analysis_id,
        )
        _METRIC_SOLVERS_SCHEDULED.labels(solver).inc()

        count += 1
        if _THOTH_GRAPH_REFRESH_EAGER_STOP and count >= _THOTH_GRAPH_REFRESH_EAGER_STOP:
            _LOGGER.info(
                "Eager stop of scheduling new solver runs for unsolved package versions, packages scheduled: %d",
                count,
            )
            return


def graph_refresh_package_analyzer() -> None:
    """Schedule refresh for packages that are not yet analyzed by package analyzer."""
    packages = _GRAPH_DB.retrieve_unanalyzed_python_package_versions()

    if not packages:
        _LOGGER.info("No unanalyzed packages found")
        return

    count = 0
    for item in packages:
        package = item["package_name"]
        version = item["package_version"]
        url = item["index_url"]
        try:
            analysis_id = openshift.schedule_package_analyzer(
                package_name=package,
                package_version=version,
                index_url=url,
                output=_PACKAGE_ANALYZER_OUTPUT,
            )
        except Exception as ecx:
            # If we get some errors from OpenShift master - do not retry. Rather schedule the remaining
            # ones and try to schedule the given package in the next run.
            _LOGGER.exception(
                f"Failed to schedule new package analyzer to analyzer package {package} in version {version}"
                f"from {url}, the graph refresh job will not fail but will try to reschedule this in next run"
            )
            _METRIC_PACKAGE_ANALYZERS_UNSCHEDULED.labels(package).inc()
            continue

        _LOGGER.info(
            "Scheduled package analyzer for package %r, version %r, index_url %r, analysis is %r",
            ,
            package,
            version,
            url,
            analysis_id,
        )
        _METRIC_PACKAGE_ANALYZERS_SCHEDULED.labels(package).inc()

        count += 1
        if _THOTH_GRAPH_REFRESH_EAGER_STOP and count >= _THOTH_GRAPH_REFRESH_EAGER_STOP:
            _LOGGER.info(
                "Eager stop of scheduling new package analyzer runs for unanalyzed packages, packages scheduled: %d",
                count,
            )
            return


def main():
    """Perform graph refresh job."""
    _LOGGER.info(f"Version v{__version__}")
    _LOGGER.debug("Debug mode is on")

    with _METRIC_RUNTIME.time():
        graph_refresh_solver()
        graph_refresh_package_analyzer()

    if _THOTH_METRICS_PUSHGATEWAY_URL:
        try:
            _LOGGER.debug(
                f"Submitting metrics to Prometheus pushgateway {_THOTH_METRICS_PUSHGATEWAY_URL}"
            )
            push_to_gateway(
                _THOTH_METRICS_PUSHGATEWAY_URL,
                job="graph-refresh",
                registry=prometheus_registry,
            )
        except Exception as e:
            _LOGGER.exception(f"An error occurred pushing the metrics: {str(e)}")


if __name__ == "__main__":
    main()
