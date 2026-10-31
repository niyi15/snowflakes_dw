from dagster import DefaultScheduleStatus, ScheduleDefinition

from .jobs import file_to_dbt_cloud_and_tests_job, members_job

schedules = [
    ScheduleDefinition(
        name="file_to_dbt_cloud_daily_7am",
        job=file_to_dbt_cloud_and_tests_job,
        cron_schedule="0 7 * * *",
        execution_timezone="America/New_York",
        default_status=DefaultScheduleStatus.RUNNING,
    ),
    ScheduleDefinition(
        name="members_every_five_minutes",
        job=members_job,
        cron_schedule="0 6 * * *",
        execution_timezone="America/New_York",
        default_status=DefaultScheduleStatus.STOPPED,
    ),
]
