"""Simulated file handoff and dbt Cloud job; no files or APIs are changed."""

from dagster import AssetExecutionContext, MaterializeResult, asset


@asset(group_name="file_to_dbt_cloud")
def simulated_file_move(context: AssetExecutionContext) -> MaterializeResult:
    source = "incoming/members.csv"
    destination = "processed/members.csv"
    context.log.info("SIMULATION: would move %s to %s. No file was changed.", source, destination)
    return MaterializeResult(
        metadata={"source": source, "destination": destination, "simulated": True}
    )


@asset(group_name="file_to_dbt_cloud", deps=[simulated_file_move])
def trigger_dbt_cloud_job(context: AssetExecutionContext) -> MaterializeResult:
    account_id = 12345
    job_id = 67890
    run_id = 100001
    context.log.info(
        "SIMULATION: dbt Cloud account %s, job %s, run %s completed successfully. No API call was made.",
        account_id, job_id, run_id,
    )
    return MaterializeResult(
        metadata={
            "simulated": True,
            "dbt_cloud_account_id": account_id,
            "dbt_cloud_job_id": job_id,
            "dbt_cloud_run_id": run_id,
            "status": "SIMULATED_SUCCESS",
        }
    )
