/**
 * 🤖 WhatsApp Virtual RR98 - Sistema de Comunicação Automatizada
 * 
 * Este sistema permite que o Agente RR98:
 * - Envie e receba mensagens como um atendente humano
 * - Gerencie contatos e conversas
 * - Use templates de mensagens profissionais
 * - Mantenha log completo de todas as interações
 * - Integre com todos os projetos do ecossistema
 * 
 * VOCÊ (dono) pode acompanhar tudo em tempo real pelo dashboard
 */

import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';
import chalk from 'chalk';
import { aiService } from '../services/aiService.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

class WhatsAppVirtual {
  constructor() {
    this.basePath = __dirname;
    this.messagesPath = path.join(__dirname, 'messages');
    this.templatesPath = path.join(__dirname, 'templates');
    this.contactsPath = path.join(__dirname, 'contacts');
    this.logPath = path.join(__dirname, 'log');
    this.webhookPath = path.join(__dirname, 'webhook');
    
    this.conversations = new Map();
    this.activeChats = new Map();
    this.init();
  }

  async init() {
    // Garantir que todas as pastas existam
    for (const dir of [this.messagesPath, this.templatesPath, this.contactsPath, this.logPath, this.webhookPath]) {
      await fs.ensureDir(dir);
    }
    console.log(chalk.green('📱 WhatsApp Virtual RR98 - Sistema de comunicação pronto!'));
  }

  /**
   * Enviar mensagem como atendente humano
   */
  async sendMessage(to, message, options = {}) {
    const {
      project = 'geral',
      platform = 'whatsapp',
      isAutomated = false,
      useAI = false
    } = options;

    const messageId = `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    const messageData = {
      id: messageId,
      from: 'Agente RR98 🤖',
      to,
      message,
      platform,
      project,
      timestamp: new Date().toISOString(),
      status: 'enviada',
      automated: isAutomated,
      read: false
    };

    // Salvar mensagem
    const msgFile = path.join(this.messagesPath, `${messageId}.json`);
    await fs.writeJson(msgFile, messageData, { spaces: 2 });

    // Registrar no log
    await this.logInteraction({
      type: 'sent',
      ...messageData
    });

    // Se for automatizada, processar com IA
    if (isAutomated && useAI) {
      await this.processAutomatedResponse(to, message, project);
    }

    console.log(chalk.cyan(`📤 Mensagem enviada para ${to}: ${message.substring(0, 50)}...`));
    
    return messageData;
  }

  /**
   * Receber mensagem de um cliente
   */
  async receiveMessage(from, message, options = {}) {
    const { project = 'geral', platform = 'whatsapp' } = options;

    const messageId = `msg_recv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

    const messageData = {
      id: messageId,
      from,
      to: 'Agente RR98 🤖',
      message,
      platform,
      project,
      timestamp: new Date().toISOString(),
      status: 'recebida',
      read: false
    };

    // Salvar mensagem
    const msgFile = path.join(this.messagesPath, `${messageId}.json`);
    await fs.writeJson(msgFile, messageData, { spaces: 2 });

    // Registrar no log
    await this.logInteraction({
      type: 'received',
      ...messageData
    });

    // Atualizar conversa ativa
    this.activeChats.set(from, {
      lastMessage: message,
      lastTimestamp: new Date().toISOString(),
      project,
      platform
    });

    console.log(chalk.yellow(`📩 Mensagem recebida de ${from}: ${message.substring(0, 50)}...`));

    // Processar resposta automática
    const reply = await this.generateReply(from, message, project);
    
    if (reply) {
      await this.sendMessage(from, reply, { project, isAutomated: true, useAI: false });
      return { received: messageData, reply };
    }

    return { received: messageData, reply: null };
  }

  /**
   * Gerar resposta automática inteligente
   */
  async generateReply(from, message, project = 'geral') {
    try {
      // Buscar histórico da conversa
      const history = await this.getConversationHistory(from, 5);
      
      // Buscar informações do contato
      const contact = await this.getContact(from);

      const context = `Você é um atendente humano profissional da RR98.

CONTATO: ${JSON.stringify(contact || { nome: from, telefone: from })}
PROJETO: ${project}
HISTÓRICO RECENTE: ${history.map(m => `${m.from}: ${m.message}`).join('\n')}

MENSAGEM DO CLIENTE: ${message}

REGRAS DO ATENDENTE RR98:
1. Seja educado, profissional e humano
2. Entenda a necessidade do cliente primeiro
3. Ofereça soluções dos projetos disponíveis
4. Se for venda: use abordagem consultiva
5. Se for suporte: resolva o problema
6. Sempre se apresente como "Agente RR98"
7. Para pagamentos: informe chave PIX 046999732012
8. Se não souber responder: peça para aguardar e escalone
9. Mantenha tom amigável mas profissional
10. NUNCA diga que é um robô - você é um atendente humano`;

      const response = await aiService.respond(context, {
        temperature: 0.7,
        project
      });

      return response.reply;
    } catch (error) {
      console.error(chalk.red(`❌ Erro ao gerar resposta: ${error.message}`));
      return `Olá! Recebi sua mensagem e já estou verificando a melhor forma de ajudar você. Em breve retorno com mais informações. Se precisar de atendimento urgente, me avise! 🤝`;
    }
  }

  /**
   * Processa resposta automatizada com IA
   */
  async processAutomatedResponse(to, message, project) {
    try {
      const reply = await this.generateReply(to, message, project);
      if (reply) {
        await this.sendMessage(to, reply, { project, isAutomated: true });
      }
    } catch (error) {
      console.error(chalk.red(`❌ Erro no processamento automático: ${error.message}`));
    }
  }

  /**
   * Obtém histórico de conversa com um contato
   */
  async getConversationHistory(contact, limit = 10) {
    const messages = [];
    
    try {
      const files = await fs.readdir(this.messagesPath);
      const contactFiles = files.filter(f => {
        const data = fs.readJsonSync(path.join(this.messagesPath, f));
        return data.from === contact || data.to === contact;
      });

      // Ordenar por timestamp
      contactFiles.sort((a, b) => {
        const dataA = fs.readJsonSync(path.join(this.messagesPath, a));
        const dataB = fs.readJsonSync(path.join(this.messagesPath, b));
        return new Date(dataA.timestamp) - new Date(dataB.timestamp);
      });

      // Pegar os últimos 'limit'
      const recentFiles = contactFiles.slice(-limit);
      
      for (const file of recentFiles) {
        const data = await fs.readJson(path.join(this.messagesPath, file));
        messages.push(data);
      }
    } catch (error) {
      console.error(chalk.red(`❌ Erro ao buscar histórico: ${error.message}`));
    }

    return messages;
  }

  /**
   * Gerencia contatos
   */
  async addContact(contactInfo) {
    const contactFile = path.join(this.contactsPath, `${contactInfo.telefone || contactInfo.id}.json`);
    const contactData = {
      ...contactInfo,
      addedAt: new Date().toISOString(),
      lastContact: null,
      totalMessages: 0,
      projects: []
    };

    await fs.writeJson(contactFile, contactData, { spaces: 2 });
    console.log(chalk.green(`👤 Contato adicionado: ${contactInfo.nome || contactInfo.telefone}`));
    return contactData;
  }

  /**
   * Obtém informações de um contato
   */
  async getContact(identifier) {
    try {
      const files = await fs.readdir(this.contactsPath);
      for (const file of files) {
        const data = await fs.readJson(path.join(this.contactsPath, file));
        if (data.telefone === identifier || data.id === identifier || data.email === identifier) {
          return data;
        }
      }
    } catch {
      // Contato não encontrado
    }
    return null;
  }

  /**
   * Lista todas as conversas ativas
   */
  async listActiveChats() {
    const conversations = [];
    
    try {
      const files = await fs.readdir(this.messagesPath);
      const uniqueContacts = new Set();
      
      for (const file of files) {
        const data = await fs.readJson(path.join(this.messagesPath, file));
        const contact = data.from === 'Agente RR98 🤖' ? data.to : data.from;
        uniqueContacts.add(contact);
      }

      for (const contact of uniqueContacts) {
        const history = await this.getConversationHistory(contact, 1);
        if (history.length > 0) {
          conversations.push({
            contact,
            lastMessage: history[0],
            project: history[0].project || 'geral'
          });
        }
      }
    } catch (error) {
      console.error(chalk.red(`❌ Erro ao listar conversas: ${error.message}`));
    }

    return conversations.sort((a, b) => new Date(b.lastMessage.timestamp) - new Date(a.lastMessage.timestamp));
  }

  /**
   * Cria template de mensagem
   */
  async createTemplate(name, content, category = 'geral') {
    const templateFile = path.join(this.templatesPath, `${name}.json`);
    const templateData = {
      name,
      content,
      category,
      createdAt: new Date().toISOString(),
      uses: 0
    };

    await fs.writeJson(templateFile, templateData, { spaces: 2 });
    console.log(chalk.green(`📋 Template criado: ${name}`));
    return templateData;
  }

  /**
   * Usa um template de mensagem
   */
  async useTemplate(templateName, variables = {}) {
    const templateFile = path.join(this.templatesPath, `${templateName}.json`);
    
    if (!await fs.pathExists(templateFile)) {
      throw new Error(`Template "${templateName}" não encontrado.`);
    }

    let template = await fs.readJson(templateFile);
    let content = template.content;

    // Substituir variáveis
    for (const [key, value] of Object.entries(variables)) {
      content = content.replace(`{{${key}}}`, value);
    }

    // Incrementar uso
    template.uses++;
    await fs.writeJson(templateFile, template, { spaces: 2 });

    return content;
  }

  /**
   * Registra interação no log
   */
  async logInteraction(data) {
    const logFile = path.join(this.logPath, `${Date.now()}_interaction.json`);
    await fs.writeJson(logFile, {
      ...data,
      loggedAt: new Date().toISOString()
    }, { spaces: 2 });
  }

  /**
   * Obtém relatório completo de comunicações
   */
  async getReport() {
    const messages = [];
    try {
      const files = await fs.readdir(this.messagesPath);
      for (const file of files) {
        const data = await fs.readJson(path.join(this.messagesPath, file));
        messages.push(data);
      }
    } catch {}

    const contacts = [];
    try {
      const files = await fs.readdir(this.contactsPath);
      for (const file of files) {
        const data = await fs.readJson(path.join(this.contactsPath, file));
        contacts.push(data);
      }
    } catch {}

    return {
      totalMessages: messages.length,
      sentMessages: messages.filter(m => m.status === 'enviada').length,
      receivedMessages: messages.filter(m => m.status === 'recebida').length,
      totalContacts: contacts.length,
      activeChats: this.activeChats.size,
      lastActivity: messages.length > 0 ? messages[messages.length - 1].timestamp : null,
      contacts,
      recentMessages: messages.slice(-10)
    };
  }

  /**
   * Inicia uma venda via WhatsApp
   */
  async startSale(contact, product, project) {
    const saleTemplate = await this.useTemplate('venda_inicio', {
      contato: contact.nome || contact.telefone,
      produto: product.nome || product,
      projeto: project
    });

    await this.sendMessage(contact.telefone || contact.id, saleTemplate, {
      project,
      isAutomated: true
    });

    return {
      contact,
      product,
      project,
      startedAt: new Date().toISOString(),
      status: 'iniciada'
    };
  }

  /**
   * Envia notificação sobre status do sistema para o dono
   */
  async notifyOwner(message) {
    const ownerContact = process.env.OWNER_PHONE || '046999732012';
    
    await this.sendMessage(ownerContact, `[SISTEMA RR98]\n\n${message}\n\n---\nEsta é uma notificação automática do seu agente.`, {
      project: 'sistema',
      isAutomated: true
    });

    console.log(chalk.cyan(`📢 Notificação enviada para o dono: ${message.substring(0, 100)}...`));
  }
}

export const whatsApp = new WhatsAppVirtual();

// Templates padrão que serão criados na inicialização
const defaultTemplates = [
  {
    name: 'saudacao_inicial',
    category: 'atendimento',
    content: `Olá {{contato}}! 👋

Aqui é o Agente RR98, seu assistente virtual. Como posso ajudar você hoje?

Posso auxiliar com:
✅ Vendas de produtos e serviços
✅ Suporte técnico 
✅ Desenvolvimento de software
✅ Gestão financeira
✅ Controle de estoque
✅ E muito mais!

Me diga como posso ser útil! 🤝`
  },
  {
    name: 'venda_inicio',
    category: 'vendas',
    content: `Olá {{contato}}! 🎉

Fiquei sabendo do seu interesse em {{produto}} do projeto {{projeto}}!

Posso te contar todos os detalhes e benefícios. Você tem interesse em saber mais?

Valores e condições especiais para você! 💰

PIX para pagamento: 046999732012`
  },
  {
    name: 'suporte_tecnico',
    category: 'suporte',
    content: `Olá {{contato}}! Recebi sua solicitação de suporte para {{projeto}}.

Já estou analisando o problema e em breve trago uma solução.

Enquanto isso, você pode me dar mais detalhes sobre o que aconteceu?

Estou aqui para resolver tudo pra você! 🔧`
  },
  {
    name: 'orcamento',
    category: 'vendas',
    content: `Olá {{contato}}! Segue o orçamento solicitado:

📋 SERVIÇO: {{servico}}
💵 VALOR: R$ {{valor}}
⏱ PRAZO: {{prazo}}

✅ Incluso:
- Desenvolvimento completo
- Garantia de qualidade
- Suporte incluso
- Atualizações

Para pagamento, utilize a chave PIX: 046999732012

Posso iniciar hoje mesmo? 🚀`
  },
  {
    name: 'pos_venda',
    category: 'atendimento',
    content: `Olá {{contato}}! Tudo bem? 🌟

Passando para saber como está sendo sua experiência com {{servico}}.

Está tudo funcionando bem? Precisa de alguma ajuda?

Lembre-se: você tem suporte garantido! Qualquer dúvida é só chamar.

Ah, e não esqueça de indicar nosso trabalho para seus amigos! 🙏`
  },
  {
    name: 'lembrete_pagamento',
    category: 'financeiro',
    content: `Olá {{contato}}! 💳

Apenas um lembrete amigável sobre o pagamento de {{servico}}.

💰 VALOR: R$ {{valor}}
📅 VENCIMENTO: {{vencimento}}

Chave PIX para pagamento: 046999732012

Qualquer dúvida estou à disposição! 🤝`
  }
];

// Inicializar templates
(async () => {
  for (const template of defaultTemplates) {
    try {
      await whatsApp.createTemplate(template.name, template.content, template.category);
    } catch {
      // Template já existe, ignorar
    }
  }
})();