from pathlib import Path

from dagster_dbt import DbtProject

dbt_project_project = DbtProject(
    profiles_dir=Path.home() / ".dbt",
    project_dir=Path(__file__).joinpath("..", "..", "..", "dbt_project").resolve(),
    packaged_project_dir=Path(__file__).joinpath("..", "..", "dbt-project").resolve(),
)
dbt_project_project.prepare_if_dev()