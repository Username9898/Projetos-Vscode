/**
 * 🛡️ SISTEMA DE PROTEÇÃO RR98
 * Roberto Ribeiro - CPF: 108.840.969-55
 * 
 * Proteção legal contra cópia não autorizada:
 * - Lei 9.610/98 (Direitos Autorais)
 * - Lei 9.279/96 (Propriedade Industrial)
 * - Marco Civil da Internet (Lei 12.965/14)
 * 
 * Royalties: 1% a 5% sobre lucro bruto para terceiros
 * Isento de impostos para o proprietário RR98
 */

import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';
import chalk from 'chalk';
import { RR98 } from '../branding/config.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

class ProtectionSystem {
  constructor() {
    this.owner = RR98.owner;
    this.license = RR98.license;
    this.royalties = RR98.royalties;
    this.watermark = this.generateWatermark();
    this.protectedFiles = new Set();
  }

  /**
   * Marca d'água digital única do RR98
   */
  generateWatermark() {
    return `
╔══════════════════════════════════════════╗
║  🛡️ RR98 - Roberto Ribeiro              ║
║  CPF: ${this.owner.cpf}                       ║
║  Lei 9.610/98 - Todos os direitos         ║
║  Uso não autorizado: 5% royalties         ║
║  PIX: ${this.owner.pix}                        ║
╚══════════════════════════════════════════╝
`;
  }

  /**
   * Adiciona proteção a um arquivo
   */
  async protectFile(filePath) {
    try {
      let content = await fs.readFile(filePath, 'utf8');
      
      // Adicionar header de proteção se não existir
      if (!content.includes('RR98 - Roberto Ribeiro')) {
        const header = `/**\n * 🛡️ RR98 - Roberto Ribeiro | CPF: ${this.owner.cpf}\n * ${this.owner.email} | ${this.owner.whatsapp}\n * PROTEÇÃO: Lei 9.610/98 - Cópia não autorizada: 5% royalties\n * PIX: ${this.owner.pix}\n */\n\n`;
        content = header + content;
        await fs.writeFile(filePath, content);
        this.protectedFiles.add(filePath);
        return true;
      }
      return false;
    } catch {
      return false;
    }
  }

  /**
   * Detecta uso não autorizado (simulação de fingerprint)
   */
  async detectUnauthorizedUse() {
    const fingerprints = [];
    const projectsDir = path.join(__dirname, '..', '..');
    
    // Verificar se há cópias dos projetos em locais não autorizados
    const projectNames = ['Fincare', 'ShopLite', 'StockPro', 'JobsBoard', 'Kanbango', 'RR98-Agent'];
    
    for (const project of projectNames) {
      const originalPath = path.join(projectsDir, project);
      if (await fs.pathExists(originalPath)) {
        fingerprints.push({
          project,
          path: originalPath,
          owner: this.owner.name,
          protected: true,
          license: this.license.type
        });
      }
    }

    return {
      owner: this.owner.name,
      cpf: this.owner.cpf,
      protectedProjects: fingerprints,
      royaltyRate: `${this.royalties.unauthorizedUse * 100}%`,
      legal: this.royalties.legal,
      timestamp: new Date().toISOString()
    };
  }

  /**
   * Gera aviso de royalty para terceiros
   */
  generateRoyaltyNotice(companyName, revenue) {
    const royaltyDue = revenue * this.royalties.unauthorizedUse;
    
    return {
      notice: 'NOTIFICAÇÃO DE ROYALTIES - RR98',
      infringer: companyName,
      infringerRevenue: revenue,
      royaltyRate: this.royalties.unauthorizedUse,
      royaltyDue,
      pixKey: this.owner.pix,
      dueDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
      legal: this.royalties.legal,
      message: `O uso não autorizado do software RR98 gera royalties de ${this.royalties.unauthorizedUse * 100}% sobre o lucro bruto. Valor devido: R$ ${royaltyDue.toFixed(2)}. Pague via PIX: ${this.owner.pix}`
    };
  }

  /**
   * Registra tentativa de cópia
   */
  async logCopyAttempt(attemptData) {
    const logDir = path.join(__dirname, '..', 'logs', 'protection');
    await fs.ensureDir(logDir);
    
    const log = {
      ...attemptData,
      detectedAt: new Date().toISOString(),
      owner: this.owner.name,
      cpf: this.owner.cpf,
      action: 'USO NÃO AUTORIZADO DETECTADO - Royalties devidos'
    };

    const file = path.join(logDir, `copy-attempt-${Date.now()}.json`);
    await fs.writeJson(file, log, { spaces: 2 });

    // Notificar via WhatsApp
    const { whatsApp } = await import('../whatsapp/index.js');
    await whatsApp.notifyOwner(
      `🚨 ALERTA DE PROTEÇÃO RR98\n\n` +
      `Tentativa de uso não autorizado detectada!\n` +
      `IP: ${attemptData.ip || 'Desconhecido'}\n` +
      `Ação: ${attemptData.action || 'N/A'}\n` +
      `Royalties devidos: 5% do lucro bruto\n` +
      `PIX: ${this.owner.pix}`
    );

    return log;
  }

  /**
   * Aplica proteção em todos os arquivos de um projeto
   */
  async protectProject(projectPath) {
    const files = await this._walkDir(projectPath);
    let protected = 0;

    for (const file of files) {
      if (file.endsWith('.js') || file.endsWith('.jsx') || file.endsWith('.ts') || file.endsWith('.tsx') || file.endsWith('.html') || file.endsWith('.css')) {
        if (await this.protectFile(file)) {
          protected++;
        }
      }
    }

    return { project: projectPath, filesProtected: protected };
  }

  /**
   * Caminha diretório recursivamente
   */
  async _walkDir(dir) {
    const files = [];
    const entries = await fs.readdir(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory() && !entry.name.startsWith('node_modules') && !entry.name.startsWith('.git')) {
        files.push(...await this._walkDir(fullPath));
      } else if (entry.isFile()) {
        files.push(fullPath);
      }
    }
    
    return files;
  }

  /**
   * Relatório de proteção
   */
  getProtectionReport() {
    return {
      owner: this.owner.name,
      cpf: this.owner.cpf,
      email: this.owner.email,
      whatsapp: this.owner.whatsapp,
      protectedFiles: this.protectedFiles.size,
      license: this.license,
      royalties: this.royalties,
      watermark: this.watermark,
      legalBasis: [
        'Lei 9.610/98 - Direitos Autorais',
        'Lei 9.279/96 - Propriedade Industrial',
        'Lei 12.965/14 - Marco Civil da Internet',
        'Código Penal - Arts. 184 a 186'
      ]
    };
  }
}

export const protectionSystem = new ProtectionSystem();