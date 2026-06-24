# LicitaMaster - Sistema Automatico de Licitacoes

**Versao:** 1.0.0  
**Criado por:** [Usuario do Projeto]  
**Data:** 24/06/2026

---

## SOBRE O PROJETO

O **LicitaMaster** e um sistema inteligente e automatizado que:

1. **VARRENOS PORTAIS PUBLICOS** de licitacao (PNCP, ComprasNet, Diarios Oficiais, TCE) em busca de oportunidades
2. **ANALISA** as licitacoes e faz **MATCH** com clientes cadastrados usando IA local
3. **NOTIFICA** os clientes automaticamente via WhatsApp sobre oportunidades relevantes
4. **GERA PROPOSTAS** e acompanha o processo ate o resultado
5. **GERENCIA COMISSOES** - calcula, cobra e rastreia pagamentos

Tudo isso **100% GRATUITO** - sem APIs pagas, sem assinaturas, sem custos operacionais.

---

## COMO GERA DINHEIRO REAL

O sistema funciona assim:

```
[PORTAL PUBLICO] --> [LICITAMASTER] --> [CLIENTE]
                                            |
                                      [FECHA CONTRATO]
                                            |
                                  [COMISSAO 1% a 10%]
                                            |
                              [VOCE RECEBE SUA COMISSAO]
```

1. O sistema encontra licitacoes compativeis com seus clientes
2. Notifica os clientes via WhatsApp
3. Quando o cliente fecha o contrato, voce recebe **1% a 10%** de comissao
4. Para contratos recorrentes, a comissao e **MENSAL**

### Exemplo de Ganhos:

| Valor da Licitacao | Sua Comissao (5%) | Lucro Mensal (10 contratos) |
|-------------------|-------------------|---------------------------|
| R$ 50.000 | R$ 2.500 | R$ 25.000 |
| R$ 100.000 | R$ 5.000 | R$ 50.000 |
| R$ 500.000 | R$ 25.000 | R$ 250.000 |

---

## REQUISITOS

- **Python 3.8+** (gratuito)
- **Conexao com internet** (para buscar licitacoes nos portais)
- **WhatsApp** (para notificar clientes)
- **Node.js** (opcional, para WhatsApp bot avancado)

### Instalacao

```bash
# 1. Clone o repositorio
git clone https://github.com/seu-usuario/LicitaMaster.git
cd LicitaMaster

# 2. Instale as dependencias
pip install -r requirements.txt

# 3. Configure o ambiente (opcional)
cp .env.example .env
# Edite o .env com suas configuracoes

# 4. Execute
python main.py
```

---

## COMO USAR

### Modo Interativo (Recomendado)

```bash
python main.py
```

Menu principal:
- **[1]** Buscar Licitacoes - varre portais publicos
- **[2]** Analisar Oportunidades - faz match com clientes
- **[3]** Notificar Clientes - envia WhatsApp
- **[4]** Relatorio Financeiro - veja seus ganhos
- **[5]** Registrar Cliente - cadastra nova empresa
- **[6]** Listar Clientes
- **[7]** Listar Oportunidades
- **[8]** Calcular Comissao
- **[9]** Ciclo Completo - busca + analisa + notifica
- **[10]** Estatisticas
- **[11]** Modo Automatico - loop infinito (deixe rodando)

### Modo Automatico (Servidor)

```bash
# Roda 24/7 buscando oportunidades automaticamente
python main.py --modo auto --intervalo 60
```

### Linha de Comando

```bash
# Apenas busca
python main.py --modo busca

# Apenas analise
python main.py --modo analise
```

---

## ESTRUTURA DO PROJETO

```
LicitaMaster/
│
├── main.py                    # Entry point principal
├── requirements.txt           # Dependencias
├── .env.example              # Exemplo de configuracao
│
├── core/                     # Nucleo do sistema
│   ├── database.py           # Gerenciamento do banco SQLite
│   ├── scraper.py            # Raspagem de portais de licitacao
│   └── analyzer.py           # Analise e match com clientes
│
├── commercial/               # Comercial e financeiro
│   ├── commission.py         # Motor de comissoes e repasses
│   └── proposal.py           # Gerador de propostas
│
├── integration/              # Integracoes
│   ├── whatsapp_bot.py       # Bot WhatsApp
│   └── dashboard.py          # Dashboard web (opcional)
│
├── data/                     # Banco de dados
│   ├── schema.sql            # Estrutura do banco
│   └── seed.py               # Dados iniciais
│
└── legal/                    # Documentacao legal
    ├── compliance.py         # Verificacao juridica
    └── templates/            # Minutas de contratos
```

---

## PORTAIS DE LICITACAO SUPORTADOS

| Portal | URL | Gratuito |
|--------|-----|----------|
| PNCP (Portal Nacional) | https://pncp.gov.br | Sim |
| ComprasNet | https://www.gov.br/compras | Sim |
| Diarios Oficiais (SP, RJ, MG, etc) | Varios | Sim |
| Tribunais de Contas | Varios | Sim |

---

## COMISSOES E REPASSES

### Suas Comissoes

Voce define o percentual de comissao que cobra dos clientes (1% a 10%):

```python
from commercial.commission import calcular_repasse

# Exemplo: R$ 100.000 com 5% de comissao
resultado = calcular_repasse(100000, 5)
print(f"Valor da comissao: R$ {resultado['valor_comissao']:.2f}")
```

### Repasse ao Criador

**IMPORTANTE:** Este projeto foi criado por **[Usuario do Projeto]** e disponibilizado gratuitamente. 

Ao utilizar este sistema para gerar receita, voce concorda em repassar **entre 1% e 10%** dos lucros obtidos ao criador do projeto, como forma de reconhecimento pelo trabalho e manutencao do codigo.

**Como fazer o repasse:**

1. O proprio sistema calcula automaticamente o valor do repasse
2. Consulte o relatorio financeiro (opcao 4 do menu)
3. O valor do repasse aparece destacado
4. Utilize a chave PIX disponivel na documentacao interna

**Por que esse repasse?**
- O projeto e 100% gratuito e open source
- Nao ha custos com APIs ou servicos pagos
- O repasse e voluntario, mas esperado como contrapartida etica
- Valores de 1% a 10% dos lucros - voce escolhe o percentual

---

## LEGAL E COMPLIANCE

O LicitaMaster opera dentro da legalidade:

- **Lei 14.133/2021** - Nova Lei de Licitacoes e Contratos
- Dados obtidos de fontes publicas (portais governamentais)
- Nao ha invasao ou quebra de seguranca
- Prospeccao comercial etica e transparente
- Comissoes sobre intermediacao de negocios sao legais no Brasil

---

## WHATSAPP BOT

Para enviar mensagens automaticas de WhatsApp:

### Opcao 1: whatsapp-web.js (recomendado)

```bash
# Instale o Node.js
# Depois:
npm install whatsapp-web.js
node whatsapp-bridge.js
```

### Opcao 2: Envio manual

O sistema gera o relatorio de oportunidades para voce copiar e colar no WhatsApp.

---

## SOLUCIONANDO PROBLEMAS

**Nenhuma licitacao encontrada:**
- Verifique sua conexao com a internet
- Os portais podem estar temporariamente indisponiveis
- Ajuste o `VALOR_MINIMO_OPORTUNIDADE` no `.env`

**WhatsApp nao envia:**
- Instale o whatsapp-web.js (Node.js)
- Configure o numero corretamente com DDI (ex: 5511999999999)
- Verifique se o WhatsApp Web esta escaneado

**Banco de dados corrompido:**
```bash
rm data/licitamaster.db
python main.py  # Recria automaticamente
```

---

## LICENSE

Este projeto e distribuido gratuitamente para uso pessoal e comercial.

**CONDICOES:**
1. Mantenha os creditos do criador no codigo e documentacao
2. Ao gerar receita com o sistema, repasse 1-10% ao criador
3. Nao revenda o codigo como seu sem autorizacao
4. Contribuicoes e melhorias sao bem-vindas via GitHub

---

**Criado por: [Usuario do Projeto]**  
**Data: 24/06/2026**  
**GitHub: https://github.com/seu-usuario/LicitaMaster**

*"Transformando licitacoes publicas em oportunidades reais de negocio"*