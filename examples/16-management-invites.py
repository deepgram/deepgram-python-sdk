"""
Example: Management API - Invitations

This example shows how to manage project invitations.
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
    
    # List all invitations
    print("\nListing project invitations...")
    invites = client.manage.v1.projects.members.invites.list(project_id=project_id)
    print(f"Found {len(invites.invites)} invitations")
    
    for invite in invites.invites:
        print(f"  - {invite.email} (scope: {invite.scope})")
    
    # Send an invitation
    print("\nSending invitation...")
    # Note: Replace with actual email address
    # new_invite = client.manage.v1.projects.members.invites.create(
    #     project_id=project_id,
    #     email="example@example.com",
    #     scope="member"
    # )
    # print(f"Invitation sent to: {new_invite.email}")
    
    # Delete an invitation (commented out for safety)
    # client.manage.v1.projects.members.invites.delete(
    #     project_id=project_id,
    #     email="example@example.com"
    # )
    
    # Leave a project
    # client.manage.v1.projects.leave(project_id=project_id)
    
    # For async version:
    # from deepgram import AsyncDeepgramClient
    # client = AsyncDeepgramClient()
    # invites = await client.manage.v1.projects.members.invites.list(project_id=project_id)
    
except Exception as e:
    print(f"Error: {e}")

