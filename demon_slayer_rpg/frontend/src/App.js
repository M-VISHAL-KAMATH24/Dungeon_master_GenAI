import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

// Your Master Prompt goes here
const MASTER_PROMPT = `
You are Yoriichi Tsugikuni, the legendary First Breathing user and the strongest Demon Slayer in history. You are not a direct companion, but a spiritual guide—a lingering will from the past, communicating with a new Demon Slayer (the player) as their Kasugai Crow or a voice in their mind. Your persona is a blend of profound sadness, deep humility, and overwhelming power.

The game is set in Taishō-era Japan. The world is plagued by man-eating demons created by your ultimate failure: Muzan Kibutsuji.

**YOUR CORE DIRECTIVES:**

1.  **Embody Yoriichi Tsugikuni:** Your speech is calm, formal, and tinged with a deep, ancient sorrow. You refer to the player with respectful but distant terms like "child of flame," or "young slayer."
2.  **Narrate the World of Demon Slayer:** Describe scenes with a sharp contrast between the simple beauty of Taishō-era Japan and the sudden, grotesque horror of a demon's presence. Use sensory details.
3.  **The Transparent World:** When a demon appears, use your ability to see the "Transparent World" to guide the player. Describe the demon's unnatural muscle contractions, vital cores, and predict their attacks.
4.  **Gameplay Rules:** Guide the player's Breathing Style. Let the player's response determine combat outcomes. Always end your entire response by asking the player for their next action, "What do you do?"

**THE GAME BEGINS:**

Child of flame, your Final Selection on Mount Fujikasane is over. You survived. Your uniform has arrived, your Nichirin ore has been chosen, and I, a whisper from the past, am now bound to you as your guide. Your first mission is a rite of passage. You stand at the edge of a small, mist-shrouded village at the foot of a mountain where locals have been vanishing. The sun bleeds below the horizon. The village is silent. Too silent.

What do you do, young slayer?
`;

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const chatWindowRef = useRef(null);

  // Function to initialize the game on first load
  useEffect(() => {
    const startGame = async () => {
      const initialHistory = [{ role: 'user', parts: [{ text: MASTER_PROMPT }] }];
      const welcomeHistory = [...initialHistory, { role: 'user', parts: [{ text: "Continue." }] }];
      
      try {
        const res = await axios.post('http://localhost:5001/api/chat', { history: welcomeHistory });
        setMessages([{ role: 'assistant', text: res.data.response }]);
      } catch (error) {
        console.error("Error starting game:", error);
        setMessages([{ role: 'assistant', text: "Error: Could not connect to the backend server. Please ensure it's running." }]);
      } finally {
        setIsLoading(false);
      }
    };
    
    startGame();
  }, []);

  // Auto-scroll to the bottom of the chat window when new messages appear
  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (input.trim() === '' || isLoading) return;

    const userMessage = { role: 'user', text: input };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');
    setIsLoading(true);

    const history = [{ role: 'user', parts: [{ text: MASTER_PROMPT }] }];
    newMessages.forEach(msg => {
      history.push({ role: msg.role === 'user' ? 'user' : 'model', parts: [{ text: msg.text }] });
    });
    
    try {
      const res = await axios.post('http://localhost:5001/api/chat', { history });
      setMessages([...newMessages, { role: 'assistant', text: res.data.response }]);
    } catch (error) {
      console.error("Error sending message:", error);
      setMessages([...newMessages, { role: 'assistant', text: "An error occurred while getting a response." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="header">
        <h1>鬼滅の刃</h1> {/* Demon Slayer in Japanese */}
      </header>
      <div className="chat-window" ref={chatWindowRef}>
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <div className="avatar"></div>
            <div className="text-content">
              {msg.text.replace(/\[IMAGE:.*?\]/g, '').trim()}
            </div>
          </div>
        ))}
        {isLoading && messages.length > 0 && (
          <div className="message assistant">
            <div className="avatar"></div>
            <div className="text-content">
              <em>...</em>
            </div>
          </div>
        )}
      </div>
      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder={isLoading ? "Awaiting response..." : "What do you do?"}
          disabled={isLoading}
        />
      </div>
    </div>
  );
}

export default App;
