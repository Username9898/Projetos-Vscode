import React from 'react';
function Dashboard() {
  const stats = { vagasAbertas: 45, candidatos: 230, contratacoes: 18, empresas: 32 };
  return (<div><div className="card"><h2>📊 Painel de Vagas</h2><p style={{color:'#888'}}>Bem-vindo ao JobsBoard - Plataforma inteligente de recrutamento</p></div><div className="dashboard-grid">
    <div className="stat-card"><h3>📋 Vagas Abertas</h3><div className="value">{stats.vagasAbertas}</div></div>
    <div className="stat-card"><h3>👤 Candidatos</h3><div className="value">{stats.candidatos}</div></div>
    <div className="stat-card"><h3>✅ Contratações</h3><div className="value" style={{color:'#27ae60'}}>{stats.contratacoes}</div></div>
    <div className="stat-card"><h3>🏢 Empresas</h3><div className="value">{stats.empresas}</div></div>
  </div>
  <div className="card" style={{marginTop:'2rem'}}><h3>🚀 Funcionalidades</h3><ul style={{lineHeight:'2',color:'#555'}}>
    <li>✅ Cadastro e busca de vagas</li><li>✅ Candidatura online</li>
    <li>✅ Match inteligente com IA Groq</li><li>✅ Notificações em tempo real</li>
    <li>✅ Painel administrativo para empresas</li></ul></div></div>);
}
export default Dashboard;