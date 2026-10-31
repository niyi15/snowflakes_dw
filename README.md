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

## Production deployment to Dagster+

Azure DevOps uses the same build stages as GitHub Actions: check out the source, install dependencies, provide build-time environment variables, generate the dbt manifest, package the source, and deploy a code location. The pipeline YAML, secret storage, and deployment invocation differ; GitHub `uses:` actions cannot be copied directly into an Azure pipeline.

### Code location and repository layout

A code location loads this project's Dagster definitions, assets, resources, and schedules. It is not the database connection. Use **Import a Dagster project** in Dagster+, because this repository already contains a Dagster package.

Keep these paths together in the deployment artifact:

```text
snowflakes_dw/
├── dagster_cloud.yaml
├── requirements.txt
├── dbt_project/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   ├── models/
│   └── target/manifest.json    # generated in CI, not committed
└── dbt_dagster/
    ├── pyproject.toml
    └── dbt_dagster/
        ├── definitions.py
        ├── project.py
        ├── assets.py
        └── schedules.py
```

The root `dagster_cloud.yaml` identifies the code location:

```yaml
locations:
  - location_name: dbt_dagster
    working_directory: ./dbt_dagster
    code_source:
      module_name: dbt_dagster.definitions
```

`working_directory` controls loading the Python module. It does not change the dependency build root. The root `requirements.txt` installs `./dbt_dagster`, whose `pyproject.toml` declares the Python dependencies, including `dagster-cloud`. Do not repeat every dependency in both files.

### Production database profile and secrets

The deployed profile is `dbt_project/profiles.yml`. Commit only environment-variable references, never real credentials. The top-level profile name must match `profile: snowflakes_dw` in `dbt_project.yml`. Its selected target/output determines the connection dbt uses; the Dagster+ deployment name `prod` does not automatically select a dbt target named `prod`.

Provide the variables referenced by the profile:

| Variable | Meaning |
| --- | --- |
| `DBT_SERVER` | Production SQL Server hostname |
| `DBT_DATABASE` | Production database |
| `DBT_SCHEMA` | Base target schema; model and macro configuration can alter final model schemas |
| `DBT_USER` | Database service account |
| `DBT_PASSWORD` | Database service account password |

For example, the profile's server setting is `server: "{{ env_var('DBT_SERVER') }}"`.

Set runtime variables in **Dagster+ → select prod → Deployment → Environment variables**, scoped to `dbt_dagster` where applicable. Reload the code location after saving.

Set the same required variables separately in CI. Dagster+ runtime variables are not automatically available to the GitHub or Azure build agent. Production credentials should be scoped to trusted production pipelines; use separate credentials and database/schema settings for branch deployments.

The current `project.py` points `profiles_dir` to the repository's `dbt_project` folder. Your laptop's `C:\Users\olada\.dbt\profiles.yml` is not uploaded to Dagster+.

### Generate and include the manifest

Dagster reads `manifest.json` to define the dbt assets before running a materialization. `prepare_if_dev()` generates it during local development, but production requires it to be prepared during the build.

The current GitHub Python-executable deployment workflows run these commands from the checked-out repository root before deployment:

```bash
python -m pip install -r requirements.txt
dbt parse --project-dir dbt_project --profiles-dir dbt_project
test -s dbt_project/target/manifest.json
```

`dbt parse` generates metadata; it does not build database tables. It still requires values for environment variables referenced by the profile. If external dbt packages are added later, install them with `dbt deps` before parsing.

Keep `target/` ignored in Git. Include the generated manifest, dbt models, macros, and profile in the deployment artifact after generation. A clean checkout in a later job will not contain the generated manifest: publish/download the prepared artifact between jobs or generate it again before packaging.

Dagster also provides `dagster-dbt project prepare-and-package --file path/to/project.py`. Use it when configuring a distinct packaged dbt directory and ensuring that directory is shipped. The current workflows use `dbt parse` directly and preserve the repository layout; changing packaging paths requires matching changes to `project.py` and the artifact contents.

See [Dagster's dbt production deployment guidance](https://dagster.io/docs/integrations/libraries/dbt/reference#deploying-a-dagster-project-with-a-dbt-project).

### GitHub Actions production deployment

1. Add `DAGSTER_CLOUD_API_TOKEN` and the five `DBT_*` values in **GitHub repository → Settings → Secrets and variables → Actions**.
2. Configure the runtime `DBT_*` values in Dagster+ too.
3. Push the deployment files, profile template, Python code, and dbt code to the configured production branch.
4. `.github/workflows/deploy.yml` installs dependencies and generates the manifest before its Python-executable deployment action.
5. Check **Dagster+ → Deployment → Code locations** for a successfully loaded `dbt_dagster` location.
6. Materialize a small asset first, check database outputs and tests, then enable the intended schedule. The scaffold's schedule list is initially empty.

The manifest-generation additions currently cover the Python-executable path. If switching to the Docker path, generate the manifest during the image build or before copying prepared source into the image.

### Azure DevOps equivalent

Use an Azure Pipeline with the same stages. Store credentials as secret pipeline variables, in a variable group, or through an approved Key Vault integration. Map secret variables explicitly into the build step's environment. Supply the Dagster+ API token separately to the deployment step.

This example is the **manifest preparation stage only**, not a complete deployment pipeline:

```yaml
pool:
  vmImage: ubuntu-22.04

steps:
  - checkout: self

  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.10'

  - bash: |
      set -euo pipefail
      python -m pip install -r requirements.txt
      dbt parse --project-dir dbt_project --profiles-dir dbt_project
      test -s dbt_project/target/manifest.json
    workingDirectory: $(Build.SourcesDirectory)
    displayName: Install dependencies and generate dbt manifest
    env:
      DBT_SERVER: $(DBT_SERVER)
      DBT_DATABASE: $(DBT_DATABASE)
      DBT_SCHEMA: $(DBT_SCHEMA)
      DBT_USER: $(DBT_USER)
      DBT_PASSWORD: $(DBT_PASSWORD)
```

After this stage, add deployment using the Dagster Cloud CLI or your chosen container deployment process. Configure the Dagster+ organization, deployment (`prod`), API token, code location configuration, and artifact/image. The existing GitHub deployment uses Python 3.10; keep build and runtime Python versions aligned if changing that version.

For Serverless, build and upload an artifact using the supported Dagster Cloud CLI workflow. For Hybrid, build and push a container image and update the code location to that image; a running Hybrid agent must be able to pull and launch it. These are different deployment mechanisms, so finalize the deploy stage for the selected mode rather than reusing GitHub action syntax in Azure.

### SQL Server runtime and networking

The production runtime needs the Microsoft ODBC driver specified by `profiles.yml`, in addition to the pip-installed `dbt-sqlserver` adapter. Installing the driver on the CI agent does not install it in the deployed runtime. If using a container, install the driver in the image.

The runtime must also resolve and reach SQL Server and use an authentication method supported in that environment. A VPN or Windows login working on your laptop does not grant access to a hosted Linux runtime. For a database inside a private company network, evaluate Hybrid with an agent inside the approved network, or an approved Serverless connectivity arrangement.

`DAGSTER_HOME` from the local setup is not uploaded to Dagster+. Dagster+ manages deployment state; Hybrid additionally needs its own agent configuration.

### Production error checklist

| Error | Check |
| --- | --- |
| No setup.py, requirements.txt, or pyproject.toml | Build root contains `requirements.txt`, and `./dbt_dagster` exists |
| DagsterDbtManifestNotFoundError | Parse ran before packaging, manifest is in the uploaded artifact, and `project.py` points to that directory |
| Missing environment variable | Configure the variable separately in CI and Dagster+ runtime |
| profiles.yml not found | Ship the profile template and match its directory to `profiles_dir` |
| SQL Server driver cannot be loaded | Install the matching ODBC driver in the runtime, not just the CI agent |
| Login failure or connection timeout | Check production credentials, authentication, DNS, firewall, routing, and database permissions |

### Automated ODBC runtime image in GitHub Actions

`Dockerfile.serverless-base` defines a Linux AMD64 Python 3.10 image with unixODBC, Microsoft ODBC Driver 18 for SQL Server, and `dagster-cloud[serverless]`. Its build verifies that `pyodbc` can load and discover the driver. Installing the Microsoft driver uses `ACCEPT_EULA=Y` to accept its license terms.

For the current Python-executable deployment path, both GitHub workflows now:

1. Generate the dbt manifest using the existing build secrets.
2. Build `Dockerfile.serverless-base` on the hosted Ubuntu runner.
3. Upload the base image using `dagster-cloud serverless upload-base-image` and the existing `DAGSTER_CLOUD_API_TOKEN`.
4. Extract the returned `sha256_...` image tag and export `SERVERLESS_BASE_IMAGE_TAG` for the subsequent deployment action.
5. Deploy the project's Python code and prepared manifest on that image.

Commit and push the Dockerfile and workflow changes. Docker Desktop and a manual image upload are not required. The runner supplies Docker, and no additional Docker Hub credentials or private image registry are needed for this upload process. The Dagster+ API token must have permission to upload the image and deploy code.

The base image is rebuilt/uploaded on each eligible deployment. It contains libraries only: repository code and database credentials are not copied into it. Keep the runtime `DBT_*` variables configured in Dagster+ and build variables in GitHub Actions. For pull requests, continue to use trusted branch workflows and separate branch database settings.

This automation applies to the existing fast Python-executable path (`ENABLE_FAST_DEPLOYS: 'true'`). Switching to the workflow's separate Docker deployment path requires adapting that path; this Dockerfile is a base image, not a standalone image containing the full project.

If changing Python versions, update both the Dockerfile and workflow `PYTHON_VERSION`. Keep the Dagster Cloud CLI/runtime versions coordinated with the deployment action. If the upload output format changes, the tag extraction fails rather than deploying on an unintended base image.

Reference: [Dagster+ custom Serverless base images](https://dagster.io/docs/deployment/dagster-plus/serverless/runtime-environment#use-a-different-base-image).

### Simulated file handoff and dbt Cloud API group

The `file_to_dbt_cloud` group contains `simulated_file_move` followed by `trigger_dbt_cloud_job`. Both are simulations: no file is moved and no API is called. The Cloud step reports dummy account ID `12345`, job ID `67890`, run ID `100001`, and status `SIMULATED_SUCCESS`. No dbt Cloud credentials or environment variables are required.

Launch `file_to_dbt_cloud_job` manually or use `file_to_dbt_cloud_daily_7am`. Its cron is `0 7 * * *`, timezone `America/New_York`, and default status `RUNNING`. It runs daily at 7 AM local time, adjusting for daylight saving time. Any saved on/off state in Dagster+ overrides the code default. The existing members schedule is unchanged.

### dbt validation after the simulated handoff

The `dbt_validation` group contains `dbt_tests`, which depends on `trigger_dbt_cloud_job`. Launch `file_to_dbt_cloud_and_tests_job` to execute `simulated_file_move` → `trigger_dbt_cloud_job` → `dbt_tests` in one run. The existing `file_to_dbt_cloud_daily_7am` schedule now targets this combined job, retaining 7 AM America/New_York and default RUNNING status. The original file-only job remains available for manual use.

The first two assets simulate work. The final asset runs **real `dbt test`** through the existing dbt CLI resource, against the database configured in the repository profile. It tests the entire dbt project; it does not build models, so their database relations must already exist. A failed test fails the asset and job. SQL Server runtime libraries and the runtime DBT_* variables are required. Since the preceding Cloud trigger is simulated, no Cloud run or model build actually occurs before these tests.

## Independent file-processing code location

`file_pipeline/` is a separate Python project with no dbt dependency or profile requirement. The root `dagster_cloud.yaml` registers it as a second code location named `file_pipeline`, using `file_pipeline/pyproject.toml` as its dependency/build root. Existing workflows deploy all configured locations; the shared workflow still prepares the original dbt project and uploads its ODBC base image, so its existing build secrets remain necessary. The sample package itself only requires Dagster and dagster-cloud.

In Dagster+, launch `file_processing_job` in the `file_pipeline` location. Its `file_processing` group runs `download_file` → `process_file`. The download is simulated using a sample CSV; the processing is real Python CSV parsing and uppercase name normalization. Data passes through Dagster's IO manager rather than a machine-local path. There are no external API calls or credentials. The `file_processing_daily_7am` schedule runs this job daily at 7 AM America/New_York (`0 7 * * *`) with default status RUNNING. A saved Dagster+ schedule toggle overrides the code default.

To develop only this location locally, from the repository root with your virtual environment active:

```powershell
python -m pip install -e ".\file_pipeline[dev]"
cd .\file_pipeline
dagster dev
```

Commit the new package and root deployment configuration, then push to deploy. This is an independent code location, not another asset group inside the dbt location. The existing dbt location remains configured separately.
