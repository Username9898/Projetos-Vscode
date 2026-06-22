import React, { useState } from 'react';
import api from '../api';

function ChatAI() {
  const [prompt, setPrompt] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    const userMessage = { role: 'user', content: prompt };
    setMessages(prev => [...prev, userMessage]);
    setPrompt('');
    setLoading(true);

    try {
      const response = await api.post('/api/chat', { prompt });
      const aiMessage = { role: 'ai', content: response.data.reply };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      const errorMessage = { role: 'ai', content: 'Erro ao conectar com a IA. Verifique sua chave da API Groq.' };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>🤖 Assistente IA - Groq</h2>
      <p style={{ color: '#888', marginBottom: '1.5rem' }}>
        Converse com a inteligência artificial usando o modelo llama-3.3-70b-versatile
      </p>
      <div className="chat-box">
        {messages.length === 0 && (
          <p style={{ textAlign: 'center', color: '#aaa' }}>
            Faça uma pergunta para começar...
          </p>
        )}
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
        {loading && (
          <div className="message ai">
            <span>🤔 Pensando...</span>
          </div>
        )}
      </div>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Digite sua mensagem para a IA..."
            rows="3"
            disabled={loading}
          />
        </div>
        <button type="submit" className="btn" disabled={loading || !prompt.trim()}>
          {loading ? 'Enviando...' : 'Enviar'}
        </button>
      </form>
    </div>
  );
}

export default ChatAI;