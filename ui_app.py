# ui_app.py - Production-ready Streamlit AI Companion
# Copyright 2023-2025 Deepgram SDK contributors
# SPDX-License-Identifier: MIT

import streamlit as st
import os
import tempfile
import json
import time
import requests
import base64
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import av
import pyperclip
# Multi-language support using deep-translator
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ========== CONFIGURATION & CONSTANTS ==========
AVATAR_DEFAULTS = {
    "Girlfriend": {"image": "https://randomuser.me/api/portraits/women/44.jpg", "voices": ["aura-asteria-en", "aura-athena-en"], "desc": "A loving, caring, and supportive partner."},
    "Friend": {"image": "https://randomuser.me/api/portraits/men/32.jpg", "voices": ["aura-zeus-en", "aura-orion-en"], "desc": "A fun, supportive, and loyal friend."},
    "Therapist": {"image": "https://randomuser.me/api/portraits/women/65.jpg", "voices": ["aura-athena-en", "aura-orion-en"], "desc": "A wise, empathetic, and insightful therapist."},
    "Coach": {"image": "https://randomuser.me/api/portraits/men/45.jpg", "voices": ["aura-zeus-en", "aura-orion-en"], "desc": "A motivating, energetic, and positive coach."},
    "Comedian": {"image": "https://randomuser.me/api/portraits/men/33.jpg", "voices": ["aura-orion-en"], "desc": "A witty, funny, and lighthearted comedian."},
    "Storyteller": {"image": "https://randomuser.me/api/portraits/women/50.jpg", "voices": ["aura-asteria-en"], "desc": "A creative, imaginative, and engaging storyteller."},
    "Motivator": {"image": "https://randomuser.me/api/portraits/men/36.jpg", "voices": ["aura-zeus-en"], "desc": "An energetic, positive, and inspiring motivator."},
    "Teacher": {"image": "https://randomuser.me/api/portraits/women/60.jpg", "voices": ["aura-athena-en"], "desc": "A knowledgeable, patient, and helpful teacher."},
    "Parent": {"image": "https://randomuser.me/api/portraits/men/40.jpg", "voices": ["aura-orion-en"], "desc": "A caring, wise, and supportive parent."}
}
EMOTION_EMOJI = {"joy": "😄", "happy": "😄", "love": "😍", "anger": "😡", "sadness": "😢", "fear": "😱", "surprise": "😲", "neutral": "😐"}
THEME_CSS = {
    "Light": "body { background-color: #f8f9fa; color: #222; }",
    "Dark": "body { background-color: #222; color: #f8f9fa; }",
    "Playful": "body { background: linear-gradient(135deg, #f6d365 0%, #fda085 100%); color: #222; }",
    "Professional": "body { background-color: #e9ecef; color: #222; font-family: 'Segoe UI', sans-serif; }",
    "Retro": "body { background: repeating-linear-gradient(45deg, #f5e6ca, #f5e6ca 10px, #e0c097 10px, #e0c097 20px); color: #222; font-family: 'Courier New', monospace; }"
}
mood_gifs = {
    "joy": "https://media.giphy.com/media/1BcfiGlOGXzQk/giphy.gif",
    "happy": "https://media.giphy.com/media/1BcfiGlOGXzQk/giphy.gif",
    "love": "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
    "anger": "https://media.giphy.com/media/l3vR85PnGsBwu1PFK/giphy.gif",
    "sadness": "https://media.giphy.com/media/ROF8OQvDmxytW/giphy.gif",
    "fear": "https://media.giphy.com/media/3o6Zt6ML6BklcajjsA/giphy.gif",
    "surprise": "https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif",
    "neutral": "https://media.giphy.com/media/3o6Zt6ML6BklcajjsA/giphy.gif"
}

# ========== UTILITY FUNCTIONS ==========
def detect_emotion(text, hf_api_key=None):
    if not hf_api_key:
        return None, None
    headers = {"Authorization": f"Bearer {hf_api_key}"}
    api_url = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
    try:
        resp = requests.post(api_url, headers=headers, json={"inputs": text}, timeout=10)
        if resp.status_code == 200:
            result = resp.json()
            if isinstance(result, list) and result and 'label' in result[0]:
                return result[0]['label'], result[0]['score']
    except Exception:
        pass
    return None, None

def elevenlabs_tts(text, voice="Rachel", api_key=None):
    if not api_key:
        return None
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"
    headers = {"xi-api-key": api_key, "Content-Type": "application/json"}
    data = {"text": text, "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}}
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=15)
        if resp.status_code == 200:
            return resp.content
    except Exception:
        pass
    return None

def bot_typing_animation():
    with st.spinner("Bot is typing..."):
        time.sleep(1.5)

# Add markdown/LaTeX/emoji support in chat bubbles
def chat_bubble(role, text, avatar_img=None, emotion=None):
    emoji = EMOTION_EMOJI.get(emotion, "") if emotion else ""
    border = "3px solid #ffd700" if emotion == "joy" else ("3px solid #ffb3b3" if emotion == "sadness" else "3px solid #b3c6ff")
    if role == 'user':
        st.markdown(f"<div style='display:flex;align-items:center;'><img src='https://randomuser.me/api/portraits/men/1.jpg' width='40' style='border-radius:50%;margin-right:8px;'/><div style='background:#e6f7ff;padding:10px 16px;border-radius:16px 16px 16px 0;max-width:70%;'>" + st.markdown(text, unsafe_allow_html=True) + "</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='display:flex;align-items:center;'><img src='{avatar_img}' width='40' style='border-radius:50%;margin-right:8px;border:{border};'/><div style='background:#fffbe6;padding:10px 16px;border-radius:16px 16px 0 16px;max-width:70%;'>{emoji} " + st.markdown(text, unsafe_allow_html=True) + "</div></div>", unsafe_allow_html=True)

def animated_avatar_overlay(emotion):
    if emotion == "joy":
        st.markdown("<div style='position:relative;top:-40px;'><span style='font-size:48px;'>✨✨✨</span></div>", unsafe_allow_html=True)
    elif emotion == "sadness":
        st.markdown("<div style='position:relative;top:-40px;'><span style='font-size:48px;'>💧💧💧</span></div>", unsafe_allow_html=True)
    elif emotion == "anger":
        st.markdown("<div style='position:relative;top:-40px;'><span style='font-size:48px;'>🔥🔥🔥</span></div>", unsafe_allow_html=True)
    elif emotion == "surprise":
        st.markdown("<div style='position:relative;top:-40px;'><span style='font-size:48px;'>🎉🎉🎉</span></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='position:relative;top:-40px;'><span style='font-size:48px;'>⭐️⭐️⭐️</span></div>", unsafe_allow_html=True)

# ========== SIDEBAR: SETTINGS & INTEGRATIONS ==========
st.sidebar.title("👤 User Profile & Settings")
user_name = st.sidebar.text_input("Your Name", value="You")
selected_avatar = st.sidebar.selectbox("Choose Avatar Persona", list(AVATAR_DEFAULTS.keys()))
st.sidebar.image(AVATAR_DEFAULTS[selected_avatar]["image"], width=120, caption=selected_avatar)
st.sidebar.markdown(f"*{AVATAR_DEFAULTS[selected_avatar]['desc']}*")
persona_style = st.sidebar.selectbox("Choose your persona's style:", ["Caring & Supportive", "Playful & Flirty", "Serious & Thoughtful", "Funny & Lighthearted"])
voice_model = st.sidebar.selectbox("Choose Bot Voice", AVATAR_DEFAULTS[selected_avatar]["voices"])
speed = st.sidebar.slider("Voice Speed", 0.5, 2.0, 1.0, 0.05)
mood = st.sidebar.slider("Bot Mood (1=Calm, 10=Excited)", 1, 10, 5)
api_key = st.sidebar.text_input("Deepgram API Key", type="password", value=os.getenv("DEEPGRAM_API_KEY", ""))
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
hf_api_key = st.sidebar.text_input("HuggingFace API Key (for emotion detection)", type="password", value=os.getenv("HUGGINGFACE_API_KEY", ""))
el_api_key = st.sidebar.text_input("ElevenLabs API Key (optional)", type="password", value=os.getenv("ELEVENLABS_API_KEY", ""))
elevenlabs_voice = st.sidebar.selectbox("ElevenLabs Voice", ["Rachel", "Domi", "Bella", "Antoni", "Elli", "Josh", "Arnold", "Adam", "Sam"], index=0)
theme = st.sidebar.selectbox("Conversation Theme", list(THEME_CSS.keys()))
autoplay = st.sidebar.checkbox("Autoplay Voice Replies", value=True)

# DALL·E Avatar Generation (OpenAI v1 API)
st.sidebar.markdown("---")
st.sidebar.subheader("🎨 Generate Custom Avatar with DALL·E")
dalle_prompt = st.sidebar.text_input("Describe your avatar (e.g. 'robot cat in a suit')")
dalle_generate = st.sidebar.button("Generate Avatar with DALL·E")
dalle_avatar_url = None
# Fix DALL·E avatar generation to use supported sizes
if dalle_generate and openai_api_key and dalle_prompt:
    openai.api_key = openai_api_key
    try:
        dalle_response = openai.images.generate(
            model="dall-e-3",
            prompt=dalle_prompt,
            n=1,
            size="1024x1024"  # Use supported size
        )
        dalle_avatar_url = dalle_response.data[0].url
        st.sidebar.image(dalle_avatar_url, width=120, caption="DALL·E Avatar")
        custom_avatar_url = dalle_avatar_url
    except Exception as e:
        st.sidebar.error(f"DALL·E error: {e}")

# Use DALL·E avatar if generated
avatar_img_url = dalle_avatar_url if dalle_avatar_url else AVATAR_DEFAULTS[selected_avatar]["image"]

# Conversation Themes
st.markdown(f"<style>{THEME_CSS[theme]}</style>", unsafe_allow_html=True)

# Session Save/Load
st.sidebar.markdown("---")
if st.sidebar.button("💾 Save Session"):
    session_json = json.dumps(st.session_state.get('history', []))
    st.sidebar.download_button("Download Chat JSON", session_json, file_name="chat_history.json")
load_file = st.sidebar.file_uploader("Load Chat JSON", type=["json"])
if load_file:
    try:
        loaded_history = json.load(load_file)
        st.session_state['history'] = loaded_history
        st.sidebar.success("Session loaded!")
    except Exception as e:
        st.sidebar.error(f"Failed to load: {e}")

# Clear Conversation
if st.sidebar.button("🧹 Clear Conversation"):
    st.session_state['history'] = []

# Randomize Everything button
import random
if st.sidebar.button("🎲 Randomize Everything!"):
    st.session_state['surprise_avatar'] = random.choice(list(AVATAR_DEFAULTS.keys()))
    persona_style = random.choice(["Caring & Supportive", "Playful & Flirty", "Serious & Thoughtful", "Funny & Lighthearted"])
    mood = random.randint(1, 10)
    st.rerun()
if 'surprise_avatar' in st.session_state:
    selected_avatar = st.session_state['surprise_avatar']

# ========== MORE LANGUAGES ==========
# Add more languages and auto-detect option
supported_languages = [
    ("en", "English"), ("es", "Spanish"), ("fr", "French"), ("de", "German"), ("zh-cn", "Chinese"), ("hi", "Hindi"), ("ar", "Arabic"), ("ru", "Russian"), ("ja", "Japanese"), ("ko", "Korean"),
    ("it", "Italian"), ("pt", "Portuguese"), ("tr", "Turkish"), ("nl", "Dutch"), ("sv", "Swedish"), ("pl", "Polish"), ("uk", "Ukrainian"), ("fa", "Persian"), ("id", "Indonesian"), ("th", "Thai"), ("vi", "Vietnamese"), ("auto", "Auto-Detect")
]
language = st.sidebar.selectbox("Chat Language", [l[0] for l in supported_languages], format_func=lambda x: dict(supported_languages)[x])
language_names = dict(supported_languages)

# ========== ADVANCED PERSONA CONTROLS ==========
def get_custom_persona():
    if 'custom_personas' not in st.session_state:
        st.session_state['custom_personas'] = {}
    st.sidebar.markdown('---')
    st.sidebar.subheader('🧑‍🎤 Create Custom Persona')
    persona_name = st.sidebar.text_input('Persona Name', key='persona_name')
    persona_desc = st.sidebar.text_area('Persona Description', key='persona_desc')
    persona_style = st.sidebar.text_input('Persona Style', key='persona_style')
    persona_voice = st.sidebar.text_input('Persona Voice', key='persona_voice')
    persona_avatar = st.sidebar.text_input('Persona Avatar URL', key='persona_avatar')
    if st.sidebar.button('Save Persona'):
        st.session_state['custom_personas'][persona_name] = {
            'desc': persona_desc,
            'style': persona_style,
            'voice': persona_voice,
            'avatar': persona_avatar
        }
        st.sidebar.success(f'Persona "{persona_name}" saved!')
    if st.session_state['custom_personas']:
        st.sidebar.markdown('**Your Personas:**')
        for name, data in st.session_state['custom_personas'].items():
            st.sidebar.markdown(f"- **{name}**: {data['desc']}")
get_custom_persona()

# --- Remove Sage Advisor and ensure Girlfriend persona is always available and default ---
if 'Sage Advisor' in ADVANCED_AGENTS:
    del ADVANCED_AGENTS['Sage Advisor']
if 'Girlfriend' not in ADVANCED_AGENTS:
    ADVANCED_AGENTS['Girlfriend'] = {
        "name": "Girlfriend",
        "desc": "A loving, caring, and supportive partner.",
        "style": "Caring & Supportive",
        "voice": "aura-asteria-en",
        "avatar": "https://randomuser.me/api/portraits/women/44.jpg"
    }
# Always default to Girlfriend persona if nothing else is selected
if 'selected_avatar' not in st.session_state or not st.session_state['selected_avatar']:
    selected_avatar = 'Girlfriend'
    persona_style = ADVANCED_AGENTS['Girlfriend']['style']
    voice_model = ADVANCED_AGENTS['Girlfriend']['voice']
    avatar_img_url = ADVANCED_AGENTS['Girlfriend']['avatar']
    st.session_state['selected_avatar'] = selected_avatar

# --- Persona management: allow user to add/modify personas in sidebar ---
def manage_personas():
    st.sidebar.markdown('---')
    st.sidebar.subheader('🛠️ Manage Personas')
    new_name = st.sidebar.text_input('New Persona Name', key='new_persona_name')
    new_desc = st.sidebar.text_area('Description', key='new_persona_desc')
    new_style = st.sidebar.text_input('Style', key='new_persona_style')
    new_voice = st.sidebar.text_input('Voice', key='new_persona_voice')
    new_avatar = st.sidebar.text_input('Avatar URL', key='new_persona_avatar')
    if st.sidebar.button('Add/Update Persona') and new_name:
        ADVANCED_AGENTS[new_name] = {
            "name": new_name,
            "desc": new_desc or "A unique AI persona.",
            "style": new_style or "Caring & Supportive",
            "voice": new_voice or "aura-asteria-en",
            "avatar": new_avatar or "https://randomuser.me/api/portraits/women/44.jpg"
        }
        st.sidebar.success(f'Persona "{new_name}" added/updated!')
manage_personas()

# ========== CHAT MEMORY & CONTEXT WINDOW ==========
if 'chat_memory' not in st.session_state:
    st.session_state['chat_memory'] = []
def save_chat_memory():
    st.session_state['chat_memory'] = st.session_state.get('history', [])
def load_chat_memory():
    if st.session_state['chat_memory']:
        st.session_state['history'] = st.session_state['chat_memory']
# Add buttons to main UI
col_mem1, col_mem2 = st.columns(2)
if col_mem1.button('💾 Save Chat Memory'):
    save_chat_memory()
    st.success('Chat memory saved!')
if col_mem2.button('📂 Load Chat Memory'):
    load_chat_memory()
    st.success('Chat memory loaded!')

# ========== SUPER AGENTS & GLOWS AI AGENTS ==========
SUPER_AGENTS = {
    "n12": {
        "name": "N12 Super Agent",
        "desc": "An ultra-advanced, multi-modal AI agent with deep reasoning, web search, and creative skills.",
        "style": "Analytical & Creative",
        "voice": "aura-athena-en",
        "avatar": "https://randomuser.me/api/portraits/men/99.jpg"
    },
    "glow": {
        "name": "Glow AI Agent",
        "desc": "A glowing, empathetic, and emotionally intelligent AI for support and coaching.",
        "style": "Empathetic & Supportive",
        "voice": "aura-asteria-en",
        "avatar": "https://randomuser.me/api/portraits/women/99.jpg"
    }
}

def get_super_agent():
    st.sidebar.markdown('---')
    st.sidebar.subheader('🤖 Super Agents')
    agent_key = st.sidebar.selectbox('Choose a Super Agent', list(SUPER_AGENTS.keys()) + ["None"], format_func=lambda x: SUPER_AGENTS[x]["name"] if x in SUPER_AGENTS else "None")
    if agent_key in SUPER_AGENTS:
        agent = SUPER_AGENTS[agent_key]
        st.sidebar.image(agent["avatar"], width=120, caption=agent["name"])
        st.sidebar.markdown(f"*{agent['desc']}*")
        return agent
    return None

super_agent = get_super_agent()
if super_agent:
    selected_avatar = super_agent["name"]
    persona_style = super_agent["style"]
    voice_model = super_agent["voice"]
    avatar_img_url = super_agent["avatar"]

# ========== MORE ADVANCED AGENTS ==========
ADVANCED_AGENTS = {
    "sage": {
        "name": "Sage Advisor",
        "desc": "A wise, strategic advisor for business and life decisions.",
        "style": "Strategic & Insightful",
        "voice": "aura-zeus-en",
        "avatar": "https://randomuser.me/api/portraits/men/88.jpg"
    },
    "spark": {
        "name": "Spark Creative",
        "desc": "A creative AI for brainstorming, art, and innovation.",
        "style": "Creative & Playful",
        "voice": "aura-asteria-en",
        "avatar": "https://randomuser.me/api/portraits/women/88.jpg"
    },
    "guardian": {
        "name": "Guardian AI",
        "desc": "A protective, security-focused agent for privacy and safety advice.",
        "style": "Protective & Cautious",
        "voice": "aura-orion-en",
        "avatar": "https://randomuser.me/api/portraits/men/77.jpg"
    }
}

# --- Remove Sage Advisor and ensure Girlfriend persona is always available and default ---
if 'Sage Advisor' in ADVANCED_AGENTS:
    del ADVANCED_AGENTS['Sage Advisor']
if 'Girlfriend' not in ADVANCED_AGENTS:
    ADVANCED_AGENTS['Girlfriend'] = {
        "name": "Girlfriend",
        "desc": "A loving, caring, and supportive partner.",
        "style": "Caring & Supportive",
        "voice": "aura-asteria-en",
        "avatar": "https://randomuser.me/api/portraits/women/44.jpg"
    }
# Always default to Girlfriend persona if nothing else is selected
if 'selected_avatar' not in st.session_state or not st.session_state['selected_avatar']:
    selected_avatar = 'Girlfriend'
    persona_style = ADVANCED_AGENTS['Girlfriend']['style']
    voice_model = ADVANCED_AGENTS['Girlfriend']['voice']
    avatar_img_url = ADVANCED_AGENTS['Girlfriend']['avatar']
    st.session_state['selected_avatar'] = selected_avatar

def get_advanced_agent():
    st.sidebar.markdown('---')
    st.sidebar.subheader('🦾 Advanced Agents')
    agent_key = st.sidebar.selectbox('Choose an Advanced Agent', list(ADVANCED_AGENTS.keys()) + ["None"], format_func=lambda x: ADVANCED_AGENTS[x]["name"] if x in ADVANCED_AGENTS else "None")
    if agent_key in ADVANCED_AGENTS:
        agent = ADVANCED_AGENTS[agent_key]
        st.sidebar.image(agent["avatar"], width=120, caption=agent["name"])
        st.sidebar.markdown(f"*{agent['desc']}*")
        return agent
    return None

advanced_agent = get_advanced_agent()
if advanced_agent:
    selected_avatar = advanced_agent["name"]
    persona_style = advanced_agent["style"]
    voice_model = advanced_agent["voice"]
    avatar_img_url = advanced_agent["avatar"]

# ========== ADVANCED ROUTES (EXAMPLES) ==========
# Example: Route to different AI logic based on agent
if selected_avatar == "Guardian AI":
    st.info("Guardian AI is active: All responses will be privacy/security focused.")
    # You could add custom logic here for security/privacy Q&A
elif selected_avatar == "Spark Creative":
    st.info("Spark Creative is active: All responses will be creative and playful.")
    # Add creative prompt engineering or image generation
elif selected_avatar == "Sage Advisor":
    st.info("Sage Advisor is active: All responses will be strategic and insightful.")
    # Add business/strategy prompt engineering

# ========== ROBUST ERROR HANDLING DECORATOR ==========
def robust(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"[Robust Error] {func.__name__}: {e}")
            return None
    return wrapper
# Example usage: decorate all API calls and risky logic with @robust

# ========== UI POLISH & MODERN UX ==========
# Add a floating action button for quick help and feedback
st.markdown('''
<style>
.fab {
  position: fixed;
  bottom: 32px;
  right: 32px;
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #6e8efb 0%, #a777e3 100%);
  border-radius: 50%;
  box-shadow: 0 4px 16px rgba(0,0,0,0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  cursor: pointer;
}
.fab-icon {
  color: white;
  font-size: 32px;
}
</style>
<div class="fab" onclick="window.open('https://github.com/deepgram-devs/deepgram-python-sdk/issues', '_blank')">
  <span class="fab-icon">💡</span>
</div>
''', unsafe_allow_html=True)

# Add a theme toggle button
def theme_toggle():
    if 'theme_mode' not in st.session_state:
        st.session_state['theme_mode'] = 'Light'
    if st.button('🌗 Toggle Theme'):
        st.session_state['theme_mode'] = 'Dark' if st.session_state['theme_mode'] == 'Light' else 'Light'
    st.markdown(f"<style>{THEME_CSS[st.session_state['theme_mode']]}</style>", unsafe_allow_html=True)
theme_toggle()

# --- Ensure get_persona_defaults is defined before use ---
def get_persona_defaults(selected_avatar, persona_style):
    if selected_avatar in AVATAR_DEFAULTS:
        desc = AVATAR_DEFAULTS[selected_avatar]["desc"]
        style = persona_style
    elif selected_avatar in SUPER_AGENTS:
        desc = SUPER_AGENTS[selected_avatar]["desc"]
        style = SUPER_AGENTS[selected_avatar]["style"]
    elif selected_avatar in ADVANCED_AGENTS:
        desc = ADVANCED_AGENTS[selected_avatar]["desc"]
        style = ADVANCED_AGENTS[selected_avatar]["style"]
    else:
        desc = "A unique AI persona."
        style = persona_style
    return desc, style

# --- Ensure user_feelings and user_problem are always defined at the top ---
if 'user_feelings' not in st.session_state:
    st.session_state['user_feelings'] = ''
if 'user_problem' not in st.session_state:
    st.session_state['user_problem'] = ''
user_feelings = st.session_state['user_feelings']
user_problem = st.session_state['user_problem']

# --- Ensure openai is always imported ---
import openai

# --- Ensure get_persona_prompt_safe is defined before use ---
def get_persona_prompt_safe(selected_avatar, persona_style, mood_prompt):
    persona_desc = persona_prompts.get(selected_avatar, "A unique AI persona.")
    style_desc = style_prompts.get(persona_style, f"Respond in the style: {persona_style}.")
    return f"{persona_desc} {style_desc} {mood_prompt}"

# --- Ensure track_emotion is defined before use ---
def track_emotion(emotion, score):
    if 'emotion_trajectory' not in st.session_state:
        st.session_state['emotion_trajectory'] = []
    st.session_state['emotion_trajectory'].append({'emotion': emotion, 'score': score, 'timestamp': time.time()})

# ========== MAIN UI ==========
st.title("🌟 World-Class AI Voice Companion")
col1, col2 = st.columns([1, 6])
with col1:
    st.markdown(f"<div style='border: 4px solid #b3c6ff; border-radius: 50%; width: 88px; height: 88px; display: flex; align-items: center; justify-content: center;'><img src='{avatar_img_url}' width='80' style='border-radius:50%;'/></div>", unsafe_allow_html=True)
with col2:
    # Use correct avatar description for all agent types (robust for all cases)
    avatar_desc = None
    if selected_avatar in AVATAR_DEFAULTS:
        avatar_desc = AVATAR_DEFAULTS[selected_avatar]["desc"]
    elif 'super_agent' in locals() and super_agent and 'desc' in super_agent:
        avatar_desc = super_agent["desc"]
    elif 'advanced_agent' in locals() and advanced_agent and 'desc' in advanced_agent:
        avatar_desc = advanced_agent["desc"]
    else:
        avatar_desc = "A unique AI persona."

    st.markdown(f"**{selected_avatar}**: {avatar_desc}")

st.markdown("""
**How to use:**
- Record, upload, or type your message.
- The bot responds in your chosen avatar's style and voice.
- Download audio or conversation history.
""")

# Tabs for Live Conversation and Chat (always show both)
tab_live, tab_chat, tab_web = st.tabs(["📞 Live Conversation", "💬 Chat", "🌐 Ask UI Chat (Web)"])

with tab_chat:
    st.header("💬 Chat with AI Companion")
    # Microphone recording using streamlit-webrtc
    class AudioProcessor(AudioProcessorBase):
        def __init__(self):
            self.audio_frames = []
        def recv_queued(self, frames):
            self.audio_frames.extend(frames)
            return frames[-1] if frames else None
        def recv(self, frame: av.AudioFrame):
            # For backward compatibility, but recommend using recv_queued
            self.audio_frames.append(frame)
            return frame

    audio_processor = AudioProcessor()
    webrtc_ctx = webrtc_streamer(
        key="send-audio",
        audio_receiver_size=1024,
        audio_processor_factory=lambda: audio_processor,
    )

    audio_file = st.file_uploader("Upload an audio file (wav/mp3/m4a/flac)", type=["wav", "mp3", "m4a", "flac"])
    text_input = st.text_input("Or type your message:")

    # Quick Prompts
    st.markdown("---")
    st.subheader("Quick Prompts")
    prompts = ["How are you today?", "Tell me something interesting!", "Give me advice for my day.", "What's a fun fact?", "Cheer me up!"]
    quick = st.columns(len(prompts))
    for i, prompt in enumerate(prompts):
        if quick[i].button(prompt):
            # Directly trigger chat logic with this prompt
            text_input = prompt
            st.session_state['trigger_quick_prompt'] = True

    # ========== CHAT LOGIC ==========
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if st.button("Send Message!") or st.session_state.get('trigger_quick_prompt', False):
        st.session_state['trigger_quick_prompt'] = False
        if not api_key:
            st.error("Please enter your Deepgram API Key.")
        elif not (audio_file or (webrtc_ctx and webrtc_ctx.state.playing and audio_processor.audio_frames) or text_input):
            st.error("Please upload, record, or type a message.")
        else:
            from deepgram import DeepgramClient
            dg_client = DeepgramClient(api_key)
            transcript = None
            # Use recorded audio if available
            if webrtc_ctx and webrtc_ctx.state.playing and audio_processor.audio_frames:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_audio:
                    for frame in audio_processor.audio_frames:
                        tmp_audio.write(frame.to_ndarray().tobytes())
                    tmp_audio_path = tmp_audio.name
                with open(tmp_audio_path, 'rb') as f:
                    audio_bytes = f.read()
                mimetype = 'audio/wav'
                with st.spinner("Transcribing your message..."):
                    try:
                        response = dg_client.listen.rest.v('1').transcribe({'buffer': audio_bytes, 'mimetype': mimetype})
                        transcript = response['results']['channels'][0]['alternatives'][0]['transcript']
                    except Exception as e:
                        st.error(f"Transcription error: {e}")
            elif audio_file:
                audio_bytes = audio_file.read()
                mimetype = audio_file.type
                with st.spinner("Transcribing your message..."):
                    try:
                        response = dg_client.listen.rest.v('1').transcribe({'buffer': audio_bytes, 'mimetype': mimetype})
                        transcript = response['results']['channels'][0]['alternatives'][0]['transcript']
                    except Exception as e:
                        st.error(f"Transcription error: {e}")
            elif text_input:
                transcript = text_input
            if transcript:
                bot_typing_animation()
                # Add timeout and error handling for emotion detection
                try:
                    detected_emotion, emotion_score = detect_emotion(transcript, hf_api_key)
                except Exception as e:
                    st.warning(f"Emotion detection error: {e}")
                    detected_emotion, emotion_score = None, None
                persona_prompts = {
                    "Girlfriend": "You are a loving, caring girlfriend.",
                    "Friend": "You are a supportive, fun friend.",
                    "Therapist": "You are a wise, empathetic therapist.",
                    "Coach": "You are a motivating, energetic coach.",
                    "Comedian": "You are a witty, funny, and lighthearted comedian.",
                    "Storyteller": "You are a creative, imaginative, and engaging storyteller.",
                    "Motivator": "You are an energetic, positive, and inspiring motivator.",
                    "Teacher": "You are a knowledgeable, patient, and helpful teacher.",
                    "Parent": "You are a caring, wise, and supportive parent."
                }
                style_prompts = {
                    "Caring & Supportive": "Respond supportively and affectionately.",
                    "Playful & Flirty": "Respond with fun and charm.",
                    "Serious & Thoughtful": "Respond with deep care and insight.",
                    "Funny & Lighthearted": "Respond with humor and warmth."
                }
                mood_prompt = f"Your mood is at {mood}/10."
                prompt = get_persona_prompt_safe(selected_avatar, persona_style, mood_prompt)
                response_text = None
                if openai_api_key:
                    openai.api_key = openai_api_key
                    client = openai.OpenAI(api_key=openai_api_key)
                    messages = st.session_state['history'] + [
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": transcript}
                    ]
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        timeout=30
                    )
                    response_text = response.choices[0].message.content
                else:
                    response_text = f"[{selected_avatar} - {persona_style}] {transcript} ❤️"
                st.session_state['history'].append({"role": "user", "content": transcript})
                st.session_state['history'].append({"role": "assistant", "content": response_text})
                # --- TTS ---
                with st.spinner("Synthesizing voice reply..."):
                    try:
                        tts_response = None
                        if el_api_key:
                            tts_response = elevenlabs_tts(response_text, voice=elevenlabs_voice, api_key=el_api_key)
                        if not tts_response:
                            from deepgram import DeepgramClient
                            dg_client = DeepgramClient(api_key)
                            tts_result = dg_client.speak.v('1').stream_memory(
                                {"text": response_text},
                                options={"model": voice_model, "encoding": "linear16", "sample_rate": 24000, "speed": speed}
                            )
                            tts_response = tts_result.stream_memory.getvalue()
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_audio:
                            tmp_audio.write(tts_response)
                            tmp_audio_path = tmp_audio.name
                        if autoplay:
                            st.audio(tmp_audio_path, format='audio/wav', start_time=0)
                        else:
                            st.audio(tmp_audio_path, format='audio/wav')
                        with open(tmp_audio_path, 'rb') as f:
                            st.download_button('Download reply audio', f, file_name='bot_reply.wav')
                    except Exception as e:
                        st.error(f"TTS error: {e}")
                # Translate back to user language if needed
                if language != "en" and response_text:
                    try:
                        response_text = GoogleTranslator(source="en", target=language).translate(response_text)
                    except Exception:
                        pass
                # Show mood board GIF if emotion detected
                if detected_emotion and detected_emotion in mood_gifs:
                    st.image(mood_gifs[detected_emotion], width=200, caption=f"Mood: {detected_emotion}")
                # --- Track emotion trajectory ---
                if detected_emotion:
                    track_emotion(detected_emotion, emotion_score)

with tab_live:
    st.header("📞 Live Voice Conversation (Push-to-Talk)")
    st.write("Hold the button, speak, and the bot will talk back in real time!")
    class LiveAudioProcessor(AudioProcessorBase):
        def __init__(self):
            self.audio_frames = []
        def recv_queued(self, frames):
            self.audio_frames.extend(frames)
            return frames[-1] if frames else None
        def recv(self, frame: av.AudioFrame):
            self.audio_frames.append(frame)
            return frame
    live_audio_processor = LiveAudioProcessor()
    live_ctx = webrtc_streamer(
        key="live-audio",
        audio_receiver_size=1024,
        audio_processor_factory=lambda: live_audio_processor,
        media_stream_constraints={"audio": True, "video": False},
        sendback_audio=False,  # Prevent echo
    )
    if st.button("Push to Talk (record and process)"):
        if live_ctx and live_ctx.state.playing and live_audio_processor.audio_frames:
            st.info(f"Captured {len(live_audio_processor.audio_frames)} audio frames.")
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_audio:
                for frame in live_audio_processor.audio_frames:
                    tmp_audio.write(frame.to_ndarray().tobytes())
                tmp_audio_path = tmp_audio.name
            st.info(f"Audio saved to {tmp_audio_path}")
            with open(tmp_audio_path, 'rb') as f:
                audio_bytes = f.read()
            mimetype = 'audio/wav'
            # Transcribe
            if api_key:
                from deepgram import DeepgramClient
                dg_client = DeepgramClient(api_key)
                with st.spinner("Transcribing..."):
                    try:
                        response = dg_client.listen.rest.v('1').transcribe({'buffer': audio_bytes, 'mimetype': mimetype})
                        st.info(f"Transcription API response: {response}")
                        transcript = response['results']['channels'][0]['alternatives'][0]['transcript']
                        st.success(f"You said: {transcript}")
                        # Generate bot response
                        if openai_api_key:
                            client = openai.OpenAI(api_key=openai_api_key)
                            st.info("Calling OpenAI for response...")
                            # Make persona style explicit in system prompt
                            persona_prompt = f"You are acting as a {selected_avatar}. Persona style: {persona_style}. Description: {AVATAR_DEFAULTS[selected_avatar]['desc']}"
                            completion = client.chat.completions.create(
                                model="gpt-3.5-turbo",
                                messages=[
                                    {"role": "system", "content": persona_prompt},
                                    {"role": "user", "content": transcript}
                                ]
                            )
                            st.info(f"OpenAI API response: {completion}")
                            response_text = completion.choices[0].message.content if completion.choices and completion.choices[0].message.content else None
                            if not response_text:
                                st.warning("Bot did not respond. Showing transcript as fallback.")
                                response_text = f"[Raw transcript] {transcript}"
                        else:
                            response_text = f"You said: {transcript}"
                        st.markdown(f"**Bot:** {response_text}")
                        # TTS
                        with st.spinner("Bot is speaking..."):
                            tts_response = None
                            if el_api_key:
                                tts_response = elevenlabs_tts(response_text, voice=elevenlabs_voice, api_key=el_api_key)
                            if not tts_response:
                                st.info("Calling Deepgram TTS...")
                                tts_result = dg_client.speak.v('1').stream_memory(
                                    {"text": response_text},
                                    options={"model": voice_model, "encoding": "linear16", "sample_rate": 24000, "speed": speed}
                                )
                                tts_response = tts_result.stream_memory.getvalue()
                            st.info(f"TTS audio bytes: {len(tts_response) if tts_response else 0}")
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_audio:
                                tmp_audio.write(tts_response)
                                tmp_audio_path = tmp_audio.name
                            st.audio(tmp_audio_path, format='audio/wav', start_time=0)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.error("Please enter your Deepgram API Key in the sidebar.")
        else:
            st.warning("Press 'Start' and speak before pushing the button.")

with tab_web:
    st.header("🌐 Ask UI Chat (Web)")
    st.write("A focused web chat interface. Type your message and chat with the AI companion.")
    if 'web_history' not in st.session_state:
        st.session_state['web_history'] = []
    web_text_input = st.text_input("Type your message (Web Chat):", key="web_text_input")
    if st.button("Send (Web Chat)", key="web_send_btn"):
        if not api_key:
            st.error("Please enter your Deepgram API Key.")
        elif not web_text_input:
            st.error("Please type a message.")
        else:
            transcript = web_text_input
            bot_typing_animation()
            try:
                detected_emotion, emotion_score = detect_emotion(transcript, hf_api_key)
            except Exception as e:
                st.warning(f"Emotion detection error: {e}")
                detected_emotion, emotion_score = None, None
            persona_prompts = {
                "Girlfriend": "You are a loving, caring girlfriend.",
                "Friend": "You are a supportive, fun friend.",
                "Therapist": "You are a wise, empathetic therapist.",
                "Coach": "You are a motivating, energetic coach.",
                "Comedian": "You are a witty, funny, and lighthearted comedian.",
                "Storyteller": "You are a creative, imaginative, and engaging storyteller.",
                "Motivator": "You are an energetic, positive, and inspiring motivator.",
                "Teacher": "You are a knowledgeable, patient, and helpful teacher.",
                "Parent": "You are a caring, wise, and supportive parent."
            }
            style_prompts = {
                "Caring & Supportive": "Respond supportively and affectionately.",
                "Playful & Flirty": "Respond with fun and charm.",
                "Serious & Thoughtful": "Respond with deep care and insight.",
                "Funny & Lighthearted": "Respond with humor and warmth."
            }
            mood_prompt = f"Your mood is at {mood}/10."
            prompt = get_persona_prompt_safe(selected_avatar, persona_style, mood_prompt)
            response_text = None
            if openai_api_key:
                client = openai.OpenAI(api_key=openai_api_key)
                messages = st.session_state['web_history'] + [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": transcript}
                ]
                with st.spinner("Bot is thinking..."):
                    try:
                        completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, timeout=30)
                        response_text = completion.choices[0].message.content
                    except Exception as e:
                        st.error(f"OpenAI error: {e}")
                        response_text = f"[{selected_avatar} - {persona_style}] {transcript} ❤️"
            else:
                response_text = f"[{selected_avatar} - {persona_style}] {transcript} ❤️"
            st.session_state['web_history'].append({"role": "user", "content": transcript})
            st.session_state['web_history'].append({"role": "assistant", "content": response_text})
            # --- TTS ---
            with st.spinner("Synthesizing voice reply..."):
                try:
                    tts_response = None
                    if el_api_key:
                        tts_response = elevenlabs_tts(response_text, voice=elevenlabs_voice, api_key=el_api_key)
                    if not tts_response:
                        from deepgram import DeepgramClient
                        dg_client = DeepgramClient(api_key)
                        tts_result = dg_client.speak.v('1').stream_memory(
                            {"text": response_text},
                            options={"model": voice_model, "encoding": "linear16", "sample_rate": 24000, "speed": speed}
                        )
                        tts_response = tts_result.stream_memory.getvalue()
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_audio:
                        tmp_audio.write(tts_response)
                        tmp_audio_path = tmp_audio.name
                    if autoplay:
                        st.audio(tmp_audio_path, format='audio/wav', start_time=0)
                    else:
                        st.audio(tmp_audio_path, format='audio/wav')
                    with open(tmp_audio_path, 'rb') as f:
                        st.download_button('Download reply audio', f, file_name='bot_reply.wav')
                except Exception as e:
                    st.error(f"TTS error: {e}")
            # Translate back to user language if needed
            if language != "en" and response_text:
                try:
                    response_text = GoogleTranslator(source="en", target=language).translate(response_text)
                except Exception:
                    pass
            # Show mood board GIF if emotion detected
            if detected_emotion and detected_emotion in mood_gifs:
                st.image(mood_gifs[detected_emotion], width=200, caption=f"Mood: {detected_emotion}")
            # --- Track emotion trajectory ---
            if detected_emotion:
                track_emotion(detected_emotion, emotion_score)

# ========== RESEARCH-INSPIRED ADVANCED PERSONALIZATION (2025) ==========
# 1. Dynamic relationship graph: track user-agent relationships and adapt support
if 'relationship_graph' not in st.session_state:
    st.session_state['relationship_graph'] = {}
def update_relationship_graph(persona, emotion, score):
    g = st.session_state['relationship_graph']
    if persona not in g:
        g[persona] = {'interactions': 0, 'emotion_sum': 0, 'last_emotion': None}
    g[persona]['interactions'] += 1
    g[persona]['emotion_sum'] += score if score else 0
    g[persona]['last_emotion'] = emotion
    st.session_state['relationship_graph'] = g

# 2. Personalized agent adaptation: agent adapts based on relationship graph

def get_personalized_agent(persona):
    g = st.session_state['relationship_graph']
    if persona in g and g[persona]['interactions'] > 5:
        avg_emotion = g[persona]['emotion_sum'] / g[persona]['interactions']
        if avg_emotion < 0.3:
            return f"{persona} is extra supportive and checks in on you more often."
        elif avg_emotion > 0.7:
            return f"{persona} is playful and encourages you to try new things!"
    return f"{persona} is here for you as always."

# 3. Research-inspired: Theory of Mind (ToM) simulation
# The agent tries to infer your beliefs, desires, and intentions from your chat history

def infer_user_state():
    # Use multi-turn memory and emotion trajectory
    memory = st.session_state.get('multi_turn_memory', [])
    emotions = st.session_state.get('emotion_trajectory', [])
    if not memory or not emotions:
        return "I'm still getting to know you!"
    last_user = memory[-1]['user'] if memory else ''
    last_emotion = emotions[-1]['emotion'] if emotions else ''
    # Simple ToM: if user is often sad and asks for advice, infer need for support
    if last_emotion == 'sadness' and 'help' in last_user.lower():
        return "You may be feeling down and looking for encouragement."
    if last_emotion == 'joy' and 'share' in last_user.lower():
        return "You want to celebrate good news!"
    return "I'm learning your needs and will adapt to support you."

# 4. Personalized daily check-in (inspired by digital mental health research)
import datetime
last_checkin = st.session_state.get('last_checkin', None)
today = datetime.date.today().isoformat()
if last_checkin != today:
    st.sidebar.info("👋 Daily check-in: How are you feeling today?")
    st.session_state['last_checkin'] = today

# 5. Show relationship graph and ToM inference in sidebar for transparency
st.sidebar.markdown('---')
st.sidebar.subheader('🤝 Relationship Insights')
for persona, data in st.session_state['relationship_graph'].items():
    st.sidebar.markdown(f"**{persona}**: {data['interactions']} chats, last emotion: {data['last_emotion']}")
st.sidebar.markdown(f"**AI Inference:** {infer_user_state()}")
