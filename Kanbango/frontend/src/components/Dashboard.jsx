import React from 'react';
function Dashboard() {
  const stats = { tarefas: 48, emAndamento: 15, concluidas: 22, membros: 8 };
  return (<div><div className="card"><h2>📊 Quadro Kanban</h2><p style={{color:'#888'}}>Bem-vindo ao Kanbango - Gerencie seus projetos com o quadro Kanban inteligente</p></div><div className="dashboard-grid">
    <div className="stat-card"><h3>📌 A Fazer</h3><div className="value">{stats.tarefas}</div></div>
    <div className="stat-card"><h3>🔄 Em Andamento</h3><div className="value" style={{color:'#f39c12'}}>{stats.emAndamento}</div></div>
    <div className="stat-card"><h3>✅ Concluídas</h3><div className="value" style={{color:'#27ae60'}}>{stats.concluidas}</div></div>
    <div className="stat-card"><h3>👥 Membros</h3><div className="value">{stats.membros}</div></div>
  </div>
  <div className="card" style={{marginTop:'2rem'}}><h3>🚀 Funcionalidades</h3><ul style={{lineHeight:'2',color:'#555'}}>
    <li>✅ Quadro Kanban com drag & drop</li><li>✅ Gerenciamento de tarefas</li>
    <li>✅ Sugestões inteligentes com IA Groq</li><li>✅ Colaboração em tempo real</li>
    <li>✅ Relatórios de produtividade</li></ul></div></div>);
}
export default Dashboard;