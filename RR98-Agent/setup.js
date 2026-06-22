/**
 * ⚙️ Script de Setup do Agente IA RR98
 * Configura e inicializa todo o ecossistema
 */

import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';
import chalk from 'chalk';
import readline from 'readline';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function ask(question) {
  return new Promise(resolve => rl.question(question, resolve));
}

async function setup() {
  console.log(chalk.cyan('\n╔══════════════════════════════════════════╗'));
  console.log(chalk.cyan('║   ⚙️  SETUP - AGENTE IA RR98             ║'));
  console.log(chalk.cyan('║   Configuração Inicial                   ║'));
  console.log(chalk.cyan('╚══════════════════════════════════════════╝\n'));

  // 1. Criar .env
  console.log(chalk.yellow('📝 Configurando variáveis de ambiente...\n'));
  
  if (!await fs.pathExists(path.join(__dirname, '.env'))) {
    const groqKey = await ask('🔑 Digite sua chave da API Groq (gsk_...): ');
    if (groqKey) {
      const envContent = `# 🤖 AGENTE IA RR98 - CONFIGURAÇÃO
GROQ_API_KEY=${groqKey}
PORT=3000
JWT_SECRET=rr98-agent-secret-key
OWNER_PHONE=046999732012
PIX_KEY=046999732012
AUTO_FIX_INTERVAL=30
AUTO_OPTIMIZE_INTERVAL=360
`;
      await fs.writeFile(path.join(__dirname, '.env'), envContent);
      console.log(chalk.green('   ✅ .env criado com sucesso!\n'));
    }
  } else {
    console.log(chalk.gray('   ⏭️  .env já existe, pulando...\n'));
  }

  // 2. Criar diretórios necessários
  console.log(chalk.yellow('📁 Criando diretórios do sistema...'));
  
  const dirs = [
    'logs', 'logs/stats', 'logs/reports', 'database', 'database/transactions',
    'database/expenses', 'backups', '.cache',
    'whatsapp/messages', 'whatsapp/templates', 'whatsapp/contacts',
    'whatsapp/log', 'whatsapp/webhook'
  ];
  
  for (const dir of dirs) {
    await fs.ensureDir(path.join(__dirname, dir));
  }
  console.log(chalk.green('   ✅ Diretórios criados!\n'));

  // 3. Instalar dependências
  console.log(chalk.yellow('📦 Instalando dependências do RR98 Agent...\n'));
  try {
    execSync('npm install', { cwd: __dirname, stdio: 'inherit' });
    console.log(chalk.green('\n   ✅ Dependências instaladas!\n'));
  } catch (error) {
    console.log(chalk.red(`   ❌ Erro ao instalar: ${error.message}\n`));
  }

  // 4. Verificar projetos existentes
  console.log(chalk.yellow('🔍 Verificando projetos do ecossistema...\n'));
  
  const projects = [
    'Fincare', 'ShopLite', 'StockPro', 'JobsBoard', 'Kanbango',
    '100%Free/DevAgentHub', 'Criador de Páginas'
  ];

  for (const project of projects) {
    const projectPath = path.join(__dirname, '..', project);
    if (await fs.pathExists(projectPath)) {
      console.log(chalk.green(`   ✅ ${project} - encontrado`));
      
      // Verificar se precisa instalar dependências
      const pkgPath = path.join(projectPath, 'package.json');
      if (await fs.pathExists(pkgPath)) {
        const nodeModules = path.join(projectPath, 'node_modules');
        if (!await fs.pathExists(nodeModules)) {
          const install = await ask(`   ❓ ${project} precisa de npm install? (s/N): `);
          if (install.toLowerCase() === 's') {
            console.log(chalk.yellow(`      📦 Instalando dependências de ${project}...`));
            try {
              execSync('npm install --loglevel=error', { cwd: projectPath, stdio: 'pipe' });
              console.log(chalk.green(`      ✅ Dependências de ${project} instaladas!`));
            } catch (error) {
              console.log(chalk.red(`      ❌ Erro: ${error.message}`));
            }
          }
        }
      }
    } else {
      console.log(chalk.yellow(`   ⚠️  ${project} - não encontrado (pode ser ignorado)`));
    }
  }

  // 5. Resumo final
  console.log(chalk.cyan('\n╔══════════════════════════════════════════╗'));
  console.log(chalk.cyan('║   ✅ SETUP CONCLUÍDO!                    ║'));
  console.log(chalk.cyan('╚══════════════════════════════════════════╝\n'));
  
  console.log(chalk.white('📋 Próximos passos:'));
  console.log(chalk.white('   1. Configure sua chave GROQ_API_KEY no .env'));
  console.log(chalk.white('   2. Execute: npm start'));
  console.log(chalk.white('   3. Acesse: http://localhost:3000'));
  console.log(chalk.white('   4. Login: admin / rr98@2026'));
  console.log(chalk.white(`\n💰 PIX: 046999732012`));
  console.log(chalk.white('📱 WhatsApp Virtual: Ativo'));
  console.log(chalk.white('🤖 Agente IA: Pronto para operar!\n'));

  rl.close();
}

setup().catch(console.error);