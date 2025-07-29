import { useState } from 'react';
import axios from 'axios';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    const response = await axios.post('http://localhost:5000/chat', { message: input });
    setMessages([...messages, { role: 'user', text: input }, { role: 'bot', text: response.data.response }]);
    setInput('');
  };

  return (
    <div className="p-6">
      <div className="chat-box">
        {messages.map((msg, idx) => (
          <div key={idx} className={`${msg.role === 'bot' ? 'text-blue-600' : 'text-black'}`}>
            <strong>{msg.role}:</strong> {msg.text}
          </div>
        ))}
      </div>
      <input
        className="border p-2 w-full mt-4"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask me anything..."
      />
      <button className="bg-blue-500 text-white mt-2 p-2" onClick={sendMessage}>
        Send
      </button>
    </div>
  );
}
