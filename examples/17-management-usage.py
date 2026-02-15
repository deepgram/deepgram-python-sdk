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
    print(f"Start: {usage.start}")
    print(f"End: {usage.end}")
    if usage.resolution:
        print(f"Resolution: {usage.resolution.amount} {usage.resolution.units}")

    # Get usage breakdown
    print("\nGetting usage breakdown...")
    breakdown = client.manage.v1.projects.usage.breakdown.get(project_id=project_id)
    print(f"Breakdown results: {len(breakdown.results) if breakdown.results else 0}")
    if breakdown.results:
        for result in breakdown.results:
            print(f"  Requests: {result.requests}, Hours: {result.hours}")

    # Get usage fields
    print("\nGetting usage fields...")
    fields = client.manage.v1.projects.usage.fields.list(project_id=project_id)
    print(f"Available models: {len(fields.models) if fields.models else 0}")
    print(f"Available features: {len(fields.features) if fields.features else 0}")

    # List usage requests
    print("\nListing usage requests...")
    requests = client.manage.v1.projects.requests.list(project_id=project_id)
    print(f"Found {len(requests.requests) if requests.requests else 0} requests")

    # Get a specific request
    if requests.requests:
        request_id = requests.requests[0].request_id
        print(f"\nGetting request details: {request_id}")
        request = client.manage.v1.projects.requests.get(project_id=project_id, request_id=request_id)
        if request.request:
            print(f"Request path: {request.request.path}")
            print(f"Request code: {request.request.code}")

    # For async version:
    # from deepgram import AsyncDeepgramClient
    # client = AsyncDeepgramClient()
    # usage = await client.manage.v1.projects.usage.get(project_id=project_id)

except Exception as e:
    print(f"Error: {e}")
