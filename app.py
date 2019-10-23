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

_OPENSHIFT = OpenShift()

_LOGGER = logging.getLogger("thoth.graph_refresh_job")

_SOLVER_OUTPUT = os.getenv(
    "THOTH_SOLVER_OUTPUT", "http://result-api/api/v1/solver-result"
)
_PACKAGE_ANALYZER_OUTPUT = os.getenv(
    "THOTH_PACKAGE_ANALYZER_OUTPUT", "http://result-api/api/v1/package-analysis-result"
)
_SUBGRAPH_CHECK_API = os.getenv(
    "THOTH_SUBGRAPH_CHECK_API", "http://result-api/api/v1/subgraph-check"
)

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
    "graph_refresh_job_solvers_scheduled_total",
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
    registry=prometheus_registry,
)
_METRIC_PACKAGE_ANALYZERS_UNSCHEDULED = Counter(
    "graph_refresh_job_package_analyzers_unscheduled_total",
    "Number of Package Analyzers failed to schedule.",
    registry=prometheus_registry,
)
# If set to non-zero value, the graph-refresh will be scheduled for only first N unsolved package-versions.
_THOTH_GRAPH_REFRESH_EAGER_STOP = int(os.getenv("THOTH_GRAPH_REFRESH_EAGER_STOP") or _GRAPH_DB.DEFAULT_COUNT)


def graph_refresh_solver() -> None:
    """Schedule refresh for packages that are not yet analyzed by solver."""
    _LOGGER.info(
        "Eager stop of scheduling new solver runs for unsolved package versions, packages scheduled: %d",
        _THOTH_GRAPH_REFRESH_EAGER_STOP,
    )

    indexes = list(_GRAPH_DB.get_python_package_index_urls())

    packages = []
    # Iterate over all registered solvers and gather packages which were not solved by them.
    for solver_name in _OPENSHIFT.get_solver_names():
        _LOGGER.info("Checking unsolved packages for solver %r", solver_name)
        solver_info = _GRAPH_DB.parse_python_solver_name(solver_name)
        for package_name, version, index_url in _GRAPH_DB.get_unsolved_python_package_versions(
            os_name=solver_info["os_name"],
            os_version=solver_info["os_version"],
            python_version=solver_info["python_version"],
            count=_THOTH_GRAPH_REFRESH_EAGER_STOP
        ):
            _LOGGER.info(
                f"Adding new package %r in version %r on index %r",
                package_name,
                version,
                index_url,
            )
            _METRIC_PACKAGES_ADDED.inc()
            packages.append((package_name, version, index_url, solver_name))

    if not packages:
        _LOGGER.info("No unsolved packages found")
        return

    for package_name, package_version, index_url, solver_name in packages:

        for index_url in [index_url] if index_url is not None else indexes:
            try:
                analysis_id = _OPENSHIFT.schedule_solver(
                    solver=solver_name,
                    debug=_LOG_SOLVER,
                    packages=f"{package_name}=={package_version}",
                    indexes=[index_url],
                    output=_SOLVER_OUTPUT,
                    transitive=False,
                )
            except Exception:
                # If we get some errors from OpenShift master - do not retry. Rather schedule the remaining
                # ones and try to schedule the given package in the next run.
                _LOGGER.exception(
                    f"Failed to schedule new solver to solve package {package_name} in version {package_version}, "
                    "the graph refresh job will not fail but will try to reschedule this in next run"
                )
                _METRIC_SOLVERS_UNSCHEDULED.labels(solver_name).inc()
                continue

            _LOGGER.info(
                "Scheduled solver %r for package %r in version %r from index %r, analysis is %r",
                solver_name,
                package_name,
                package_version,
                index_url,
                analysis_id,
            )
            _METRIC_SOLVERS_SCHEDULED.labels(solver_name).inc()


def graph_refresh_package_analyzer() -> None:
    """Schedule refresh for packages that are not yet analyzed by package analyzer."""
    _LOGGER.info(
        "Eager stop of scheduling new package analyzer runs"
        "for unanalyzed package versions, packages scheduled: %d",
        _THOTH_GRAPH_REFRESH_EAGER_STOP,
    )
    packages = _GRAPH_DB.get_unanalyzed_python_package_versions(
        count=_THOTH_GRAPH_REFRESH_EAGER_STOP
    )

    if not packages:
        _LOGGER.info("No unanalyzed packages found")
        return

    count = 0
    for item in packages:
        package = item["package_name"]
        version = item["package_version"]
        url = item["index_url"]
        try:
            analysis_id = _OPENSHIFT.schedule_package_analyzer(
                package_name=package,
                package_version=version,
                index_url=url,
                output=_PACKAGE_ANALYZER_OUTPUT,
            )
        except Exception:
            # If we get some errors from OpenShift master - do not retry. Rather schedule the remaining
            # ones and try to schedule the given package in the next run.
            _LOGGER.exception(
                f"Failed to schedule new package analyzer to analyzer package {package} in version {version}"
                f"from {url}, the graph refresh job will not fail but will try to reschedule this in next run"
            )
            _METRIC_PACKAGE_ANALYZERS_UNSCHEDULED.inc()
            continue

        _LOGGER.info(
            "Scheduled package analyzer for package %r, version %r, index_url %r, analysis is %r",
            package,
            version,
            url,
            analysis_id,
        )
        _METRIC_PACKAGE_ANALYZERS_SCHEDULED.inc()

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
        if not bool(int(os.getenv("GRAPH_REFRESH_NO_SOLVERS", 0))):
            graph_refresh_solver()
        else:
            _LOGGER.warning(
                "Skipping scheduling of solvers based on user configuration"
            )

        if not bool(int(os.getenv("GRAPH_REFRESH_NO_PACKAGE_ANALYZERS", 0))):
            graph_refresh_package_analyzer()
        else:
            _LOGGER.warning(
                "Skipping scheduling of package-analyzers based on user configuration"
            )

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
