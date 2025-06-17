import streamlit as st

def test_ui_app_runs():
    """Basic smoke test: can the Streamlit app run without crashing?"""
    try:
        import ui_app  # This will run the Streamlit script
    except Exception as e:
        assert False, f"App failed to run: {e}"

def test_persona_prompt():
    """Test persona prompt construction for OpenAI system message."""
    from ui_app import AVATAR_DEFAULTS
    persona = "Coach"
    persona_style = "Serious & Thoughtful"
    prompt = f"You are acting as a {persona}. Persona style: {persona_style}. Description: {AVATAR_DEFAULTS[persona]['desc']}"
    assert "Coach" in prompt and persona_style in prompt

def test_web_search_duckduckgo():
    from ui_app import web_search
    result = web_search("US president of USA")
    assert isinstance(result, str) and len(result) > 0
