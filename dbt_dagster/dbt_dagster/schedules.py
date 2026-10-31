from dagster import DefaultScheduleStatus, ScheduleDefinition

from .jobs import members_job

schedules = [
    ScheduleDefinition(
        name="members_every_five_minutes",
        job=members_job,
        cron_schedule="0 6 * * *",
        execution_timezone="America/New_York",
        default_status=DefaultScheduleStatus.STOPPED,
    ),
]
