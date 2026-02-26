import argparse
import os
import dotenv

from pytfe import TFEClient, TFEConfig

def create(name):
    pass

def read(name):
    pass

def list():
    pass

def update(name):
    pass

def delete(name):
    pass

if __name__ == "__main__":
    dotenv.load_dotenv()
    
    org = os.getenv("TFE_ORGANIZATION")
    client = TFEClient(TFEConfig())
    
    parser = argparse.ArgumentParser(description="Team management CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new team')
    create_parser.add_argument("--name", type=str, required=True, help="Name of the team")
    
    # Read command
    read_parser = subparsers.add_parser('read', help='Read team details')
    read_parser.add_argument("--name", type=str, required=True, help="Name of the team to read")
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all teams')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update a team')
    update_parser.add_argument("--name", type=str, required=True, help="Name of the team to update")
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a team')
    delete_parser.add_argument("--name", type=str, required=True, help="Name of the team to delete")
    
    args = parser.parse_args()
    
    # Handle commands
    if args.command == 'create':
        print(f"Creating team: {args.name}")
        create(name=args.name)
    elif args.command == 'read':
        print(f"Reading team: {args.name}")
        read(name=args.name)
    elif args.command == 'list':
        print("Listing all teams")
        list()
    elif args.command == 'update':
        print(f"Updating team: {args.name}")
        update(name=args.name)
    elif args.command == 'delete':
        print(f"Deleting team: {args.name}")
        delete(name=args.name)
    else:
        parser.print_help()