from dagster import Definitions
from dagster_dbt import DbtCliResource
from .assets import dbt_project_dbt_assets
from .cloud_assets import simulated_file_move, trigger_dbt_cloud_job
from .jobs import file_to_dbt_cloud_and_tests_job, file_to_dbt_cloud_job, members_job
from .project import dbt_project_project
from .schedules import schedules
from .validation_assets import dbt_tests

defs = Definitions(
    assets=[dbt_project_dbt_assets, simulated_file_move, trigger_dbt_cloud_job, dbt_tests],
    jobs=[members_job, file_to_dbt_cloud_job, file_to_dbt_cloud_and_tests_job],
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=dbt_project_project),
    },
)