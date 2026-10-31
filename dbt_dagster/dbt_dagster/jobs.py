from dagster import define_asset_job
from dagster_dbt import build_dbt_asset_selection

from .assets import dbt_project_dbt_assets

members_job = define_asset_job(
    name="members_and_downstream",
    selection=build_dbt_asset_selection(
        [dbt_project_dbt_assets],
        dbt_select="stg_core__members+",
    ),
)
