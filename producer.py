#!/usr/bin/env python3
# thoth-graph-refresh-job-producer
# Copyright(C) 2020 Sai Sankar Gochhayat, Fridolin Pokorny
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

"""Refresh data stored in the graph database.

Produces messages regarding knowledge missing about a certain package. Those messages are handled by thoth-investigator
which decide which workflows need to run to acquire that knowledge.
"""

import logging
import random
import os

from thoth.common import init_logging
from thoth.common import OpenShift
from prometheus_client import CollectorRegistry, Gauge, Counter, push_to_gateway

import thoth.messaging.producer as producer
from thoth.messaging import (
    unresolved_package_message,
    unrevsolved_package_message,
    si_unanalyzed_package_message,
)
from thoth.messaging.unresolved_package import (
    MessageContents as UnresolvedPackageContents,
)
from thoth.messaging.unrevsolved_package import (
    MessageContents as UnrevsolvedPackageContents,
)
from thoth.messaging.si_unanalyzed_package import (
    MessageContents as SIUnanalyzedPackageContents,
)
from thoth.common import __version__ as __common__version__
from thoth.storages import __version__ as __storage__version__
from thoth.messaging import __version__ as __messaging__version__
from thoth.storages import GraphDatabase
from version import __version__

init_logging()

__service_version__ = f"{__version__}+storage.{__storage__version__}.common.{__common__version__}.messaging.{__messaging__version__}"  # noqa: E501

_LOGGER = logging.getLogger("thoth.graph_refresh_job")
_LOGGER.info("Thoth graph refresh producer v%s", __service_version__)

p = producer.create_producer()

_GRAPH_DB = GraphDatabase()
_GRAPH_DB.connect()
_COUNT = (
    int(os.getenv("THOTH_GRAPH_REFRESH_COUNT", GraphDatabase.DEFAULT_COUNT)) or None
)

_OPENSHIFT = OpenShift()

prometheus_registry = CollectorRegistry()
THOTH_DEPLOYMENT_NAME = os.getenv("THOTH_DEPLOYMENT_NAME")
_THOTH_METRICS_PUSHGATEWAY_URL = os.getenv("PROMETHEUS_PUSHGATEWAY_URL")

# Conditional scheduling, by default we schedule everything.
THOTH_GRAPH_REFRESH_SOLVER = int(os.getenv("THOTH_GRAPH_REFRESH_SOLVER", 1))
_LOGGER.info("Schedule Solver Messages set to - %r", THOTH_GRAPH_REFRESH_SOLVER)
THOTH_GRAPH_REFRESH_REVSOLVER = int(os.getenv("THOTH_GRAPH_REFRESH_REVSOLVER", 1))
_LOGGER.info(
    "Schedule Reverse Solver Messages set to - %r", THOTH_GRAPH_REFRESH_REVSOLVER
)
THOTH_GRAPH_REFRESH_SECURITY = int(os.getenv("THOTH_GRAPH_REFRESH_SECURITY", 1))
_LOGGER.info(
    "Schedule Unanalyzed SI Messages set to - %r", THOTH_GRAPH_REFRESH_SECURITY
)
COMPONENT_NAME = "graph-refresh-job"

# Metrics Exporter Metrics
_METRIC_INFO = Gauge(
    "thoth_graph_refresh_job_info",
    "Thoth Graph Refresh Producer information",
    ["env", "version"],
    registry=prometheus_registry,
)

_METRIC_MESSSAGES_SENT = Counter(
    "thoth_graph_refresh_job_messages_sent",
    "Thoth Graph Refresh Producer information sent",
    ["message_type", "env", "version"],
    registry=prometheus_registry,
)

_METRIC_DATABASE_SCHEMA_SCRIPT = Gauge(
    "thoth_database_schema_revision_script",
    "Thoth database schema revision from script",
    ["component", "revision", "env"],
    registry=prometheus_registry,
)

_METRIC_INFO.labels(THOTH_DEPLOYMENT_NAME, __service_version__).inc()
_METRIC_DATABASE_SCHEMA_SCRIPT.labels(
    COMPONENT_NAME, _GRAPH_DB.get_script_alembic_version_head(), THOTH_DEPLOYMENT_NAME
).inc()


def _unsolved_packages(packages: list) -> list:
    """Find packages that are not solved."""
    # Iterate over all registered solvers and gather packages which were not solved by them. Shuffle solvers
    # not to block a solver on another one.
    solver_names = _OPENSHIFT.get_solver_names()
    random.shuffle(solver_names)
    for solver_name in solver_names:
        _LOGGER.info("Checking unsolved packages for solver %r", solver_name)
        solver_info = _OPENSHIFT.parse_python_solver_name(solver_name)
        for (
            package_name,
            version,
            index_url,
        ) in _GRAPH_DB.get_unsolved_python_package_versions_all(
            os_name=solver_info["os_name"],
            os_version=solver_info["os_version"],
            python_version=solver_info["python_version"],
            count=_COUNT,
        ):
            _LOGGER.info(
                "Adding new package %r in version %r on index %r",
                package_name,
                version,
                index_url,
            )
            packages.append((package_name, version, index_url, solver_name))
    return packages


def main() -> None:
    """Produce Kafka messages depending on the knowledge that needs to be acquired for a certain package."""
    if _COUNT:
        _LOGGER.info(
            "Graph refresh will produce at most %d messages per each category of messages.",
            _COUNT,
        )

        factor = 0
        if THOTH_GRAPH_REFRESH_SOLVER:
            _LOGGER.info("unresolved_package_message messages will be sent!")
            factor += 1

        if THOTH_GRAPH_REFRESH_REVSOLVER:
            _LOGGER.info("unrevsolved_package_message messages will be sent!")
            factor += 1

        if THOTH_GRAPH_REFRESH_SECURITY:
            _LOGGER.info("si_unanalyzed_package messages will be sent!")
            factor += 1

        max_messages_sent = _COUNT * factor

    if not max_messages_sent:
        _LOGGER.info("All messages for Graph-refresh-job are disabled.")
        return

    else:
        _LOGGER.info(
            "Graph refresh will produce at most %d messages ", max_messages_sent
        )

    packages: list = []

    solver_messages_sent = 0
    revsolver_messages_sent = 0
    security_messages_sent = 0

    # We dont fetch unsolved packages if both solver and revsolver messages are disabled.
    if THOTH_GRAPH_REFRESH_SOLVER or THOTH_GRAPH_REFRESH_REVSOLVER:
        indexes = _GRAPH_DB.get_python_package_index_urls_all()
        packages = _unsolved_packages(packages=packages)

    if not packages:
        _LOGGER.info("No unsolved packages found")

    # Shuffle not to be dependent on solver message ordering.
    random.shuffle(packages)

    revsolver_packages_seen = set()

    for package_name, package_version, index_url, solver_name in packages:
        if THOTH_GRAPH_REFRESH_SOLVER:
            for index_url in [index_url] if index_url is not None else indexes:
                try:
                    producer.publish_to_topic(
                        p,
                        unresolved_package_message,
                        UnresolvedPackageContents(
                            package_name=package_name,
                            package_version=package_version,
                            index_url=[index_url],
                            solver=solver_name,
                            component_name=COMPONENT_NAME,
                            service_version=__service_version__,
                        ),
                    )
                    _LOGGER.info(
                        "Published message for solver %r for package %r in version %r from index %r",
                        solver_name,
                        package_name,
                        package_version,
                        index_url,
                    )
                    solver_messages_sent += 1
                except Exception as identifier:
                    _LOGGER.exception(
                        "Failed to publish solver message with the following error message: %r",
                        identifier,
                    )

        # Send reverse solver message if not done for this packge, package_version
        if THOTH_GRAPH_REFRESH_REVSOLVER:
            if (package_name, package_version) not in revsolver_packages_seen:
                try:
                    producer.publish_to_topic(
                        p,
                        unrevsolved_package_message,
                        UnrevsolvedPackageContents(
                            package_name=package_name,
                            package_version=package_version,
                            component_name=COMPONENT_NAME,
                            service_version=__service_version__,
                        ),
                    )
                    _LOGGER.info(
                        "Published message for reverse solver message for package %r in version %r",
                        package_name,
                        package_version,
                    )
                    revsolver_messages_sent += 1
                    revsolver_packages_seen.add((package_name, package_version))
                except Exception as identifier:
                    _LOGGER.exception(
                        "Failed to publish reverse solver message with the following error message: %r",
                        identifier,
                    )

    # Lets find the packages solved by solver, but unsolved by SI.
    if THOTH_GRAPH_REFRESH_SECURITY:
        for (
            package_name,
            package_version,
            index_url,
        ) in _GRAPH_DB.get_si_unanalyzed_python_package_versions_all(count=_COUNT):
            try:
                producer.publish_to_topic(
                    p,
                    si_unanalyzed_package_message,
                    SIUnanalyzedPackageContents(
                        package_name=package_name,
                        package_version=package_version,
                        index_url=index_url,
                        component_name=COMPONENT_NAME,
                        service_version=__service_version__,
                    ),
                )
                _LOGGER.info(
                    "Published message for SI unanalyzed package message for package %r in version %r, index_url is %r",
                    package_name,
                    package_version,
                    index_url,
                )
                security_messages_sent += 1
            except Exception as identifier:
                _LOGGER.exception(
                    "Failed to publish SI unanalyzed package message with the following error message: %r",
                    identifier,
                )
    p.flush()

    _METRIC_MESSSAGES_SENT.labels(
        message_type=unresolved_package_message.topic_name,
        env=THOTH_DEPLOYMENT_NAME,
        version=__service_version__,
    ).inc(solver_messages_sent)

    _METRIC_MESSSAGES_SENT.labels(
        message_type=unrevsolved_package_message.topic_name,
        env=THOTH_DEPLOYMENT_NAME,
        version=__service_version__,
    ).inc(revsolver_messages_sent)

    _METRIC_MESSSAGES_SENT.labels(
        message_type=si_unanalyzed_package_message.topic_name,
        env=THOTH_DEPLOYMENT_NAME,
        version=__service_version__,
    ).inc(security_messages_sent)

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
