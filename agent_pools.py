import argparse
import os
import dotenv

from pytfe import TFEClient, TFEConfig
from pytfe.models import (
    AgentPoolCreateOptions,
    AgentPoolListOptions,
    AgentPoolReadOptions,
    AgentPoolUpdateOptions,
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
    else:
        parser.print_help()
