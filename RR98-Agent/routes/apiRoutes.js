import { Router } from 'express';
import { aiService } from '../services/aiService.js';
import { selfHealEngine } from '../engine/self-heal.js';
import { integrationHub } from '../integration/hub.js';
import { paymentService } from '../services/paymentService.js';
import { monitorService } from '../monitoring/monitor.js';
import { whatsApp } from '../whatsapp/index.js';

const router = Router();

// === Dashboard Principal ===
router.get('/dashboard', (req, res) => {
  res.json({
    agent: 'RR98',
    version: '1.0.0',
    status: 'online',
    services: ['ai', 'self-heal', 'integration', 'payment', 'monitor', 'whatsapp'],
    projects: ['Fincare', 'ShopLite', 'StockPro', 'JobsBoard', 'Kanbango', 'DevAgentHub', 'Criador de Páginas']
  });
});

// === Chat com IA ===
router.post('/chat', async (req, res) => {
  const { prompt, context, project } = req.body;
  if (!prompt) return res.status(400).json({ error: 'Prompt é obrigatório' });
  
  monitorService.trackRequest();
  try {
    const result = await aiService.respond(prompt, { context, project });
    res.json(result);
  } catch (error) {
    monitorService.trackRequest(false);
    res.status(500).json({ error: error.message });
  }
});

// === Vendas via IA ===
router.post('/sell', async (req, res) => {
  const { product, platform, customer } = req.body;
  try {
    const result = await aiService.sell(product, platform, customer);
    monitorService.trackSale(product.price || 0);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// === WhatsApp ===
router.post('/whatsapp/send', async (req, res) => {
  const { to, message, project } = req.body;
  try {
    const result = await whatsApp.sendMessage(to, message, { project });
    monitorService.trackMessage('sent');
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.post('/whatsapp/receive', async (req, res) => {
  const { from, message, project } = req.body;
  try {
    const result = await whatsApp.receiveMessage(from, message, { project });
    monitorService.trackMessage('received');
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/whatsapp/chats', async (req, res) => {
  try {
    const chats = await whatsApp.listActiveChats();
    res.json(chats);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/whatsapp/report', async (req, res) => {
  try {
    const report = await whatsApp.getReport();
    res.json(report);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// === Integração com Projetos ===
router.post('/project/install', async (req, res) => {
  const { project } = req.body;
  try {
    const result = await integrationHub.installDependencies({ project });
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/projects/status', async (req, res) => {
  try {
    const status = await integrationHub.getProjectStatus();
    res.json(status);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// === Pagamentos e Financeiro ===
router.post('/payment/process', async (req, res) => {
  const { amount, customer, service } = req.body;
  try {
    const result = await paymentService.processPayment(amount, { customer, service });
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/payment/report', (req, res) => {
  res.json(paymentService.getFinancialReport());
});

// === Auto-Correção e Diagnóstico ===
router.post('/system/diagnose', async (req, res) => {
  try {
    const result = await selfHealEngine.diagnose();
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.post('/system/scan-fix', async (req, res) => {
  try {
    const result = await selfHealEngine.scanAndFix();
    monitorService.trackBugFix();
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.post('/system/optimize', async (req, res) => {
  try {
    const result = await selfHealEngine.optimize();
    monitorService.trackOptimization();
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// === Monitoramento ===
router.get('/monitor/stats', (req, res) => {
  res.json(monitorService.getStats());
});

router.get('/monitor/health', async (req, res) => {
  try {
    const health = await monitorService.healthCheck();
    res.json(health);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// === Hub de Ações ===
router.post('/action/:actionName', async (req, res) => {
  const { actionName } = req.params;
  const params = req.body;
  try {
    const result = await integrationHub.execute(actionName, params);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/actions', (req, res) => {
  res.json(integrationHub.listActions());
});

export default router;