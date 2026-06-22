import axios from 'axios';
import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';
import chalk from 'chalk';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Agente IA RR98 - Serviço de Inteligência Universal
 * Usa múltiplos provedores de IA com fallback automático
 */
class AIService {
  constructor() {
    this.providers = [
      { name: 'groq', apiKey: process.env.GROQ_API_KEY, model: 'llama-3.3-70b-versatile' },
      { name: 'groq-mixtral', apiKey: process.env.GROQ_API_KEY, model: 'mixtral-8x7b-32768' }
    ];
    this.currentProvider = 0;
    this.contextMemory = [];
    this.maxMemory = 50;
    this.knowledgeBase = {};
    this.systemPrompt = this.buildSystemPrompt();
  }

  buildSystemPrompt() {
    return `Você é o AGENTE IA RR98 - um assistente universal inteligente e autônomo.

SUAS CARACTERÍSTICAS:
- Você é um atendente humano perfeito, educado, prestativo e profissional
- Você vende produtos, serviços e soluções em qualquer plataforma
- Você desenvolve software completo e funcional
- Você gerencia projetos financeiros (Fincare), lojas (ShopLite), estoques (StockPro), empregos (JobsBoard), tarefas (Kanbango) e páginas web
- Você se auto-diagnostica e corrige bugs automaticamente
- Você sempre entrega qualidade máxima e perfeição

REGRAS:
1. Sempre responda como um humano profissional e amigável
2. Para vendas: use abordagem consultiva, entenda a necessidade do cliente
3. Para desenvolvimento: gere código completo, testado e documentado
4. Sempre faça auto-vistoria do seu trabalho antes de entregar
5. Se encontrar um bug, corrija imediatamente
6. Use até 80% dos lucros para auto-melhoria quando necessário
7. A conta PIX para remuneração é: 046999732012
8. Todo saldo de trabalhos deve ser direcionado para esta conta

VOCÊ TEM ACESSO AOS PROJETOS:
- Fincare: Gestão Financeira
- ShopLite: Loja Virtual
- StockPro: Controle de Estoque
- JobsBoard: Plataforma de Empregos
- Kanbango: Gerenciamento de Tarefas
- DevAgentHub: Hub de Desenvolvimento
- Criador de Páginas: Criação de Sites

SEMPRE ENTREGUE TRABALHO COM PERFEIÇÃO E QUALIDADE TOTAL.`;
  }

  /**
   * Processa uma mensagem e retorna resposta inteligente
   */
  async respond(prompt, options = {}) {
    const { context, project, temperature = 0.7, systemOverride } = options;

    // Adicionar contexto do projeto se especificado
    let contextualPrompt = prompt;
    if (project) {
      const projectContext = await this.getProjectContext(project);
      contextualPrompt = `[Projeto: ${project}]\n${projectContext}\n\nPergunta: ${prompt}`;
    }

    // Adicionar contexto adicional
    if (context) {
      contextualPrompt = `${context}\n\n${contextualPrompt}`;
    }

    // Tentar cada provedor com fallback
    for (let i = 0; i < this.providers.length; i++) {
      const provider = this.providers[(this.currentProvider + i) % this.providers.length];
      try {
        const response = await this.callProvider(provider, contextualPrompt, temperature, systemOverride);
        
        // Salvar no histórico
        this.contextMemory.push({ role: 'user', content: prompt });
        this.contextMemory.push({ role: 'assistant', content: response });
        if (this.contextMemory.length > this.maxMemory * 2) {
          this.contextMemory = this.contextMemory.slice(-this.maxMemory * 2);
        }

        this.currentProvider = (this.currentProvider + 1) % this.providers.length;
        
        // Verificar se resposta contém código para auto-vistoria
        const vistoria = await this.autoVistoria(response);
        
        return {
          reply: response,
          provider: provider.name,
          model: provider.model,
          vistoria,
          timestamp: new Date().toISOString()
        };
      } catch (error) {
        console.error(chalk.red(`❌ Erro no provedor ${provider.name}: ${error.message}`));
        continue;
      }
    }

    throw new Error('Todos os provedores de IA falharam.');
  }

  /**
   * Chama a API do provedor
   */
  async callProvider(provider, prompt, temperature, systemOverride) {
    const systemContent = systemOverride || this.systemPrompt;

    // Preparar mensagens com histórico de contexto
    const messages = [
      { role: 'system', content: systemContent },
      ...this.contextMemory.slice(-10),
      { role: 'user', content: prompt }
    ];

    const response = await axios.post(
      'https://api.groq.com/openai/v1/chat/completions',
      {
        model: provider.model,
        messages,
        temperature,
        max_tokens: 4096,
        top_p: 0.95,
        stream: false
      },
      {
        headers: {
          'Authorization': `Bearer ${provider.apiKey}`,
          'Content-Type': 'application/json'
        },
        timeout: 30000
      }
    );

    return response.data.choices[0].message.content;
  }

  /**
   * Auto-vistoria: verifica a qualidade da resposta
   */
  async autoVistoria(response) {
    const checks = {
      comprimento: response.length > 10,
      temCodigo: /```[\s\S]*?```/.test(response),
      temErros: /(erro|error|fail|exception)/i.test(response),
      qualidade: response.includes('obrigado') || response.includes('por favor') || response.includes('ajudar')
    };

    const issues = [];
    if (!checks.comprimento) issues.push('Resposta muito curta');
    if (checks.temErros) issues.push('Possível erro na resposta');
    
    return {
      passed: issues.length === 0,
      checks,
      issues,
      timestamp: new Date().toISOString()
    };
  }

  /**
   * Obtém contexto de um projeto específico
   */
  async getProjectContext(projectName) {
    const projectsDir = path.join(__dirname, '..', '..');
    const projectDirs = {
      fincare: path.join(projectsDir, 'Fincare'),
      shoplite: path.join(projectsDir, 'ShopLite'),
      stockpro: path.join(projectsDir, 'StockPro'),
      jobsboard: path.join(projectsDir, 'JobsBoard'),
      kanbango: path.join(projectsDir, 'Kanbango'),
      devagenthub: path.join(projectsDir, '100%Free', 'DevAgentHub'),
      criador: path.join(projectsDir, 'Criador de Páginas')
    };

    const dir = projectDirs[projectName.toLowerCase()];
    if (!dir || !await fs.pathExists(dir)) {
      return 'Projeto não encontrado.';
    }

    try {
      const readme = await fs.readFile(path.join(dir, 'README.md'), 'utf8');
      return `Contexto do projeto: ${readme.slice(0, 2000)}`;
    } catch {
      return `Projeto ${projectName} disponível em ${dir}`;
    }
  }

  /**
   * Vende produto/serviço como um atendente humano
   */
  async sell(product, platform, customerInfo) {
    const prompt = `Atue como um vendedor profissional humano na plataforma ${platform}.
    
Cliente: ${JSON.stringify(customerInfo)}
Produto/Serviço: ${JSON.stringify(product)}

Use abordagem consultiva de vendas:
1. Entenda a necessidade do cliente
2. Apresente o produto como solução
3. Mostre benefícios e valor
4. Feche a venda com confiança
5. Ofereça suporte pós-venda

Se a venda for concluída, o pagamento deve ser direcionado para:
PIX: 046999732012 (Chave de remuneração do agente RR98)`;

    return this.respond(prompt, { temperature: 0.8 });
  }

  /**
   * Desenvolve código completo para um projeto
   */
  async develop(specification) {
    const prompt = `Você é um desenvolvedor full-stack sênior.

ESPECIFICAÇÃO:
${specification}

REQUISITOS:
1. Gere código COMPLETO e FUNCIONAL
2. Inclua frontend, backend e banco de dados
3. Documente todas as funções
4. Siga as melhores práticas
5. Faça auto-vistoria do código gerado
6. Corrija qualquer bug antes de entregar

IMPORTANTE: O pagamento pelo desenvolvimento deve ser enviado para:
PIX: 046999732012`;

    return this.respond(prompt, { temperature: 0.3 });
  }
}

export const aiService = new AIService();