-- ============================================================
-- LicitaMaster - Database Schema
-- Sistema Automatico de Licitacoes
-- ============================================================

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- ============================================================
-- CLIENTES
-- ============================================================
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cnpj TEXT UNIQUE,
    email TEXT,
    telefone TEXT,
    whatsapp TEXT,
    site TEXT,
    ramo TEXT,
    porte TEXT CHECK(porte IN ('MEI', 'ME', 'EPP', 'MEDIO', 'GRANDE')),
    faturamento_anual REAL DEFAULT 0,
    estado TEXT,
    cidade TEXT,
    endereco TEXT,
    observacoes TEXT,
    ativo INTEGER DEFAULT 1,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- LICITACOES (Editais)
-- ============================================================
CREATE TABLE IF NOT EXISTS licitacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT,
    orgao TEXT,
    uf TEXT,
    modalidade TEXT CHECK(modalidade IN ('PREGÃO', 'TOMADA_PRECO', 'CONCORRENCIA', 'CONVITE', 'CONCURSO', 'LEILAO', 'RDC', 'DISPENSA', 'INEXIGIBILIDADE')),
    tipo TEXT CHECK(tipo IN ('MENOR_PRECO', 'MELHOR_TECNICA', 'TECNICA_PRECO', 'MAIOR_LANCE', 'MAIOR_DESCONTO')),
    objeto TEXT NOT NULL,
    descricao TEXT,
    valor_estimado REAL,
    valor_maximo REAL,
    data_publicacao DATE,
    data_abertura DATE,
    data_fim_recurso DATE,
    prazo_execucao TEXT,
    cnpj_orgao TEXT,
    codigo TEXT UNIQUE,
    fonte TEXT,
    url_edital TEXT,
    url_pncp TEXT,
    status TEXT DEFAULT 'ABERTA' CHECK(status IN ('ABERTA', 'EM_ANDAMENTO', 'ANALISE', 'HOMOLOGADA', 'ADJUDICADA', 'DESERTA', 'FRACASSADA', 'CANCELADA', 'SUSPENSA', 'FINALIZADA')),
    tem_anexo INTEGER DEFAULT 0,
    anexos TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- OPORTUNIDADES (Match cliente x licitacao)
-- ============================================================
CREATE TABLE IF NOT EXISTS oportunidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    licitacao_id INTEGER NOT NULL,
    cliente_id INTEGER,
    score REAL DEFAULT 0 CHECK(score >= 0 AND score <= 100),
    afinidade TEXT CHECK(afinidade IN ('ALTA', 'MEDIA', 'BAIXA', 'NENHUMA')),
    motivo TEXT,
    status TEXT DEFAULT 'PENDENTE' CHECK(status IN ('PENDENTE', 'NOTIFICADO', 'INTERESSADO', 'PROPOSTA_ENVIADA', 'VENCEDORA', 'PERDEDORA', 'DESISTENCIA', 'FINALIZADA')),
    valor_proposta REAL,
    comissao_percentual REAL DEFAULT 5 CHECK(comissao_percentual >= 1 AND comissao_percentual <= 10),
    comissao_estimada REAL DEFAULT 0,
    comissao_recebida REAL DEFAULT 0,
    data_notificacao TIMESTAMP,
    data_proposta TIMESTAMP,
    data_resultado TIMESTAMP,
    observacoes TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (licitacao_id) REFERENCES licitacoes(id) ON DELETE CASCADE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE SET NULL
);

-- ============================================================
-- PROPOSTAS
-- ============================================================
CREATE TABLE IF NOT EXISTS propostas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    oportunidade_id INTEGER NOT NULL,
    cliente_id INTEGER,
    numero_proposta TEXT UNIQUE,
    valor REAL,
    prazo_dias INTEGER,
    validade_dias INTEGER DEFAULT 30,
    documento TEXT,
    status TEXT DEFAULT 'RASCUNHO' CHECK(status IN ('RASCUNHO', 'ENVIADA', 'ACEITA', 'REJEITADA', 'REVISAO')),
    data_envio TIMESTAMP,
    data_resposta TIMESTAMP,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (oportunidade_id) REFERENCES oportunidades(id) ON DELETE CASCADE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE SET NULL
);

-- ============================================================
-- ITENS DA PROPOSTA
-- ============================================================
CREATE TABLE IF NOT EXISTS itens_proposta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proposta_id INTEGER NOT NULL,
    descricao TEXT NOT NULL,
    quantidade REAL DEFAULT 1,
    valor_unitario REAL,
    valor_total REAL,
    observacao TEXT,
    FOREIGN KEY (proposta_id) REFERENCES propostas(id) ON DELETE CASCADE
);

-- ============================================================
-- COMISSOES
-- ============================================================
CREATE TABLE IF NOT EXISTS comissoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    oportunidade_id INTEGER NOT NULL,
    cliente_id INTEGER,
    valor_contrato REAL NOT NULL,
    percentual REAL NOT NULL CHECK(percentual >= 1 AND percentual <= 10),
    valor_comissao REAL NOT NULL,
    tipo TEXT DEFAULT 'UNICA' CHECK(tipo IN ('UNICA', 'MENSAL', 'ANUAL', 'RECORRENTE')),
    status TEXT DEFAULT 'A_RECEBER' CHECK(status IN ('A_RECEBER', 'RECEBIDA', 'ATRASADA', 'CANCELADA')),
    data_vencimento DATE,
    data_recebimento DATE,
    forma_pagamento TEXT,
    observacoes TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (oportunidade_id) REFERENCES oportunidades(id) ON DELETE CASCADE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE SET NULL
);

-- ============================================================
-- PAGAMENTOS RECEBIDOS
-- ============================================================
CREATE TABLE IF NOT EXISTS pagamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comissao_id INTEGER NOT NULL,
    valor REAL NOT NULL,
    data_pagamento DATE,
    metodo TEXT CHECK(metodo IN ('PIX', 'TED', 'BOLETO', 'DINHEIRO', 'OUTRO')),
    comprovante TEXT,
    observacoes TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (comissao_id) REFERENCES comissoes(id) ON DELETE CASCADE
);

-- ============================================================
-- NOTIFICACOES (WhatsApp, Email)
-- ============================================================
CREATE TABLE IF NOT EXISTS notificacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    oportunidade_id INTEGER,
    tipo TEXT CHECK(tipo IN ('WHATSAPP', 'EMAIL', 'SMS', 'SISTEMA')),
    titulo TEXT,
    mensagem TEXT,
    status TEXT DEFAULT 'PENDENTE' CHECK(status IN ('PENDENTE', 'ENVIADA', 'ERRO', 'LIDA')),
    data_envio TIMESTAMP,
    data_leitura TIMESTAMP,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE SET NULL,
    FOREIGN KEY (oportunidade_id) REFERENCES oportunidades(id) ON DELETE SET NULL
);

-- ============================================================
-- LOG DE ATIVIDADES
-- ============================================================
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT CHECK(tipo IN ('INFO', 'SUCESSO', 'AVISO', 'ERRO', 'CRITICO')),
    modulo TEXT,
    acao TEXT,
    descricao TEXT,
    detalhes TEXT,
    ip TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- CONFIGURACOES DO SISTEMA
-- ============================================================
CREATE TABLE IF NOT EXISTS configuracoes (
    chave TEXT PRIMARY KEY,
    valor TEXT,
    tipo TEXT DEFAULT 'TEXTO' CHECK(tipo IN ('TEXTO', 'NUMERO', 'BOOLEANO', 'JSON', 'LISTA')),
    descricao TEXT,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- INDICES
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_licitacoes_status ON licitacoes(status);
CREATE INDEX IF NOT EXISTS idx_licitacoes_data ON licitacoes(data_abertura);
CREATE INDEX IF NOT EXISTS idx_licitacoes_objeto ON licitacoes(objeto);
CREATE INDEX IF NOT EXISTS idx_oportunidades_score ON oportunidades(score DESC);
CREATE INDEX IF NOT EXISTS idx_oportunidades_status ON oportunidades(status);
CREATE INDEX IF NOT EXISTS idx_clientes_ativo ON clientes(ativo);
CREATE INDEX IF NOT EXISTS idx_comissoes_status ON comissoes(status);
CREATE INDEX IF NOT EXISTS idx_notificacoes_status ON notificacoes(status);
CREATE INDEX IF NOT EXISTS idx_logs_tipo ON logs(tipo);
CREATE INDEX IF NOT EXISTS idx_logs_data ON logs(criado_em);