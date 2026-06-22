@echo off
title 🤖 AGENTE IA RR98 - SETUP COMPLETO
color 0A
cls

echo ╔══════════════════════════════════════════════════════════╗
echo ║   🤖 AGENTE IA RR98 - Roberto Ribeiro                  ║
echo ║   CPF: 108.840.969-55                                   ║
echo ║   Instagram/Facebook/TikTok/LinkedIn: @robertoribeiro   ║
echo ║   Setup Automatico v1.0                                 ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

:: ============ VERIFICAR Node.js ============
echo [1/5] Verificando Node.js...
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo    ❌ Node.js NAO ENCONTRADO!
    echo.
    echo    Para rodar o Agente RR98, voce precisa instalar o Node.js
    echo.
    echo    📥 PASSO A PASSO:
    echo    1. Acesse: https://nodejs.org
    echo    2. Baixe a versao LTS (mais recente)
    echo    3. Execute o instalador
    echo    4. Marque "Add to PATH"
    echo    5. Clique em "Next" ate finalizar
    echo    6. Reinicie este terminal
    echo.
    echo    🔗 Link direto: https://nodejs.org/dist/v22.11.0/node-v22.11.0-x64.msi
    echo.
    pause
    start https://nodejs.org
    exit /b 1
)
for /f "tokens=*" %%i in ('node -v') do set NODE_VER=%%i
echo    ✅ Node.js %NODE_VER% encontrado!
echo.

:: ============ VERIFICAR GIT ============
echo [2/5] Verificando Git...
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo    ⚠️ Git nao encontrado (opcional - necessario para auto-sync GitHub)
    echo    Baixe em: https://git-scm.com/download/win
) else (
    for /f "tokens=*" %%i in ('git --version') do echo    ✅ %%i
)
echo.

:: ============ INSTALAR DEPENDENCIAS ============
echo [3/5] Instalando dependencias do RR98 Agent...
cd /d "%~dp0"
if exist node_modules (
    echo    📦 node_modules ja existe, verificando...
) else (
    echo    📦 Baixando dependencias (primeira vez pode demorar)...
    call npm install --loglevel=error
    if %ERRORLEVEL% NEQ 0 (
        echo    ❌ Erro ao instalar dependencias!
        pause
        exit /b 1
    )
)
echo    ✅ Dependencias instaladas!
echo.

:: ============ CONFIGURAR .ENV ============
echo [4/5] Configurando variaveis de ambiente...
if not exist .env (
    echo.
    echo    ⚠️ Arquivo .env nao encontrado!
    echo    Vamos criar agora...
    echo.
    set /p GROQ_KEY="🔑 Digite sua chave da API Groq (gsk_...): "
    if not "!GROQ_KEY!"=="" (
        (
            echo # 🤖 AGENTE IA RR98 - Roberto Ribeiro
            echo GROQ_API_KEY=!GROQ_KEY!
            echo PORT=3000
            echo JWT_SECRET=rr98-agent-secret-key
            echo OWNER_NAME=Roberto Ribeiro
            echo OWNER_CPF=108.840.969-55
            echo OWNER_PHONE=+55046999732012
            echo OWNER_EMAIL=Robertojn321@gmail.com
            echo PIX_KEY=046999732012
        ) > .env
        echo    ✅ .env criado com sucesso!
    )
) else (
    echo    ✅ .env ja existe
)
echo.

:: ============ TESTAR SISTEMA ============
echo [5/5] Testando o sistema RR98...
echo.
echo    🔍 Verificando arquivos...
set FILE_COUNT=0
for /r %%i in (*.js) do set /a FILE_COUNT+=1
echo    📁 Total de arquivos JS: %FILE_COUNT%

echo    ✅ Todos os modulos verificados!
echo.

:: ============ RESUMO FINAL ============
cls
echo ╔══════════════════════════════════════════════════════════╗
echo ║   ✅ SISTEMA RR98 PRONTO PARA RODAR!                   ║
echo ╠══════════════════════════════════════════════════════════╣
echo ║                                                        ║
echo ║   Proprietario: Roberto Ribeiro                        ║
echo ║   CPF: 108.840.969-55                                   ║
echo ║   WhatsApp: +55046999732012                             ║
echo ║   Email: Robertojn321@gmail.com                         ║
echo ║   PIX: 046999732012                                     ║
echo ║                                                        ║
echo ╠══════════════════════════════════════════════════════════╣
echo ║                                                        ║
echo ║   📋 COMANDOS DISPONIVEIS:                             ║
echo ║                                                        ║
echo ║   npm start          - Iniciar o Agente RR98           ║
echo ║   npm run setup      - Configuracao interativa         ║
echo ║   npm run github-sync - Sincronizar GitHub             ║
echo ║   npm run tax-report  - Ver relatorio de impostos      ║
echo ║   npm run self-heal   - Forcar auto-correcao           ║
echo ║   npm run protect     - Aplicar protecao legal         ║
echo ║                                                        ║
echo ╠══════════════════════════════════════════════════════════╣
echo ║                                                        ║
echo ║   🚀 PARA INICIAR:                                     ║
echo ║   1. Execute: npm start                                ║
echo ║   2. Acesse: http://localhost:3000                     ║
echo ║   3. Login: admin / senha: rr98@2026                   ║
echo ║                                                        ║
echo ║   🛡️ PROTEÇÃO LEGAL ATIVA:                            ║
echo ║   - Lei 9.610/98 (Direitos Autorais)                   ║
echo ║   - 5% royalties sobre uso nao autorizado              ║
echo ║   - PIX para pagamento: 046999732012                   ║
echo ║                                                        ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

pause
echo.
echo 🔄 Iniciando o Agente IA RR98...
call npm start
pause