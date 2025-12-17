"""
Example: Management API - Models

This example shows how to retrieve model information.
"""

from dotenv import load_dotenv

load_dotenv()

from deepgram import DeepgramClient

client = DeepgramClient()

try:
    # List all public models
    print("Listing all public models...")
    models = client.manage.v1.models.list()
    print(f"Found {len(models.models) if models.models else 0} models")

    for model in models.models or []:
        print(f"  - {model.name} (ID: {model.model_id})")
        if hasattr(model, "language") and model.language:
            print(f"    Language: {model.language}")

    # List including outdated models
    print("\nListing all models (including outdated)...")
    all_models = client.manage.v1.models.list(include_outdated=True)
    print(f"Found {len(all_models.models) if all_models.models else 0} total models")

    # Get a specific model
    if models.models:
        model_id = models.models[0].model_id
        print(f"\nGetting model details: {model_id}")
        model = client.manage.v1.models.get(model_id=model_id)
        print(f"Model name: {model.name}")
        if hasattr(model, "language") and model.language:
            print(f"Language: {model.language}")

    # Get project-specific models
    projects = client.manage.v1.projects.list()
    if projects.projects:
        project_id = projects.projects[0].project_id
        print(f"\nGetting models for project: {project_id}")
        project_models = client.manage.v1.projects.models.list(project_id=project_id)
        print(f"Found {len(project_models.models) if project_models.models else 0} project models")

        if project_models.models:
            project_model_id = project_models.models[0].model_id
            print(f"\nGetting project model details: {project_model_id}")
            project_model = client.manage.v1.projects.models.get(project_id=project_id, model_id=project_model_id)
            print(f"Model name: {project_model.name}")

    # For async version:
    # from deepgram import AsyncDeepgramClient
    # client = AsyncDeepgramClient()
    # models = await client.manage.v1.models.list()

except Exception as e:
    print(f"Error: {e}")
