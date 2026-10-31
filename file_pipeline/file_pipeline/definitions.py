import csv
import io

from dagster import AssetExecutionContext, AssetSelection, DefaultScheduleStatus, Definitions, ScheduleDefinition, asset, define_asset_job


@asset(group_name="file_processing")
def download_file(context: AssetExecutionContext) -> str:
    """Simulate downloading a small CSV; no network or external file is needed."""
    content = "member_id,name\n1,Alice\n2,Bob\n"
    context.log.info("Simulated download of members.csv")
    context.add_output_metadata({"filename": "members.csv", "simulated_download": True})
    return content


@asset(group_name="file_processing")
def process_file(context: AssetExecutionContext, download_file: str) -> list[dict[str, str]]:
    """Parse the CSV and normalize names; Dagster persists data between steps."""
    rows = list(csv.DictReader(io.StringIO(download_file)))
    processed = [{"member_id": row["member_id"], "name": row["name"].upper()} for row in rows]
    context.log.info("Processed %s CSV rows", len(processed))
    context.add_output_metadata({"row_count": len(processed), "transformation": "uppercase names"})
    return processed


file_processing_job = define_asset_job(
    name="file_processing_job",
    selection=AssetSelection.groups("file_processing"),
)

file_processing_daily_7am = ScheduleDefinition(
    name="file_processing_daily_7am",
    job=file_processing_job,
    cron_schedule="0 7 * * *",
    execution_timezone="America/New_York",
    default_status=DefaultScheduleStatus.RUNNING,
)

defs = Definitions(
    assets=[download_file, process_file],
    jobs=[file_processing_job],
    schedules=[file_processing_daily_7am],
)
