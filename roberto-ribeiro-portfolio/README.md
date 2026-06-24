# Roberto Ribeiro - Portfolio Pessoal

![Status](https://img.shields.io/badge/Status-Ativo-success.svg)
![Auto-Update](https://img.shields.io/badge/Auto--Update-Enabled-green.svg)
![GitHub](https://img.shields.io/badge/GitHub-Username9898-black.svg)

**Desenvolvedor Full Stack & Arquiteto de Soluções**

---

## 📋 Sobre

Portfolio pessoal automatizado que exibe projetos, habilidades e informações de contato. Auto-atualiza via GitHub Actions quando novos projetos são adicionados.

### Funcionalidades

- ✅ **Auto-atualização** - Detecta novos projetos automaticamente
- ✅ **Instruções de setup** - Passo a passo para cada projeto
- ✅ **Design moderno** - Interface clean e responsiva
- ✅ **GitHub Pages** - Deploy automático
- ✅ **Multi idioma** - Preparado para internacionalização

---

## 🚀 Tecnologias

- **HTML5** + **Tailwind CSS** (via CDN)
- **JavaScript ES6+** (vanilla)
- **Font Awesome** (ícones)
- **GitHub Actions** (CI/CD)
- **GitHub Pages** (hosting)

---

## 📦 Estrutura

```
roberto-ribeiro-portfolio/
├── index.html                   # Página principal (single-page)
├── README.md                    # Esta página
├── .gitignore                   # Ignorar arquivos desnecessários
└── .github/
    └── workflows/
        └── deploy.yml           # Auto-deploy no GitHub Pages
```

---

## 🎨 Customização

### Informações Pessoais

Edite o arquivo `index.html`:

**Linha ~470 - Configurações:**
```javascript
const GITHUB_USERNAME = 'Username9898';
```

**Links e contatos:**
- GitHub: https://github.com/Username9898
- LinkedIn: https://www.linkedin.com/in/roberto-ribeiro9898
- Email: robertojn321@gmail.com

### Adicionar Projetos

Na seção `PROJECTS_DATA` (linha ~490):

```javascript
{
    id: 'nome-do-projeto',
    name: 'Nome do Projeto',
    description: 'Descrição curta',
    longDescription: 'Descrição detalhada',
    tech: ['Tech1', 'Tech2'],
    stars: 0,
    forks: 0,
    featured: true,
    setupSteps: [
        'Passo 1',
        'Passo 2',
        'Passo 3'
    ]
}
```

---

## 🔄 Auto-Atualização

### Como Funciona

1. **GitHub Actions** monitora mudanças no repositório
2. Quando você push código, o workflow é triggerado
3. O site é rebuild e deploy automaticamente no GitHub Pages
4. O JavaScript no frontend verifica atualizações a cada 5 minutos

### GitHub Actions Workflow

Criado em `.github/workflows/deploy.yml` - deploy automático a cada push.

---

## 🚀 Deploy no GitHub Pages

### Passo a Passo

1. **Criar repositório:**
   ```
   Nome: username9898.github.io (substitua username9898 pelo seu usuário)
   OU
   Nome: portfolio (qualquer nome)
   ```

2. **Subir código:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Portfolio pessoal"
   git branch -M main
   git remote add origin https://github.com/Username9898/roberto-ribeiro-portfolio.git
   git push -u origin main
   ```

3. **Ativar GitHub Pages:**
   - Vá em Settings → Pages
   - Source: Deploy from a branch
   - Branch: main / root
   - Clique em Save

4. **Pronto!**
   - Acesse: https://username9898.github.io/roberto-ribeiro-portfolio/

---

## 🔧 Manutenção

### Adicionar Novo Projeto

1. Edite `index.html`
2. Adicione o projeto na lista `PROJECTS_DATA`
3. Commit e push:
   ```bash
   git add .
   git commit -m "Add: Novo Projeto X"
   git push
   ```
4. GitHub Actions deplota automaticamente

### Atualizar Informações Pessoais

```bash
# Edite index.html
git add .
git commit -m "Update: Informações pessoais"
git push
```

### Modificar Setup Steps

Cada projeto pode ter suas próprias instruções:

```javascript
setupSteps: [
    'Clone: git clone https://github.com/Username9898/projeto.git',
    'Entre na pasta: cd projeto',
    'Instale dependências: npm install',
    'Configure variáveis: cp .env.example .env',
    'Rode o projeto: npm start'
]
```

---

## 📱 Funcionalidades

### Para Visitantes

- 🔍 **Ver projetos** com cards interativos
- 📊 **Estatísticas** (stars, forks, commits)
- 🚀 **Passo a passo** de como rodar cada projeto
- 🔗 **Links diretos** para GitHub
- 📱 **100% responsivo** (mobile, tablet, desktop)

### Para Você (Admin)

- ✅ Auto-sync com GitHub
- ✅ Deploy automático
- ✅ Atualização sem esforço
- ✅ Centralização de portfólio

---

## 🎯 Próximos Passos

- [ ] Integração real com GitHub API (buscar stats automaticamente)
- [ ] Sistema de busca de projetos
- [ ] Filtros por tecnologia
- [ ] Modo escuro/claro
- [ ] Blog integrado
- [ ] Formulário de contato
- [ ] Analytics (Google Analytics)

---

## 📄 Licença

Este projeto é open source. Veja [LICENSE.txt](../LICENSE.txt) para detalhes.

**Autor:** Roberto Ribeiro  
**GitHub:** [@Username9898](https://github.com/Username9898)  
**LinkedIn:** [roberto-ribeiro9898](https://www.linkedin.com/in/roberto-ribeiro9898)  
**Email:** robertojn321@gmail.com

---

**Última atualização:** Janeiro 2025  
**Versão:** 1.0.0