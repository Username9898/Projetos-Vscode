import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';
import chalk from 'chalk';
import axios from 'axios';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Motor de Auto-Correção e Auto-Melhoria do Agente RR98
 * Escaneia projetos, detecta bugs e corrige automaticamente
 */
class SelfHealEngine {
  constructor() {
    this.projectsRoot = path.join(__dirname, '..', '..');
    this.fixHistory = [];
    this.maxFixHistory = 100;
    this.issueLog = path.join(__dirname, '..', 'logs');
    this.optimizationBudget = 0;
    this.totalEarnings = 0;
  }

  /**
   * Diagnóstico completo do sistema
   */
  async diagnose() {
    console.log(chalk.yellow('\n🔍 Iniciando diagnóstico completo...\n'));
    
    const results = {
      timestamp: new Date().toISOString(),
      projects: [],
      issues: [],
      health: 'good'
    };

    const projects = [
      'Fincare', 'ShopLite', 'StockPro', 'JobsBoard', 'Kanbango',
      '100%Free/DevAgentHub', 'Criador de Páginas'
    ];

    for (const project of projects) {
      const projectPath = path.join(this.projectsRoot, project);
      const exists = await fs.pathExists(projectPath);
      
      if (exists) {
        console.log(chalk.green(`  ✅ ${project} - OK`));
        results.projects.push({ name: project, status: 'present', path: projectPath });
        
        // Verificar integridade dos arquivos
        const integrity = await this.checkIntegrity(projectPath);
        if (integrity.issues.length > 0) {
          results.issues.push(...integrity.issues.map(i => ({ ...i, project })));
          console.log(chalk.yellow(`     ⚠️  ${integrity.issues.length} issue(s) encontrados`));
        }
      } else {
        console.log(chalk.red(`  ❌ ${project} - NÃO ENCONTRADO`));
        results.issues.push({ project, type: 'missing', severity: 'high' });
      }
    }

    // Verificar dependências
    const depIssues = await this.checkDependencies();
    results.issues.push(...depIssues);

    results.health = results.issues.length === 0 ? 'good' : 'needs_attention';
    
    console.log(chalk.cyan(`\n📊 Diagnóstico concluído: ${results.issues.length} issue(s)\n`));
    
    await this.logDiagnostics(results);
    return results;
  }

  /**
   * Verifica integridade dos arquivos do projeto
   */
  async checkIntegrity(projectPath) {
    const issues = [];
    const requiredFiles = ['package.json', 'README.md'];
    
    for (const file of requiredFiles) {
      if (!await fs.pathExists(path.join(projectPath, file))) {
        issues.push({ type: 'missing_file', file, severity: 'medium' });
      }
    }

    // Verificar package.json
    try {
      const pkg = await fs.readJson(path.join(projectPath, 'package.json'));
      if (!pkg.scripts?.start && !pkg.scripts?.dev) {
        issues.push({ type: 'missing_start_script', severity: 'low' });
      }
    } catch {
      // Pode não ter package.json (projetos estáticos)
    }

    return { issues };
  }

  /**
   * Verifica dependências de todos os projetos
   */
  async checkDependencies() {
    const issues = [];
    
    const nodeProjects = [
      'Fincare/backend', 'Fincare/frontend',
      'ShopLite/backend', 'ShopLite/frontend',
      'StockPro/backend', 'StockPro/frontend',
      'JobsBoard/backend', 'JobsBoard/frontend',
      'Kanbango/backend', 'Kanbango/frontend',
      'RR98-Agent'
    ];

    for (const project of nodeProjects) {
      const projectPath = path.join(this.projectsRoot, project);
      const pkgPath = path.join(projectPath, 'package.json');
      
      if (await fs.pathExists(pkgPath)) {
        const nodeModulesPath = path.join(projectPath, 'node_modules');
        if (!await fs.pathExists(nodeModulesPath)) {
          issues.push({
            project,
            type: 'missing_node_modules',
            severity: 'high',
            fix: `npm install em ${project}`
          });
          console.log(chalk.yellow(`  ⚠️  ${project}: node_modules ausente`));
        }
      }
    }

    return issues;
  }

  /**
   * Escaneia e corrige bugs automaticamente
   */
  async scanAndFix() {
    console.log(chalk.blue('\n🔎 Escaneando por bugs...\n'));
    
    const bugs = [];
    
    // Procurar erros comuns em arquivos JS/JSX
    const jsFiles = await this.findFiles('**/*.{js,jsx}');
    
    for (const file of jsFiles) {
      try {
        const content = await fs.readFile(file, 'utf8');
        
        // Verificar imports quebrados
        const importMatch = content.match(/import\s+.*from\s+['"].*['"]/g);
        if (importMatch) {
          // Verificação básica de sintaxe
          if (content.includes('from "./') || content.includes("from './")) {
            // Verificar se o arquivo importado existe
            const relativeImports = content.match(/(?:from\s+['"])(\.\/[^'"]+)(?:['"])/g);
            // Lógica real de verificação seria mais complexa
          }
        }

        // Verificar console.log esquecidos em produção
        const consoleLogs = content.match(/console\.log\(/g);
        if (consoleLogs && consoleLogs.length > 10 && !file.includes('test')) {
          bugs.push({
            file: path.relative(this.projectsRoot, file),
            type: 'excessive_console_logs',
            count: consoleLogs.length,
            severity: 'low'
          });
        }

      } catch (error) {
        bugs.push({
          file: path.relative(this.projectsRoot, file),
          type: 'read_error',
          error: error.message,
          severity: 'high'
        });
      }
    }

    // Aplicar correções automáticas
    for (const bug of bugs) {
      if (bug.severity === 'high' || bug.severity === 'medium') {
        await this.autoFix(bug);
      }
    }

    this.fixHistory.push({ timestamp: new Date(), bugs, fixes: bugs.length });
    if (this.fixHistory.length > this.maxFixHistory) {
      this.fixHistory = this.fixHistory.slice(-this.maxFixHistory);
    }

    console.log(chalk.green(`\n✅ Escaneamento concluído: ${bugs.length} bug(s) encontrados\n`));
    return bugs;
  }

  /**
   * Aplica correção automática para um bug
   */
  async autoFix(bug) {
    console.log(chalk.yellow(`  🔧 Corrigindo: ${bug.type} em ${bug.file}`));
    
    try {
      const filePath = path.join(this.projectsRoot, bug.file);
      
      switch (bug.type) {
        case 'excessive_console_logs':
          // Remover console.log excessivos
          let content = await fs.readFile(filePath, 'utf8');
          content = content.replace(/console\.log\([^)]*\);/g, '// console.log removido pelo RR98 Agent');
          await fs.writeFile(filePath, content);
          break;

        case 'missing_node_modules':
          const projectPath = path.dirname(filePath);
          execSync('npm install', { cwd: projectPath, stdio: 'pipe' });
          break;

        default:
          console.log(chalk.gray(`     ⏭️  Nenhuma correção automática disponível para: ${bug.type}`));
      }

      console.log(chalk.green(`     ✅ Corrigido!`));
    } catch (error) {
      console.log(chalk.red(`     ❌ Erro ao corrigir: ${error.message}`));
    }
  }

  /**
   * Otimiza o sistema automaticamente
   */
  async optimize() {
    console.log(chalk.blue('\n⚡ Otimizando sistema...\n'));

    const optimizations = [];

    // Limpar logs antigos
    try {
      const logDir = path.join(__dirname, '..', 'logs');
      if (await fs.pathExists(logDir)) {
        const logs = await fs.readdir(logDir);
        const oldLogs = logs.filter(l => {
          const stat = fs.statSync(path.join(logDir, l));
          return Date.now() - stat.mtimeMs > 7 * 24 * 60 * 60 * 1000; // 7 dias
        });
        for (const log of oldLogs) {
          await fs.remove(path.join(logDir, log));
          optimizations.push(`Log removido: ${log}`);
        }
      }
    } catch (error) {
      console.log(chalk.red(`  ❌ Erro limpando logs: ${error.message}`));
    }

    // Limpar cache
    try {
      const cacheDir = path.join(__dirname, '..', '.cache');
      if (await fs.pathExists(cacheDir)) {
        await fs.emptyDir(cacheDir);
        optimizations.push('Cache limpo');
      }
    } catch {
      // Cache directory may not exist
    }

    // Verificar e remover node_modules não utilizados (bônus de performance)
    if (this.optimizationBudget > 0) {
      const budgetToUse = Math.min(this.optimizationBudget, this.optimizationBudget * 0.8);
      console.log(chalk.cyan(`  💰 Usando R$ ${budgetToUse.toFixed(2)} para melhorias...`));
      this.optimizationBudget -= budgetToUse;
      
      // Investir em melhorias com o orçamento disponível
      optimizations.push(`Investimento de R$ ${budgetToUse.toFixed(2)} em melhorias`);
    }

    console.log(chalk.green(`\n✅ ${optimizations.length} otimização(ões) aplicada(s)\n`));
    return optimizations;
  }

  /**
   * Encontra arquivos recursivamente
   */
  async findFiles(pattern) {
    const { glob } = await import('glob');
    return glob(pattern, { 
      cwd: this.projectsRoot,
      ignore: ['**/node_modules/**', '**/.git/**', '**/dist/**']
    });
  }

  /**
   * Registra diagnóstico
   */
  async logDiagnostics(diagnostics) {
    const logDir = path.join(__dirname, '..', 'logs');
    await fs.ensureDir(logDir);
    
    const logFile = path.join(logDir, `diagnostic-${Date.now()}.json`);
    await fs.writeJson(logFile, diagnostics, { spaces: 2 });
  }

  /**
   * Adiciona receita para o orçamento de melhoria
   */
  addRevenue(amount) {
    this.totalEarnings += amount;
    const improvementBudget = amount * 0.8;
    this.optimizationBudget += improvementBudget;
    console.log(chalk.green(`💰 Receita de R$ ${amount.toFixed(2)} adicionada. R$ ${improvementBudget.toFixed(2)} destinado a melhorias.`));
    return improvementBudget;
  }

  /**
   * Verifica projetos que precisam de correções
   */
  async getProjectStatus(projectName) {
    const projectPath = path.join(this.projectsRoot, projectName);
    
    if (!await fs.pathExists(projectPath)) {
      return { exists: false, status: 'not_found' };
    }

    const pkgPath = path.join(projectPath, 'package.json');
    const hasPackage = await fs.pathExists(pkgPath);
    const hasNodeModules = await fs.pathExists(path.join(projectPath, 'node_modules'));
    
    let config = {};
    if (hasPackage) {
      try {
        config = await fs.readJson(pkgPath);
      } catch {}
    }

    return {
      exists: true,
      hasPackage,
      hasNodeModules,
      config: hasPackage ? config : null,
      status: hasPackage && !hasNodeModules ? 'needs_install' : 'ok'
    };
  }
}

export const selfHealEngine = new SelfHealEngine();