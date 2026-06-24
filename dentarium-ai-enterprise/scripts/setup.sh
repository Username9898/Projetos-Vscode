#!/bin/bash
# Setup script para Dentarium AI Enterprise
# Autor: Roberto Ribeiro

set -e

echo "=========================================="
echo "Dentarium AI Enterprise - Setup"
echo "=========================================="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar pré-requisitos
check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 encontrado"
        return 0
    } else
        echo -e "${RED}✗${NC} $1 não encontrado"
        return 1
    fi
}

echo "Verificando pré-requisitos..."
check_command "docker"
check_command "docker-compose"
check_command "python3"
check_command "node"
check_command "npm"

echo ""
echo "Configurando variáveis de ambiente..."

# Backend
if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo -e "${GREEN}✓${NC} backend/.env criado"
else
    echo -e "${YELLOW}!${NC} backend/.env já existe"
fi

# Frontend
if [ ! -f frontend/.env.local ]; then
    cp frontend/.env.example frontend/.env.local
    echo -e "${GREEN}✓${NC} frontend/.env.local criado"
else
    echo -e "${YELLOW}!${NC} frontend/.env.local já existe"
fi

echo ""
echo "Criando diretórios necessários..."
mkdir -p logs temp uploads backups

echo ""
echo "Instalando dependências..."
echo "Backend (Poetry)..."
cd backend
if command -v poetry &> /dev/null; then
    poetry install
else
    echo -e "${RED}✗${NC} Poetry não encontrado. Instale manualmente."
fi
cd ..

echo ""
echo "Frontend (npm)..."
cd frontend
npm install
cd ..

echo ""
echo "=========================================="
echo -e "${GREEN}Setup concluído com sucesso!${NC}"
echo "=========================================="
echo ""
echo "Próximos passos:"
echo "1. Revise as variáveis de ambiente em backend/.env e frontend/.env.local"
echo "2. Execute: docker-compose up -d"
echo "3. Acesse: http://localhost:3000"
echo ""
echo "Para mais informações, consulte o README.md"