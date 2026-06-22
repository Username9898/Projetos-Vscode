-- ============================================
-- DevAgent Hub - Database Schema for Supabase
-- Execute este SQL no SQL Editor do Supabase
-- ============================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- Tabela: projects
-- ============================================
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome TEXT NOT NULL,
    descricao TEXT,
    status TEXT DEFAULT 'ativo' CHECK (status IN ('ativo', 'pausado', 'concluido', 'arquivado')),
    tecnologias TEXT,
    link TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

-- Create policy for public access (for demo purposes)
CREATE POLICY "Public access for projects" ON projects
    FOR ALL USING (true);

-- ============================================
-- Tabela: tasks
-- ============================================
CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    titulo TEXT NOT NULL,
    descricao TEXT,
    status TEXT DEFAULT 'todo' CHECK (status IN ('todo', 'doing', 'done')),
    prioridade TEXT DEFAULT 'media' CHECK (prioridade IN ('baixa', 'media', 'alta')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public access for tasks" ON tasks
    FOR ALL USING (true);

-- ============================================
-- Tabela: prompts
-- ============================================
CREATE TABLE IF NOT EXISTS prompts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    titulo TEXT NOT NULL,
    conteudo TEXT NOT NULL,
    categoria TEXT DEFAULT 'desenvolvimento' CHECK (categoria IN ('desenvolvimento', 'arquitetura', 'banco-dados', 'frontend', 'backend', 'deploy')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE prompts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public access for prompts" ON prompts
    FOR ALL USING (true);

-- ============================================
-- Tabela: docs
-- ============================================
CREATE TABLE IF NOT EXISTS docs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    titulo TEXT NOT NULL,
    conteudo TEXT NOT NULL,
    tipo TEXT DEFAULT 'nota' CHECK (tipo IN ('nota', 'tutorial', 'ideia', 'documentacao')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE docs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public access for docs" ON docs
    FOR ALL USING (true);

-- ============================================
-- Create indexes for better performance
-- ============================================
CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
CREATE INDEX IF NOT EXISTS idx_projects_created ON projects(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_created ON tasks(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_prompts_categoria ON prompts(categoria);
CREATE INDEX IF NOT EXISTS idx_prompts_created ON prompts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_docs_tipo ON docs(tipo);
CREATE INDEX IF NOT EXISTS idx_docs_created ON docs(created_at DESC);

-- ============================================
-- Auto-update updated_at trigger function
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to tables with updated_at
CREATE TRIGGER update_projects_updated_at
    BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_docs_updated_at
    BEFORE UPDATE ON docs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- Sample data (opcional)
-- ============================================
-- INSERT INTO projects (nome, descricao, status, tecnologias) VALUES
--     ('Meu Primeiro SaaS', 'Sistema financeiro completo', 'ativo', 'React, Node.js, Supabase'),
--     ('API RESTful', 'API para e-commerce', 'ativo', 'Node.js, Express, PostgreSQL');

-- INSERT INTO tasks (titulo, descricao, status, prioridade) VALUES
--     ('Configurar Supabase', 'Criar projeto e tabelas', 'doing', 'alta'),
--     ('Criar tela de login', 'Implementar autenticação', 'todo', 'media'),
--     ('Documentar API', 'Escrever documentação', 'done', 'baixa');