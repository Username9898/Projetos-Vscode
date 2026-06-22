/**
 * 💰 SISTEMA DE IMPOSTOS AUTOMÁTICO RR98
 * Roberto Ribeiro (RR98) - CPF: 108.840.969-55
 * 
 * Calcula, separa e gerencia impostos automaticamente
 * para TODOS os projetos do ecossistema RR98
 * 
 * Regime: MEI (recomendado para desenvolvedor individual)
 * - DAS: 6% (R$ 72,90/mês fixo)
 * - INSS: 11% (recolhido no DAS)
 * - IRPF: Isento até R$ 28.559,70/ano
 */

import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';
import chalk from 'chalk';
import { RR98 } from '../branding/config.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

class TaxSystem {
  constructor() {
    this.owner = RR98.owner;
    this.brand = RR98.owner.brand;
    
    // Regras fiscais brasileiras 2026 - MEI
    this.taxRules = {
      mei: {
        das: { percentual: 0.06, descricao: 'DAS - Simples Nacional MEI' },
        inss: { percentual: 0.11, descricao: 'INSS - Contribuição Previdenciária' },
        iss: { percentual: 0.02, descricao: 'ISS - Serviços' },
        icms: { percentual: 0.00, descricao: 'ICMS - Comércio (isento MEI)' }
      },
      lucroPresumido: {
        irpj: 0.15,
        csll: 0.09,
        pis: 0.0065,
        cofins: 0.03,
        iss: 0.05
      },
      // Faixas IRPF 2026
      irpf: [
        { ate: 28559.70, aliquota: 0, deducao: 0 },
        { ate: 40220.36, aliquota: 0.075, deducao: 2142.56 },
        { ate: 50249.08, aliquota: 0.15, deducao: 5357.79 },
        { ate: 69480.78, aliquota: 0.225, deducao: 11409.62 },
        { ate: Infinity, aliquota: 0.275, deducao: 17378.50 }
      ]
    };

    // Config MEI - Valor fixo mensal
    this.meiFixedMonthly = 72.90; // DAS MEI 2026
    
    // Contas
    this.taxDir = __dirname;
    this.init();
  }

  async init() {
    const dirs = ['reports', 'history', 'separated', 'das', 'ir'];
    for (const dir of dirs) {
      await fs.ensureDir(path.join(this.taxDir, dir));
    }
    console.log(chalk.green(`💰 Sistema de Impostos RR98 - ${this.owner.name}`));
  }

  /**
   * Calcula imposto para uma venda
   */
  calculate(amount, projectNome, tipo = 'servico') {
    const calc = {
      proprietario: this.owner.name,
      cpf: this.owner.cpf,
      projeto: projectNome,
      receitaBruta: amount,
      data: new Date().toISOString(),
      
      // MEI - Regime simplificado
      regime: 'MEI',
      dasMensal: this.meiFixedMonthly,
      inss: amount * 0.11,
      iss: tipo === 'servico' ? amount * 0.02 : 0,
      
      // Totais
      totalImpostos: 0,
      receitaLiquida: 0,
      percentualImpostos: 0,
      
      // Reservas
      reservaImpostos: amount * 0.05, // 5% reserva
      disponivelProprietario: 0
    };

    // Total de impostos
    calc.totalImpostos = calc.inss + calc.iss + calc.dasMensal;
    calc.receitaLiquida = amount - calc.totalImpostos - calc.reservaImpostos;
    calc.percentualImpostos = (calc.totalImpostos / amount) * 100;
    calc.disponivelProprietario = calc.receitaLiquida;
    
    // Salvar
    this._salvar(calc);
    
    return calc;
  }

  /**
   * Calcula IRPF - Imposto de Renda Pessoa Física
   */
  calcularIRPF(rendaAnual) {
    for (const faixa of this.taxRules.irpf) {
      if (rendaAnual <= faixa.ate) {
        return Math.max(0, rendaAnual * faixa.aliquota - faixa.deducao);
      }
    }
    return 0;
  }

  /**
   * Relatório fiscal mensal completo
   */
  async relatorioMensal() {
    const transacoes = await this._coletarTransacoes();
    
    const relatorio = {
      proprietario: this.owner.name,
      cpf: this.owner.cpf,
      email: this.owner.email,
      whatsapp: this.owner.whatsapp,
      data: new Date().toISOString(),
      periodo: 'Mensal',
      
      receitaTotal: 0,
      totalImpostos: 0,
      dasMEI: this.meiFixedMonthly,
      inssTotal: 0,
      issTotal: 0,
      receitaLiquida: 0,
      
      projetos: {},
      transacoes: transacoes.length,
      
      declaracao: {
        tipo: 'MEI - Declaração Anual Simplificada',
        prazo: '31 de maio do ano seguinte',
        dasEmDia: true,
        irpfIsento: true,
        observacao: 'MEI é isento de IRPF se não ultrapassar R$ 81.000/ano'
      }
    };

    for (const tx of transacoes) {
      relatorio.receitaTotal += tx.amount || 0;
      const calc = this.calculate(tx.amount || 0, tx.project || 'RR98-Agent');
      relatorio.totalImpostos += calc.totalImpostos;
      relatorio.inssTotal += calc.inss;
      relatorio.issTotal += calc.iss;
    }

    relatorio.receitaLiquida = relatorio.receitaTotal - relatorio.totalImpostos;
    
    // Salvar
    const file = path.join(this.taxDir, 'reports', `mensal-${Date.now()}.json`);
    await fs.writeJson(file, relatorio, { spaces: 2 });

    return relatorio;
  }

  /**
   * Gera DAS - Documento de Arrecadação
   */
  async gerarDAS(mes, ano) {
    const das = {
      emitente: this.owner.name,
      cpf: this.owner.cpf,
      competencia: `${mes}/${ano}`,
      vencimento: `20/${String(mes + 1).padStart(2, '0')}/${ano}`,
      
      valorDAS: this.meiFixedMonthly,
      inss: 71.40, // INSS incluso no DAS
      valorTotal: this.meiFixedMonthly,
      
      pago: false,
      dataPagamento: null,
      
      geradoPor: `Agente RR98 - ${this.owner.name}`,
      timestamp: new Date().toISOString()
    };

    const file = path.join(this.taxDir, 'das', `DAS-${mes}-${ano}.json`);
    await fs.writeJson(file, das, { spaces: 2 });

    return das;
  }

  /**
   * Prepara declaração de IRPF
   */
  async declaracaoIRPF(ano) {
    const relatorio = await this.relatorioMensal();
    const rendaAnual = relatorio.receitaTotal;
    
    const irpfDevido = this.calcularIRPF(rendaAnual);
    const irpfRetido = relatorio.totalImpostos * 0.075; // Estimativa
    
    const declaracao = {
      ano,
      contribuinte: this.owner.name,
      cpf: this.owner.cpf,
      email: this.owner.email,
      
      rendimentos: {
        total: rendaAnual,
        tributaveis: rendaAnual,
        isentos: 0
      },
      
      impostoDevido: irpfDevido,
      impostoPago: irpfRetido,
      saldoAPagar: Math.max(0, irpfDevido - irpfRetido),
      restituicao: Math.max(0, irpfRetido - irpfDevido),
      
      projetos: Object.keys(relatorio.projetos || {}),
      
      status: irpfDevido <= 0 ? 'Isento' : 'Declarar',
      observacao: 'Mantenha registros de todas as transações por 5 anos'
    };

    const file = path.join(this.taxDir, 'ir', `IRPF-${ano}.json`);
    await fs.writeJson(file, declaracao, { spaces: 2 });

    return declaracao;
  }

  /**
   * Separa imposto automaticamente
   */
  async separarImposto(amount, projeto, transactionId) {
    const calc = this.calculate(amount, projeto);
    
    const separacao = {
      transacaoId: transactionId,
      projeto,
      receita: amount,
      
      contas: {
        das: this.meiFixedMonthly,
        inss: calc.inss,
        iss: calc.iss,
        reservaEmergencia: calc.reservaImpostos
      },
      
      totalSeparado: calc.totalImpostos + calc.reservaImpostos,
      disponivel: calc.disponivelProprietario,
      
      pago: false,
      data: new Date().toISOString()
    };

    const file = path.join(this.taxDir, 'separated', `separado-${transactionId}.json`);
    await fs.writeJson(file, separacao, { spaces: 2 });

    return separacao;
  }

  /**
   * Coleta transações de todos os projetos
   */
  async _coletarTransacoes() {
    let todas = [];

    // RR98 Agent
    const txDir = path.join(__dirname, '..', 'database', 'transactions');
    try {
      if (await fs.pathExists(txDir)) {
        const files = await fs.readdir(txDir);
        for (const f of files) {
          const data = await fs.readJson(path.join(txDir, f));
          todas.push({ ...data, project: data.project || 'RR98-Agent' });
        }
      }
    } catch {}

    // Outros projetos
    const projetos = ['Fincare', 'ShopLite', 'StockPro', 'JobsBoard', 'Kanbango'];
    for (const proj of projetos) {
      const projTxDir = path.join(__dirname, '..', '..', proj, 'database', 'transactions');
      try {
        if (await fs.pathExists(projTxDir)) {
          const files = await fs.readdir(projTxDir);
          for (const f of files) {
            const data = await fs.readJson(path.join(projTxDir, f));
            todas.push({ ...data, project: proj });
          }
        }
      } catch {}
    }

    return todas.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  }

  /**
   * Salva cálculo
   */
  _salvar(calc) {
    const file = path.join(this.taxDir, 'history', `calc-${Date.now()}.json`);
    fs.writeJson(file, calc, { spaces: 2 }).catch(() => {});
  }

  /**
   * Resumo fiscal para dashboard
   */
  async resumo() {
    const relatorio = await this.relatorioMensal();
    return {
      proprietario: this.owner.name,
      cpf: this.owner.cpf,
      email: this.owner.email,
      regime: 'MEI',
      dasMensal: `R$ ${this.meiFixedMonthly.toFixed(2)}`,
      faturamento: relatorio.receitaTotal,
      impostos: relatorio.totalImpostos,
      liquido: relatorio.receitaLiquida,
      transacoes: relatorio.transacoes,
      irpf: relatorio.declaracao.irpfIsento ? 'Isento' : 'Declarar'
    };
  }
}

export const taxSystem = new TaxSystem();