import React from 'react';
function Dashboard() {
  const stats = { produtos: 2345, baixoEstoque: 23, valorTotal: 589000.00, movimentacoes: 156 };
  return (<div><div className="card"><h2>📊 Controle de Estoque</h2><p style={{color:'#888'}}>Bem-vindo ao StockPro - Sistema inteligente de gestão de estoque</p></div><div className="dashboard-grid">
    <div className="stat-card"><h3>📦 Produtos</h3><div className="value">{stats.produtos}</div></div>
    <div className="stat-card"><h3>⚠️ Baixo Estoque</h3><div className="value" style={{color:'#e74c3c'}}>{stats.baixoEstoque}</div></div>
    <div className="stat-card"><h3>💰 Valor Total</h3><div className="value">R$ {stats.valorTotal.toLocaleString('pt-BR',{minimumFractionDigits:2})}</div></div>
    <div className="stat-card"><h3>🔄 Movimentações</h3><div className="value">{stats.movimentacoes}</div></div>
  </div>
  <div className="card" style={{marginTop:'2rem'}}><h3>🚀 Funcionalidades</h3><ul style={{lineHeight:'2',color:'#555'}}>
    <li>✅ Controle de entrada e saída de produtos</li><li>✅ Alertas de estoque baixo</li>
    <li>✅ Relatórios com IA Groq</li><li>✅ Código de barras e QR Code</li>
    <li>✅ Múltiplos depósitos</li></ul></div></div>);
}
export default Dashboard;