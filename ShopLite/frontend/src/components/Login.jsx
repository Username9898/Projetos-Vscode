import React, { useState } from 'react';
import api from '../api';

function Login() {
  const [isRegister, setIsRegister] = useState(false);
  const [formData, setFormData] = useState({ name: '', email: '', password: '' });
  const [message, setMessage] = useState({ type: '', text: '' });

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage({ type: '', text: '' });
    try {
      const endpoint = isRegister ? '/api/auth/register' : '/api/auth/login';
      const response = await api.post(endpoint, formData);
      localStorage.setItem('token', response.data.token);
      setMessage({ type: 'success', text: response.data.message });
    } catch (error) {
      setMessage({ type: 'error', text: error.response?.data?.message || 'Erro ao processar requisição.' });
    }
  };

  return (
    <div className="card" style={{ maxWidth: '500px', margin: '0 auto' }}>
      <h2>{isRegister ? '📝 Criar Conta' : '🔑 Login'}</h2>
      {message.text && <div className={`${message.type}-message`}>{message.text}</div>}
      <form onSubmit={handleSubmit}>
        {isRegister && (
          <div className="form-group">
            <label>Nome</label>
            <input type="text" name="name" value={formData.name} onChange={handleChange} placeholder="Seu nome" required={isRegister} />
          </div>
        )}
        <div className="form-group">
          <label>Email</label>
          <input type="email" name="email" value={formData.email} onChange={handleChange} placeholder="seu@email.com" required />
        </div>
        <div className="form-group">
          <label>Senha</label>
          <input type="password" name="password" value={formData.password} onChange={handleChange} placeholder="Sua senha" required />
        </div>
        <button type="submit" className="btn" style={{ width: '100%' }}>{isRegister ? 'Criar Conta' : 'Entrar'}</button>
      </form>
      <p style={{ textAlign: 'center', marginTop: '1rem', color: '#888' }}>
        {isRegister ? 'Já tem conta?' : 'Não tem conta?'}{' '}
        <button onClick={() => setIsRegister(!isRegister)} style={{ background: 'none', border: 'none', color: '#f5576c', cursor: 'pointer', fontWeight: '600' }}>
          {isRegister ? 'Fazer Login' : 'Registrar-se'}
        </button>
      </p>
    </div>
  );
}

export default Login;