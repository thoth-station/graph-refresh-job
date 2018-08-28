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

from thoth.common import init_logging
from thoth.common import OpenShift
from thoth.storages import __version__ as __storage_version__
from thoth.storages import GraphDatabase


__version__ = '0.4.0'
__git_commit_id__ = os.getenv('OPENSHIFT_BUILD_COMMIT', '')

init_logging()


_LOGGER = logging.getLogger('thoth.graph_refresh_job')

_SOLVER_OUTPUT = os.environ['THOTH_SOLVER_OUTPUT']
_LOG_SOLVER = os.environ.get('THOTH_LOG_SOLVER') == 'DEBUG'
_OPENSHIFT = OpenShift()


def graph_refresh(graph_hosts: str = None, graph_port: int = None) -> None:
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

    if not packages:
        return

    for solver in _OPENSHIFT.get_solver_names():
        pod_id = _OPENSHIFT.run_solver(solver=solver, debug=_LOG_SOLVER, packages=packages, output=_SOLVER_OUTPUT)
        _LOGGER.info("Scheduled solver %r for packages %r, pod id is %r", solver, packages, pod_id)


def main():
    """Perform graph refresh job."""
    _LOGGER.debug("Debug mode is on and hardcoded!")

    _LOGGER.info(
        f"Version v{__version__}+{__git_commit_id__}.thoth_storages-{__storage_version__}")

    graph_refresh()


if __name__ == '__main__':
    main()
