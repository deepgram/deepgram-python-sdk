"""
Example: Self-Hosted API - Distribution Credentials

This example shows how to manage distribution credentials for on-premises deployments.
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
    
    # List all distribution credentials
    print("\nListing distribution credentials...")
    credentials = client.self_hosted.v1.distribution_credentials.list(project_id=project_id)
    print(f"Found {len(credentials.distribution_credentials) if credentials.distribution_credentials else 0} credentials")
    
    for cred in credentials.distribution_credentials or []:
        print(f"  - ID: {cred.distribution_credentials_id}, Provider: {cred.provider}")
        if hasattr(cred, 'comment') and cred.comment:
            print(f"    Comment: {cred.comment}")
    
    # Create new distribution credentials
    print("\nCreating new distribution credentials...")
    # Note: Adjust scopes and provider as needed
    # new_cred = client.self_hosted.v1.distribution_credentials.create(
    #     project_id=project_id,
    #     scopes=["read", "write"],
    #     provider="quay",
    #     comment="Example credentials"
    # )
    # print(f"Created credentials ID: {new_cred.distribution_credentials_id}")
    
    # Get a specific credential
    if credentials.distribution_credentials:
        cred_id = credentials.distribution_credentials[0].distribution_credentials_id
        print(f"\nGetting credential details: {cred_id}")
        cred = client.self_hosted.v1.distribution_credentials.get(
            project_id=project_id,
            distribution_credentials_id=cred_id
        )
        print(f"Provider: {cred.provider}")
        print(f"Scopes: {cred.scopes}")
    
    # Delete credentials (commented out for safety)
    # client.self_hosted.v1.distribution_credentials.delete(
    #     project_id=project_id,
    #     distribution_credentials_id=cred_id
    # )
    
    # For async version:
    # from deepgram import AsyncDeepgramClient
    # client = AsyncDeepgramClient()
    # credentials = await client.self_hosted.v1.distribution_credentials.list(project_id=project_id)
    
except Exception as e:
    print(f"Error: {e}")

