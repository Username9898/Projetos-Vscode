#!/usr/bin/env node

/**
 * Script para atualizar automaticamente a lista de projetos no portfolio
 * Busca repositórios do GitHub e atualiza o PROJECTS_DATA no index.html
 */

const fs = require('fs');
const path = require('path');

const GITHUB_USERNAME = 'Username9898';
const PORTFOLIO_PATH = path.join(__dirname, '..', 'index.html');

// Lista de projetos atualizada (adicione novos projetos aqui)
const PROJECTS_DATA = [
  {
    id: 'dentarium-ai-enterprise',
    name: 'Dentarium AI Enterprise',
    description: 'Plataforma SaaS empresarial com IA para automação de dashboards, processamento de documentos, OCR, CAD/CAM e analytics.',
    longDescription: 'Sistema completo de IA empresarial que automatiza processos operacionais em múltiplos setores (odontologia, engenharia, indústria, logística, financeiro, RH e saúde). Inclui OCR automático, geração de dashboards, processamento CAD/CAM, redução de desperdícios e monitoramento auto-curador.',
    tech: ['Python', 'FastAPI', 'Next.js', 'PostgreSQL', 'Docker', 'Kubernetes', 'Ollama', 'OpenCV', 'Open3D'],
    stars: 0,
    forks: 0,
    featured: true,
    setupSteps: [
      'Clone o repositório: git clone https://github.com/Username9898/dentarium-ai-enterprise.git',
      'Entre na pasta: cd dentarium-ai-enterprise',
      'Copie as variáveis de ambiente: cp backend/.env.example backend/.env',
      'Suba a stack: docker-compose up -d',
      'Acesse: http://localhost:3000 (frontend) e http://localhost:8000 (API)'
    ]
  },
  {
    id: 'studyforge-ai',
    name: 'StudyForge AI',
    description: 'Criador inteligente de conteúdo educativo que gera materiais de estudo completos e passo a passo usando IA gratuita.',
    longDescription: 'Plataforma que democratiza o acesso ao conhecimento. Usuários escolhem qualquer tema e a IA gera automaticamente conteúdo educativo completo, detalhado e estruturado passo a passo. Inclui upload/download de arquivos, exportação multi-formato e auto-atualização contínua.',
    tech: ['Python', 'FastAPI', 'Next.js', 'Ollama', 'LangChain', 'PostgreSQL', 'MinIO', 'Docker'],
    stars: 0,
    forks: 0,
    featured: true,
    setupSteps: [
      'Clone: git clone https://github.com/Username9898/studyforge-ai.git',
      'Entre: cd studyforge-ai',
      'Configure .env: cp backend/.env.example backend/.env',
      'Inicie: docker-compose up -d',
      'Acesse: http://localhost:3000'
    ]
  },
  {
    id: 'RR98-Agent',
    name: 'RR98-Agent',
    description: 'Agente de IA autônomo para automação de tarefas, integração com WhatsApp e monitoramento inteligente.',
    tech: ['JavaScript', 'Node.js', 'OpenAI', 'WhatsApp API', 'Docker'],
    stars: 0,
    forks: 0,
    featured: false,
    setupSteps: [
      'Clone: git clone https://github.com/Username9898/RR98-Agent.git',
      'Entre: cd RR98-Agent',
      'Instale: npm install',
      'Configure: cp .env.example .env',
      'Rode: npm start'
    ]
  },
  {
    id: 'LicitaMaster',
    name: 'LicitaMaster',
    description: 'Sistema de automação para licitações e pregões eletrônicos com IA para análise de editais.',
    tech: ['Python', 'Scrapy', 'Selenium', 'PostgreSQL', 'FastAPI'],
    stars: 0,
    forks: 0,
    featured: true,
    setupSteps: [
      'Clone: git clone https://github.com/Username9898/LicitaMaster.git',
      'Instale dependências: pip install -r requirements.txt',
      'Configure: cp .env.example .env',
      'Rode: python main.py'
    ]
  }
];

function generateProjectsJS() {
  const jsCode = `        // Configuração
        const GITHUB_USERNAME = '${GITHUB_USERNAME}';
        const PORTFOLIO_CONFIG = {
            autoUpdate: true,
            showStats: true,
            projectsPerPage: 12
        };

        // Lista de projetos com instruções de setup
        const PROJECTS_DATA = ${JSON.stringify(PROJECTS_DATA, null, 8)};

        // Função para buscar projetos do GitHub (futura implementação)
        async function fetchGitHubProjects() {
            // TODO: Implementar busca real na API do GitHub
            // const response = await fetch(\`https://api.github.com/users/\${GITHUB_USERNAME}/repos\`);
            // const repos = await response.json();
            // Processar e adicionar à lista PROJECTS_DATA
            
            // Por enquanto, retorna os projetos estáticos
            return PROJECTS_DATA;
        }
`;

  return jsCode;
}

function updatePortfolio() {
  console.log('🔄 Atualizando portfolio...');
  
  let html = fs.readFileSync(PORTFOLIO_PATH, 'utf8');
  
  // Encontrar e substituir a seção de configuração e PROJECTS_DATA
  const startMarker = '// Configuração';
  const endMarker = '        // Função para buscar projetos do GitHub';
  
  const startIndex = html.indexOf(startMarker);
  const endIndex = html.indexOf(endMarker);
  
  if (startIndex === -1 || endIndex === -1) {
    console.error('❌ Marcadores não encontrados no index.html');
    process.exit(1);
  }
  
  const newCode = generateProjectsJS();
  
  html = html.substring(0, startIndex) + newCode + html.substring(endIndex);
  
  fs.writeFileSync(PORTFOLIO_PATH, html, 'utf8');
  
  console.log('✅ Portfolio atualizado com sucesso!');
  console.log(`📊 ${PROJECTS_DATA.length} projetos encontrados`);
}

// Executar
try {
  updatePortfolio();
} catch (error) {
  console.error('❌ Erro:', error.message);
  process.exit(1);
}