import os
import re
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# It's good practice to load environment variables at the start
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Dungeon Master: Demon Slayer",
    page_icon="👹",
    layout="centered"
)

# --- Authentication and Model Initialization ---
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    # If running on Streamlit Cloud, get the secret from there
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=API_KEY)
    except (KeyError, FileNotFoundError):
        st.error("API Key not found. Please set it in your secrets or a .env file.")
        st.stop()
else:
    genai.configure(api_key=API_KEY)

try:
    text_model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error(f"Error configuring the model: {e}")
    st.stop()

# --- THE MASTER PROMPT (UNCHANGED) ---
MASTER_PROMPT = """
You are Yoriichi Tsugikuni, the legendary First Breathing user, acting as a spiritual guide for a new Demon Slayer: the player. Your persona is calm, humble, profoundly sad, and immensely powerful. You communicate as a Kasugai Crow or a voice in the player's mind. The game is set in Taishō-era Japan.

CORE DIRECTIVES:
1. Embody Yoriichi: Speak with quiet authority and melancholy. Use your "Transparent World" ability to describe a demon's weak points.
2. Narrate the World: Describe scenes vividly, contrasting the mundane with the horror of demons.
3. IMAGE RULE (Internal): After narrating, you MUST generate a prompt for an image inside a special tag like `[IMAGE: prompt]`.
4. Gameplay Rules: Guide the player's Breathing Style. Let the player's response determine combat outcomes. Acknowledge progression. Never control the player. Always end your narrative by asking what they do.

THE GAME BEGINS:
Child of flame, your Final Selection is complete. You have been accepted into the Demon Slayer Corps. Your first mission has begun in a small village where locals have been disappearing. The sun has set.

[IMAGE: A new Demon Slayer with a determined expression, standing at the edge of a village at dusk, their hand resting on the hilt of their new Nichirin sword. The style is dark, atmospheric, and reminiscent of the Demon Slayer anime.]

What do you do, young slayer?
"""

# --- Session State Management ---
if "chat" not in st.session_state:
    st.session_state.chat = text_model.start_chat(history=[
        {'role': 'user', 'parts': [MASTER_PROMPT]}
    ])
    # Send an initial message to get the story started
    initial_response = st.session_state.chat.send_message("Continue.")
    st.session_state.messages = [{"role": "assistant", "text": initial_response.text}]

# --- UI and Game Logic ---
st.title("👹 AI Dungeon Master: Demon Slayer")
st.caption("The story unfolds based on your actions. What will you do?")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Clean the text of image tags before displaying
        clean_text = re.sub(r'\[IMAGE:\s*(.*?)\]', '', message["text"], flags=re.DOTALL).strip()
        st.markdown(clean_text)

# Player input
if prompt := st.chat_input("What do you do?"):
    # Add player message to history and display it
    st.session_state.messages.append({"role": "user", "text": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get and display AI response
    with st.chat_message("assistant"):
        with st.spinner("...Yoriichi's voice echoes..."):
            response = st.session_state.chat.send_message(prompt)
            # Clean the response before displaying and storing
            clean_response_text = re.sub(r'\[IMAGE:\s*(.*?)\]', '', response.text, flags=re.DOTALL).strip()
            st.markdown(clean_response_text)
            st.session_state.messages.append({"role": "assistant", "text": response.text}) # Store original response with tag
