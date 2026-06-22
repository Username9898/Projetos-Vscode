import React, { useState, useEffect } from 'react';
import api from '../api';

function Dashboard() {
  const [stats, setStats] = useState({ receitas: 0, despesas: 0, saldo: 0 });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get('/api/health');
        if (response.data.status === 'ok') {
          setStats({
            receitas: 45800.00,
            despesas: 32150.00,
            saldo: 13650.00
          });
        }
      } catch (error) {
        console.log('Backend não disponível, exibindo dados mockados');
        setStats({
          receitas: 45800.00,
          despesas: 32150.00,
          saldo: 13650.00
        });
      }
    };
    fetchData();
  }, []);

  return (
    <div>
      <div className="card">
        <h2>📊 Dashboard Financeiro</h2>
        <p style={{ color: '#888' }}>
          Bem-vindo ao Fincare - Seu sistema de gestão financeira inteligente
        </p>
      </div>

      <div className="dashboard-grid">
        <div className="stat-card">
          <h3>💰 Receitas</h3>
          <div className="value">R$ {stats.receitas.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</div>
        </div>
        <div className="stat-card">
          <h3>📉 Despesas</h3>
          <div className="value" style={{ color: '#e74c3c' }}>R$ {stats.despesas.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</div>
        </div>
        <div className="stat-card">
          <h3>✅ Saldo</h3>
          <div className="value" style={{ color: stats.saldo >= 0 ? '#27ae60' : '#e74c3c' }}>
            R$ {stats.saldo.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
          </div>
        </div>
      </div>

      <div className="card" style={{ marginTop: '2rem' }}>
        <h3>🚀 Funcionalidades</h3>
        <ul style={{ lineHeight: '2', color: '#555' }}>
          <li>✅ Controle de receitas e despesas</li>
          <li>✅ Relatórios financeiros detalhados</li>
          <li>✅ Assistente IA com Groq para análises</li>
          <li>✅ Autenticação segura com JWT</li>
          <li>✅ Integração com PostgreSQL</li>
        </ul>
      </div>
    </div>
  );
}

export default Dashboard;