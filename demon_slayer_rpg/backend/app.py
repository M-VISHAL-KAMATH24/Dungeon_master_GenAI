from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app) # Allows your React app to communicate with this backend

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    chat_history = data.get('history', [])
    
    if not chat_history:
        return jsonify({"error": "No history provided"}), 400

    try:
        chat_session = model.start_chat(history=chat_history)
        # We assume the last message is the new prompt
        prompt = chat_history[-1]['parts'][0] 
        response = chat_session.send_message(prompt)
        
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001) # Run on a different port than React
