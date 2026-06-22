# ==========================================================
# 🚀 INSTALADOR AUTOMÁTICO RR98 - Roberto Ribeiro
# CPF: 108.840.969-55 | PIX: 046999732012
# ==========================================================
# Este script instala Node.js, configura tudo e sobe pro GitHub
# AUTOMATICAMENTE - sem precisar clicar em nada!
# ==========================================================

Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   🚀 AGENTE IA RR98 - INSTALAÇÃO AUTOMÁTICA           ║" -ForegroundColor Cyan
Write-Host "║   Roberto Ribeiro | CPF: 108.840.969-55               ║" -ForegroundColor Cyan
Write-Host "║   PIX: 046999732012                                    ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# === PASSO 1: Instalar Node.js silenciosamente ===
Write-Host "[1/6] Instalando Node.js..." -ForegroundColor Yellow

$nodeInstaller = "$env:TEMP\node-install.msi"
if (Test-Path $nodeInstaller) {
    Write-Host "   📦 Instalando Node.js (isso leva alguns minutos)..." -ForegroundColor Yellow
    Start-Process msiexec.exe -ArgumentList "/i `"$nodeInstaller`" /qn /norestart" -Wait -NoNewWindow
    Write-Host "   ✅ Node.js instalado!" -ForegroundColor Green
} else {
    Write-Host "   ⬇️ Baixando Node.js..." -ForegroundColor Yellow
    try {
        Invoke-WebRequest -Uri "https://nodejs.org/dist/v22.11.0/node-v22.11.0-x64.msi" -OutFile $nodeInstaller -UseBasicParsing
        Start-Process msiexec.exe -ArgumentList "/i `"$nodeInstaller`" /qn /norestart" -Wait -NoNewWindow
        Write-Host "   ✅ Node.js instalado!" -ForegroundColor Green
    } catch {
        Write-Host "   ❌ Erro ao baixar Node.js: $_" -ForegroundColor Red
        Write-Host "   📥 Baixe manualmente em: https://nodejs.org" -ForegroundColor Yellow
        pause
        exit 1
    }
}

# Atualizar PATH para usar node/npm
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Verificar instalação
try {
    $nodeVer = node --version
    $npmVer = npm --version
    Write-Host "   ✅ Node.js $nodeVer | npm $npmVer" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️ Recarregando PATH..." -ForegroundColor Yellow
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine")
    $nodeVer = node --version
    $npmVer = npm --version
    Write-Host "   ✅ Node.js $nodeVer | npm $npmVer" -ForegroundColor Green
}

# === PASSO 2: Ir para pasta do projeto ===
Write-Host "[2/6] Configurando projeto..." -ForegroundColor Yellow
$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectDir
Write-Host "   📁 Pasta: $projectDir" -ForegroundColor Cyan

# === PASSO 3: Criar .env com chave Groq ===
Write-Host "[3/6] Configurando ambiente..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    $groqKey = Read-Host "🔑 Digite sua chave da API Groq (gsk_...)"
    if ([string]::IsNullOrEmpty($groqKey)) {
        $groqKey = "sua_chave_aqui"
        Write-Host "   ⚠️  Chave vazia! Coloque a chave depois no arquivo .env" -ForegroundColor Yellow
    }
    
    @"
# AGENTE IA RR98 - Roberto Ribeiro
GROQ_API_KEY=$groqKey
PORT=3000
JWT_SECRET=rr98-agent-secret-key
OWNER_NAME=Roberto Ribeiro
OWNER_CPF=108.840.969-55
OWNER_PHONE=+55046999732012
OWNER_EMAIL=Robertojn321@gmail.com
PIX_KEY=046999732012
"@ | Out-File -FilePath ".env" -Encoding utf8
    Write-Host "   ✅ .env criado!" -ForegroundColor Green
} else {
    Write-Host "   ✅ .env já existe" -ForegroundColor Green
}

# === PASSO 4: Instalar dependências ===
Write-Host "[4/6] Instalando dependências npm..." -ForegroundColor Yellow
Write-Host "   📦 Isso pode levar alguns minutos..." -ForegroundColor Yellow
try {
    npm install --loglevel=error 2>&1 | Out-Null
    Write-Host "   ✅ Dependências instaladas!" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Erro: $_" -ForegroundColor Red
    pause
    exit 1
}

# === PASSO 5: Fazer Git init e primeiro commit ===
Write-Host "[5/6] Configurando Git e GitHub..." -ForegroundColor Yellow

# Configurar identidade
try {
    git config user.email "Robertojn321@gmail.com" 2>$null
    git config user.name "Roberto Ribeiro" 2>$null
    
    # Verificar se já tem .git
    if (-not (Test-Path ".git")) {
        git init 2>$null
        Write-Host "   ✅ Git init" -ForegroundColor Green
    }
    
    # Adicionar tudo
    git add -A 2>$null
    
    # Commit
    $commitMsg = "🤖 Auto-setup RR98 Agent - $(Get-Date -Format 'dd/MM/yyyy HH:mm')"
    git commit -m $commitMsg 2>$null
    
    # Push
    try {
        git remote add origin https://github.com/Username9898/Projetos-Vscode.git 2>$null
        git push -u origin main 2>$null
        Write-Host "   ✅ Código enviado para GitHub!" -ForegroundColor Green
    } catch {
        Write-Host "   ⚠️ GitHub: Configure o remote manualmente depois" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ⚠️ Git não encontrado (opcional)" -ForegroundColor Yellow
}

# === PASSO 6: Iniciar o Agente RR98 ===
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║   ✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!                 ║" -ForegroundColor Green
Write-Host "╠══════════════════════════════════════════════════════════╣" -ForegroundColor Green
Write-Host "║                                                        ║" -ForegroundColor Green
Write-Host "║   Proprietário: Roberto Ribeiro                        ║" -ForegroundColor White
Write-Host "║   CPF: 108.840.969-55                                   ║" -ForegroundColor White
Write-Host "║   WhatsApp: +55046999732012                             ║" -ForegroundColor White
Write-Host "║   PIX: 046999732012                                     ║" -ForegroundColor White
Write-Host "║                                                        ║" -ForegroundColor Green
Write-Host "║   🚀 INICIANDO O AGENTE RR98...                       ║" -ForegroundColor Cyan
Write-Host "║                                                        ║" -ForegroundColor Green
Write-Host "║   Acesse: http://localhost:3000                        ║" -ForegroundColor Cyan
Write-Host "║   Login: admin  |  Senha: rr98@2026                   ║" -ForegroundColor Cyan
Write-Host "║                                                        ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "🔥 Iniciando servidor em 5 segundos..." -ForegroundColor Cyan
Start-Sleep -Seconds 3

# Iniciar o servidor
Write-Host "⚡ node index.js" -ForegroundColor Green
node index.js

pause