/**
 * 🔄 GITHUB AUTO-SYNC RR98
 * Roberto Ribeiro - CPF: 108.840.969-55
 * 
 * Sincroniza automaticamente todos os projetos com o GitHub
 * Mantém backup e versionamento de tudo
 */

import { execSync } from 'child_process';
import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';
import chalk from 'chalk';
import { RR98 } from '../branding/config.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

class GitHubSync {
  constructor() {
    this.repoUrl = RR98.github.repository;
    this.branch = RR98.github.branch;
    this.owner = RR98.owner;
    this.projectsRoot = path.join(__dirname, '..', '..');
    this.syncHistory = [];
  }

  /**
   * Sincroniza todos os projetos com o GitHub
   */
  async syncAll() {
    console.log(chalk.cyan('\n🔄 Sincronizando com GitHub...\n'));

    try {
      // Verificar se git está disponível
      execSync('git --version', { stdio: 'pipe' });
    } catch {
      console.log(chalk.yellow('⚠️ Git não encontrado. Instale o Git para auto-sync.'));
      return { error: 'Git not found' };
    }

    const projects = [
      'Fincare', 'ShopLite', 'StockPro', 'JobsBoard', 'Kanbango',
      '100%Free/DevAgentHub', 'Criador de Páginas', 'RR98-Agent'
    ];

    const results = [];

    for (const project of projects) {
      const projectPath = path.join(this.projectsRoot, project);
      if (await fs.pathExists(projectPath)) {
        console.log(chalk.blue(`   📤 Sincronizando ${project}...`));
        try {
          const result = await this.syncProject(projectPath, project);
          results.push(result);
        } catch (error) {
          results.push({ project, status: 'error', error: error.message });
        }
      }
    }

    // Registrar sync
    this.syncHistory.push({
      timestamp: new Date().toISOString(),
      results
    });

    return {
      owner: this.owner.name,
      repository: this.repoUrl,
      branch: this.branch,
      results,
      total: results.length,
      success: results.filter(r => r.status === 'ok').length,
      errors: results.filter(r => r.status === 'error').length
    };
  }

  /**
   * Sincroniza um projeto específico
   */
  async syncProject(projectPath, projectName) {
    const gitPath = path.join(projectPath, '.git');
    
    // Se não tem git, inicializar
    if (!await fs.pathExists(gitPath)) {
      execSync('git init', { cwd: projectPath, stdio: 'pipe' });
      execSync(`git remote add origin ${this.repoUrl}`, { cwd: projectPath, stdio: 'pipe' });
    }

    // Configurar identidade
    execSync(`git config user.email "${this.owner.email}"`, { cwd: projectPath, stdio: 'pipe' });
    execSync(`git config user.name "${this.owner.name}"`, { cwd: projectPath, stdio: 'pipe' });

    // Adicionar arquivos
    execSync('git add -A', { cwd: projectPath, stdio: 'pipe' });

    // Commit
    try {
      execSync(`git commit -m "${RR98.github.commitMessage} - ${projectName}"`, {
        cwd: projectPath,
        stdio: 'pipe'
      });
    } catch {
      // Nada para commitar
    }

    // Push
    try {
      execSync(`git push -u origin ${this.branch}`, {
        cwd: projectPath,
        stdio: 'pipe'
      });
    } catch (error) {
      return { project: projectName, status: 'push_failed', error: error.message };
    }

    return {
      project: projectName,
      status: 'ok',
      syncedAt: new Date().toISOString(),
      owner: this.owner.name,
      email: this.owner.email
    };
  }

  /**
   * Cria LICENSE no repositório
   */
  async createLicense(projectPath) {
    const licenseContent = `LICENÇA EXCLUSIVA RR98 - Roberto Ribeiro

Titular: ${this.owner.name} (RR98)
CPF: ${this.owner.cpf}
Email: ${this.owner.email}
WhatsApp: ${this.owner.whatsapp}

Copyright © ${new Date().getFullYear()} ${this.owner.name} - RR98. Todos os direitos reservados.

Este software é propriedade exclusiva de ${this.owner.name} (RR98).
É protegido pelas leis brasileiras de direitos autorais (Lei 9.610/98)
e propriedade industrial (Lei 9.279/96).

USO NÃO AUTORIZADO:
- Pessoas físicas/jurídicas que utilizarem este software sem autorização
  devem pagar royalties de 5% sobre o lucro bruto obtido
- O pagamento deve ser feito via PIX para: ${this.owner.pix}
- Isento de impostos para o proprietário

PENALIDADES:
- Multa de 3x o valor dos royalties devidos
- Indenização por perdas e danos
- Responsabilização criminal (Arts. 184-186 do Código Penal)

Para uso autorizado, contate: ${this.owner.email} ou ${this.owner.whatsapp}

---
${this.owner.name} (RR98) - Tecnologia Inteligente para Resultados Reais
`;

    await fs.writeFile(path.join(projectPath, 'LICENSE'), licenseContent);
    return true;
  }

  /**
   * Cria .gitignore padrão
   */
  async createGitignore(projectPath) {
    const gitignore = `# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Database
*.sqlite
*.sqlite3

# Build
dist/
build/
.next/

# Runtime
.pnp
.pnp.js

# RR98 Protection
# © ${new Date().getFullYear()} ${this.owner.name} (RR98) - Todos os direitos reservados
`;

    await fs.writeFile(path.join(projectPath, '.gitignore'), gitignore);
  }

  /**
   * Agenda sync automático
   */
  startAutoSync(intervalHours = 6) {
    console.log(chalk.green(`🔄 Auto-sync GitHub a cada ${intervalHours}h`));
    
    setInterval(async () => {
      console.log(chalk.blue('\n🔄 Auto-sync GitHub iniciado...'));
      const result = await this.syncAll();
      console.log(chalk.green(`✅ Sync concluído: ${result.success}/${result.total} projetos\n`));
      
      // Notificar dono
      const { whatsApp } = await import('../whatsapp/index.js');
      await whatsApp.notifyOwner(
        `🔄 GitHub Auto-Sync\n\n` +
        `Projetos sincronizados: ${result.success}/${result.total}\n` +
        `Erros: ${result.errors}\n` +
        `Repositório: ${this.repoUrl}`
      );
    }, 1000 * 60 * 60 * intervalHours);
  }
}

export const gitHubSync = new GitHubSync();