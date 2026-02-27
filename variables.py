import argparse
import os
import dotenv

from pytfe import TFEClient, TFEConfig
from pytfe.models import (
    VariableCreateOptions,
    VariableListOptions,
    VariableUpdateOptions,
)

def create(workspace_name, key, value, description=None, category="terraform", sensitive=False, hcl=False):
    """Create a variable in a workspace
    
    Args:
        workspace_name: Name of the workspace
        key: Variable key/name
        value: Variable value
        description: Optional description
        category: Variable category (terraform or env)
        sensitive: Mark variable as sensitive
        hcl: Parse value as HCL
    """
    try:
        # Get workspace ID from name
        workspace = client.workspaces.read(workspace_name, organization=org)
        
        create_options = VariableCreateOptions(
            key=key,
            value=value,
            category=category,
            sensitive=sensitive,
            hcl=hcl,
        )
        
        if description:
            create_options.description = description
        
        variable = client.variables.create(workspace.id, create_options)
        print(f"Successfully created variable: {variable.key}")
        print(f"Variable ID: {variable.id}")
    except Exception as e:
        print(f"Error creating variable: {e}")

def read(workspace_name, key=None, variable_id=None):
    """Read variable details by key or ID"""
    try:
        # Get workspace ID from name
        workspace = client.workspaces.read(workspace_name, organization=org)
        
        variables = client.variables.list(workspace.id, VariableListOptions())
        
        found_var = None
        if key:
            for var in variables:
                if var.key == key:
                    found_var = var
                    break
        elif variable_id:
            for var in variables:
                if var.id == variable_id:
                    found_var = var
                    break
        else:
            print("Please provide either --key or --id")
            return
        
        if found_var:
            print(f"Variable: {found_var.key}")
            print(f"ID: {found_var.id}")
            print(f"Category: {found_var.category}")
            print(f"Sensitive: {found_var.sensitive}")
            print(f"HCL: {found_var.hcl}")
            if not found_var.sensitive:
                print(f"Value: {found_var.value}")
            else:
                print("Value: [SENSITIVE - hidden]")
            if found_var.description:
                print(f"Description: {found_var.description}")
        else:
            identifier = key if key else variable_id
            print(f"Variable '{identifier}' not found in workspace '{workspace_name}'")
    except Exception as e:
        print(f"Error reading variable: {e}")

def list(workspace_name):
    """List all variables in a workspace"""
    try:
        # Get workspace ID from name
        workspace = client.workspaces.read(workspace_name, organization=org)
        
        variables = client.variables.list(workspace.id, VariableListOptions())
        
        if not variables:
            print(f"No variables found in workspace '{workspace_name}'")
            return
        
        for var in variables:
            value_display = "[SENSITIVE]" if var.sensitive else var.value
            print(f"- {var.key} = {value_display} (ID: {var.id}, Category: {var.category})")
    except Exception as e:
        print(f"Error listing variables: {e}")

def update(workspace_name, key=None, variable_id=None, value=None, description=None, sensitive=None, hcl=None):
    """Update a variable in a workspace"""
    try:
        # Get workspace ID from name
        workspace = client.workspaces.read(workspace_name, organization=org)
        
        # Find the variable ID if only key is provided
        if key and not variable_id:
            variables = client.variables.list(workspace.id, VariableListOptions())
            for var in variables:
                if var.key == key:
                    variable_id = var.id
                    break
            else:
                print(f"Variable '{key}' not found in workspace '{workspace_name}'")
                return
        
        if not variable_id:
            print("Please provide either --key or --id")
            return
        
        update_options = VariableUpdateOptions()
        
        if value is not None:
            update_options.value = value
        if description is not None:
            update_options.description = description
        if sensitive is not None:
            update_options.sensitive = sensitive
        if hcl is not None:
            update_options.hcl = hcl
        
        variable = client.variables.update(workspace.id, variable_id, update_options)
        print(f"Successfully updated variable: {variable.key}")
    except Exception as e:
        print(f"Error updating variable: {e}")

def delete(workspace_name, key=None, variable_id=None):
    """Delete a variable from a workspace"""
    try:
        # Get workspace ID from name
        workspace = client.workspaces.read(workspace_name, organization=org)
        
        # Find the variable ID if only key is provided
        if key and not variable_id:
            variables = client.variables.list(workspace.id, VariableListOptions())
            for var in variables:
                if var.key == key:
                    variable_id = var.id
                    break
            else:
                print(f"Variable '{key}' not found in workspace '{workspace_name}'")
                return
        
        if not variable_id:
            print("Please provide either --key or --id")
            return
        
        client.variables.delete(workspace.id, variable_id)
        print(f"Successfully deleted variable")
    except Exception as e:
        print(f"Error deleting variable: {e}")

if __name__ == "__main__":
    dotenv.load_dotenv()
    
    org = os.getenv("TFE_ORGANIZATION")
    client = TFEClient(TFEConfig())
    
    parser = argparse.ArgumentParser(description="Workspace Variable management CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new variable in a workspace')
    create_parser.add_argument("--workspace", type=str, required=True, help="Name of the workspace")
    create_parser.add_argument("--key", type=str, required=True, help="Variable key/name")
    create_parser.add_argument("--value", type=str, required=True, help="Variable value")
    create_parser.add_argument("--description", type=str, help="Variable description")
    create_parser.add_argument("--category", type=str, choices=["terraform", "env"], default="terraform", help="Variable category")
    create_parser.add_argument("--sensitive", action="store_true", help="Mark variable as sensitive")
    create_parser.add_argument("--hcl", action="store_true", help="Parse value as HCL")
    
    # Read command
    read_parser = subparsers.add_parser('read', help='Read variable details')
    read_parser.add_argument("--workspace", type=str, required=True, help="Name of the workspace")
    read_parser.add_argument("--key", type=str, help="Variable key/name to read")
    read_parser.add_argument("--id", type=str, help="ID of the variable to read")
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all variables in a workspace')
    list_parser.add_argument("--workspace", type=str, required=True, help="Name of the workspace")
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update a variable')
    update_parser.add_argument("--workspace", type=str, required=True, help="Name of the workspace")
    update_parser.add_argument("--key", type=str, help="Variable key/name to update")
    update_parser.add_argument("--id", type=str, help="ID of the variable to update")
    update_parser.add_argument("--value", type=str, help="New variable value")
    update_parser.add_argument("--description", type=str, help="New variable description")
    update_parser.add_argument("--sensitive", action="store_true", help="Mark variable as sensitive")
    update_parser.add_argument("--hcl", action="store_true", help="Parse value as HCL")
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a variable')
    delete_parser.add_argument("--workspace", type=str, required=True, help="Name of the workspace")
    delete_parser.add_argument("--key", type=str, help="Variable key/name to delete")
    delete_parser.add_argument("--id", type=str, help="ID of the variable to delete")
    
    args = parser.parse_args()
    
    # Handle commands
    if args.command == 'create':
        print(f"Creating variable '{args.key}' in workspace '{args.workspace}'")
        create(
            workspace_name=args.workspace,
            key=args.key,
            value=args.value,
            description=args.description,
            category=args.category,
            sensitive=args.sensitive,
            hcl=args.hcl
        )
    elif args.command == 'read':
        if args.key:
            print(f"Reading variable by key: {args.key}")
            read(workspace_name=args.workspace, key=args.key)
        elif args.id:
            print(f"Reading variable by ID: {args.id}")
            read(workspace_name=args.workspace, variable_id=args.id)
        else:
            print("Please provide either --key or --id")
            read_parser.print_help()
    elif args.command == 'list':
        print(f"Listing all variables in workspace '{args.workspace}'")
        list(workspace_name=args.workspace)
    elif args.command == 'update':
        print(f"Updating variable in workspace '{args.workspace}'")
        update(
            workspace_name=args.workspace,
            key=args.key,
            variable_id=args.id,
            value=args.value,
            description=args.description,
            sensitive=args.sensitive if hasattr(args, 'sensitive') and args.sensitive else None,
            hcl=args.hcl if hasattr(args, 'hcl') and args.hcl else None
        )
    elif args.command == 'delete':
        print(f"Deleting variable from workspace '{args.workspace}'")
        delete(workspace_name=args.workspace, key=args.key, variable_id=args.id)
    else:
        parser.print_help()
