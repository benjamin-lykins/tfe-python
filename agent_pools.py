import argparse
import os
import dotenv

from pytfe import TFEClient, TFEConfig
from pytfe.models import (
    AgentPoolAssignToWorkspacesOptions,
    AgentPoolCreateOptions,
    AgentPoolListOptions,
    AgentPoolReadOptions,
    AgentPoolRemoveFromWorkspacesOptions,
    AgentPoolUpdateOptions,
    ProjectListOptions,
    WorkspaceListOptions,
)

def create(name, description=None):
    """Create a new agent pool"""
    try:
        create_options = AgentPoolCreateOptions(name=name)
        
        pool = client.agent_pools.create(org, create_options)
        print(f"Successfully created agent pool: {pool.name}")
        print(f"Agent Pool ID: {pool.id}")
    except Exception as e:
        print(f"Error creating agent pool: {e}")

def read(name=None, pool_id=None):
    """Read agent pool details by name or ID"""
    try:
        # If name is provided, list and find it
        if name and not pool_id:
            pools = client.agent_pools.list(org, AgentPoolListOptions())
            for pool in pools:
                if pool.name == name:
                    pool_id = pool.id
                    break
            else:
                print(f"Agent pool '{name}' not found")
                return
        
        if not pool_id:
            print("Please provide either --name or --id")
            return
        
        pool = client.agent_pools.read(pool_id)
        
        print(f"Agent Pool: {pool.name}")
        print(f"ID: {pool.id}")
        print(f"Organization Scoped: {pool.organization_scoped}")
        print(f"Agents Count: {pool.agent_count}")
        print(f"Organization: {pool.organization}")
        print(f"Created At: {pool.created_at}")
    except Exception as e:
        print(f"Error reading agent pool: {e}")

def list():
    """List all agent pools in the organization"""
    try:
        pools = client.agent_pools.list(org, AgentPoolListOptions())
        
        if not pools:
            print("No agent pools found")
            return
        
        for pool in pools:
            agent_count = pool.agent_count if hasattr(pool, 'agent_count') else 'N/A'
            print(f"- {pool.name} (ID: {pool.id}, Agents: {agent_count})")
    except Exception as e:
        print(f"Error listing agent pools: {e}")

def update(name=None, pool_id=None, new_name=None, description=None):
    """Update an agent pool"""
    try:
        # If name is provided, find the pool ID
        if name and not pool_id:
            pools = client.agent_pools.list(org, AgentPoolListOptions())
            for pool in pools:
                if pool.name == name:
                    pool_id = pool.id
                    break
            else:
                print(f"Agent pool '{name}' not found")
                return
        
        if not pool_id:
            print("Please provide either --name or --id")
            return
        
        if not new_name:
            print("Please provide --new-name")
            return
        
        update_options = AgentPoolUpdateOptions(name=new_name)
        
        pool = client.agent_pools.update(pool_id, update_options)
        print(f"Successfully updated agent pool: {pool.name}")
    except Exception as e:
        print(f"Error updating agent pool: {e}")

def delete(name=None, pool_id=None):
    """Delete an agent pool"""
    try:
        # If name is provided, find the pool ID
        if name and not pool_id:
            pools = client.agent_pools.list(org, AgentPoolListOptions())
            for pool in pools:
                if pool.name == name:
                    pool_id = pool.id
                    break
            else:
                print(f"Agent pool '{name}' not found")
                return
        
        if not pool_id:
            print("Please provide either --name or --id")
            return
        
        client.agent_pools.delete(pool_id)
        print(f"Successfully deleted agent pool")
    except Exception as e:
        print(f"Error deleting agent pool: {e}")

def _resolve_pool_id(pool_name=None, pool_id=None):
    """Resolve pool name to ID if needed"""
    if pool_id:
        return pool_id
    if not pool_name:
        print("Please provide either --pool-name or --pool-id")
        return None
    
    pools = client.agent_pools.list(org, AgentPoolListOptions())
    for pool in pools:
        if pool.name == pool_name:
            return pool.id
    
    print(f"Agent pool '{pool_name}' not found")
    return None

def _resolve_project_id(project_name=None, project_id=None):
    """Resolve project name to ID if needed"""
    if project_id:
        return project_id
    if not project_name:
        print("Please provide either --project-name or --project-id")
        return None
    
    projects = client.projects.list(org, ProjectListOptions())
    for project in projects:
        if project.name == project_name:
            return project.id
    
    print(f"Project '{project_name}' not found")
    return None

def _get_workspaces_in_project(project_id):
    """Get all workspace IDs for a project"""
    options = WorkspaceListOptions(project_id=project_id)
    workspaces = client.workspaces.list(org, options)
    project_workspace_ids = [ws.id for ws in workspaces]
    return project_workspace_ids

def assign_to_project(pool_name=None, pool_id=None, project_name=None, project_id=None):
    """Assign agent pool to all workspaces in a project"""
    try:
        pool_id = _resolve_pool_id(pool_name=pool_name, pool_id=pool_id)
        if not pool_id:
            return
        
        project_id = _resolve_project_id(project_name=project_name, project_id=project_id)
        if not project_id:
            return
        
        workspace_ids = _get_workspaces_in_project(project_id)
        if not workspace_ids:
            print(f"No workspaces found in project {project_id}")
            return
        
        options = AgentPoolAssignToWorkspacesOptions(workspace_ids=workspace_ids)
        client.agent_pools.assign_to_workspaces(pool_id, options)
        print(f"Successfully assigned agent pool to {len(workspace_ids)} workspace(s) in project")
    except Exception as e:
        print(f"Error assigning agent pool to project: {e}")

def remove_from_project(pool_name=None, pool_id=None, project_name=None, project_id=None):
    """Remove agent pool from all workspaces in a project"""
    try:
        pool_id = _resolve_pool_id(pool_name=pool_name, pool_id=pool_id)
        if not pool_id:
            return
        
        project_id = _resolve_project_id(project_name=project_name, project_id=project_id)
        if not project_id:
            return
        
        workspace_ids = _get_workspaces_in_project(project_id)
        if not workspace_ids:
            print(f"No workspaces found in project {project_id}")
            return
        
        options = AgentPoolRemoveFromWorkspacesOptions(workspace_ids=workspace_ids)
        client.agent_pools.remove_from_workspaces(pool_id, options)
        print(f"Successfully removed agent pool from {len(workspace_ids)} workspace(s) in project")
    except Exception as e:
        print(f"Error removing agent pool from project: {e}")

if __name__ == "__main__":
    dotenv.load_dotenv()
    
    org = os.getenv("TFE_ORGANIZATION")
    client = TFEClient(TFEConfig())
    
    parser = argparse.ArgumentParser(description="Agent Pool management CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new agent pool')
    create_parser.add_argument("--name", type=str, required=True, help="Name of the agent pool")
    
    # Read command
    read_parser = subparsers.add_parser('read', help='Read agent pool details')
    read_parser.add_argument("--name", type=str, help="Name of the agent pool to read")
    read_parser.add_argument("--id", type=str, help="ID of the agent pool to read")
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all agent pools')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update an agent pool')
    update_parser.add_argument("--name", type=str, help="Current name of the agent pool to update")
    update_parser.add_argument("--id", type=str, help="ID of the agent pool to update")
    update_parser.add_argument("--new-name", type=str, help="New name for the agent pool")
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete an agent pool')
    delete_parser.add_argument("--name", type=str, help="Name of the agent pool to delete")
    delete_parser.add_argument("--id", type=str, help="ID of the agent pool to delete")
    
    # Assign to project command
    assign_project_parser = subparsers.add_parser('assign-to-project', help='Assign agent pool to all workspaces in a project')
    assign_project_parser.add_argument("--pool-name", type=str, help="Name of the agent pool")
    assign_project_parser.add_argument("--pool-id", type=str, help="ID of the agent pool")
    assign_project_parser.add_argument("--project-name", type=str, help="Name of the project")
    assign_project_parser.add_argument("--project-id", type=str, help="ID of the project")
    
    # Remove from project command
    remove_project_parser = subparsers.add_parser('remove-from-project', help='Remove agent pool from all workspaces in a project')
    remove_project_parser.add_argument("--pool-name", type=str, help="Name of the agent pool")
    remove_project_parser.add_argument("--pool-id", type=str, help="ID of the agent pool")
    remove_project_parser.add_argument("--project-name", type=str, help="Name of the project")
    remove_project_parser.add_argument("--project-id", type=str, help="ID of the project")
    
    args = parser.parse_args()
    
    # Handle commands
    if args.command == 'create':
        print(f"Creating agent pool: {args.name}")
        create(name=args.name)
    elif args.command == 'read':
        if args.name:
            print(f"Reading agent pool by name: {args.name}")
            read(name=args.name)
        elif args.id:
            print(f"Reading agent pool by ID: {args.id}")
            read(pool_id=args.id)
        else:
            print("Please provide either --name or --id")
            read_parser.print_help()
    elif args.command == 'list':
        print("Listing all agent pools")
        list()
    elif args.command == 'update':
        print(f"Updating agent pool...")
        update(name=args.name, pool_id=args.id, new_name=args.new_name)
    elif args.command == 'delete':
        print(f"Deleting agent pool...")
        delete(name=args.name, pool_id=args.id)
    elif args.command == 'assign-to-project':
        print("Assigning agent pool to project workspaces...")
        assign_to_project(pool_name=args.pool_name, pool_id=args.pool_id, project_name=args.project_name, project_id=args.project_id)
    elif args.command == 'remove-from-project':
        print("Removing agent pool from project workspaces...")
        remove_from_project(pool_name=args.pool_name, pool_id=args.pool_id, project_name=args.project_name, project_id=args.project_id)
    else:
        parser.print_help()
