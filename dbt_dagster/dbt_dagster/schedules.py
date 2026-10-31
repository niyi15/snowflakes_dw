from dagster import DefaultScheduleStatus, ScheduleDefinition

from .jobs import members_job

schedules = [
    ScheduleDefinition(
        name="members_every_five_minutes",
        job=members_job,
        cron_schedule="*/5 * * * *",
        execution_timezone="America/New_York",
        default_status=DefaultScheduleStatus.RUNNING,
    ),
]
