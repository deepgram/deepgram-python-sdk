"""
Example: Management API - Members

This example shows how to manage project members.
"""

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient

client = DeepgramClient()

try:
    # Get project ID (replace with your actual project ID)
    projects = client.manage.v1.projects.list()
    if not projects.projects:
        print("No projects found. Please create a project first.")
        exit(1)
    
    project_id = projects.projects[0].project_id
    print(f"Using project: {project_id}")
    
    # List all members
    print("\nListing project members...")
    members = client.manage.v1.projects.members.list(project_id=project_id)
    print(f"Found {len(members.members)} members")
    
    for member in members.members:
        print(f"  - {member.email} (ID: {member.member_id})")
    
    # Get member scopes
    if members.members:
        member_id = members.members[0].member_id
        print(f"\nGetting scopes for member: {member_id}")
        scopes = client.manage.v1.projects.members.scopes.list(
            project_id=project_id,
            member_id=member_id
        )
        print(f"Member scopes: {scopes.scope}")
        
        # Update member scopes
        print(f"\nUpdating member scopes...")
        updated = client.manage.v1.projects.members.scopes.update(
            project_id=project_id,
            member_id=member_id,
            scope="admin"
        )
        print(f"Updated scopes: {updated.scope}")
    
    # Remove a member (commented out for safety)
    # client.manage.v1.projects.members.delete(
    #     project_id=project_id,
    #     member_id=member_id
    # )
    
    # For async version:
    # from deepgram import AsyncDeepgramClient
    # client = AsyncDeepgramClient()
    # members = await client.manage.v1.projects.members.list(project_id=project_id)
    
except Exception as e:
    print(f"Error: {e}")

