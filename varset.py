import argparse
import os
import dotenv

from pytfe import TFEClient, TFEConfig
from pytfe.models import (
    VariableSetCreateOptions,
    VariableSetListOptions,
    VariableSetUpdateOptions,
    VariableSetVariableCreateOptions,
    VariableSetVariableListOptions,
    VariableSetVariableUpdateOptions,
)

def create(name, description, is_global):
    try:
        create_options = VariableSetCreateOptions(
            **{
                "name": name,
                "description": description,
                "global": is_global
            }
        )
        
        varset = client.variable_sets.create(org, create_options)
        print(f"Successfully created variable set: {varset.name}")
    except Exception as e:
        print(f"Error creating variable set: {e}")

def read(name):
    try:
        varsets = client.variable_sets.list(org, VariableSetListOptions())
        for varset in varsets:
            if varset.name == name:
                print(f"Variable Set: {varset.name}")
                print(f"Description: {varset.description}")
                print(f"ID: {varset.id}")
                return
        print(f"Variable set with name {name} not found")
    except Exception as e:
        print(f"Error reading variable set: {e}")

def list():
    try:
        varsets = client.variable_sets.list(org, VariableSetListOptions())
        for varset in varsets:
            print(f"- {varset.name} (ID: {varset.id})")
    except Exception as e:
        print(f"Error listing variable sets: {e}")

def update(name, description):
    try:
        varsets = client.variable_sets.list(org, VariableSetListOptions())
        varset_id = None
        for varset in varsets:
            if varset.name == name:
                varset_id = varset.id
                break
        
        if not varset_id:
            print(f"Variable set with name {name} not found")
            return
        
        update_options = VariableSetUpdateOptions(
            description=description
        )
        varset = client.variable_sets.update(varset_id, update_options)
        print(f"Successfully updated variable set: {varset.name}")
    except Exception as e:
        print(f"Error updating variable set: {e}")

def delete(name):
    try:
        varsets = client.variable_sets.list(org, VariableSetListOptions())
        varset_id = None
        for varset in varsets:
            if varset.name == name:
                varset_id = varset.id
                break
        
        if not varset_id:
            print(f"Variable set with name {name} not found")
            return
        
        client.variable_sets.delete(varset_id)
        print(f"Successfully deleted variable set: {name}")
    except Exception as e:
        print(f"Error deleting variable set: {e}")

# Variable Set Variable Management Functions

def var_create(varset_name, key, value, description=None, category="terraform", sensitive=False, hcl=False):
    """Create a variable in a variable set"""
    try:
        # Find the variable set ID
        varsets = client.variable_sets.list(org, VariableSetListOptions())
        varset_id = None
        for varset in varsets:
            if varset.name == varset_name:
                varset_id = varset.id
                break
        
        if not varset_id:
            print(f"Variable set '{varset_name}' not found")
            return
        
        create_options = VariableSetVariableCreateOptions(
            key=key,
            value=value,
            category=category,
            sensitive=sensitive,
            hcl=hcl,
        )
        
        if description:
            create_options.description = description
        
        variable = client.variable_set_variables.create(varset_id, create_options)
        print(f"Successfully created variable '{variable.key}' in variable set '{varset_name}'")
        print(f"Variable ID: {variable.id}")
    except Exception as e:
        print(f"Error creating variable: {e}")

def var_read(varset_name, key=None, variable_id=None):
    """Read a variable from a variable set"""
    try:
        # Find the variable set ID
        varsets = client.variable_sets.list(org, VariableSetListOptions())
        varset_id = None
        for varset in varsets:
            if varset.name == varset_name:
                varset_id = varset.id
                break
        
        if not varset_id:
            print(f"Variable set '{varset_name}' not found")
            return
        
        variables = client.variable_set_variables.list(varset_id, VariableSetVariableListOptions())
        
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
            print("Please provide either --key or --var-id")
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
            print(f"Variable '{identifier}' not found in variable set '{varset_name}'")
    except Exception as e:
        print(f"Error reading variable: {e}")

def var_list(varset_name):
    """List all variables in a variable set"""
    try:
        # Find the variable set ID
        varsets = client.variable_sets.list(org, VariableSetListOptions())
        varset_id = None
        for varset in varsets:
            if varset.name == varset_name:
                varset_id = varset.id
                break
        
        if not varset_id:
            print(f"Variable set '{varset_name}' not found")
            return
        
        variables = client.variable_set_variables.list(varset_id, VariableSetVariableListOptions())
        
        if not variables:
            print(f"No variables found in variable set '{varset_name}'")
            return
        
        for var in variables:
            value_display = "[SENSITIVE]" if var.sensitive else var.value
            print(f"- {var.key} = {value_display} (ID: {var.id}, Category: {var.category})")
    except Exception as e:
        print(f"Error listing variables: {e}")

def var_update(varset_name, key=None, variable_id=None, value=None, description=None, sensitive=None, hcl=None):
    """Update a variable in a variable set"""
    try:
        # Find the variable set ID
        varsets = client.variable_sets.list(org, VariableSetListOptions())
        varset_id = None
        for varset in varsets:
            if varset.name == varset_name:
                varset_id = varset.id
                break
        
        if not varset_id:
            print(f"Variable set '{varset_name}' not found")
            return
        
        # Find the variable ID if only key is provided
        if key and not variable_id:
            variables = client.variable_set_variables.list(varset_id, VariableSetVariableListOptions())
            for var in variables:
                if var.key == key:
                    variable_id = var.id
                    break
            else:
                print(f"Variable '{key}' not found in variable set '{varset_name}'")
                return
        
        if not variable_id:
            print("Please provide either --key or --var-id")
            return
        
        update_options = VariableSetVariableUpdateOptions()
        
        if value is not None:
            update_options.value = value
        if description is not None:
            update_options.description = description
        if sensitive is not None:
            update_options.sensitive = sensitive
        if hcl is not None:
            update_options.hcl = hcl
        
        variable = client.variable_set_variables.update(varset_id, variable_id, update_options)
        print(f"Successfully updated variable: {variable.key}")
    except Exception as e:
        print(f"Error updating variable: {e}")

def var_delete(varset_name, key=None, variable_id=None):
    """Delete a variable from a variable set"""
    try:
        # Find the variable set ID
        varsets = client.variable_sets.list(org, VariableSetListOptions())
        varset_id = None
        for varset in varsets:
            if varset.name == varset_name:
                varset_id = varset.id
                break
        
        if not varset_id:
            print(f"Variable set '{varset_name}' not found")
            return
        
        # Find the variable ID if only key is provided
        if key and not variable_id:
            variables = client.variable_set_variables.list(varset_id, VariableSetVariableListOptions())
            for var in variables:
                if var.key == key:
                    variable_id = var.id
                    break
            else:
                print(f"Variable '{key}' not found in variable set '{varset_name}'")
                return
        
        if not variable_id:
            print("Please provide either --key or --var-id")
            return
        
        client.variable_set_variables.delete(varset_id, variable_id)
        print(f"Successfully deleted variable from variable set '{varset_name}'")
    except Exception as e:
        print(f"Error deleting variable: {e}")

if __name__ == "__main__":
    dotenv.load_dotenv()
    
    org = os.getenv("TFE_ORGANIZATION")
    client = TFEClient(TFEConfig())
    
    parser = argparse.ArgumentParser(description="Variable Set management CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Variable Set commands
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new variable set')
    create_parser.add_argument("--name", type=str, required=True, help="Name of the variable set")
    create_parser.add_argument("--description", type=str, help="Variable set description")
    create_parser.add_argument("--global", dest="is_global", action="store_true", help="Make this a global variable set")
    
    # Read command
    read_parser = subparsers.add_parser('read', help='Read variable set details')
    read_parser.add_argument("--name", type=str, required=True, help="Name of the variable set to read")
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all variable sets')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update a variable set')
    update_parser.add_argument("--name", type=str, required=True, help="Name of the variable set to update")
    update_parser.add_argument("--description", type=str, help="New variable set description")
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a variable set')
    delete_parser.add_argument("--name", type=str, required=True, help="Name of the variable set to delete")
    
    # Variable Set Variable commands
    # Var-create command
    var_create_parser = subparsers.add_parser('var-create', help='Create a variable in a variable set')
    var_create_parser.add_argument("--varset", type=str, required=True, help="Name of the variable set")
    var_create_parser.add_argument("--key", type=str, required=True, help="Variable key/name")
    var_create_parser.add_argument("--value", type=str, required=True, help="Variable value")
    var_create_parser.add_argument("--description", type=str, help="Variable description")
    var_create_parser.add_argument("--category", type=str, choices=["terraform", "env"], default="terraform", help="Variable category")
    var_create_parser.add_argument("--sensitive", action="store_true", help="Mark variable as sensitive")
    var_create_parser.add_argument("--hcl", action="store_true", help="Parse value as HCL")
    
    # Var-read command
    var_read_parser = subparsers.add_parser('var-read', help='Read a variable from a variable set')
    var_read_parser.add_argument("--varset", type=str, required=True, help="Name of the variable set")
    var_read_parser.add_argument("--key", type=str, help="Variable key/name to read")
    var_read_parser.add_argument("--var-id", type=str, help="ID of the variable to read")
    
    # Var-list command
    var_list_parser = subparsers.add_parser('var-list', help='List all variables in a variable set')
    var_list_parser.add_argument("--varset", type=str, required=True, help="Name of the variable set")
    
    # Var-update command
    var_update_parser = subparsers.add_parser('var-update', help='Update a variable in a variable set')
    var_update_parser.add_argument("--varset", type=str, required=True, help="Name of the variable set")
    var_update_parser.add_argument("--key", type=str, help="Variable key/name to update")
    var_update_parser.add_argument("--var-id", type=str, help="ID of the variable to update")
    var_update_parser.add_argument("--value", type=str, help="New variable value")
    var_update_parser.add_argument("--description", type=str, help="New variable description")
    var_update_parser.add_argument("--sensitive", action="store_true", help="Mark variable as sensitive")
    var_update_parser.add_argument("--hcl", action="store_true", help="Parse value as HCL")
    
    # Var-delete command
    var_delete_parser = subparsers.add_parser('var-delete', help='Delete a variable from a variable set')
    var_delete_parser.add_argument("--varset", type=str, required=True, help="Name of the variable set")
    var_delete_parser.add_argument("--key", type=str, help="Variable key/name to delete")
    var_delete_parser.add_argument("--var-id", type=str, help="ID of the variable to delete")
    
    args = parser.parse_args()
    
    # Handle commands
    if args.command == 'create':
        print(f"Creating variable set: {args.name}")
        if args.description:
            print(f"Description: {args.description}")
        create(name=args.name, description=args.description, is_global=args.is_global)
    elif args.command == 'read':
        print(f"Reading variable set: {args.name}")
        read(name=args.name)
    elif args.command == 'list':
        print("Listing all variable sets")
        list()
    elif args.command == 'update':
        print(f"Updating variable set: {args.name}")
        if args.description:
            print(f"New description: {args.description}")
        update(name=args.name, description=args.description)
    elif args.command == 'delete':
        print(f"Deleting variable set: {args.name}")
        delete(name=args.name)
    # Variable set variable commands
    elif args.command == 'var-create':
        print(f"Creating variable '{args.key}' in variable set '{args.varset}'")
        var_create(
            varset_name=args.varset,
            key=args.key,
            value=args.value,
            description=args.description,
            category=args.category,
            sensitive=args.sensitive,
            hcl=args.hcl
        )
    elif args.command == 'var-read':
        print(f"Reading variable from variable set '{args.varset}'")
        var_read(varset_name=args.varset, key=args.key, variable_id=args.var_id)
    elif args.command == 'var-list':
        print(f"Listing variables in variable set '{args.varset}'")
        var_list(varset_name=args.varset)
    elif args.command == 'var-update':
        print(f"Updating variable in variable set '{args.varset}'")
        var_update(
            varset_name=args.varset,
            key=args.key,
            variable_id=args.var_id,
            value=args.value,
            description=args.description,
            sensitive=args.sensitive if hasattr(args, 'sensitive') and args.sensitive else None,
            hcl=args.hcl if hasattr(args, 'hcl') and args.hcl else None
        )
    elif args.command == 'var-delete':
        print(f"Deleting variable from variable set '{args.varset}'")
        var_delete(varset_name=args.varset, key=args.key, variable_id=args.var_id)
    else:
        parser.print_help()