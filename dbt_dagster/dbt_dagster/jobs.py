from dagster import AssetSelection, define_asset_job
from dagster_dbt import build_dbt_asset_selection

from .assets import dbt_project_dbt_assets

members_job = define_asset_job(
    name="members_and_downstream",
    selection=build_dbt_asset_selection(
        [dbt_project_dbt_assets],
        dbt_select="stg_core__members+",
    ),
)

file_to_dbt_cloud_job = define_asset_job(
    name="file_to_dbt_cloud_job",
    selection=AssetSelection.groups("file_to_dbt_cloud"),
)

# Include upstream assets so validation follows this run's file/Cloud steps.
file_to_dbt_cloud_and_tests_job = define_asset_job(
    name="file_to_dbt_cloud_and_tests_job",
    selection=AssetSelection.groups("dbt_validation").upstream(),
)