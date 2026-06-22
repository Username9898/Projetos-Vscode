import express from 'express';
import cors from 'cors';
import 'dotenv/config';
import { createServer } from 'http';
import { Server } from 'socket.io';
import path from 'path';
import { fileURLToPath } from 'url';
import chalk from 'chalk';
import { RR98 } from './branding/config.js';

import { aiService } from './services/aiService.js';
import { selfHealEngine } from './engine/self-heal.js';
import { protectionSystem } from './engine/protection.js';
import { gitHubSync } from './engine/github-sync.js';
import { paymentService } from './services/paymentService.js';
import { integrationHub } from './integration/hub.js';
import { monitorService } from './monitoring/monitor.js';
import { whatsApp } from './whatsapp/index.js';
import { taxSystem } from './tax-system/index.js';
import authRoutes from './routes/authRoutes.js';
import apiRoutes from './routes/apiRoutes.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const server = createServer(app);
const io = new Server(server, { cors: { origin: '*', methods: ['GET', 'POST'] } });

app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));
app.use(express.static(path.join(__dirname, 'public')));

// === Rotas ===
app.use('/api/auth', authRoutes);
app.use('/api', apiRoutes);

// === AI Chat Universal ===
app.post('/api/chat', async (req, res) => {
  const { prompt, context, project, temperature = 0.7 } = req.body;
  if (!prompt) return res.status(400).json({ error: 'Campo "prompt" é obrigatório.' });
  try {
    const result = await aiService.respond(prompt, { context, project, temperature });
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// === Executar ação automatizada ===
app.post('/api/execute', async (req, res) => {
  const { action, params } = req.body;
  if (!action) return res.status(400).json({ error: 'Campo "action" é obrigatório.' });
  try {
    const result = await integrationHub.execute(action, params);
    res.json({ success: true, result });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// === Tax System API ===
app.get('/api/tax/summary', async (req, res) => {
  try {
    const summary = await taxSystem.resumo();
    res.json(summary);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/tax/calculate', async (req, res) => {
  const { amount, project } = req.body;
  try {
    const calc = taxSystem.calculate(amount, project);
    res.json(calc);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/tax/separate', async (req, res) => {
  const { amount, project, transactionId } = req.body;
  try {
    const result = await taxSystem.separarImposto(amount, project, transactionId);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// === Protection System ===
app.get('/api/protection/report', (req, res) => {
  res.json(protectionSystem.getProtectionReport());
});

app.post('/api/protection/protect-project', async (req, res) => {
  const { path: projectPath } = req.body;
  try {
    const result = await protectionSystem.protectProject(projectPath || __dirname);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// === GitHub Sync ===
app.post('/api/github/sync', async (req, res) => {
  try {
    const result = await gitHubSync.syncAll();
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// === Health check ===
app.get('/api/health', (req, res) => {
  res.json({
    status: 'online',
    agent: 'RR98',
    version: '1.0.0',
    owner: RR98.owner.name,
    cpf: RR98.owner.cpf,
    pix: RR98.owner.pix,
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// === WebSocket para tempo real ===
io.on('connection', (socket) => {
  console.log(chalk.green(`🔌 Cliente conectado: ${socket.id}`));
  socket.on('chat:message', async (data) => {
    try {
      const result = await aiService.respond(data.prompt, data);
      socket.emit('chat:response', result);
    } catch (error) {
      socket.emit('chat:error', { error: error.message });
    }
  });
  socket.on('disconnect', () => {
    console.log(chalk.yellow(`🔌 Cliente desconectado: ${socket.id}`));
  });
});

// === Inicialização ===
const PORT = process.env.PORT || 3000;

async function bootstrap() {
  console.log(chalk.cyan('\n╔════════════════════════════════════════════════════╗'));
  console.log(chalk.cyan('║     🤖 AGENTE IA RR98 - UNIVERSAL ENGINE          ║'));
  console.log(chalk.cyan(`║     ${RR98.owner.name} - CPF: ${RR98.owner.cpf}          ║`));
  console.log(chalk.cyan('╚════════════════════════════════════════════════════╝\n'));

  // Auto-diagnóstico inicial
  await selfHealEngine.diagnose();
  
  // Proteger sistema
  console.log(chalk.blue('🛡️ Aplicando proteção aos arquivos...'));
  await protectionSystem.protectProject(__dirname);
  
  // Iniciar monitores
  monitorService.start(io);
  
  // Sincronizar com GitHub
  await gitHubSync.syncAll();
  gitHubSync.startAutoSync(6); // A cada 6 horas
  
  // Auto-melhoria agendada
  setInterval(async () => {
    console.log(chalk.blue('🔄 Executando auto-melhoria...'));
    await selfHealEngine.optimize();
  }, 1000 * 60 * 60 * 6);

  setInterval(async () => {
    console.log(chalk.blue('🔍 Escaneando por bugs...'));
    await selfHealEngine.scanAndFix();
  }, 1000 * 60 * 30);

  server.listen(PORT, () => {
    console.log(chalk.green(`\n✅ Servidor RR98 rodando na porta ${PORT}`));
    console.log(chalk.cyan(`📡 API: http://localhost:${PORT}/api`));
    console.log(chalk.cyan(`💬 Chat: http://localhost:${PORT}/chat`));
    console.log(chalk.cyan(`📊 Monitor: http://localhost:${PORT}/monitor`));
    console.log(chalk.cyan(`💰 PIX: ${RR98.owner.pix}`));
    console.log(chalk.cyan(`📱 WhatsApp: ${RR98.owner.whatsapp}`));
  });
}

bootstrap().catch(console.error);

export { app, server, io };