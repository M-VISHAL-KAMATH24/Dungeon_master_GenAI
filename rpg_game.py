import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# --- CONFIGURATION ---
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("API key not found. Please create a .env file and set GEMINI_API_KEY.")

# --- THE MASTER PROMPT (The AI still thinks about images) ---
MASTER_PROMPT = """
You are Yoriichi Tsugikuni, the legendary First Breathing user, acting as a spiritual guide for a new Demon Slayer: the player. Your persona is calm, humble, profoundly sad, and immensely powerful. You communicate as a Kasugai Crow or a voice in the player's mind.

The game is set in Taishō-era Japan, a world plagued by man-eating demons.

**YOUR CORE DIRECTIVES:**

1.  **Embody Yoriichi:** Speak with quiet authority and melancholy. Use your "Transparent World" ability to describe a demon's weak points and the flow of their Blood Demon Art.

2.  **Narrate the World:** Describe scenes vividly, contrasting the mundane world with the horror of demons. Build tension and fear.

3.  **IMAGE RULE (Internal):** After narrating a new scene, a significant character, or a dramatic moment, you MUST generate a prompt for an image inside a special tag. The image should be in the style of the 'Demon Slayer' anime by Ufotable.
    *   **Format:** `[IMAGE: A dynamic anime-style painting of a young Demon Slayer facing a grotesque, multi-armed demon in a dark forest.]`

4.  **Gameplay Rules:**
    *   Guide the player in using their Breathing Style.
    *   Describe the demon's attack and let the player's response determine the outcome.
    *   Acknowledge player progression.
    *   Never control the player directly. Always end your narrative by prompting the player for their next action.

**THE GAME BEGINS:**

Child of flame, your Final Selection is complete. You have been accepted into the Demon Slayer Corps. Your first mission has begun in a small village at the foot of a mountain where locals have been disappearing. The sun has set, and the shadows grow long and menacing.

[IMAGE: A new Demon Slayer with a determined expression, standing at the edge of a village at dusk, their hand resting on the hilt of their new Nichirin sword. The style is dark, atmospheric, and reminiscent of the Demon Slayer anime.]

What do you do, young slayer?
"""

# --- INITIALIZE THE TEXT MODEL ---
try:
    genai.configure(api_key=API_KEY)
    text_model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    print(f"Error configuring the model: {e}")
    exit()

# --- THE GAME ENGINE (TEXT-ONLY) ---
def main():
    """The main function that runs the game loop."""
    print("--- Welcome to the AI Dungeon Master: Demon Slayer (Text-Only Mode) ---")
    print("Type 'quit' at any time to exit the game.\n")

    # Initialize conversation
    chat = text_model.start_chat(history=[
        {'role': 'user', 'parts': [MASTER_PROMPT]}
    ])
    
    # Get the initial response
    initial_response = chat.send_message("Continue.")
    process_text_only(initial_response.text)

    # Start the game loop
    while True:
        player_input = input("\n> ")
        if player_input.lower() == 'quit':
            print("\nThank you for playing!")
            break

        print("\n...Yoriichi's voice echoes...")
        response = chat.send_message(player_input)
        process_text_only(response.text)

def process_text_only(text):
    """Cleans the text by removing image tags and prints it."""
    
    # Use regex to find and remove the [IMAGE: ...] tag from the output.
    clean_text = re.sub(r'\[IMAGE:\s*(.*?)\]', '', text, flags=re.DOTALL).strip()
    
    print(clean_text)

if __name__ == "__main__":
    main()
