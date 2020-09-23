thoth-graph-refresh-job
-----------------------

A job for scheduling solver to resolve dependency graphs and package-analyzer to gather digests and ABI of new packages or packages not analyzed yet.

Running the job locally
=======================

You can run this job locally. Run a faust consumer and then run the faust producer with help of app.sh.
The steps to run the consumer is well documented here - `link <https://github.com/thoth-station/messaging/#development-and-testing>`_.
You can run the producer as - `faust -A producer main`

Notes on configuring producer.
==============================
The producer currently produces three types of messages i.e. solver, revsolver and unanalyzed-si messages.
These can be disabled by passing the respective env variables -

* THOTH_GRAPH_REFRESH_SOLVER=0
* THOTH_GRAPH_REFRESH_REVSOLVER=0
* THOTH_GRAPH_REFRESH_SECURITY=0
* THOTH_GRAPH_REFRESH_COUNT=<GraphDatabase.DEFAULT_COUNT> (This restricts the number of messages per solver for solver messages and the total number of messages generated for security and revsolver.)

Insights to graph-refresh job
=============================

The job is run periodically as OpenShift's CronJob. It can be also triggered
automatically by Thoth's monitoring system when there is no workload happening
in Thoth's middletier namespace.

.. note::

  * graph-refresh job is run in Thoth's frontend namespace
  * kafka producer ensures that the messages to schedule solvers and reverse solvers(revsolvers) are sent to the kafka broker

Packages which are not resolved yet might be coming from:

* user requests on advises for software stacks
* user requests for provenance checks
* container image scans
* explicitly registering Python packages to Thoth on Management API endpoint
