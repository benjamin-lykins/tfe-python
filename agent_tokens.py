import argparse
import os
import dotenv

from pytfe import TFEClient, TFEConfig
from pytfe.models import (
    AgentTokenCreateOptions,
    AgentTokenListOptions,
)

def create(pool_name=None, pool_id=None, description=None):
    """Create a new agent token in an agent pool"""
    try:
        # If pool_name is provided, find the pool ID
        if pool_name and not pool_id:
            pools = client.agent_pools.list(org)
            for pool in pools:
                if pool.name == pool_name:
                    pool_id = pool.id
                    break
            else:
                print(f"Agent pool '{pool_name}' not found")
                return
        
        if not pool_id:
            print("Please provide either --pool-name or --pool-id")
            return
        
        create_options = AgentTokenCreateOptions(description=description) if description else AgentTokenCreateOptions()
        
        token = client.agent_tokens.create(pool_id, create_options)
        print(f"Successfully created agent token")
        print(f"Token ID: {token.id}")
        print(f"Token: {token.token}")
        print(f"⚠️  Save this token now - you won't be able to see it again!")
    except Exception as e:
        print(f"Error creating agent token: {e}")

def read(token_id):
    """Read agent token details (limited - tokens don't show values after creation)"""
    try:
        token = client.agent_tokens.read(token_id)
        
        print(f"Agent Token: {token.id}")
        if token.description:
            print(f"Description: {token.description}")
        print(f"Created At: {token.created_at}")
    except Exception as e:
        print(f"Error reading agent token: {e}")

def list(pool_name=None, pool_id=None):
    """List all agent tokens in an agent pool"""
    try:
        # If pool_name is provided, find the pool ID
        if pool_name and not pool_id:
            pools = client.agent_pools.list(org)
            for pool in pools:
                if pool.name == pool_name:
                    pool_id = pool.id
                    break
            else:
                print(f"Agent pool '{pool_name}' not found")
                return
        
        if not pool_id:
            print("Please provide either --pool-name or --pool-id")
            return
        
        tokens = client.agent_tokens.list(pool_id, AgentTokenListOptions())
        
        if not tokens:
            print(f"No agent tokens found in the agent pool")
            return
        
        for token in tokens:
            desc = f" - {token.description}" if token.description else ""
            print(f"- {token.id}{desc} (Created: {token.created_at})")
    except Exception as e:
        print(f"Error listing agent tokens: {e}")

def delete(token_id):
    """Delete an agent token"""
    try:
        client.agent_tokens.delete(token_id)
        print(f"Successfully deleted agent token")
    except Exception as e:
        print(f"Error deleting agent token: {e}")

if __name__ == "__main__":
    dotenv.load_dotenv()
    
    org = os.getenv("TFE_ORGANIZATION")
    client = TFEClient(TFEConfig())
    
    parser = argparse.ArgumentParser(description="Agent Token management CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new agent token')
    create_parser.add_argument("--pool-name", type=str, help="Name of the agent pool")
    create_parser.add_argument("--pool-id", type=str, help="ID of the agent pool")
    create_parser.add_argument("--description", type=str, help="Optional token description")
    
    # Read command
    read_parser = subparsers.add_parser('read', help='Read agent token details')
    read_parser.add_argument("--id", type=str, required=True, help="ID of the agent token to read")
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all agent tokens in a pool')
    list_parser.add_argument("--pool-name", type=str, help="Name of the agent pool")
    list_parser.add_argument("--pool-id", type=str, help="ID of the agent pool")
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete an agent token')
    delete_parser.add_argument("--id", type=str, required=True, help="ID of the agent token to delete")
    
    args = parser.parse_args()
    
    # Handle commands
    if args.command == 'create':
        print(f"Creating agent token...")
        if args.pool_name:
            print(f"Agent Pool: {args.pool_name}")
        elif args.pool_id:
            print(f"Agent Pool ID: {args.pool_id}")
        create(pool_name=args.pool_name, pool_id=args.pool_id, description=args.description)
    elif args.command == 'read':
        print(f"Reading agent token: {args.id}")
        read(token_id=args.id)
    elif args.command == 'list':
        print(f"Listing agent tokens...")
        list(pool_name=args.pool_name, pool_id=args.pool_id)
    elif args.command == 'delete':
        print(f"Deleting agent token: {args.id}")
        delete(token_id=args.id)
    else:
        parser.print_help()
