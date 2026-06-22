/**
 * ⚡ RR98 BRANDING & OWNER CONFIG
 * Roberto Ribeiro - Todos os direitos reservados
 * 
 * Esta é a configuração central de identidade
 * que será usada por TODOS os projetos do ecossistema
 */

export const RR98 = {
  // === DADOS DO PROPRIETÁRIO ===
  owner: {
    name: 'Roberto Ribeiro',
    brand: 'RR98',
    cpf: '108.840.969-55',
    whatsapp: '+55046999732012',
    email: 'Robertojn321@gmail.com',
    birthYear: 1998,
    pix: '046999732012'
  },

  // === LICENCIAMENTO E PROTEÇÃO ===
  license: {
    type: 'RR98 Exclusive License',
    version: '1.0.0',
    description: 'Software protegido por direitos autorais. Uso não autorizado sujeito a penalidades legais.',
    royaltyRate: 0.05, // 5% de royalties para uso não-autorizado
    legalProtection: true,
    jurisdiction: 'Brasil'
  },

  // === TAXAS DE USO (cobradas de terceiros que copiarem) ===
  royalties: {
    unauthorizedUse: 0.05, // 5% do lucro bruto
    authorizedUse: 0.01,  // 1% se autorizado por contrato
    taxFree: true,        // Isento de impostos para o proprietário
    pixKey: '046999732012',
    legal: 'Lei 9.610/98 (Direitos Autorais) + Lei 9.279/96 (Propriedade Industrial)'
  },

  // === GITHUB AUTO-UPLOAD ===
  github: {
    repository: 'https://github.com/Username9898/Projetos-Vscode',
    autoUpload: true,
    branch: 'main',
    commitMessage: '🤖 Auto-upload RR98 Agent - Sistema atualizado'
  }
};