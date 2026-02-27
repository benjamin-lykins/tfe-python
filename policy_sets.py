import argparse
import os
import dotenv

from pytfe import TFEClient, TFEConfig
from pytfe.models import (
    PolicySetCreateOptions,
    PolicySetListOptions,
    PolicySetUpdateOptions,
    PolicySetAddPoliciesOptions,
    PolicySetAddWorkspacesOptions,
    PolicySetAddProjectsOptions,
    PolicySetRemovePoliciesOptions,
    PolicySetRemoveWorkspacesOptions,
    PolicySetRemoveProjectsOptions,
)

def create(name, description=None, is_global=False):
    """Create a new policy set"""
    try:
        create_options = PolicySetCreateOptions(
            name=name,
            **{"global": is_global}
        )
        if description:
            create_options.description = description
        
        policy_set = client.policy_sets.create(org, create_options)
        print(f"Successfully created policy set: {policy_set.name}")
        print(f"Policy Set ID: {policy_set.id}")
    except Exception as e:
        print(f"Error creating policy set: {e}")

def read(name=None, policy_set_id=None):
    """Read policy set details by name or ID"""
    try:
        # If name is provided, list and find it
        if name and not policy_set_id:
            result = client.policy_sets.list(org, PolicySetListOptions())
            policy_sets = result.items if hasattr(result, 'items') else result
            for ps in policy_sets:
                if ps.name == name:
                    policy_set_id = ps.id
                    break
            else:
                print(f"Policy set '{name}' not found")
                return
        
        if not policy_set_id:
            print("Please provide either --name or --id")
            return
        
        policy_set = client.policy_sets.read(policy_set_id)
        
        print(f"Policy Set: {policy_set.name}")
        print(f"ID: {policy_set.id}")
        if policy_set.description:
            print(f"Description: {policy_set.description}")
        print(f"Policies Count: {policy_set.policy_count if hasattr(policy_set, 'policy_count') else 'N/A'}")
        print(f"Workspaces Count: {policy_set.workspace_count if hasattr(policy_set, 'workspace_count') else 'N/A'}")
        print(f"Created At: {policy_set.created_at}")
    except Exception as e:
        print(f"Error reading policy set: {e}")

def list():
    """List all policy sets in the organization"""
    try:
        result = client.policy_sets.list(org, PolicySetListOptions())
        policy_sets = result.items if hasattr(result, 'items') else result
        
        if not policy_sets:
            print("No policy sets found")
            return
        
        for ps in policy_sets:
            policy_count = ps.policy_count if hasattr(ps, 'policy_count') else 'N/A'
            ws_count = ps.workspace_count if hasattr(ps, 'workspace_count') else 'N/A'
            print(f"- {ps.name} (ID: {ps.id}, Policies: {policy_count}, Workspaces: {ws_count})")
    except Exception as e:
        print(f"Error listing policy sets: {e}")

def update(name=None, policy_set_id=None, new_name=None, description=None):
    """Update a policy set"""
    try:
        # If name is provided, find the policy set ID
        if name and not policy_set_id:
            result = client.policy_sets.list(org, PolicySetListOptions())
            policy_sets = result.items if hasattr(result, 'items') else result
            for ps in policy_sets:
                if ps.name == name:
                    policy_set_id = ps.id
                    break
            else:
                print(f"Policy set '{name}' not found")
                return
        
        if not policy_set_id:
            print("Please provide either --name or --id")
            return
        
        update_options = PolicySetUpdateOptions()
        if new_name:
            update_options.name = new_name
        if description is not None:
            update_options.description = description
        
        policy_set = client.policy_sets.update(policy_set_id, update_options)
        print(f"Successfully updated policy set: {policy_set.name}")
    except Exception as e:
        print(f"Error updating policy set: {e}")

def delete(name=None, policy_set_id=None):
    """Delete a policy set"""
    try:
        # If name is provided, find the policy set ID
        if name and not policy_set_id:
            result = client.policy_sets.list(org, PolicySetListOptions())
            policy_sets = result.items if hasattr(result, 'items') else result
            for ps in policy_sets:
                if ps.name == name:
                    policy_set_id = ps.id
                    break
            else:
                print(f"Policy set '{name}' not found")
                return
        
        if not policy_set_id:
            print("Please provide either --name or --id")
            return
        
        client.policy_sets.delete(policy_set_id)
        print(f"Successfully deleted policy set")
    except Exception as e:
        print(f"Error deleting policy set: {e}")

def add_policies(policy_set_name=None, policy_set_id=None, policy_ids=None):
    """Add policies to a policy set"""
    try:
        # If name is provided, find the policy set ID
        if policy_set_name and not policy_set_id:
            result = client.policy_sets.list(org, PolicySetListOptions())
            policy_sets = result.items if hasattr(result, 'items') else result
            for ps in policy_sets:
                if ps.name == policy_set_name:
                    policy_set_id = ps.id
                    break
            else:
                print(f"Policy set '{policy_set_name}' not found")
                return
        
        if not policy_set_id:
            print("Please provide either --policy-set-name or --policy-set-id")
            return
        
        if not policy_ids:
            print("Please provide at least one policy ID with --policy-id")
            return
        
        options = PolicySetAddPoliciesOptions(policy_ids=policy_ids)
        client.policy_sets.add_policies(policy_set_id, options)
        print(f"Successfully added {len(policy_ids)} policy/policies to policy set")
    except Exception as e:
        print(f"Error adding policies: {e}")

def remove_policies(policy_set_name=None, policy_set_id=None, policy_ids=None):
    """Remove policies from a policy set"""
    try:
        # If name is provided, find the policy set ID
        if policy_set_name and not policy_set_id:
            result = client.policy_sets.list(org, PolicySetListOptions())
            policy_sets = result.items if hasattr(result, 'items') else result
            for ps in policy_sets:
                if ps.name == policy_set_name:
                    policy_set_id = ps.id
                    break
            else:
                print(f"Policy set '{policy_set_name}' not found")
                return
        
        if not policy_set_id:
            print("Please provide either --policy-set-name or --policy-set-id")
            return
        
        if not policy_ids:
            print("Please provide at least one policy ID with --policy-id")
            return
        
        options = PolicySetRemovePoliciesOptions(policy_ids=policy_ids)
        client.policy_sets.remove_policies(policy_set_id, options)
        print(f"Successfully removed {len(policy_ids)} policy/policies from policy set")
    except Exception as e:
        print(f"Error removing policies: {e}")

def add_workspaces(policy_set_name=None, policy_set_id=None, workspace_ids=None):
    """Add workspaces to a policy set"""
    try:
        # If name is provided, find the policy set ID
        if policy_set_name and not policy_set_id:
            result = client.policy_sets.list(org, PolicySetListOptions())
            policy_sets = result.items if hasattr(result, 'items') else result
            for ps in policy_sets:
                if ps.name == policy_set_name:
                    policy_set_id = ps.id
                    break
            else:
                print(f"Policy set '{policy_set_name}' not found")
                return
        
        if not policy_set_id:
            print("Please provide either --policy-set-name or --policy-set-id")
            return
        
        if not workspace_ids:
            print("Please provide at least one workspace ID with --workspace-id")
            return
        
        options = PolicySetAddWorkspacesOptions(workspace_ids=workspace_ids)
        client.policy_sets.add_workspaces(policy_set_id, options)
        print(f"Successfully added {len(workspace_ids)} workspace(s) to policy set")
    except Exception as e:
        print(f"Error adding workspaces: {e}")

def remove_workspaces(policy_set_name=None, policy_set_id=None, workspace_ids=None):
    """Remove workspaces from a policy set"""
    try:
        # If name is provided, find the policy set ID
        if policy_set_name and not policy_set_id:
            result = client.policy_sets.list(org, PolicySetListOptions())
            policy_sets = result.items if hasattr(result, 'items') else result
            for ps in policy_sets:
                if ps.name == policy_set_name:
                    policy_set_id = ps.id
                    break
            else:
                print(f"Policy set '{policy_set_name}' not found")
                return
        
        if not policy_set_id:
            print("Please provide either --policy-set-name or --policy-set-id")
            return
        
        if not workspace_ids:
            print("Please provide at least one workspace ID with --workspace-id")
            return
        
        options = PolicySetRemoveWorkspacesOptions(workspace_ids=workspace_ids)
        client.policy_sets.remove_workspaces(policy_set_id, options)
        print(f"Successfully removed {len(workspace_ids)} workspace(s) from policy set")
    except Exception as e:
        print(f"Error removing workspaces: {e}")

def add_projects(policy_set_name=None, policy_set_id=None, project_ids=None):
    """Add projects to a policy set"""
    try:
        # If name is provided, find the policy set ID
        if policy_set_name and not policy_set_id:
            result = client.policy_sets.list(org, PolicySetListOptions())
            policy_sets = result.items if hasattr(result, 'items') else result
            for ps in policy_sets:
                if ps.name == policy_set_name:
                    policy_set_id = ps.id
                    break
            else:
                print(f"Policy set '{policy_set_name}' not found")
                return
        
        if not policy_set_id:
            print("Please provide either --policy-set-name or --policy-set-id")
            return
        
        if not project_ids:
            print("Please provide at least one project ID with --project-id")
            return
        
        options = PolicySetAddProjectsOptions(project_ids=project_ids)
        client.policy_sets.add_projects(policy_set_id, options)
        print(f"Successfully added {len(project_ids)} project(s) to policy set")
    except Exception as e:
        print(f"Error adding projects: {e}")

def remove_projects(policy_set_name=None, policy_set_id=None, project_ids=None):
    """Remove projects from a policy set"""
    try:
        # If name is provided, find the policy set ID
        if policy_set_name and not policy_set_id:
            result = client.policy_sets.list(org, PolicySetListOptions())
            policy_sets = result.items if hasattr(result, 'items') else result
            for ps in policy_sets:
                if ps.name == policy_set_name:
                    policy_set_id = ps.id
                    break
            else:
                print(f"Policy set '{policy_set_name}' not found")
                return
        
        if not policy_set_id:
            print("Please provide either --policy-set-name or --policy-set-id")
            return
        
        if not project_ids:
            print("Please provide at least one project ID with --project-id")
            return
        
        options = PolicySetRemoveProjectsOptions(project_ids=project_ids)
        client.policy_sets.remove_projects(policy_set_id, options)
        print(f"Successfully removed {len(project_ids)} project(s) from policy set")
    except Exception as e:
        print(f"Error removing projects: {e}")

if __name__ == "__main__":
    dotenv.load_dotenv()
    
    org = os.getenv("TFE_ORGANIZATION")
    client = TFEClient(TFEConfig())
    
    parser = argparse.ArgumentParser(description="Policy Set management CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new policy set')
    create_parser.add_argument("--name", type=str, required=True, help="Name of the policy set")
    create_parser.add_argument("--description", type=str, help="Policy set description")
    create_parser.add_argument("--global", dest="is_global", action="store_true", help="Make this a global policy set")
    
    # Read command
    read_parser = subparsers.add_parser('read', help='Read policy set details')
    read_parser.add_argument("--name", type=str, help="Name of the policy set to read")
    read_parser.add_argument("--id", type=str, help="ID of the policy set to read")
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all policy sets')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update a policy set')
    update_parser.add_argument("--name", type=str, help="Current name of the policy set to update")
    update_parser.add_argument("--id", type=str, help="ID of the policy set to update")
    update_parser.add_argument("--new-name", type=str, help="New name for the policy set")
    update_parser.add_argument("--description", type=str, help="New description for the policy set")
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a policy set')
    delete_parser.add_argument("--name", type=str, help="Name of the policy set to delete")
    delete_parser.add_argument("--id", type=str, help="ID of the policy set to delete")
    
    # Add policies command
    add_policies_parser = subparsers.add_parser('add-policies', help='Add policies to a policy set')
    add_policies_parser.add_argument("--policy-set-name", type=str, help="Name of the policy set")
    add_policies_parser.add_argument("--policy-set-id", type=str, help="ID of the policy set")
    add_policies_parser.add_argument("--policy-id", type=str, action="append", dest="policy_ids", help="Policy ID (can be repeated)")
    
    # Remove policies command
    remove_policies_parser = subparsers.add_parser('remove-policies', help='Remove policies from a policy set')
    remove_policies_parser.add_argument("--policy-set-name", type=str, help="Name of the policy set")
    remove_policies_parser.add_argument("--policy-set-id", type=str, help="ID of the policy set")
    remove_policies_parser.add_argument("--policy-id", type=str, action="append", dest="policy_ids", help="Policy ID (can be repeated)")
    
    # Add workspaces command
    add_workspaces_parser = subparsers.add_parser('add-workspaces', help='Add workspaces to a policy set')
    add_workspaces_parser.add_argument("--policy-set-name", type=str, help="Name of the policy set")
    add_workspaces_parser.add_argument("--policy-set-id", type=str, help="ID of the policy set")
    add_workspaces_parser.add_argument("--workspace-id", type=str, action="append", dest="workspace_ids", help="Workspace ID (can be repeated)")
    
    # Remove workspaces command
    remove_workspaces_parser = subparsers.add_parser('remove-workspaces', help='Remove workspaces from a policy set')
    remove_workspaces_parser.add_argument("--policy-set-name", type=str, help="Name of the policy set")
    remove_workspaces_parser.add_argument("--policy-set-id", type=str, help="ID of the policy set")
    remove_workspaces_parser.add_argument("--workspace-id", type=str, action="append", dest="workspace_ids", help="Workspace ID (can be repeated)")
    
    # Add projects command
    add_projects_parser = subparsers.add_parser('add-projects', help='Add projects to a policy set')
    add_projects_parser.add_argument("--policy-set-name", type=str, help="Name of the policy set")
    add_projects_parser.add_argument("--policy-set-id", type=str, help="ID of the policy set")
    add_projects_parser.add_argument("--project-id", type=str, action="append", dest="project_ids", help="Project ID (can be repeated)")
    
    # Remove projects command
    remove_projects_parser = subparsers.add_parser('remove-projects', help='Remove projects from a policy set')
    remove_projects_parser.add_argument("--policy-set-name", type=str, help="Name of the policy set")
    remove_projects_parser.add_argument("--policy-set-id", type=str, help="ID of the policy set")
    remove_projects_parser.add_argument("--project-id", type=str, action="append", dest="project_ids", help="Project ID (can be repeated)")
    
    args = parser.parse_args()
    
    # Handle commands
    if args.command == 'create':
        print(f"Creating policy set: {args.name}")
        if args.description:
            print(f"Description: {args.description}")
        create(name=args.name, description=args.description, is_global=args.is_global)
    elif args.command == 'read':
        if args.name:
            print(f"Reading policy set by name: {args.name}")
            read(name=args.name)
        elif args.id:
            print(f"Reading policy set by ID: {args.id}")
            read(policy_set_id=args.id)
        else:
            print("Please provide either --name or --id")
            read_parser.print_help()
    elif args.command == 'list':
        print("Listing all policy sets")
        list()
    elif args.command == 'update':
        print(f"Updating policy set...")
        update(name=args.name, policy_set_id=args.id, new_name=args.new_name, description=args.description)
    elif args.command == 'delete':
        print(f"Deleting policy set...")
        delete(name=args.name, policy_set_id=args.id)
    elif args.command == 'add-policies':
        print(f"Adding policies to policy set...")
        add_policies(policy_set_name=args.policy_set_name, policy_set_id=args.policy_set_id, policy_ids=args.policy_ids)
    elif args.command == 'remove-policies':
        print(f"Removing policies from policy set...")
        remove_policies(policy_set_name=args.policy_set_name, policy_set_id=args.policy_set_id, policy_ids=args.policy_ids)
    elif args.command == 'add-workspaces':
        print(f"Adding workspaces to policy set...")
        add_workspaces(policy_set_name=args.policy_set_name, policy_set_id=args.policy_set_id, workspace_ids=args.workspace_ids)
    elif args.command == 'remove-workspaces':
        print(f"Removing workspaces from policy set...")
        remove_workspaces(policy_set_name=args.policy_set_name, policy_set_id=args.policy_set_id, workspace_ids=args.workspace_ids)
    elif args.command == 'add-projects':
        print(f"Adding projects to policy set...")
        add_projects(policy_set_name=args.policy_set_name, policy_set_id=args.policy_set_id, project_ids=args.project_ids)
    elif args.command == 'remove-projects':
        print(f"Removing projects from policy set...")
        remove_projects(policy_set_name=args.policy_set_name, policy_set_id=args.policy_set_id, project_ids=args.project_ids)
    else:
        parser.print_help()
