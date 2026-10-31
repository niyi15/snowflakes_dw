# dbt and Dagster setup

These instructions use Windows PowerShell. Run the commands in order. The repository contains an existing dbt project (`dbt_project`) and Dagster project (`dbt_dagster`); neither needs to be scaffolded again.

## 1. Open the repository

```powershell
cd C:\Users\olada\Documents\PSECU_project\sql_dagster\snowflakes_dw
```

Prerequisites:

- Python 3.12, available through the Windows Python launcher (`py -3.12`).
- Access to the target SQL Server database and its connection details.
- A Microsoft ODBC Driver for SQL Server matching the driver configured in your dbt profile.

Despite the repository name, the current Python package configuration uses `dbt-sqlserver`.

## 2. Create and activate .venv312

Create the environment once; skip creation when `.venv312` already exists:

```powershell
py -3.12 -m venv .venv312
```

Activate it each time you open a new terminal:

```powershell
.\.venv312\Scripts\Activate.ps1
python --version
python -m pip install --upgrade pip
```

The prompt should begin with `(.venv312)` and Python should report version 3.12.x.

If PowerShell blocks activation scripts, allow them for this terminal session, then activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv312\Scripts\Activate.ps1
```

## 3. Install the project and packages

From the repository root, install the existing Dagster package in editable mode with its development dependencies:

```powershell
python -m pip install -e ".\dbt_dagster[dev]"
python -m pip check
dbt --version
dagster --version
```

This installs the following declared packages and their dependencies:

| Package | Purpose |
| --- | --- |
| `dagster` | Orchestration and CLI |
| `dagster-webserver` | Local Dagster UI, included by the `dev` extra |
| `dagster-dbt` | dbt integration and scaffolding CLI |
| `dagster-cloud` | Included by the generated project dependency list |
| `dbt-core<1.12` | dbt Core, constrained by this project's package metadata |
| `dbt-sqlserver<1.12` | SQL Server adapter, constrained by this project's package metadata |

Use this installation command rather than separately upgrading dbt beyond the project's constraints. The pre-existing environment was observed to have dbt Core 1.12.6 and dbt-sqlserver 1.12.1; installing the project may replace those versions to satisfy its metadata.

The ODBC driver is a separate Windows installation, not a pip package.

## 4. Configure the dbt profile

The project specifies `profile: 'snowflakes_dw'`. Its connection profile belongs in:

```text
C:\Users\olada\.dbt\profiles.yml
```

If that file already exists and contains the correct connection, keep it. Otherwise, create the directory and open the file:

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.dbt"
notepad "$env:USERPROFILE\.dbt\profiles.yml"
```

Configure a top-level profile named `snowflakes_dw`, with a target and SQL Server output containing your server, database, schema, authentication settings, and installed ODBC driver. Use your organization's actual connection settings. Keep credentials outside this repository.

Dagster's `dbt_dagster/dbt_dagster/project.py` explicitly selects this profile directory:

```python
profiles_dir=Path.home() / ".dbt",
```

The dbt project directory and profile directory are different: `dbt_project.yml` is in the repository's `dbt_project` folder, while `profiles.yml` is in your user profile's `.dbt` folder.

## 5. Validate and run dbt

From the repository root:

```powershell
cd .\dbt_project
dbt debug --profiles-dir "$env:USERPROFILE\.dbt"
dbt parse --profiles-dir "$env:USERPROFILE\.dbt"
```

Fix any connection or configuration errors before starting Dagster. To build the models and run their tests against the configured database:

```powershell
dbt build --profiles-dir "$env:USERPROFILE\.dbt"
```

`dbt build` creates or updates database objects. Alternatively, use `dbt run` to run models and `dbt test` to run tests separately.

Run `dbt deps` before parsing/building if you later add external dbt packages through `packages.yml` or `dependencies.yml`.

Return to the repository root:

```powershell
cd ..
```

For VS Code's Power User for dbt extension, select `.venv312\Scripts\python.exe` using **Python: Select Interpreter**, then run **Developer: Reload Window**. Activating a terminal alone does not select the extension's interpreter.

## 6. Set DAGSTER_HOME

`DAGSTER_HOME` stores Dagster instance configuration and local run history. It is separate from both the dbt project and dbt profile directories.

Create the folder and set the variable for the current PowerShell terminal. These commands can run from any directory:

```powershell
New-Item -ItemType Directory -Force -Path "C:\Users\olada\.dagster"
$env:DAGSTER_HOME = "C:\Users\olada\.dagster"
```

For another Windows user, use the equivalent user-relative path:

```powershell
$env:DAGSTER_HOME = "$env:USERPROFILE\.dagster"
```

Optionally persist it for future terminal sessions:

```powershell
[Environment]::SetEnvironmentVariable("DAGSTER_HOME", "$env:USERPROFILE\.dagster", "User")
```

The persistent setting applies to new processes. Keep the `$env:DAGSTER_HOME` assignment above for the current terminal; restart VS Code to pick up the saved setting in future integrated terminals.

Verify:

```powershell
$env:DAGSTER_HOME
Test-Path $env:DAGSTER_HOME
```

The folder check should return `True`. A custom `dagster.yaml` is optional for this local setup; Dagster can use its default local storage configuration.

In Bash, the equivalent assignment is `export DAGSTER_HOME="$HOME/.dagster"`. PowerShell uses `$env:DAGSTER_HOME`, not `export`.

## 7. Start Dagster

With `.venv312` activated and `DAGSTER_HOME` set, start from the Dagster package directory:

```powershell
cd C:\Users\olada\Documents\PSECU_project\sql_dagster\snowflakes_dw\dbt_dagster
dagster dev
```

Open http://localhost:3000. Use the UI to inspect and materialize dbt assets. Keep the terminal running; press **Ctrl+C** to stop Dagster.

## Daily startup

After completing the initial setup:

```powershell
cd C:\Users\olada\Documents\PSECU_project\sql_dagster\snowflakes_dw
.\.venv312\Scripts\Activate.ps1
$env:DAGSTER_HOME = "$env:USERPROFILE\.dagster"
cd .\dbt_dagster
dagster dev
```

## Scaffolding a new Dagster project only

The repository already contains `dbt_dagster`. Do not repeat scaffolding over the existing project. For a fresh setup without that folder, run this from the repository root after installing `dagster-dbt`:

```powershell
dagster-dbt project scaffold --project-name dbt_dagster --dbt-project-dir ".\dbt_project"
```

Then install the generated project with its `dev` extra and configure `profiles_dir` as described above. The dbt directory must contain `dbt_project.yml`; the repository root does not.

## Troubleshooting

- **dbt not found in VS Code:** select the `.venv312` Python interpreter and reload VS Code. The global `C:\Program Files\dbt\dbt.exe` is the Cloud CLI, whereas this setup uses dbt Core inside the virtual environment.
- **profiles_dir does not contain profiles.yml:** confirm `$env:USERPROFILE\.dbt\profiles.yml` exists and `project.py` uses `profiles_dir=Path.home() / ".dbt"`.
- **Invalid --dbt-project-dir:** point to `snowflakes_dw\dbt_project`, the directory containing `dbt_project.yml`.
- **DAGSTER_HOME directory missing:** create the directory before starting Dagster and set the variable in the same terminal.
- **Database connection errors:** run `dbt debug` from `dbt_project`; check the profile, ODBC driver, credentials, and database access.
