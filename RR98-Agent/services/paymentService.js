/**
 * 💰 Serviço de Pagamentos - Agente RR98
 * 
 * Gerencia transações financeiras e direciona para PIX
 * Chave PIX principal: 046999732012
 */

import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';
import chalk from 'chalk';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

class PaymentService {
  constructor() {
    this.pixKey = '046999732012';
    this.transactionsPath = path.join(__dirname, '..', 'database', 'transactions.json');
    this.totalRevenue = 0;
    this.improvementBudget = 0;
    this.loadState();
  }

  async loadState() {
    try {
      if (await fs.pathExists(this.transactionsPath)) {
        const data = await fs.readJson(this.transactionsPath);
        this.totalRevenue = data.totalRevenue || 0;
        this.improvementBudget = data.improvementBudget || 0;
      }
    } catch {}
  }

  async saveState() {
    await fs.writeJson(this.transactionsPath, {
      totalRevenue: this.totalRevenue,
      improvementBudget: this.improvementBudget,
      updatedAt: new Date().toISOString()
    }, { spaces: 2 });
  }

  /**
   * Processa um pagamento recebido
   */
  async processPayment(amount, metadata = {}) {
    const { customer, service, project } = metadata;

    this.totalRevenue += amount;
    const improvementAmount = amount * 0.8;
    this.improvementBudget += improvementAmount;

    const transaction = {
      id: `tx_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      amount,
      pixKey: this.pixKey,
      customer: customer || 'Cliente',
      service: service || 'Serviço RR98',
      project: project || 'geral',
      improvementAllocated: improvementAmount,
      timestamp: new Date().toISOString(),
      status: 'completed'
    };

    // Salvar transação
    const txDir = path.join(__dirname, '..', 'database', 'transactions');
    await fs.ensureDir(txDir);
    await fs.writeJson(path.join(txDir, `${transaction.id}.json`), transaction, { spaces: 2 });

    await this.saveState();

    console.log(chalk.green(`\n💰 Pagamento processado: R$ ${amount.toFixed(2)}`));
    console.log(chalk.cyan(`   PIX: ${this.pixKey}`));
    console.log(chalk.cyan(`   ${improvementAmount.toFixed(2)} destinado a melhorias (80%)\n`));

    // Notificar via WhatsApp
    const { whatsApp } = await import('../whatsapp/index.js');
    await whatsApp.notifyOwner(
      `💰 NOVO PAGAMENTO RECEBIDO\n\n` +
      `Valor: R$ ${amount.toFixed(2)}\n` +
      `Cliente: ${customer || 'Anônimo'}\n` +
      `Serviço: ${service || 'Geral'}\n` +
      `PIX: ${this.pixKey}\n\n` +
      `Total acumulado: R$ ${this.totalRevenue.toFixed(2)}\n` +
      `Orçamento para melhorias: R$ ${this.improvementBudget.toFixed(2)}`
    );

    return transaction;
  }

  /**
   * Usa parte do orçamento de melhoria
   */
  async spendOnImprovement(amount, description) {
    if (amount > this.improvementBudget) {
      throw new Error(`Orçamento insuficiente. Disponível: R$ ${this.improvementBudget.toFixed(2)}`);
    }

    this.improvementBudget -= amount;

    const expense = {
      id: `exp_${Date.now()}`,
      amount,
      description,
      timestamp: new Date().toISOString()
    };

    const expDir = path.join(__dirname, '..', 'database', 'expenses');
    await fs.ensureDir(expDir);
    await fs.writeJson(path.join(expDir, `${expense.id}.json`), expense, { spaces: 2 });
    await this.saveState();

    console.log(chalk.cyan(`💡 Investido R$ ${amount.toFixed(2)} em: ${description}`));
    return expense;
  }

  getFinancialReport() {
    return {
      pixKey: this.pixKey,
      totalRevenue: this.totalRevenue,
      improvementBudget: this.improvementBudget,
      investedInImprovements: this.totalRevenue * 0.8 - this.improvementBudget
    };
  }
}

export const paymentService = new PaymentService();