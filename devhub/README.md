# DevHub - Hub Central de Projetos

![Status](https://img.shields.io/badge/Status-Online-success.svg)
![Auto-Update](https://img.shields.io/badge/Auto--Update-Ativo-green.svg)
![GitHub](https://img.shields.io/badge/GitHub-Username9898-black.svg)

**Hub central que lista automaticamente todos os projetos do GitHub de Roberto Ribeiro**

---

## Sobre

Projeto que funciona como **hub central** conectando automaticamente a todos os repositórios públicos do GitHub. Lista projetos em tempo real, detecta novos projetos automaticamente e gera arquivos `.bat` para executar cada projeto com um clique.

### Funcionalidades

- 🔄 **Auto-sync** - Busca projetos diretamente da API do GitHub
- 📦 **Lista dinâmica** - Novos projetos aparecem automaticamente
- ⬇️ **Download .BAT** - Um clique para baixar script de execução
- 🚀 **Setup automático** - Instala dependências e abre projeto
- 📊 **Estatísticas** - Stars, forks e data de atualização

---

## Como Funciona

1. **Busca automática** na API do GitHub
2. **Filtra** repositórios válidos (não-forks)
3. **Classifica** por tipo: Docker, Node.js ou Python
4. **Gera** arquivos `.bat` personalizados para cada projeto

### Tipos de Projeto Suportados

- 🐳 **Docker** - `docker-compose up -d`
- 📦 **Node.js** - `npm install && npm start`
- 🐍 **Python** - `pip install -r requirements.txt && python main.py`

---

## Estrutura

```
devhub/
├── index.html              # Página principal (single-file)
├── README.md               # Documentação
└── .github/workflows/      # CI/CD (opcional)
```

---

## Como Usar

### Online (GitHub Pages)

1. Acesse: https://username9898.github.io/devhub/
2. Veja todos os projetos automaticamente
3. Clique em qualquer projeto
4. Baixe o `.bat` correspondente
5. Execute no Windows

### Local

```bash
# Clone ou baixe
git clone https://github.com/Username9898/devhub.git
cd devhub

# Abra no navegador
start index.html
# Ou
python -m http.server 8080
# Acesse: http://localhost:8080
```

---

## GitHub Actions (Deploy Automático)

### Workflow: `.github/workflows/deploy.yml`

```yaml
name: Deploy DevHub

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - uses: actions/deploy-pages@v4
```

### Deploy Manual

1. Vá em **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: **main**
4. Salve

---

## Funcionalidades do .BAT

### Docker Compose Projects

```batch
@echo off
chcp 65001 >nul
echo ========================================
echo Nome do Projeto
echo ========================================

echo 📦 Verificando Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker não encontrado!
    pause
    exit /b 1
)

echo 🔍 Verificando containers...
cd "nome-do-projeto"
docker-compose up -d

echo ✅ Projeto iniciado!
echo 🌐 Acesse: http://localhost:3000
echo.
echo Para parar: docker-compose down
pause
```

### Node.js Projects

```batch
@echo off
chcp 65001 >nul
echo 📦 Verificando Node.js...

node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js não encontrado!
    pause
    exit /b 1
)

echo 📥 Instalando dependências...
cd "nome-do-projeto"
npm install

echo 🚀 Iniciando servidor...
echo 🌐 Acesse: http://localhost:3000
npm start
```

### Python Projects

```batch
@echo off
chcp 65001 >nul
echo 🐍 Verificando Python...

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    pause
    exit /b 1
)

echo 📥 Instalando dependências...
cd "nome-do-projeto"
pip install -r requirements.txt

echo 🚀 Iniciando projeto...
echo 🌐 Acesse: http://localhost:8000
python main.py
```

---

## Adicionar Novos Projetos

### Automático (Recomendado)

Basta criar um novo repositório no GitHub. O DevHub detecta automaticamente em até 10 minutos.

### Manual (Editar `index.html`)

Na seção `PROJECTS_DATA`:

```javascript
const PROJECTS = [
    {
        id: 'nome-do-repo',
        name: 'Nome do Projeto',
        description: 'Descrição curta',
        url: 'https://github.com/Username9898/nome-do-repo',
        type: 'docker' // ou 'node' ou 'python'
    }
];
```

---

## Integração com GitHub API

### Rate Limit

- **Não autenticado:** 60 requisições/hora
- **Autenticado:** 5.000 requisições/hora

Para aumentar limite, adicione token:

```javascript
const response = await fetch(
    `https://api.github.com/users/${GITHUB_USERNAME}/repos`,
    {
        headers: {
            'Authorization': 'token SEU_TOKEN_AQUI'
        }
    }
);
```

### Obter Token

1. Vá em https://github.com/settings/tokens
2. **Generate new token (classic)**
3. Selecione: `public_repo`
4. Copie o token

---

## Personalização

### Alterar usuário do GitHub

```javascript
// Linha ~150
const GITHUB_USERNAME = 'Username9898';
```

### Cores do tema

```javascript
// No CSS
.gradient-primary { 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
}
```

### Adicionar novos tipos de projeto

Edite a função `generateBatFile()` no JavaScript.

---

## Deploy no GitHub Pages

### Passo a Passo

1. **Criar repositório:**
   ```
   Nome: devhub
   ```

2. **Subir código:**
   ```bash
   cd devhub
   git init
   git add .
   git commit -m "Initial commit: DevHub"
   git branch -M main
   git remote add origin https://github.com/Username9898/devhub.git
   git push -u origin main
   ```

3. **Ativar Pages:**
   - Settings → Pages
   - Source: Deploy from branch
   - Branch: main
   - Save

4. **Pronto!**
   - https://username9898.github.io/devhub/

---

## Tecnologias

- **HTML5** + **Tailwind CSS** (CDN)
- **JavaScript ES6+** (Vanilla)
- **Font Awesome** (Ícones)
- **GitHub API** (Busca de repositórios)
- **GitHub Actions** (CI/CD)
- **GitHub Pages** (Hosting)

---

## Próximos Passos

- [ ] Sistema de favoritos
- [ ] Filtros por linguagem
- [ ] Busca por nome
- [ ] Ordenação customizada
- [ ] Temas (dark/light)
- [ ] Estatísticas avançadas
- [ ] Integração com README.md de cada projeto
- [ ] Preview de código

---

## Contato

**Roberto Ribeiro**
- GitHub: [@Username9898](https://github.com/Username9898)
- LinkedIn: [roberto-ribeiro9898](https://www.linkedin.com/in/roberto-ribeiro9898)
- Email: robertojn321@gmail.com

---

## Licença

Este projeto é open source. Veja [LICENSE.txt](../LICENSE.txt).

**Última atualização:** Janeiro 2025  
**Versão:** 1.0.0