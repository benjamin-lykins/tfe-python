import argparse
import os
import dotenv

from pytfe import TFEClient, TFEConfig
from pytfe.models import (
    WorkspaceCreateOptions,
    WorkspaceListOptions,
    WorkspaceUpdateOptions,
)

def create(name, project=None):
    try:
        create_options = WorkspaceCreateOptions(
            name=name,
            project_id=project
        )
        
        workspace = client.workspaces.create(org, create_options)
        print(f"Successfully created workspace: {workspace.name}")
    except Exception as e:
        print(f"Error creating workspace: {e}")

def read(name):
    try:
        workspaces = client.workspaces.list(org, WorkspaceListOptions())
        for workspace in workspaces:
            if workspace.name == name:
                print(f"Workspace: {workspace.name}")
                print(f"ID: {workspace.id}")
                print(f"Description: {workspace.description}")
                return
        print(f"Workspace with name {name} not found")
    except Exception as e:
        print(f"Error reading workspace: {e}")

def list():
    try:
        workspaces = client.workspaces.list(org, WorkspaceListOptions())
        for workspace in workspaces:
            print(f"- {workspace.name} (ID: {workspace.id})")
    except Exception as e:
        print(f"Error listing workspaces: {e}")

def update(name, description=None):
    try:
        update_options = WorkspaceUpdateOptions()
        if description:
            update_options.description = description
        workspace = client.workspaces.update(name, update_options, organization=org)
        print(f"Successfully updated workspace: {workspace.name}")
    except Exception as e:
        print(f"Error updating workspace: {e}")

def delete(name):
    try:
        client.workspaces.delete(name, organization=org)
        print(f"Successfully deleted workspace: {name}")
    except Exception as e:
        print(f"Error deleting workspace: {e}")

if __name__ == "__main__":
    dotenv.load_dotenv()
    
    org = os.getenv("TFE_ORGANIZATION")
    client = TFEClient(TFEConfig())
    
    parser = argparse.ArgumentParser(description="Workspace management CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new workspace')
    create_parser.add_argument("--name", type=str, required=True, help="Name of the workspace")
    create_parser.add_argument("--project", type=str, help="Project ID")
    
    # Read command
    read_parser = subparsers.add_parser('read', help='Read workspace details')
    read_parser.add_argument("--name", type=str, required=True, help="Name of the workspace to read")
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all workspaces')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update a workspace')
    update_parser.add_argument("--name", type=str, required=True, help="Name of the workspace to update")
    update_parser.add_argument("--description", type=str, help="New workspace description")
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a workspace')
    delete_parser.add_argument("--name", type=str, required=True, help="Name of the workspace to delete")
    
    args = parser.parse_args()
    
    # Handle commands
    if args.command == 'create':
        print(f"Creating workspace: {args.name}")
        if args.project:
            print(f"Project ID: {args.project}")
        create(name=args.name, project=args.project)
    elif args.command == 'read':
        print(f"Reading workspace: {args.name}")
        read(name=args.name)
    elif args.command == 'list':
        print("Listing all workspaces")
        list()
    elif args.command == 'update':
        print(f"Updating workspace: {args.name}")
        if args.description:
            print(f"New description: {args.description}")
        update(name=args.name, description=args.description)
    elif args.command == 'delete':
        print(f"Deleting workspace: {args.name}")
        delete(name=args.name)
    else:
        parser.print_help()
