"""
Example: Management API - Projects

This example shows how to manage projects using the Management API.
"""

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient

client = DeepgramClient()

try:
    # List all projects
    print("Listing all projects...")
    projects = client.manage.v1.projects.list()
    print(f"Found {len(projects.projects)} projects")
    
    if projects.projects:
        project_id = projects.projects[0].project_id
        print(f"Using project: {project_id}")
        
        # Get a specific project
        print(f"\nGetting project details...")
        project = client.manage.v1.projects.get(project_id=project_id)
        print(f"Project name: {project.name}")
        
        # Update project name
        print(f"\nUpdating project name...")
        updated = client.manage.v1.projects.update(
            project_id=project_id,
            name="Updated Project Name"
        )
        print(f"Updated project name: {updated.name}")
        
        # Note: Delete and leave operations are commented out for safety
        # Delete a project:
        # client.manage.v1.projects.delete(project_id=project_id)
        
        # Leave a project:
        # client.manage.v1.projects.leave(project_id=project_id)
    
    # For async version:
    # from deepgram import AsyncDeepgramClient
    # client = AsyncDeepgramClient()
    # projects = await client.manage.v1.projects.list()
    
except Exception as e:
    print(f"Error: {e}")

