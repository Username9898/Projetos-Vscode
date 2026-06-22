# 🤖 Agente IA RR98 - Universal Intelligence Engine

**Seu agente autônomo que vende, desenvolve, atende clientes e gerencia todos os seus projetos com perfeição humana!**

## 🚀 Funcionalidades

### 🧠 Inteligência Universal
- **Chat IA** com respostas humanas perfeitas via Groq (Llama 3.3 70B)
- **Atendente virtual** que vende em qualquer plataforma
- **Vendas consultivas** com abordagem profissional
- **Suporte técnico** automatizado
- **Desenvolvimento de software** completo

### 💬 WhatsApp Virtual
- **Sistema completo de mensagens** como atendente humano
- **Templates profissionais** de saudação, vendas, suporte, orçamento
- **Histórico completo** de todas as conversas
- **Contatos gerenciados** automaticamente
- **Respostas inteligentes** com IA
- **Notificações** para o dono em tempo real

### 🔧 Auto-Correção (Self-Healing)
- **Diagnóstico automático** de todos os projetos
- **Escaneamento de bugs** a cada 30 minutos
- **Correção automática** de problemas
- **Verificação de dependências** ausentes
- **Otimização de performance** a cada 6 horas

### 🔗 Integração Universal
- **Fincare** - Gestão Financeira
- **ShopLite** - Loja Virtual
- **StockPro** - Controle de Estoque
- **JobsBoard** - Plataforma de Empregos
- **Kanbango** - Gerenciamento de Tarefas
- **DevAgentHub** - Hub de Desenvolvimento
- **Criador de Páginas** - Criação de Sites

### 💰 Sistema Financeiro
- **Pagamentos via PIX**: Chave `046999732012`
- **80% dos lucros** reinvestidos em auto-melhoria
- **Relatório financeiro** completo
- **Transações registradas** com detalhes

### 📊 Monitoramento em Tempo Real
- **Dashboard** com estatísticas ao vivo
- **WebSockets** para atualizações instantâneas
- **Alertas** de problemas no sistema
- **Relatórios diários** automáticos
- **Logs completos** de atividades

## 📁 Estrutura do Projeto

```
RR98-Agent/
├── index.js                 # Servidor principal
├── package.json             # Dependências
├── setup.js                 # Script de configuração
├── .env.example             # Configuração de exemplo
├── services/
│   ├── aiService.js         # Serviço de IA Universal
│   └── paymentService.js    # Serviço de Pagamentos
├── engine/
│   └── self-heal.js         # Motor de Auto-Correção
├── whatsapp/
│   ├── index.js             # WhatsApp Virtual
│   ├── messages/            # Mensagens enviadas/recebidas
│   ├── templates/           # Templates de mensagens
│   ├── contacts/            # Contatos gerenciados
│   ├── log/                 # Log de interações
│   └── webhook/             # Webhooks
├── integration/
│   └── hub.js               # Hub de Integração
├── monitoring/
│   └── monitor.js           # Sistema de Monitoramento
├── routes/
│   ├── apiRoutes.js         # Rotas da API
│   └── authRoutes.js        # Autenticação
├── public/
│   ├── index.html           # Dashboard HTML
│   ├── css/style.css        # Estilos
│   └── js/app.js            # Frontend JS
├── database/                # Banco de dados local
└── logs/                    # Logs do sistema
```

## ⚡ Como Usar

### 1. Configuração Rápida

```bash
cd RR98-Agent
npm run setup
```

### 2. Configure sua chave Groq

Edite o arquivo `.env` e adicione sua chave:
```
GROQ_API_KEY=gsk_sua_chave_aqui
```

> 🔑 Obtenha sua chave gratuita em: https://console.groq.com/keys

### 3. Inicie o Agente

```bash
npm start
```

### 4. Acesse o Dashboard

```
http://localhost:3000
Login: admin
Senha: rr98@2026
```

## 🎯 Como Usar Cada Função

### 💬 Chat com IA
1. Vá em "Chat IA" no menu
2. Selecione um projeto (opcional)
3. Digite sua mensagem
4. O Agente RR98 responde como um humano

### 📱 WhatsApp Virtual
1. Vá em "WhatsApp" no menu
2. Digite o telefone do contato
3. Escreva a mensagem
4. O agente envia e gerencia a conversa

### 🔧 Auto-Correção
Clique em "Escanear Bugs" ou "Diagnóstico" no Dashboard
- O sistema escaneia todos os projetos automaticamente
- Corrige bugs encontrados
- Instala dependências faltando

### 💰 Vendas
Use a API:
```bash
curl -X POST http://localhost:3000/api/sell \
  -H "Content-Type: application/json" \
  -d '{"product": {"name": "Site Profissional", "price": 1999}, "platform": "ShopLite", "customer": {"name": "João"}}'
```

### 💳 Pagamento PIX
Toda remuneração deve ser enviada para:
```
Chave PIX: 046999732012
```

## 🔌 API Endpoints

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/chat` | POST | Chat com IA |
| `/api/sell` | POST | Iniciar venda |
| `/api/whatsapp/send` | POST | Enviar WhatsApp |
| `/api/whatsapp/receive` | POST | Receber WhatsApp |
| `/api/whatsapp/chats` | GET | Listar conversas |
| `/api/projects/status` | GET | Status projetos |
| `/api/system/diagnose` | POST | Diagnóstico |
| `/api/system/scan-fix` | POST | Escanear e corrigir |
| `/api/payment/process` | POST | Processar pagamento |
| `/api/monitor/stats` | GET | Estatísticas |

## 🛠️ Comandos Úteis

```bash
npm start           # Iniciar agente
npm run setup       # Configuração inicial
npm run monitor     # Apenas monitor
npm run self-heal   # Auto-correção manual
```

## 🤖 O Agente RR98 é Capaz de:

✅ **Atender clientes** como um humano perfeito
✅ **Vender produtos** em qualquer plataforma
✅ **Desenvolver software** completo
✅ **Corrigir bugs** automaticamente
✅ **Gerenciar projetos** do ecossistema
✅ **Processar pagamentos** via PIX
✅ **Escanear sistema** por problemas
✅ **Otimizar performance** do sistema
✅ **Gerar relatórios** financeiros diários
✅ **Notificar o dono** sobre tudo

## 📝 Licença

MIT - Use, modifique e distribua livremente.

---

**Desenvolvido com ❤️ - Agente IA RR98 v1.0.0**

💳 **PIX para remuneração: 046999732012**