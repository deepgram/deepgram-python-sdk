"""
Example: Management API - Usage

This example shows how to retrieve usage statistics and request information.
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
    
    # Get usage summary
    print("\nGetting usage summary...")
    usage = client.manage.v1.projects.usage.get(project_id=project_id)
    print(f"Total requests: {usage.total_requests}")
    print(f"Total hours: {usage.total_hours}")
    
    # Get usage breakdown
    print("\nGetting usage breakdown...")
    breakdown = client.manage.v1.projects.usage.breakdown.get(project_id=project_id)
    print(f"Breakdown entries: {len(breakdown.entries) if breakdown.entries else 0}")
    
    # Get usage fields
    print("\nGetting usage fields...")
    fields = client.manage.v1.projects.usage.fields.list(project_id=project_id)
    print(f"Available fields: {len(fields.fields) if fields.fields else 0}")
    
    # List usage requests
    print("\nListing usage requests...")
    requests = client.manage.v1.projects.requests.list(project_id=project_id)
    print(f"Found {len(requests.requests) if requests.requests else 0} requests")
    
    # Get a specific request
    if requests.requests:
        request_id = requests.requests[0].request_id
        print(f"\nGetting request details: {request_id}")
        request = client.manage.v1.projects.requests.get(
            project_id=project_id,
            request_id=request_id
        )
        print(f"Request method: {request.method}")
        print(f"Request endpoint: {request.endpoint}")
    
    # For async version:
    # from deepgram import AsyncDeepgramClient
    # client = AsyncDeepgramClient()
    # usage = await client.manage.v1.projects.usage.get(project_id=project_id)
    
except Exception as e:
    print(f"Error: {e}")

