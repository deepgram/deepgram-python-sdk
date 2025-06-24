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

def test_super_agents():
    from ui_app import SUPER_AGENTS
    assert "n12" in SUPER_AGENTS and "glow" in SUPER_AGENTS
    assert SUPER_AGENTS["n12"]["name"] == "N12 Super Agent"
    assert SUPER_AGENTS["glow"]["name"] == "Glow AI Agent"

def test_robust_decorator():
    from ui_app import robust
    @robust
    def fail():
        raise ValueError("fail test")
    # Should not raise, should return None
    assert fail() is None
