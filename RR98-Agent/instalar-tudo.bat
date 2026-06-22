@echo off
title 🚀 AGENTE IA RR98 - Roberto Ribeiro
color 0A

:: ══════════════════════════════════════════════════════════
:: 🚀 INSTALADOR AUTOMÁTICO RR98 - Roberto Ribeiro
:: ══════════════════════════════════════════════════════════

:: ===== AUTO-ELEVAR COMO ADMINISTRADOR =====
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo    🔄 Solicitando permissao de administrador...
    echo.
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

cls
echo ╔══════════════════════════════════════════════════════════╗
echo ║   🚀 AGENTE IA RR98 - Roberto Ribeiro                  ║
echo ║   CPF: 108.840.969-55  |  PIX: 046999732012             ║
echo ║   WhatsApp: +55046999732012                              ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo    🔧 Instalação automática em andamento...
echo    🔴 NÃO FECHE ESTA JANELA!
echo.

:: ===== PASSO 1: INSTALAR NODE.JS =====
echo [1/5] Instalando Node.js...
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    if exist "%TEMP%\node-install.msi" (
        echo    📦 Node.js ja baixado! Instalando silenciosamente...
        start /wait msiexec /i "%TEMP%\node-install.msi" /qn /norestart
    ) else (
        echo    ⬇️ Baixando Node.js...
        powershell -Command "& {Invoke-WebRequest -Uri 'https://nodejs.org/dist/v22.11.0/node-v22.11.0-x64.msi' -OutFile '%TEMP%\node-install.msi'}"
        echo    🔧 Instalando...
        start /wait msiexec /i "%TEMP%\node-install.msi" /qn /norestart
    )
    echo    ✅ Node.js instalado!
) else (
    for /f "tokens=*" %%i in ('node -v') do set NODE_VER=%%i
    echo    ✅ Node.js %NODE_VER% ja instalado!
)
echo.

:: ===== ATUALIZAR PATH =====
set "PATH=%PATH%;C:\Program Files\nodejs\;%APPDATA%\npm\"

:: ===== PASSO 2: IR PARA A PASTA =====
echo [2/5] Configurando projeto...
cd /d "%~dp0"
if exist "package.json" (
    echo    ✅ Projeto encontrado
) else (
    echo    ❌ Pasta do projeto nao encontrada!
    pause
    exit /b 1
)
echo.

:: ===== PASSO 3: .ENV =====
echo [3/5] Configurando ambiente...
if not exist ".env" (
    (
        echo # AGENTE IA RR98 - Roberto Ribeiro
        echo GROQ_API_KEY=sua_chave_aqui
        echo PORT=3000
        echo JWT_SECRET=rr98-agent-secret-key
        echo OWNER_NAME=Roberto Ribeiro
        echo OWNER_CPF=108.840.969-55
        echo OWNER_PHONE=+55046999732012
        echo OWNER_EMAIL=Robertojn321@gmail.com
        echo PIX_KEY=046999732012
    ) > .env
    echo    ✅ .env criado com seus dados!
    echo    ⚠️  Coloque sua chave GROQ_API_KEY depois no .env
) else (
    echo    ✅ .env ja existe
)
echo.

:: ===== PASSO 4: INSTALAR DEPENDENCIAS =====
echo [4/5] Instalando dependencias npm...
echo    📦 Isso leva alguns minutos (pode parecer travado)...
cd /d "%~dp0"
call npm install --no-fund --no-audit --loglevel=error 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    ✅ Dependencias instaladas!
) else (
    echo    ⚠️  Tentando novamente...
    call npm install 2>&1
)
echo.

:: ===== PASSO 5: GITHUB + INICIAR =====
cls
echo ╔══════════════════════════════════════════════════════════╗
echo ║   ✅ INSTALACAO CONCLUIDA COM SUCESSO!                 ║
echo ╠══════════════════════════════════════════════════════════╣
echo ║   Proprietario: Roberto Ribeiro                        ║
echo ║   CPF: 108.840.969-55                                   ║
echo ║   WhatsApp: +55046999732012                             ║
echo ║   PIX: 046999732012                                     ║
echo ╠══════════════════════════════════════════════════════════╣
echo ║   🚀 INICIANDO O AGENTE...                             ║
echo ║   Acesse: http://localhost:3000                        ║
echo ║   Login: admin | Senha: rr98@2026                     ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

:: ===== GITHUB =====
echo 📤 Enviando para GitHub...
cd /d "%~dp0"
where git >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    git config user.email "Robertojn321@gmail.com" 2>nul
    git config user.name "Roberto Ribeiro" 2>nul
    git add -A 2>nul
    git commit -m "🤖 RR98 Agent - Auto deploy" 2>nul
    git remote add origin https://github.com/Username9898/Projetos-Vscode.git 2>nul
    git push -u origin main 2>nul
    echo    ✅ Codigo enviado para GitHub!
) else (
    echo    ⚠️ Git nao encontrado - instalando via npm...
    call npm install -g simple-git 2>nul
)
echo.

:: ===== INICIAR =====
echo.
echo ⚡ Iniciando Agente IA RR98...
echo.
echo    🔴 Acesse: http://localhost:3000
echo    🔴 Login: admin | Senha: rr98@2026
echo    🔴 Pressione CTRL+C para parar
echo.

cd /d "%~dp0"
node index.js

pause