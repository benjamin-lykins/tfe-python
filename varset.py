import argparse
import os
import dotenv

from pytfe import TFEClient, TFEConfig
from pytfe.models import (
    VariableSetCreateOptions,
    VariableSetListOptions,
    VariableSetUpdateOptions,
)

def create(name, description, is_global):
    try:
        create_options = VariableSetCreateOptions(
            name=name,
            description=description,
        )

        if is_global:
            create_options["global"] = True
        
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

if __name__ == "__main__":
    dotenv.load_dotenv()
    
    org = os.getenv("TFE_ORGANIZATION")
    client = TFEClient(TFEConfig())
    
    parser = argparse.ArgumentParser(description="Variable Set management CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
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
    else:
        parser.print_help()