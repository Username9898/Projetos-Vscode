@echo off
title 🚀 AGENTE IA RR98 - Roberto Ribeiro
color 0A
cls

echo ╔══════════════════════════════════════════════════════════╗
echo ║   🚀 AGENTE IA RR98 - Roberto Ribeiro                  ║
echo ║   CPF: 108.840.969-55  |  PIX: 046999732012             ║
echo ║   WhatsApp: +55046999732012                              ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

:: ===== VERIFICAR NODE.JS =====
echo [1/5] Verificando Node.js...
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo    ❌ Node.js NAO ENCONTRADO!
    echo.
    echo    📥 Para instalar, acesse: https://nodejs.org
    echo    📦 Baixe a versao LTS e instale (Next, Next, Install)
    echo.
    echo    🔗 Abrindo site do Node.js...
    start https://nodejs.org
    echo.
    echo    ⏸️  APOS INSTALAR, execute este script NOVAMENTE.
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node -v') do set NODE_VER=%%i
echo    ✅ Node.js %NODE_VER% encontrado!
echo.

:: ===== IR PARA PASTA =====
echo [2/5] Localizando projeto...
cd /d "%~dp0"
echo    📁 %cd%
echo.

:: ===== CONFIGURAR .ENV =====
echo [3/5] Configurando ambiente...
if not exist ".env" (
    echo    🔑 Criando arquivo .env com seus dados...
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
    echo    ✅ .env criado!
    echo    ⚠️  Lembre-se de colocar sua chave GROQ_API_KEY no arquivo .env
) else (
    echo    ✅ .env ja existe
)
echo.

:: ===== INSTALAR DEPENDENCIAS =====
echo [4/5] Instalando dependencias...
echo    📦 npm install...
call npm install --no-fund --no-audit --loglevel=error 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    ✅ Dependencias instaladas!
) else (
    echo    ⚠️  Tentando novamente...
    call npm install 2>&1
)
echo.

:: ===== INICIAR =====
cls
echo ╔══════════════════════════════════════════════════════════╗
echo ║   ✅ SISTEMA PRONTO!                                    ║
echo ╠══════════════════════════════════════════════════════════╣
echo ║                                                        ║
echo ║   Proprietario: Roberto Ribeiro                        ║
echo ║   WhatsApp: +55046999732012                             ║
echo ║   PIX: 046999732012                                     ║
echo ║                                                        ║
echo ╠══════════════════════════════════════════════════════════╣
echo ║   🚀 INICIANDO O AGENTE RR98...                       ║
echo ║                                                        ║
echo ║   Acesse: http://localhost:3000                        ║
echo ║   Login: admin                                         ║
echo ║   Senha: rr98@2026                                     ║
echo ║                                                        ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

:: ===== GITHUB SYNC =====
echo 📤 Enviando para GitHub...
where git >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    git config user.email "Robertojn321@gmail.com" 2>nul
    git config user.name "Roberto Ribeiro" 2>nul
    git add -A 2>nul
    git commit -m "🤖 RR98 Agent - Auto update" 2>nul
    git remote add origin https://github.com/Username9898/Projetos-Vscode.git 2>nul
    git push -u origin main 2>nul
    echo    ✅ GitHub atualizado!
) else (
    echo    ⚠️ Git nao encontrado
)
echo.

:: ===== RODAR =====
echo ⚡ node index.js
echo.
echo    🔴 Pressione CTRL+C para parar o servidor
echo.
node index.js

pause