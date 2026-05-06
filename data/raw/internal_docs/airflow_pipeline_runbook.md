# DAG failures
### Task state changed externally:
There are many potential causes for a task’s state to be changed by a component other than the executor, which might cause some confusion when reviewing task instance or scheduler logs.

Below are some example scenarios that could cause a task’s state to change by a component other than the executor:

If a task’s Dag failed to parse on the worker, the scheduler may mark the task as failed. If confirmed, consider increasing core.dagbag_import_timeout and dag_processor.dag_file_processor_timeout.

The scheduler will mark a task as failed if the task has been queued for longer than scheduler.task_queued_timeout.

If a task instance’s heartbeat times out, it will be marked failed by the scheduler.

A user marked the task as successful or failed in the Airflow UI.

An external script or process used the Airflow REST API to change the state of a task.

### Process terminated by signal:
Sometimes, Airflow or some adjacent system will kill a task instance’s TaskRunner, causing the task instance to fail.

Below we discuss a few common cases.

Dag run timeout:
A dag run timeout can be specified by dagrun_timeout in the dag’s definition. The task process would likely be killed with SIGTERM (exit code -15).

Out of memory error (OOM):
When a task process consumes too much memory for a worker, the best case scenario is it is killed with SIGKILL (exit code -9). Depending on configuration and infrastructure, it is also possible that the whole worker will be killed due to OOM and then the tasks would be marked as failed after failing to heartbeat.

Lingering task supervisor processes:
Under very high concurrency the socket handlers inside the task supervisor may miss the final EOF events from the task process. When this occurs the supervisor believes sockets are still open and will not exit. The workers.socket_cleanup_timeout option controls how long the supervisor waits after the task finishes before force-closing any remaining sockets. If you observe leftover supervisor processes, consider increasing this delay.

# Retries
Apache Airflow retries automatically re-run failed tasks based on configured retries (count) and retry_delay (time interval) parameters within DAGs or operators. These settings handle transient failures (e.g., API timeouts) and can be set globally in default_args or per-task. Use on_retry_callback to trigger actions when retries occur.

## Key Concepts for Airflow Retries
- Configuration Parameters: Define retries (int: number of attempts) and retry_delay (timedelta: wait time).

- Setting Retries: You can set them in default_args for all tasks, or individually in operators like PythonOperator or BashOperator.

- TaskFlow API: Use @task(retries=3) for cleaner syntax.

- Idempotency: Ensure tasks can safely run multiple times without causing data duplication or errors.

- Zombie Task Handling: Airflow automatically detects and retries tasks that were killed unexpectedly (zombies).

# Backfill
Backfill is when you create runs for past dates of a Dag. Airflow provides a mechanism to do this through the CLI and REST API. You provide a Dag, a start date, and an end date, and Airflow will create runs in the range according to the Dag’s schedule.

Backfill does not make sense for Dags that don’t have a time-based schedule.

## Control over data reprocessing
There are three options for reprocessing behavior:

- none - if there’s already a run for this logical date, do not create another, no matter the state

- failed - if a run exists, if the state is failed, create a new run for this date

- completed - if a run exists, if the state is completed or failed, create a new run for this date

If the latest run is still running or is queued, we do not create another run, no matter the chosen reprocessing behavior.

## Concurrency control
You can set max_active_runs on a backfill and it will control how many Dag runs in the backfill can run concurrently. Backfill max_active_runs is applied independently the Dag max_active_runs setting.

## Run ordering
You can run your backfill in reverse, i.e. latest runs first. The CLI option is --run-backwards.

## Dry run
Backfill dry run is a CLI option that will print out the dates that the backfill will consider creating runs for. Whether or not they will be created depends on your chosen reprocessing behavior and the states of any existing runs in the range at the time you actually run the backfill.

## Example
Backfill can be created from either the CLI or the UI.

For CLI, below is an example command:

airflow backfill create --dag-id tutorial \
    --start-date 2015-06-01 \
    --end-date 2015-06-07 \
    --reprocessing-behavior failed \
    --max-active-runs 3 \
    --run-backwards \
    --dag-run-conf '{"my": "param"}'

For UI, follow the following steps:

1. Navigate to a Dag’s Details page and click Trigger.

2. In the pop-up window, select Backfill.

3. Fill in the form:
- Date range: set “From” and “To” logical datetimes for the backfill window.

- Reprocess behavior: choose one of Missing Runs, Missing and Errored Runs, or All Runs.

- Max active runs: limit concurrent backfill runs for this backfill.

- Run backwards: execute most recent intervals first.

- Advanced Config: optionally provide JSON dag_run.conf.

- If the Dag is paused, you can Unpause it in the same window.
# Task Dependencies
A Task/Operator does not usually live alone; it has dependencies on other tasks (those upstream of it), and other tasks depend on it (those downstream of it). Declaring these dependencies between tasks is what makes up the Dag structure.

There are two main ways to declare individual task dependencies. The recommended one is to use the >> and << operators:

first_task >> [second_task, third_task]
third_task << fourth_task

There are also shortcuts to declaring more complex dependencies. If you want to make a list of tasks depend on another list of tasks, you can’t use either of the approaches above, so you need to use cross_downstream:

from airflow.sdk import cross_downstream

Replaces
[op1, op2] >> op3
and [op1, op2] >> op4

cross_downstream([op1, op2], [op3, op4])

Chain can also do pairwise dependencies for lists the same size (this is different from the cross dependencies created by cross_downstream!):

from airflow.sdk import chain

Replaces
op1 >> op2 >> op4 >> op6 and 
op1 >> op3 >> op5 >> op6

chain(op1, [op2, op3], [op4, op5], op6)

# SLA Misses
In Apache Airflow, a Service Level Agreement (SLA) miss occurs when a task does not complete within a specified time. 
When an SLA is missed, Airflow records the event in its metadata database and can trigger automated alerts.

## Key Concepts of SLAs
Definition: An SLA is the maximum expected time for a task to reach a successful state.

Configuration: You set an SLA by passing a timedelta object to the sla parameter of a task or operator.

Measurement: The SLA timer starts from the logical date (execution date) of the DAG run, not the actual start time of the task. For example, if a daily DAG with a logical date of 12:00 AM has a 1-hour SLA, the miss is triggered if the task isn't finished by 1:00 AM.

# Logging & Monitoring
Since data pipelines are generally run without any manual supervision, observability is critical.

Airflow has support for multiple logging mechanisms, as well as a built-in mechanism to emit metrics for gathering, processing, and visualization in other downstream systems. The logging capabilities are critical for diagnosis of problems which may occur in the process of running data pipelines.

In addition to the standard logging and metrics capabilities, Airflow supports the ability to detect errors in the operation of Airflow itself, using an Airflow health check. Since Airflow is generally used for running data pipelines in production, it also supports real-time error notification via integration with Sentry.

