"""
Example: Management API - Billing

This example shows how to retrieve billing and balance information.
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

    # List all balances
    print("\nListing billing balances...")
    balances = client.manage.v1.projects.billing.balances.list(project_id=project_id)
    print(f"Found {len(balances.balances) if balances.balances else 0} balances")

    for balance in balances.balances or []:
        print(f"  - Balance ID: {balance.balance_id}, Amount: {balance.amount}")

    # Get a specific balance
    if balances.balances:
        balance_id = balances.balances[0].balance_id
        print(f"\nGetting balance details: {balance_id}")
        balance = client.manage.v1.projects.billing.balances.get(project_id=project_id, balance_id=balance_id)
        print(f"Balance amount: {balance.amount}")

    # Get billing breakdown
    print("\nGetting billing breakdown...")
    breakdown = client.manage.v1.projects.billing.breakdown.get(project_id=project_id)
    print(f"Breakdown entries: {len(breakdown.entries) if breakdown.entries else 0}")

    # Get billing fields
    print("\nGetting billing fields...")
    fields = client.manage.v1.projects.billing.fields.list(project_id=project_id)
    print(f"Available fields: {len(fields.fields) if fields.fields else 0}")

    # List billing purchases
    print("\nListing billing purchases...")
    purchases = client.manage.v1.projects.billing.purchases.list(project_id=project_id)
    print(f"Found {len(purchases.purchases) if purchases.purchases else 0} purchases")

    # For async version:
    # from deepgram import AsyncDeepgramClient
    # client = AsyncDeepgramClient()
    # balances = await client.manage.v1.projects.billing.balances.list(project_id=project_id)

except Exception as e:
    print(f"Error: {e}")
