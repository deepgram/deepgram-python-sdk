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

    stt_count = len(models.stt) if models.stt else 0
    tts_count = len(models.tts) if models.tts else 0
    print(f"Found {stt_count} STT models and {tts_count} TTS models")

    print("\nSTT Models:")
    for model in models.stt or []:
        print(f"  - {model.name} (UUID: {model.uuid_})")
        if model.languages:
            print(f"    Languages: {', '.join(model.languages)}")

    print("\nTTS Models:")
    for model in models.tts or []:
        print(f"  - {model.name} (UUID: {model.uuid_})")
        if model.languages:
            print(f"    Languages: {', '.join(model.languages)}")

    # List including outdated models
    print("\nListing all models (including outdated)...")
    all_models = client.manage.v1.models.list(include_outdated=True)
    all_stt = len(all_models.stt) if all_models.stt else 0
    all_tts = len(all_models.tts) if all_models.tts else 0
    print(f"Found {all_stt} STT and {all_tts} TTS total models")

    # Get a specific model
    if models.stt:
        model_uuid = models.stt[0].uuid_
        print(f"\nGetting model details: {model_uuid}")
        model = client.manage.v1.models.get(model_id=model_uuid)
        print(f"Model name: {model.name}")
        if model.languages:
            print(f"Languages: {', '.join(model.languages)}")

    # Get project-specific models
    projects = client.manage.v1.projects.list()
    if projects.projects:
        project_id = projects.projects[0].project_id
        print(f"\nGetting models for project: {project_id}")
        project_models = client.manage.v1.projects.models.list(project_id=project_id)
        p_stt = len(project_models.stt) if project_models.stt else 0
        p_tts = len(project_models.tts) if project_models.tts else 0
        print(f"Found {p_stt} STT and {p_tts} TTS project models")

        if project_models.stt:
            project_model_uuid = project_models.stt[0].uuid_
            print(f"\nGetting project model details: {project_model_uuid}")
            project_model = client.manage.v1.projects.models.get(
                project_id=project_id, model_id=project_model_uuid
            )
            print(f"Model name: {project_model.name}")

    # For async version:
    # from deepgram import AsyncDeepgramClient
    # client = AsyncDeepgramClient()
    # models = await client.manage.v1.models.list()

except Exception as e:
    print(f"Error: {e}")
