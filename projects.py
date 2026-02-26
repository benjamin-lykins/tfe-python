import argparse
import os
import dotenv

from pytfe import TFEClient, TFEConfig
from pytfe._http import HTTPTransport
from pytfe.errors import NotFound
from pytfe.models import (
    ProjectAddTagBindingsOptions,
    ProjectCreateOptions,
    ProjectListOptions,
    ProjectUpdateOptions,
    TagBinding,
)

def create(name, description):
    try:
        create_options = ProjectCreateOptions(
            name=name,
            description=description
        )
        
        project = client.projects.create(org, create_options)
    except Exception as e:
        print(f"Error creating project: {e}")
    pass

def read(name=None, project_id=None):
    try:
        # Get all projects
        projects = client.projects.list(org, ProjectListOptions())
        
        # Find the matching project
        found_project = None
        if name:
            for project in projects:
                if project.name == name:
                    found_project = project
                    break
        elif project_id:
            for project in projects:
                if project.id == project_id:
                    found_project = project
                    break
        else:
            print("Please provide either --name or --id")
            return
        
        # Display the project details
        if found_project:
            print(f"Project: {found_project.name}")
            print(f"ID: {found_project.id}")
            print(f"Description: {found_project.description}")
            print(f"Organization: {found_project.organization}")
            print(f"Workspace Count: {found_project.workspace_count}")
            print(f"Created: {found_project.created_at}")
        else:
            identifier = name if name else project_id
            print(f"Project '{identifier}' not found")
    except Exception as e:
        print(f"Error reading project: {e}")
    pass

def list():
    try:
        projects = client.projects.list(org, ProjectListOptions())
        for project in projects:
            print(f"- {project}")
    except Exception as e:
        print(f"Error listing projects: {e}")
    pass

def update(project_id=None, name=None, description=None):
    try:
        # If name is provided, find the project by name first
        if name and not project_id:
            projects = client.projects.list(org, ProjectListOptions())
            for project in projects:
                if project.name == name:
                    project_id = project.id
                    break
            else:
                print(f"Project with name '{name}' not found")
                return
        
        if not project_id:
            print("Please provide either --name or --id")
            return
        
        update_options = ProjectUpdateOptions(
            description=description
        )
        client.projects.update(project_id, update_options)
        print(f"Successfully updated project")
    except Exception as e:
        print(f"Error updating project: {e}")
    pass

def delete(project_id=None, name=None):
    try:
        # If name is provided, find the project by name first
        if name and not project_id:
            projects = client.projects.list(org, ProjectListOptions())
            for project in projects:
                if project.name == name:
                    project_id = project.id
                    break
            else:
                print(f"Project with name '{name}' not found")
                return
        
        if not project_id:
            print("Please provide either --name or --id")
            return
        
        project = client.projects.delete(project_id)
        print(f"Successfully deleted project")
    except Exception as e:
        print(f"Error deleting project: {e}")
    pass



if __name__ == "__main__":

    dotenv.load_dotenv()

    org = os.getenv("TFE_ORGANIZATION")

    client = TFEClient(TFEConfig())

    
    parser = argparse.ArgumentParser(description="Project management CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new project')
    create_parser.add_argument("--name", type=str, required=True, help="Name of the project")
    create_parser.add_argument("--description", type=str, help="Project description")
    
    # Read command
    read_parser = subparsers.add_parser('read', help='Read project details')
    read_parser.add_argument("--name", type=str, help="Name of the project to read")
    read_parser.add_argument("--id", type=str, help="ID of the project to read")

    # List command
    list_parser = subparsers.add_parser('list', help='List all projects')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update a project')
    update_parser.add_argument("--name", type=str, help="Name of the project to update")
    update_parser.add_argument("--id", type=str, help="ID of the project to update")
    update_parser.add_argument("--description", type=str, help="New project description")
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a project')
    delete_parser.add_argument("--name", type=str, help="Name of the project to delete")
    delete_parser.add_argument("--id", type=str, help="ID of the project to delete")
    
    args = parser.parse_args()
    
    # Handle commands
    if args.command == 'create':
        print(f"Creating project: {args.name}")
        if args.description:
            print(f"Description: {args.description}")
        create(name=args.name, description=args.description)
    elif args.command == 'read':
        if args.name:
            print(f"Reading project by name: {args.name}")
            read(name=args.name)
        elif args.id:
            print(f"Reading project by ID: {args.id}")
            read(project_id=args.id)
        else:
            print("Please provide either --name or --id")
            read_parser.print_help()
    elif args.command == 'list':
        print("Listing all projects")
        list()
    elif args.command == 'update':
        print(f"Updating project...")
        if args.description:
            print(f"New description: {args.description}")
        update(project_id=args.id, name=args.name, description=args.description)
    elif args.command == 'delete':
        print(f"Deleting project...")
        delete(project_id=args.id, name=args.name)
    else:
        parser.print_help()