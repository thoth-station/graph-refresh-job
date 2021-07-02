# Changelog for Thoth's Graph Refresh Job

## [0.4.0] - 2018-Jul-02 - goern

### Added

Starting with this release we have a Zuul-CI pipeline that:

* lints on Pull Requrest and gate/merge

## [0.3.0] - 2018-Jun-12 - goern

### Added

Set resource limits of BuildConfig and Deployment to reasonable values, this will prevent unpredicted behavior on UpShift.

## Release 0.1.1 (2020-07-08T10:13:26)
* issue template for release via bots
* Schedule reverse solver workflow (#428)
* Drop package analyzer (#427)
* migrate manifest for the application to config app (#426)
* Remove result-api leftovers (#425)
* enable version to be managed at release (#424)
* enable pre-commit support for the application (#423)
* :pushpin: Automatic update of dependency thoth-storages from 0.22.12 to 0.24.0 (#421)
* :pushpin: Automatic update of dependency thoth-common from 0.13.8 to 0.14.1 (#420)
* :pushpin: Automatic update of dependency thoth-storages from 0.22.12 to 0.24.0 (#419)
* :pushpin: Automatic update of dependency thoth-common from 0.13.8 to 0.14.1 (#418)
* Update OWNERS
* added a 'tekton trigger tag_release pipeline issue'
* :pushpin: Automatic update of dependency thoth-common from 0.13.7 to 0.13.8
* :pushpin: Automatic update of dependency thoth-storages from 0.22.11 to 0.22.12
* :pushpin: Automatic update of dependency thoth-common from 0.13.6 to 0.13.7
* :pushpin: Automatic update of dependency prometheus-client from 0.7.1 to 0.8.0
* :pushpin: Automatic update of dependency thoth-common from 0.13.5 to 0.13.6
* :pushpin: Automatic update of dependency thoth-common from 0.13.4 to 0.13.5
* :pushpin: Automatic update of dependency thoth-storages from 0.22.10 to 0.22.11
* :pushpin: Automatic update of dependency thoth-common from 0.13.3 to 0.13.4
* :pushpin: Automatic update of dependency thoth-storages from 0.22.9 to 0.22.10
* :pushpin: Automatic dependency re-locking
* :pushpin: Automatic update of dependency thoth-common from 0.13.1 to 0.13.2
* :pushpin: Automatic update of dependency thoth-storages from 0.22.8 to 0.22.9
* :pushpin: Automatic update of dependency thoth-common from 0.13.0 to 0.13.1
* :pushpin: Automatic update of dependency thoth-storages from 0.22.7 to 0.22.8
* :pushpin: Automatic update of dependency thoth-common from 0.12.10 to 0.13.0
* :pushpin: Automatic update of dependency thoth-common from 0.12.9 to 0.12.10
* :pushpin: Automatic update of dependency thoth-common from 0.12.8 to 0.12.9
* :pushpin: Automatic update of dependency thoth-common from 0.12.7 to 0.12.8
* Remove latest version restriction from .thoth.yaml
* :pushpin: Automatic update of dependency thoth-common from 0.12.6 to 0.12.7
* Shuffle solvers not to block, the relative solver positioning is not relevant
* :pushpin: Automatic update of dependency thoth-common from 0.12.5 to 0.12.6
* :pushpin: Automatic update of dependency thoth-common from 0.12.4 to 0.12.5
* :pushpin: Automatic update of dependency thoth-storages from 0.22.6 to 0.22.7
* :pushpin: Automatic update of dependency thoth-storages from 0.22.5 to 0.22.6
* :pushpin: Automatic update of dependency thoth-common from 0.12.3 to 0.12.4
* :pushpin: Automatic update of dependency thoth-common from 0.12.2 to 0.12.3
* :pushpin: Automatic update of dependency thoth-common from 0.12.1 to 0.12.2
* :pushpin: Automatic update of dependency thoth-common from 0.12.0 to 0.12.1
* :pushpin: Automatic update of dependency thoth-common from 0.10.12 to 0.12.0
* :pushpin: Automatic update of dependency thoth-storages from 0.22.4 to 0.22.5
* :pushpin: Automatic update of dependency thoth-storages from 0.22.3 to 0.22.4
* :pushpin: Automatic update of dependency thoth-common from 0.10.11 to 0.10.12
* :pushpin: Automatic update of dependency thoth-common from 0.10.9 to 0.10.11
* Add variables for solver workflows
* :pushpin: Automatic update of dependency thoth-common from 0.10.8 to 0.10.9
* Update version
* Add environment variable to run solvers through Argo
* :pushpin: Automatic update of dependency thoth-storages from 0.22.2 to 0.22.3
* :pushpin: Automatic update of dependency thoth-common from 0.10.7 to 0.10.8
* :pushpin: Automatic update of dependency thoth-common from 0.10.6 to 0.10.7
* :pushpin: Automatic update of dependency thoth-storages from 0.22.1 to 0.22.2
* :pushpin: Automatic update of dependency thoth-common from 0.10.5 to 0.10.6
* :pushpin: Automatic update of dependency thoth-storages from 0.22.0 to 0.22.1
* :pushpin: Automatic update of dependency thoth-storages from 0.21.11 to 0.22.0
* Update .thoth.yaml
* :pushpin: Automatic update of dependency thoth-common from 0.10.4 to 0.10.5
* :pushpin: Automatic update of dependency thoth-common from 0.10.3 to 0.10.4
* :pushpin: Automatic update of dependency thoth-common from 0.10.2 to 0.10.3
* :pushpin: Automatic update of dependency thoth-common from 0.10.1 to 0.10.2
* :pushpin: Automatic update of dependency thoth-common from 0.10.0 to 0.10.1
* :pushpin: Automatic update of dependency thoth-common from 0.9.31 to 0.10.0
* :pushpin: Automatic update of dependency thoth-common from 0.9.30 to 0.9.31
* :pushpin: Automatic update of dependency thoth-storages from 0.21.10 to 0.21.11
* :pushpin: Automatic update of dependency thoth-common from 0.9.29 to 0.9.30
* :pushpin: Automatic update of dependency thoth-storages from 0.21.9 to 0.21.10
* :pushpin: Automatic update of dependency thoth-storages from 0.21.8 to 0.21.9
* :pushpin: Automatic update of dependency thoth-storages from 0.21.7 to 0.21.8
* :pushpin: Automatic update of dependency thoth-common from 0.9.28 to 0.9.29
* :pushpin: Automatic update of dependency thoth-common from 0.9.27 to 0.9.28
* :pushpin: Automatic update of dependency thoth-common from 0.9.26 to 0.9.27
* :pushpin: Automatic update of dependency thoth-storages from 0.21.6 to 0.21.7
* :pushpin: Automatic update of dependency thoth-common from 0.9.25 to 0.9.26
* :pushpin: Automatic update of dependency thoth-storages from 0.21.5 to 0.21.6
* :pushpin: Automatic update of dependency thoth-common from 0.9.24 to 0.9.25
* :pushpin: Automatic update of dependency thoth-storages from 0.21.4 to 0.21.5
* :pushpin: Automatic update of dependency thoth-storages from 0.21.3 to 0.21.4
* :pushpin: Automatic update of dependency thoth-storages from 0.21.2 to 0.21.3
* :pushpin: Automatic update of dependency thoth-storages from 0.21.1 to 0.21.2
* :pushpin: Automatic update of dependency thoth-common from 0.9.23 to 0.9.24
* :pushpin: Automatic update of dependency thoth-storages from 0.21.0 to 0.21.1
* :pushpin: Automatic update of dependency thoth-storages from 0.20.6 to 0.21.0
* :pushpin: Automatic update of dependency thoth-storages from 0.20.5 to 0.20.6
* Do not run adviser from bc in debug mode
* :pushpin: Automatic update of dependency thoth-common from 0.9.22 to 0.9.23
* Do not run adviser from bc in debug mode
* :pushpin: Automatic update of dependency thoth-storages from 0.20.4 to 0.20.5
* :pushpin: Automatic update of dependency thoth-storages from 0.20.3 to 0.20.4
* :pushpin: Automatic update of dependency thoth-storages from 0.20.2 to 0.20.3
* Correctly handle eager stop for packages
* :pushpin: Automatic update of dependency thoth-storages from 0.20.1 to 0.20.2
* Happy new year!
* :pushpin: Automatic update of dependency thoth-storages from 0.20.0 to 0.20.1
* :pushpin: Automatic update of dependency thoth-storages from 0.19.30 to 0.20.0
* Use arbitrary equality for solvers
* Shuffle not to be dependent on relative solver ordering
* :pushpin: Automatic update of dependency thoth-storages from 0.19.27 to 0.19.30
* :pushpin: Automatic update of dependency thoth-common from 0.9.21 to 0.9.22
* Use RHEL instead of UBI
* Update Thoth configuration file and Thoth's s2i configuration
* :pushpin: Automatic update of dependency thoth-storages from 0.19.26 to 0.19.27
* :pushpin: Automatic update of dependency thoth-storages from 0.19.25 to 0.19.26
* :pushpin: Automatic update of dependency thoth-common from 0.9.20 to 0.9.21
* :pushpin: Automatic update of dependency thoth-common from 0.9.19 to 0.9.20
* :pushpin: Automatic update of dependency thoth-storages from 0.19.24 to 0.19.25
* :pushpin: Automatic update of dependency thoth-common from 0.9.18 to 0.9.19
* :pushpin: Automatic update of dependency thoth-common from 0.9.17 to 0.9.18
* :pushpin: Automatic update of dependency thoth-common from 0.9.16 to 0.9.17
* :pushpin: Automatic update of dependency thoth-storages from 0.19.23 to 0.19.24
* :pushpin: Automatic update of dependency thoth-storages from 0.19.22 to 0.19.23
* Add liveness probe
* :pushpin: Automatic update of dependency thoth-storages from 0.19.21 to 0.19.22
* :pushpin: Automatic update of dependency thoth-storages from 0.19.19 to 0.19.21
* :pushpin: Automatic update of dependency thoth-common from 0.9.15 to 0.9.16
* :pushpin: Automatic update of dependency thoth-common from 0.9.14 to 0.9.15
* :pushpin: Automatic update of dependency thoth-storages from 0.19.18 to 0.19.19
* :pushpin: Automatic update of dependency thoth-storages from 0.19.17 to 0.19.18
* :pushpin: Automatic update of dependency thoth-storages from 0.19.15 to 0.19.17
* :pushpin: Automatic update of dependency thoth-storages from 0.19.14 to 0.19.15
* Stop using starting deadline seconds
* Increase eager stop to 200 by default
* Remove list casting
* Change count to all
* Follow the convention
* :pushpin: Automatic update of dependency thoth-storages from 0.19.13 to 0.19.14
* :pushpin: Automatic update of dependency thoth-storages from 0.19.12 to 0.19.13
* updated templates with annotations and param thoth-advise-value
* Fix return value when querying for un-analyzed Python packages
* :pushpin: Automatic update of dependency thoth-storages from 0.19.11 to 0.19.12
* :pushpin: Automatic update of dependency thoth-storages from 0.19.10 to 0.19.11
* Update analyzer function
* Update function to retrieve unsolved packages
* :pushpin: Automatic update of dependency thoth-storages from 0.19.9 to 0.19.10
* :pushpin: Automatic update of dependency thoth-common from 0.9.12 to 0.9.14
* :pushpin: Automatic update of dependency thoth-common from 0.9.11 to 0.9.12
* Remove subgraph checks
* :pushpin: Automatic update of dependency thoth-common from 0.9.10 to 0.9.11
* :pushpin: Automatic update of dependency thoth-storages from 0.19.8 to 0.19.9
* :pushpin: Automatic update of dependency thoth-storages from 0.19.7 to 0.19.8
* Schedule solvers only for unsolved packages based on index
* :pushpin: Automatic update of dependency thoth-storages from 0.19.6 to 0.19.7
* use postgresql hostname from thoth configmap
* :pushpin: Automatic update of dependency thoth-storages from 0.19.5 to 0.19.6
* :pushpin: Automatic update of dependency thoth-common from 0.9.9 to 0.9.10
* :pushpin: Automatic update of dependency thoth-storages from 0.19.4 to 0.19.5
* :pushpin: Automatic update of dependency thoth-common from 0.9.8 to 0.9.9
* :pushpin: Automatic update of dependency thoth-storages from 0.19.3 to 0.19.4
* Provide a way to turn off solver and package-analyzer scheduling
* Fix iterating over versions - we have directly package_name, package_version
* Fix iterating over unsolved Python packages
* :pushpin: Automatic update of dependency thoth-storages from 0.19.2 to 0.19.3
* :pushpin: Automatic update of dependency thoth-storages from 0.19.1 to 0.19.2
* :pushpin: Automatic update of dependency thoth-storages from 0.19.0 to 0.19.1
* :pushpin: Automatic update of dependency thoth-storages from 0.18.6 to 0.19.0
* Use more generic env var names
* Switch from Dgraph to PostgreSQL in deployment
* Add ABI and templates for Package Analyzer
* Add package analyzer to the description
* Remove unused variables
* Schedule solvers without a need to retrieve transitive dependencies
* Registy support for the cronjob image
* Start using Thoth's s2i base image
* Fix invalid metric label
* Initialize Openshift outside of the function
* Delete extra comma
* change graph_refresh_job_solvers_scheduler_total to graph_refresh_job_solvers_scheduled_total
* change graph_refresh_job_package_analyzers_scheduler_total to graph_refresh_job_package_analyzers_scheduled_total
* Place graph_refresh_package_analyzer under the existing timing
* Change graph_refresh to graph_refresh_solver
* One connection to database
* Add graph package analyzer refresh job
* :pushpin: Automatic update of dependency thoth-storages from 0.18.5 to 0.18.6
* :pushpin: Automatic update of dependency thoth-common from 0.9.7 to 0.9.8
* Added config
* Initial dependency lock
* Add missing deployment name for Sentry reports
* Stop using extras in thoth-common
* Fix method name - the name has changed
* Remove old .thoth.yaml configuration file
* :pushpin: Automatic update of dependency thoth-storages from 0.18.4 to 0.18.5
* Change name of Thoth template to make Coala happy
* Start using Thoth in OpenShift's s2i
* :pushpin: Automatic update of dependency thoth-storages from 0.18.3 to 0.18.4
* :pushpin: Automatic update of dependency thoth-common from 0.9.5 to 0.9.6
* :pushpin: Automatic update of dependency thoth-storages from 0.18.1 to 0.18.3
* :pushpin: Automatic update of dependency thoth-storages from 0.18.0 to 0.18.1
* :pushpin: Automatic update of dependency thoth-storages from 0.17.0 to 0.18.0
* :pushpin: Automatic update of dependency thoth-storages from 0.16.0 to 0.17.0
* :pushpin: Automatic update of dependency thoth-storages from 0.15.2 to 0.16.0
* :pushpin: Automatic update of dependency thoth-common from 0.9.4 to 0.9.5
* :pushpin: Automatic update of dependency thoth-storages from 0.15.1 to 0.15.2
* :pushpin: Automatic update of dependency thoth-storages from 0.15.0 to 0.15.1
* :pushpin: Automatic update of dependency thoth-storages from 0.14.8 to 0.15.0
* :pushpin: Automatic update of dependency thoth-common from 0.9.3 to 0.9.4
* :pushpin: Automatic update of dependency thoth-storages from 0.14.7 to 0.14.8
* :pushpin: Automatic update of dependency thoth-common from 0.9.2 to 0.9.3
* :pushpin: Automatic update of dependency thoth-storages from 0.14.6 to 0.14.7
* :pushpin: Automatic update of dependency thoth-common from 0.9.1 to 0.9.2
* :pushpin: Automatic update of dependency thoth-storages from 0.14.5 to 0.14.6
* :pushpin: Automatic update of dependency thoth-storages from 0.14.4 to 0.14.5
* :pushpin: Automatic update of dependency thoth-storages from 0.14.3 to 0.14.4
* :pushpin: Automatic update of dependency thoth-storages from 0.14.2 to 0.14.3
* State also information about TLS certificates
* :pushpin: Automatic update of dependency thoth-storages from 0.14.1 to 0.14.2
* Provide sane defaults for running the job locally
* Document graph refresh job
* :pushpin: Automatic update of dependency thoth-common from 0.9.0 to 0.9.1
* Reformat using black
* Schedule solvers based depending on packages which were not analyzed by these solvers
* :pushpin: Automatic update of dependency prometheus-client from 0.7.0 to 0.7.1
* Remove scheduling of dependent packages
* :pushpin: Automatic update of dependency thoth-common from 0.8.11 to 0.9.0
* Standardize environment variables
* Fix error when serializing parameters to JSON
* Increase resources needed for a job run
* Configure starting deadline seconds to large number
* Update zuul pipeline to use the new version trigger build job
* :pushpin: Automatic update of dependency prometheus-client from 0.6.0 to 0.7.0
* :pushpin: Automatic update of dependency thoth-common from 0.8.7 to 0.8.11
* :pushpin: Automatic update of dependency thoth-storages from 0.14.0 to 0.14.1
* :pushpin: Automatic update of dependency thoth-storages from 0.11.4 to 0.14.0
* Use graph database adapter without explicit values
* :wrench: minor fix template for openshift >=3.11
* :pushpin: Automatic update of dependency thoth-common from 0.8.5 to 0.8.7
* :pushpin: Automatic update of dependency thoth-storages from 0.11.3 to 0.11.4
* :pushpin: Automatic update of dependency thoth-storages from 0.11.2 to 0.11.3
* :pushpin: Automatic update of dependency thoth-storages from 0.11.1 to 0.11.2
* :pushpin: Automatic update of dependency thoth-storages from 0.11.0 to 0.11.1
* :pushpin: Automatic update of dependency thoth-storages from 0.10.0 to 0.11.0
* Adjust graph-refresh-job for Dgraph
* :pushpin: Automatic update of dependency thoth-storages from 0.9.7 to 0.10.0
* :pushpin: Automatic update of dependency thoth-common from 0.8.4 to 0.8.5
* Automatic update of dependency thoth-common from 0.8.3 to 0.8.4
* Automatic update of dependency thoth-common from 0.8.2 to 0.8.3
* Automatic update of dependency thoth-common from 0.8.1 to 0.8.2
* Automatic update of dependency thoth-storages from 0.9.6 to 0.9.7
* Add Thoth's configuration file
* Automatic update of dependency thoth-common from 0.8.0 to 0.8.1
* Automatic update of dependency thoth-common from 0.7.1 to 0.8.0
* :bug: fixed webhhok url
* :bug: added service account to cronjob
* :sparkles: added image stream tag and namespace parameter
* Report solver name which is queried
* Automatic update of dependency prometheus-client from 0.5.0 to 0.6.0
* Get unsolved packages depending on solver
* Automatic update of dependency thoth-storages from 0.9.5 to 0.9.6
* Automatic update of dependency thoth-common from 0.6.0 to 0.7.1
* It's already 2019
* Automatic update of dependency thoth-common from 0.5.0 to 0.6.0
* Schedule solver instead of directly running it
* Reformat using black
* Propagate subgraph-check api on graph refresh
* Automatic update of dependency thoth-storages from 0.9.4 to 0.9.5
* Automatic update of dependency thoth-storages from 0.9.3 to 0.9.4
* Automatic update of dependency thoth-common from 0.4.6 to 0.5.0
* Automatic update of dependency prometheus-client from 0.4.2 to 0.5.0
* Automatic update of dependency thoth-storages from 0.9.0 to 0.9.3
* Automatic update of dependency thoth-common from 0.4.5 to 0.4.6
* Automatic update of dependency thoth-storages from 0.8.0 to 0.9.0
* Propagate index urls to solver runs
* Automatic update of dependency thoth-common from 0.4.4 to 0.4.5
* Automatic update of dependency thoth-common from 0.4.3 to 0.4.4
* Automatic update of dependency thoth-common from 0.4.2 to 0.4.3
* Automatic update of dependency thoth-common from 0.4.1 to 0.4.2
* Automatic update of dependency thoth-common from 0.4.0 to 0.4.1
* Automatic update of dependency thoth-storages from 0.7.6 to 0.8.0
* Extras are not markers
* Automatic update of dependency thoth-storages from 0.7.5 to 0.7.6
* Automatic update of dependency thoth-storages from 0.7.4 to 0.7.5
* Markers are not extras
* added _info metric
* added detailed version string, removed git commit hash from version string
* Automatic update of dependency thoth-storages from 0.7.3 to 0.7.4
* Extras are not markers
* Automatic update of dependency thoth-storages from 0.7.2 to 0.7.3
* Fix log message
* Extras are not markers
* Automatic update of dependency thoth-common from 0.3.16 to 0.4.0
* Automatic update of dependency thoth-storages from 0.7.1 to 0.7.2
* Rename pod id to analysis id
* Extras are not markers
* Automatic update of dependency thoth-storages from 0.7.0 to 0.7.1
* Update thoth-common package
* Delete invalid markers
* Fix extras issues
* Automatic update of dependency thoth-common from 0.3.14 to 0.3.15
* Report any issues when scheduling solvers
* No need to have new line to delimit a single package request
* Automatic update of dependency thoth-common from 0.3.13 to 0.3.14
* Automatic update of dependency thoth-common from 0.3.12 to 0.3.13
* Update app.py
* Stop eagerly after N solvers being scheduled
* Automatic update of dependency thoth-storages from 0.5.4 to 0.6.0
* relocked
* fixing coala issues
* added counting dependant packages
* moved creating on the client closer to its usage
* fixing coala issues
* fixing coala issues
* Automatic update of dependency thoth-common from 0.3.11 to 0.3.12
* update zuul and coala configs to latest standards
* adding logic to push metrics to prometheus pushgateway
* added SENTRY_DSN envvar and removed JANUSGRAPH
* Automatic update of dependency thoth-storages from 0.5.3 to 0.5.4
* Automatic update of dependency thoth-storages from 0.5.2 to 0.5.3
* Automatic update of dependency thoth-common from 0.3.10 to 0.3.11
* Automatic update of dependency thoth-common from 0.3.9 to 0.3.10
* Automatic update of dependency thoth-common from 0.3.8 to 0.3.9
* Automatic update of dependency thoth-common from 0.3.7 to 0.3.8
* Automatic update of dependency thoth-common from 0.3.6 to 0.3.7
* Automatic update of dependency thoth-common from 0.3.5 to 0.3.6
* Automatic update of dependency thoth-common from 0.3.2 to 0.3.5
* Automatic update of dependency thoth-common from 0.3.1 to 0.3.2
* Reduce number of packages in solver run
* Automatic update of dependency thoth-common from 0.3.0 to 0.3.1
* Automatic update of dependency thoth-common from 0.2.7 to 0.3.0
* removed the jenkinsfile and updated the templates
* Automatic update of dependency thoth-common from 0.2.6 to 0.2.7
* Automatic update of dependency thoth-common from 0.2.5 to 0.2.6
* better formating
* Automatic update of dependency thoth-storages from 0.5.1 to 0.5.2
* Automatic update of dependency thoth-common from 0.2.4 to 0.2.5
* Automatic update of dependency thoth-common from 0.2.3 to 0.2.4
* Automatic update of dependency thoth-common from 0.2.2 to 0.2.3
* Automatic update of dependency thoth-storages from 0.5.0 to 0.5.1
* Debug mode is not hardcoded
* Automatic update of dependency thoth-storages from 0.4.0 to 0.5.0
* Automatic update of dependency thoth-storages from 0.3.0 to 0.4.0
* Automatic update of dependency thoth-storages from 0.2.0 to 0.3.0
* Automatic update of dependency thoth-storages from 0.1.1 to 0.2.0
* Decrease cronjob run
* Provide infra namespace configuration for templates
* Use OpenShift object from thoth-common
* Add metadata to job template
* Automatic update of dependency thoth-common from 0.2.1 to 0.2.2
* Automatic update of dependency thoth-storages from 0.1.0 to 0.1.1
* new templates
* Run solver only if there are some packages
* Template default parameter fix
* Template default parameter fix
* Template default parameter fix
* Adjust template labels
* fixed names of the templates
* Introduce CronJob suspend parameter
* Automatic update of dependency thoth-storages from 0.0.33 to 0.1.0
* Automatic update of dependency thoth-common from 0.2.0 to 0.2.1
* Automatic update of dependency thoth-common from 0.2.0 to 0.2.1
* Automatic update of dependency thoth-common from 0.2.0 to 0.2.1
* Initial dependency lock
* Delete Pipfile.lock for relocking dependencies
* Automatic update of dependency thoth-common from 0.1.0 to 0.2.0
* Update .zuul.yaml
* Update .zuul.yaml
* Automatic update of dependency thoth-common from 0.0.9 to 0.1.0
* added a zuul config, removed travis, relocked, CHANGELOG!!
* Use service account token function from thoth-common
* Automatic update of dependency thoth-storages from 0.0.29 to 0.0.32
* set resource limits of BC, DC; relocked Pipfile
* started using a CHANGELOG
* relocked Pipfile
* set resource limits of BC, DC
* Automatic update of dependency thoth-storages from 0.0.28 to 0.0.29
* Automatic update of dependency thoth-storages from 0.0.27 to 0.0.28
* Do not restrict Thoth packages
* Update thoth-common for rsyslog logging
* Add rsyslog logging
* Update thoth-storages
* Run coala in CI
* Update thoth-storages
* Use coala for code checks
* Increase duration of solver so it does not get killed too soon
* Improve logging
* We need to scan also transitive dependencies
* Use common logging configuration
* Fix error with escaped package listing
* Omit non-int division check
* now we get a semver
* added git commit hash to version output
* added KUBERNETES_ to the ENV
* using MIDDLETIER now all over the place
* License headers
* Use GPLv3 LICENSE file
* Provide missing solver output endpoint
* Add missing middletier namespace configuration
* Cronjob should have a service account to run solver pods
* Add missing parameter to method call
* Cast to bool to proberly check for configuration
* Fix naming in openshift templates
* Remove thoth- prefix
* Fix wrong rebase
* Namespace separation is handled by ansible
* Move image stream to a separate file
* Add image stream template
* adding the OWNERS file
* experimenting with adding all the objects we need from within the build pipeline
* fixed the name of the template
* adding Jenkinsfile so that we have a buildpipeline
* Propagate arguments for s2i
* Add OpenShift templates
* Initial implementation
* Use reStructuredText for README file

## Release 0.1.2 (2020-08-18T16:30:53)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.0 to 0.25.1 (#452)
* :pushpin: Automatic update of dependency thoth-common from 0.16.0 to 0.16.1 (#451)
* Readme (#444)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.5 to 0.25.0 (#447)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.5 to 0.25.0 (#446)
* :pushpin: Automatic update of dependency thoth-common from 0.14.2 to 0.16.0 (#445)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.0 to 0.24.5 (#443)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.0 to 0.24.5 (#442)
* :pushpin: Automatic update of dependency thoth-common from 0.14.1 to 0.14.2 (#441)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.0 to 0.24.5 (#440)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.0 to 0.24.5 (#439)
* :pushpin: Automatic update of dependency thoth-common from 0.14.1 to 0.14.2 (#438)
* :pushpin: Automatic update of dependency thoth-common from 0.14.1 to 0.14.2 (#437)
* :pushpin: Automatic update of dependency thoth-common from 0.14.1 to 0.14.2 (#436)

## Release 0.2.0 (2020-09-16T13:09:23)
### Features
* Add env var to configure number of messages sent (#474)
* Update .thoth.yaml (#468)
* Initial producer to replace app.py (#448)
* parse_python_solver_name is function of thoth-common (#456)
### Improvements
* Added producer logic for sending unanalyzed si packages (#478)
* Added component name and service version to messages (#466)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-storages from 0.25.8 to 0.25.9 (#479)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.0 to 0.7.2 (#477)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.0 to 0.7.2 (#476)
* :pushpin: Automatic update of dependency thoth-common from 0.18.3 to 0.19.0 (#475)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.5 to 0.25.8 (#472)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.5 to 0.25.8 (#471)
* :pushpin: Automatic update of dependency thoth-common from 0.17.3 to 0.18.3 (#470)
* :pushpin: Automatic update of dependency thoth-messaging from 0.6.5 to 0.7.0 (#465)
* :pushpin: Automatic update of dependency thoth-common from 0.16.1 to 0.17.3 (#464)
* :pushpin: Automatic update of dependency thoth-messaging from 0.6.4 to 0.6.5 (#461)
* :pushpin: Automatic update of dependency thoth-messaging from 0.6.4 to 0.6.5 (#460)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.2 to 0.25.5 (#459)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.1 to 0.25.2 (#458)

## Release 0.2.1 (2020-09-21T17:25:23)
### Features
* Add missing aicoe yaml (#484)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-storages from 0.25.10 to 0.25.11 (#491)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.3 to 0.7.6 (#489)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.2 to 0.7.3 (#487)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.2 to 0.7.3 (#486)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.9 to 0.25.10 (#485)

## Release 0.2.2 (2020-09-23T19:31:42)
### Features
* Added conditional env variables (#496)

## Release 0.2.3 (2020-09-24T16:28:37)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-common from 0.19.0 to 0.20.0

## Release 0.2.4 (2020-09-24T17:50:16)
### Features
* Make app.sh executable (#506)

## Release 0.2.5 (2020-09-30T17:37:26)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.6 to 0.7.8 (#511)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.11 to 0.25.13 (#510)

## Release 0.2.6 (2020-10-01T07:06:31)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.8 to 0.7.9 (#516)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.13 to 0.25.14 (#515)

## Release 0.2.7 (2020-10-08T13:01:50)
### Features
* Messages sent metrics (#521)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-storages from 0.25.14 to 0.25.15 (#524)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.14 to 0.25.15 (#523)

## Release 0.2.8 (2020-10-08T17:44:43)
### Features
* Use topic_name (#530)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.9 to 0.7.11 (#529)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.9 to 0.7.11 (#528)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.9 to 0.7.11 (#527)

## Release 0.2.9 (2020-11-10T19:33:13)
### Features
* Locked thoth-messaging (#534)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-storages from 0.25.15 to 0.26.0 (#538)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.15 to 0.26.0 (#537)
* :pushpin: Automatic update of dependency thoth-common from 0.20.1 to 0.20.4 (#536)

## Release 0.3.0 (2021-01-20T19:43:36)
### Features
* add maintainer (#553)
* Add schema metric (#550)
* Adjust rebase error (#549)
* update to latest messaging (#548)
* Use deployment-name for metrics (#545)
* :arrow_up: Automatic update of dependencies by kebechet. (#547)
* update .thoth.yaml (#544)
* port to python 38 (#543)
* Updated pipfile lock with new storages (#542)
### Improvements
* removed bissenbay, thanks for your contributions!

## Release 0.3.1 (2021-01-21T21:38:12)
### Features
* Correct base image (#558)
* :arrow_up: Automatic update of dependencies by kebechet. (#556)

## Release 0.3.2 (2021-01-27T14:06:32)
### Features
* :arrow_up: Automatic update of dependencies by kebechet. (#565)
### Bug Fixes
* fix the pre-commit issue in producer.py (#566)
* Relock pipfile for typing_extension issue fix (#564)

## Release 0.3.3 (2021-02-02T19:15:43)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet (#571)

## Release 0.3.4 (2021-03-21T17:54:01)
### Features
* configure ci/cd prow on the app and updated pre-commit
* :arrow_up: Automatic update of dependencies by Kebechet (#579)
* Adjust label metrics (#577)
* :arrow_up: Automatic update of dependencies by Kebechet (#576)
* Add Kebechet templates

## Release 0.3.5 (2021-05-02T23:00:45)
### Features
* constrain thoth-messaging (#582)
### Improvements
* use thoth-messaging >=0.14 (#583)

## Release 0.3.6 (2021-05-17T08:11:41)
### Features
* flush all pending messages (#593)
* :arrow_up: Automatic update of dependencies by Kebechet (#592)

## Release 0.3.7 (2021-06-03T17:35:39)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet
* :hatched_chick: update the prow resource limits (#597)

## Release 0.3.8 (2021-06-09T12:00:24)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet
### Improvements
* make index singular

## Release 0.3.9 (2021-06-14T15:00:24)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet

## Release 0.3.10 (2021-06-30T03:09:05)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet

## Release 0.3.11 (2021-07-02T06:40:28)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
