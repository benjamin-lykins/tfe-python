import argparse
import os
import dotenv
import json

from pytfe import TFEClient, TFEConfig
from pytfe._http import HTTPTransport

def create(name, visibility="secret", organization_access=None):
    """Create a new team
    
    Args:
        name: Name of the team
        visibility: Team visibility (secret or organization)
        organization_access: Dict with organization-level permissions
    """
    try:
        payload = {
            "data": {
                "type": "teams",
                "attributes": {
                    "name": name,
                    "visibility": visibility
                }
            }
        }
        
        if organization_access:
            payload["data"]["attributes"]["organization-access"] = organization_access
        
        response = http.request("POST", f"/api/v2/organizations/{org}/teams", json_body=payload)
        team_data = response.json()["data"]
        print(f"Successfully created team: {team_data['attributes']['name']}")
        print(f"Team ID: {team_data['id']}")
    except Exception as e:
        print(f"Error creating team: {e}")

def read(name=None, team_id=None):
    """Read team details by name or ID"""
    try:
        # If name is provided, we need to list and find it
        if name and not team_id:
            response = http.request("GET", f"/api/v2/organizations/{org}/teams")
            teams_data = response.json()["data"]
            
            found_team = None
            for team in teams_data:
                if team["attributes"]["name"] == name:
                    found_team = team
                    break
            
            if not found_team:
                print(f"Team '{name}' not found")
                return
            
            team_id = found_team["id"]
        
        if not team_id:
            print("Please provide either --name or --id")
            return
        
        # Get detailed team information
        response = http.request("GET", f"/api/v2/teams/{team_id}")
        team_data = response.json()["data"]
        attrs = team_data["attributes"]
        
        print(f"Team: {attrs['name']}")
        print(f"ID: {team_data['id']}")
        print(f"Visibility: {attrs.get('visibility', 'N/A')}")
        print(f"Users Count: {attrs.get('users-count', 'N/A')}")
        if attrs.get('organization-access'):
            print(f"Organization Access: {attrs['organization-access']}")
    except Exception as e:
        print(f"Error reading team: {e}")

def list():
    """List all teams in the organization"""
    try:
        response = http.request("GET", f"/api/v2/organizations/{org}/teams")
        teams_data = response.json()["data"]
        
        if not teams_data:
            print("No teams found")
            return
        
        for team in teams_data:
            attrs = team["attributes"]
            print(f"- {attrs['name']} (ID: {team['id']}, Visibility: {attrs.get('visibility', 'N/A')})")
    except Exception as e:
        print(f"Error listing teams: {e}")

def update(name=None, team_id=None, new_name=None, visibility=None, organization_access=None):
    """Update a team"""
    try:
        # If name is provided, find the team ID
        if name and not team_id:
            response = http.request("GET", f"/api/v2/organizations/{org}/teams")
            teams_data = response.json()["data"]
            
            for team in teams_data:
                if team["attributes"]["name"] == name:
                    team_id = team["id"]
                    break
            else:
                print(f"Team '{name}' not found")
                return
        
        if not team_id:
            print("Please provide either --name or --id")
            return
        
        payload = {
            "data": {
                "type": "teams",
                "attributes": {}
            }
        }
        
        if new_name:
            payload["data"]["attributes"]["name"] = new_name
        if visibility:
            payload["data"]["attributes"]["visibility"] = visibility
        if organization_access:
            payload["data"]["attributes"]["organization-access"] = organization_access
        
        response = http.request("PATCH", f"/api/v2/teams/{team_id}", json_body=payload)
        team_data = response.json()["data"]
        print(f"Successfully updated team: {team_data['attributes']['name']}")
    except Exception as e:
        print(f"Error updating team: {e}")

def delete(name=None, team_id=None):
    """Delete a team"""
    try:
        # If name is provided, find the team ID
        if name and not team_id:
            response = http.request("GET", f"/api/v2/organizations/{org}/teams")
            teams_data = response.json()["data"]
            
            for team in teams_data:
                if team["attributes"]["name"] == name:
                    team_id = team["id"]
                    break
            else:
                print(f"Team '{name}' not found")
                return
        
        if not team_id:
            print("Please provide either --name or --id")
            return
        
        http.request("DELETE", f"/api/v2/teams/{team_id}")
        print(f"Successfully deleted team")
    except Exception as e:
        print(f"Error deleting team: {e}")

if __name__ == "__main__":
    dotenv.load_dotenv()
    
    org = os.getenv("TFE_ORGANIZATION")
    config = TFEConfig()
    client = TFEClient(config)
    http = HTTPTransport(
        address=config.address,
        token=config.token,
        timeout=config.timeout,
        verify_tls=config.verify_tls,
        user_agent_suffix=config.user_agent_suffix,
        max_retries=config.max_retries,
        backoff_base=config.backoff_base,
        backoff_cap=config.backoff_cap,
        backoff_jitter=config.backoff_jitter,
        http2=config.http2,
        proxies=config.proxies,
        ca_bundle=config.ca_bundle
    )
    
    parser = argparse.ArgumentParser(description="Team management CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new team')
    create_parser.add_argument("--name", type=str, required=True, help="Name of the team")
    create_parser.add_argument("--visibility", type=str, choices=["secret", "organization"], default="secret", help="Team visibility (secret or organization)")
    
    # Read command
    read_parser = subparsers.add_parser('read', help='Read team details')
    read_parser.add_argument("--name", type=str, help="Name of the team to read")
    read_parser.add_argument("--id", type=str, help="ID of the team to read")
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all teams')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update a team')
    update_parser.add_argument("--name", type=str, help="Current name of the team to update")
    update_parser.add_argument("--id", type=str, help="ID of the team to update")
    update_parser.add_argument("--new-name", type=str, help="New name for the team")
    update_parser.add_argument("--visibility", type=str, choices=["secret", "organization"], help="New team visibility")
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a team')
    delete_parser.add_argument("--name", type=str, help="Name of the team to delete")
    delete_parser.add_argument("--id", type=str, help="ID of the team to delete")
    
    args = parser.parse_args()
    
    # Handle commands
    if args.command == 'create':
        print(f"Creating team: {args.name}")
        create(name=args.name, visibility=args.visibility)
    elif args.command == 'read':
        if args.name:
            print(f"Reading team by name: {args.name}")
            read(name=args.name)
        elif args.id:
            print(f"Reading team by ID: {args.id}")
            read(team_id=args.id)
        else:
            print("Please provide either --name or --id")
            read_parser.print_help()
    elif args.command == 'list':
        print("Listing all teams")
        list()
    elif args.command == 'update':
        print(f"Updating team...")
        update(name=args.name, team_id=args.id, new_name=args.new_name, visibility=args.visibility)
    elif args.command == 'delete':
        print(f"Deleting team...")
        delete(name=args.name, team_id=args.id)
    else:
        parser.print_help()