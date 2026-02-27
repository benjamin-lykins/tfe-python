# TFE-Python

Small CLI helpers for Terraform Cloud/Enterprise using the `pytfe` SDK.

It is really basic, just messing around with Python and the `pytfe` SDK to interact with Terraform Cloud/Enterprise.

## Prerequisites

- Python 3.11+
- Terraform Cloud/Enterprise token with access to your organization

Install dependencies:

```bash
pip install pytfe python-dotenv
```

## Configuration

Create a `.env` file (or copy the example) and set your credentials:

```bash
cp .env.example .env
```

Required variables:

- `TFE_TOKEN`
- `TFE_ORGANIZATION`
- `TFE_HOSTNAME` (for Terraform Cloud use `app.terraform.io`)

## Scripts

### Projects

```bash
python projects.py list
python projects.py create --name "my-project" --description "Example"
python projects.py read --name "my-project"
python projects.py read --id prj-xxxxxxxxxxxxxxxx
python projects.py update --name "my-project" --description "Updated"
python projects.py delete --name "my-project"
```

### Workspaces

```bash
python workspace.py list
python workspace.py create --name "my-workspace" --project-id prj-xxxxxxxxxxxxxxxx
python workspace.py create --name "my-workspace" --project-name "my-project"
python workspace.py read --name "my-workspace"
python workspace.py update --name "my-workspace" --description "Updated"
python workspace.py delete --name "my-workspace"
```

### Variable Sets

```bash
python varset.py list
python varset.py create --name "my-varset" --description "Example"
python varset.py create --name "my-varset" --description "Example" --global
python varset.py read --name "my-varset"
python varset.py update --name "my-varset" --description "Updated"
python varset.py delete --name "my-varset"

# Manage variables within a variable set
python varset.py var-create --varset "my-varset" --key "my_var" --value "my_value"
python varset.py var-create --varset "my-varset" --key "my_var" --value "my_value" --category env --sensitive
python varset.py var-list --varset "my-varset"
python varset.py var-read --varset "my-varset" --key "my_var"
python varset.py var-update --varset "my-varset" --key "my_var" --value "new_value"
python varset.py var-delete --varset "my-varset" --key "my_var"
```

### Workspace Variables

```bash
python variables.py list --workspace "my-workspace"
python variables.py create --workspace "my-workspace" --key "my_var" --value "my_value"
python variables.py create --workspace "my-workspace" --key "my_var" --value "my_value" --category env --sensitive
python variables.py read --workspace "my-workspace" --key "my_var"
python variables.py update --workspace "my-workspace" --key "my_var" --value "new_value"
python variables.py delete --workspace "my-workspace" --key "my_var"
```

### Teams

```bash
python teams.py list
python teams.py create --name "my-team" --visibility secret
python teams.py create --name "my-team" --visibility organization
python teams.py read --name "my-team"
python teams.py read --id team-xxxxxxxxxxxxxxxx
python teams.py update --name "my-team" --new-name "renamed-team"
python teams.py update --name "my-team" --visibility organization
python teams.py delete --name "my-team"
```

## Notes

- All scripts use environment variables via `python-dotenv`.
- If a resource is not found, try `list` to confirm names and IDs.
- Teams API uses direct HTTP calls via the TFE API (not yet supported in pytfe SDK).
- Variable categories can be `terraform` (default) or `env` for environment variables.
- Use `--sensitive` flag to mark variables as sensitive (values will be write-only).
- Use `--hcl` flag to parse variable values as HCL.
