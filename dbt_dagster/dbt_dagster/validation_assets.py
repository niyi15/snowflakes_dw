"""Run real dbt tests after the simulated file and Cloud handoff."""

from dagster import AssetExecutionContext, MaterializeResult, asset
from dagster_dbt import DbtCliResource

from .cloud_assets import trigger_dbt_cloud_job


@asset(group_name="dbt_validation", deps=[trigger_dbt_cloud_job])
def dbt_tests(context: AssetExecutionContext, dbt: DbtCliResource) -> MaterializeResult:
    context.log.info("Running dbt test against the configured dbt target.")
    # This is a regular orchestration asset, so do not emit model materializations.
    dbt.cli(["test"]).wait()
    return MaterializeResult(metadata={"command": "dbt test", "simulated": False})
