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
import asyncio

from thoth.common import init_logging
from thoth.common import OpenShift
from prometheus_client import CollectorRegistry, Gauge

from thoth.messaging import MessageBase
from thoth.messaging.unresolved_package import UnresolvedPackageMessage
from thoth.messaging.unrevsolved_package import UnrevsolvedPackageMessage
from thoth.common import __version__ as __common__version__
from thoth.storages import __version__ as __storage__version__
from thoth.messaging import __version__ as __messaging__version__
from thoth.storages import GraphDatabase
from version import __version__

__service_version__ = f"{__version__}+storage.{__storage__version__}.common.{__common__version__}.messaging.{__messaging__version__}"  # noqa: E501

_LOGGER = logging.getLogger("thoth.graph_refresh_job")
_LOGGER.info("Thoth graph refresh producer v%s", __service_version__)

app = MessageBase().app

init_logging()
_GRAPH_DB = GraphDatabase()
_GRAPH_DB.connect()

_OPENSHIFT = OpenShift()

prometheus_registry = CollectorRegistry()
THOTH_MY_NAMESPACE = os.getenv("NAMESPACE")

# Metrics Exporter Metrics
_METRIC_INFO = Gauge(
    "thoth_graph_refresh_job_info",
    "Thoth Graph Refresh Job information",
    ["env", "version"],
    registry=prometheus_registry,
)
_METRIC_INFO.labels(THOTH_MY_NAMESPACE, __service_version__).inc()


@app.command()
async def main() -> None:
    """Produce Kafka messages depending on the knowledge that needs to be acquired for a certain package."""
    indexes = _GRAPH_DB.get_python_package_index_urls_all()
    packages: list = []
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
        ):
            _LOGGER.info(
                "Adding new package %r in version %r on index %r",
                package_name,
                version,
                index_url,
            )
            packages.append((package_name, version, index_url, solver_name))

    if not packages:
        _LOGGER.info("No unsolved packages found")
        return

    # Shuffle not to be dependent on solver message ordering.
    random.shuffle(packages)

    revsolver_packages_seen = set()
    async_tasks = []
    # Class for solver messages
    unresolved_package = UnresolvedPackageMessage()
    # Class for reverse solver messages
    unrevsolved_package = UnrevsolvedPackageMessage()

    for package_name, package_version, index_url, solver_name in packages:
        for index_url in [index_url] if index_url is not None else indexes:
            try:
                async_tasks.append(
                    unresolved_package.publish_to_topic(
                        unresolved_package.MessageContents(
                            package_name=package_name,
                            package_version=package_version,
                            index_url=[index_url],
                            solver=solver_name,
                        )
                    )
                )
                _LOGGER.info(
                    "Published message for solver %r for package %r in version %r from index %r, analysis is %r",
                    solver_name,
                    package_name,
                    package_version,
                    index_url,
                )
            except Exception as identifier:
                _LOGGER.exception(
                    "Failed to publish solver message with the following error message: %r",
                    identifier,
                )

            # Send reverse solver message if not done for this packge, package_version
            if (package_name, package_version) not in revsolver_packages_seen:
                try:
                    async_tasks.append(
                        unrevsolved_package.publish_to_topic(
                            unrevsolved_package.MessageContents(
                                package_name=package_name,
                                package_version=package_version,
                            )
                        )
                    )
                    _LOGGER.info(
                        "Published message for reverse solver message for package %r in version %r, analysis is %r",
                        package_name,
                        package_version,
                    )
                    revsolver_packages_seen.add((package_name, package_version))
                except Exception as identifier:
                    _LOGGER.exception(
                        "Failed to publish reverse solver message with the following error message: %r",
                        identifier,
                    )

    # Finally gather all the async co-routines
    await asyncio.gather(*async_tasks)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
