from dagster import Definitions
from dagster_dbt import DbtCliResource
from .assets import dbt_project_dbt_assets
from .jobs import members_job
from .project import dbt_project_project
from .schedules import schedules

defs = Definitions(
    assets=[dbt_project_dbt_assets],
    jobs=[members_job],
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=dbt_project_project),
    },
)