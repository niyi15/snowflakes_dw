from pathlib import Path

from dagster_dbt import DbtProject
from dotenv import load_dotenv

# Load local settings even when Dagster starts from the repository workspace.
# Existing runtime environment variables take precedence.
load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=False)

dbt_project_project = DbtProject(
    profiles_dir=Path(__file__).resolve().parents[2] / "dbt_project",
    project_dir=Path(__file__).joinpath("..", "..", "..", "dbt_project").resolve(),
    packaged_project_dir=Path(__file__).joinpath("..", "..", "dbt_project").resolve(),
)
dbt_project_project.prepare_if_dev()