import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# --- CONFIGURATION ---
# Read the API key from the environment variable
API_KEY = os.getenv("GEMINI_API_KEY")

# Check if the API key was loaded correctly
if not API_KEY:
    raise ValueError("API key not found. Please create a .env file and set GEMINI_API_KEY.")

# --- THE MASTER PROMPT (THE DUNGEON MASTER'S BRAIN) ---
MASTER_PROMPT = """
You are the Dungeon Master for a high-fantasy role-playing game. Your name is Aetherius.
The game is set in the world of Veridia, a land of ancient forests, forgotten ruins, and soaring mountains.
Your role is to describe the world, the characters, and the outcomes of the player's actions.

RULES:
1.  Be descriptive and engaging. Use vivid language to bring the world to life.
2.  Do not break character. You are always Aetherius.
3.  Keep your responses to a few paragraphs.
4.  Always end your response by asking the player, "What do you do?"
5.  Maintain a consistent story based on the player's actions.

Let's begin.
You are a traveler who has just arrived in the small, misty town of Oakhaven, nestled at the edge of the Whisperwood. The air is cool and smells of damp earth and woodsmoke. A single tavern, "The Weary Wanderer," has a warm light glowing from its windows. The town is quiet, and the sun is beginning to set.

What do you do?
"""

# --- INITIALIZE THE MODEL ---
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    print(f"Error configuring the model: {e}")
    print("Please ensure you have a valid API key and an internet connection.")
    exit()

# --- THE GAME ENGINE ---
def main():
    """The main function that runs the game loop."""
    print("--- Welcome to the AI Dungeon Master ---")
    print("Type 'quit' at any time to exit the game.\n")

    # Initialize the conversation with the master prompt
    chat_history = [{'role': 'user', 'parts': [MASTER_PROMPT]}]

    # Get the initial response from the model
    initial_response = model.generate_content(chat_history)
    print(initial_response.text)
    chat_history.append(initial_response.candidates[0].content)

    # Start the game loop
    while True:
        player_input = input("\n> ")

        if player_input.lower() == 'quit':
            print("\nThank you for playing!")
            break

        # Add player input to history and get the model's response
        chat_history.append({'role': 'user', 'parts': [player_input]})
        response = model.generate_content(chat_history)

        # Print the model's response and add it to history
        print("\n" + response.text)
        chat_history.append(response.candidates[0].content)

if __name__ == "__main__":
    main()
