import React from 'react';

function Dashboard() {
  const stats = { produtos: 156, pedidos: 42, vendas: 28750.00, clientes: 89 };

  return (
    <div>
      <div className="card">
        <h2>📊 Dashboard E-commerce</h2>
        <p style={{ color: '#888' }}>Bem-vindo ao ShopLite - Sua plataforma de e-commerce inteligente</p>
      </div>
      <div className="dashboard-grid">
        <div className="stat-card">
          <h3>📦 Produtos</h3>
          <div className="value">{stats.produtos}</div>
        </div>
        <div className="stat-card">
          <h3>📋 Pedidos</h3>
          <div className="value">{stats.pedidos}</div>
        </div>
        <div className="stat-card">
          <h3>💰 Vendas</h3>
          <div className="value">R$ {stats.vendas.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</div>
        </div>
        <div className="stat-card">
          <h3>👥 Clientes</h3>
          <div className="value">{stats.clientes}</div>
        </div>
      </div>
      <div className="card" style={{ marginTop: '2rem' }}>
        <h3>🚀 Funcionalidades</h3>
        <ul style={{ lineHeight: '2', color: '#555' }}>
          <li>✅ Catálogo de produtos com busca inteligente</li>
          <li>✅ Carrinho de compras e checkout</li>
          <li>✅ Assistente IA para recomendações</li>
          <li>✅ Painel administrativo completo</li>
          <li>✅ Integração com meios de pagamento</li>
        </ul>
      </div>
    </div>
  );
}

export default Dashboard;