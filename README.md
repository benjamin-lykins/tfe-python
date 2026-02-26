# TFE Onboarding Python

Small CLI helpers for Terraform Cloud/Enterprise using the `pytfe` SDK.

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
python workspace.py create --name "my-workspace" --project prj-xxxxxxxxxxxxxxxx
python workspace.py read --name "my-workspace"
python workspace.py update --name "my-workspace" --description "Updated"
python workspace.py delete --name "my-workspace"
```

### Variable Sets

```bash
python varset.py list
python varset.py create --name "my-varset" --description "Example"
python varset.py read --name "my-varset"
python varset.py update --name "my-varset" --description "Updated"
python varset.py delete --name "my-varset"
```

### Teams

`pytfe` does not currently expose team management APIs. The `teams.py` script prints guidance for now.

## Notes

- All scripts use environment variables via `python-dotenv`.
- If a resource is not found, try `list` to confirm names and IDs.
# tfe-python
