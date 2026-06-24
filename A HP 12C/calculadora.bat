@echo off
chcp 65001 >nul
title HP 12C - Calculadora Financeira
color 0a
cls

echo.
echo   Iniciando HP-12C Calculadora Financeira...
echo.
python "%~dp0calculadora_financeira.py"

if %errorlevel% neq 0 (
    echo.
    echo   ERRO: Nao foi possivel executar o Python.
    echo   Verifique se o Python esta instalado.
    echo.
    pause
)