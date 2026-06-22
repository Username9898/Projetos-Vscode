import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';
import chalk from 'chalk';
import os from 'os';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Sistema de Monitoramento do Agente RR98
 * Acompanha performance, atividades e saúde do sistema
 */
class MonitorService {
  constructor() {
    this.stats = {
      startTime: Date.now(),
      requests: { total: 0, success: 0, error: 0 },
      messages: { sent: 0, received: 0 },
      sales: { total: 0, revenue: 0 },
      bugsFixed: 0,
      optimizations: 0,
      uptime: 0
    };
    this.alerts = [];
    this.io = null;
  }

  start(io) {
    this.io = io;
    console.log(chalk.green('📊 Monitor RR98 iniciado'));

    // Atualizar estatísticas a cada 10 segundos
    setInterval(() => this.updateStats(), 10000);
    
    // Verificar saúde do sistema a cada minuto
    setInterval(() => this.healthCheck(), 60000);
    
    // Gerar relatório diário
    setInterval(() => this.dailyReport(), 24 * 60 * 60 * 1000);
  }

  async updateStats() {
    this.stats.uptime = Math.floor((Date.now() - this.stats.startTime) / 1000);
    
    const stats = {
      ...this.stats,
      memoryUsage: process.memoryUsage(),
      cpuLoad: os.loadavg(),
      freeMemory: os.freemem(),
      totalMemory: os.totalmem(),
      timestamp: new Date().toISOString()
    };

    // Emitir via WebSocket se conectado
    if (this.io) {
      this.io.emit('monitor:stats', stats);
    }

    // Salvar estatísticas
    await this.saveStats(stats);
  }

  async healthCheck() {
    const health = {
      status: 'healthy',
      memory: process.memoryUsage().heapUsed / process.memoryUsage().heapTotal < 0.9 ? 'ok' : 'warning',
      uptime: this.stats.uptime,
      requestsOk: this.stats.requests.error / Math.max(this.stats.requests.total, 1) < 0.1,
      timestamp: new Date().toISOString()
    };

    // Verificar projetos
    const projectsPath = path.join(__dirname, '..', '..');
    const projects = ['Fincare', 'ShopLite', 'StockPro', 'JobsBoard', 'Kanbango'];
    
    for (const project of projects) {
      const exists = await fs.pathExists(path.join(projectsPath, project));
      if (!exists) {
        health.status = 'degraded';
        this.addAlert('warning', `Projeto ${project} não encontrado`);
      }
    }

    if (this.io) {
      this.io.emit('monitor:health', health);
    }

    // Se degradado, tentar auto-recuperação
    if (health.status === 'degraded') {
      const { selfHealEngine } = await import('../engine/self-heal.js');
      await selfHealEngine.diagnose();
    }

    return health;
  }

  trackRequest(success = true) {
    this.stats.requests.total++;
    if (success) {
      this.stats.requests.success++;
    } else {
      this.stats.requests.error++;
    }
  }

  trackMessage(type = 'sent') {
    if (type === 'sent') this.stats.messages.sent++;
    else this.stats.messages.received++;
  }

  trackSale(amount) {
    this.stats.sales.total++;
    this.stats.sales.revenue += amount;
  }

  trackBugFix() {
    this.stats.bugsFixed++;
  }

  trackOptimization() {
    this.stats.optimizations++;
  }

  addAlert(level, message) {
    const alert = {
      level,
      message,
      timestamp: new Date().toISOString()
    };
    this.alerts.push(alert);
    
    console.log(chalk.yellow(`⚠️  Alerta [${level}]: ${message}`));

    if (this.io) {
      this.io.emit('monitor:alert', alert);
    }

    // Manter apenas últimos 100 alertas
    if (this.alerts.length > 100) {
      this.alerts = this.alerts.slice(-100);
    }
  }

  async saveStats(stats) {
    const logDir = path.join(__dirname, '..', 'logs', 'stats');
    await fs.ensureDir(logDir);
    const statFile = path.join(logDir, `stats-${Date.now()}.json`);
    await fs.writeJson(statFile, stats, { spaces: 2 });
  }

  async dailyReport() {
    const report = {
      date: new Date().toISOString().split('T')[0],
      period: '24h',
      stats: this.stats,
      alerts: this.alerts.slice(-20),
      health: await this.healthCheck(),
      timestamp: new Date().toISOString()
    };

    const reportDir = path.join(__dirname, '..', 'logs', 'reports');
    await fs.ensureDir(reportDir);
    const reportFile = path.join(reportDir, `report-${report.date}.json`);
    await fs.writeJson(reportFile, report, { spaces: 2 });

    console.log(chalk.cyan(`\n📋 Relatório diário gerado: ${report.date}`));
    console.log(chalk.cyan(`   Requisições: ${this.stats.requests.total}`));
    console.log(chalk.cyan(`   Mensagens: ${this.stats.messages.sent + this.stats.messages.received}`));
    console.log(chalk.cyan(`   Vendas: ${this.stats.sales.total}`));
    console.log(chalk.cyan(`   Bugs corrigidos: ${this.stats.bugsFixed}\n`));

    // Notificar dono via WhatsApp
    const { whatsApp } = await import('../whatsapp/index.js');
    await whatsApp.notifyOwner(
      `📊 RELATÓRIO DIÁRIO - ${report.date}\n\n` +
      `✅ Requisições: ${this.stats.requests.total}\n` +
      `💬 Mensagens: ${this.stats.messages.sent + this.stats.messages.received}\n` +
      `💰 Vendas: ${this.stats.sales.total} (R$ ${this.stats.sales.revenue})\n` +
      `🔧 Bugs corrigidos: ${this.stats.bugsFixed}\n` +
      `⚡ Otimizações: ${this.stats.optimizations}\n` +
      `📈 Uptime: ${Math.floor(this.stats.uptime / 3600)}h`
    );
  }

  getStats() {
    return {
      ...this.stats,
      alerts: this.alerts.slice(-10),
      memoryUsage: process.memoryUsage(),
      uptime: Math.floor((Date.now() - this.stats.startTime) / 1000)
    };
  }
}

export const monitorService = new MonitorService();