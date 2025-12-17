"""
Example: Management API - API Keys

This example shows how to manage API keys for a project.
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
    
    # List all API keys for the project
    print("\nListing API keys...")
    keys = client.manage.v1.projects.keys.list(project_id=project_id)
    print(f"Found {len(keys.api_keys)} API keys")
    
    # List only active keys
    print("\nListing active API keys...")
    active_keys = client.manage.v1.projects.keys.list(
        project_id=project_id,
        status="active"
    )
    print(f"Found {len(active_keys.api_keys)} active keys")
    
    # Create a new API key
    print("\nCreating new API key...")
    new_key = client.manage.v1.projects.keys.create(
        project_id=project_id,
        request={
            "comment": "Example API key",
            "scopes": ["usage:read"],
        }
    )
    print(f"Created key ID: {new_key.key_id}")
    print(f"Key: {new_key.key}")
    print("⚠️  Save this key now - it won't be shown again!")
    
    # Get a specific key
    if keys.api_keys:
        key_id = keys.api_keys[0].key_id
        print(f"\nGetting key details for: {key_id}")
        key = client.manage.v1.projects.keys.get(
            project_id=project_id,
            key_id=key_id
        )
        print(f"Key comment: {key.comment}")
        print(f"Key scopes: {key.scopes}")
    
    # Delete a key (commented out for safety)
    # client.manage.v1.projects.keys.delete(
    #     project_id=project_id,
    #     key_id=key_id
    # )
    
    # For async version:
    # from deepgram import AsyncDeepgramClient
    # client = AsyncDeepgramClient()
    # keys = await client.manage.v1.projects.keys.list(project_id=project_id)
    
except Exception as e:
    print(f"Error: {e}")

