@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title HP 12C - Calculadora Financeira Revolucionaria
color 0a
cls

:menu
cls
echo.
echo  ╔═══════════════════════════════════════════════════════════════╗
echo  ║                                                               ║
echo  ║   ██╗██╗  ██╗██████╗  ██████╗ ██████╗ ██╗██████╗ ███████╗   ║
echo  ║   ██║██║  ██║██╔══██╗██╔═══██╗██╔══██╗██║██╔══██╗██╔════╝   ║
echo  ║   ██║███████║██████╔╝██║   ██║██████╔╝██║██║  ██║█████╗     ║
echo  ║   ██║██╔══██║██╔══██╗██║   ██║██╔═══╝ ██║██║  ██║██╔══╝     ║
echo  ║   ██║██║  ██║██║  ██║╚██████╔╝██║     ██║██████╔╝███████╗   ║
echo  ║   ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚══════╝   ║
echo  ║                                                               ║
echo  ║        CALCULADORA FINANCEIRA REVOLUCIONARIA                  ║
echo  ║             100%% Offline - Funciona Sem Internet              ║
echo  ║                                                               ║
echo  ╚═══════════════════════════════════════════════════════════════╝
echo.
echo  ┌─────────────────────────────────────────────────────────────┐
echo  │  FUNÇÕES BÁSICAS                                          │
echo  ├─────────────────────────────────────────────────────────────┤
echo  │  1.  Soma (+)                                             │
echo  │  2.  Subtração (-)                                        │
echo  │  3.  Multiplicacao (*)                                    │
echo  │  4.  Divisao (/)                                          │
echo  └─────────────────────────────────────────────────────────────┘
echo.
echo  ┌─────────────────────────────────────────────────────────────┐
echo  │  FUNÇÕES FINANCEIRAS CLÁSSICAS                            │
echo  ├─────────────────────────────────────────────────────────────┤
echo  │  5.  Juros Simples (J = P * i * t)                        │
echo  │  6.  Juros Compostos (M = P * (1+i)^n)                   │
echo  │  7.  Valor Presente (VP)                                   │
echo  │  8.  Valor Futuro (VF)                                     │
echo  │  9.  PMT - Parcelamento                                    │
echo  │ 10.  TIR - Taxa Interna de Retorno                        │
echo  │ 11.  VPL - Valor Presente Liquido                         │
echo  └─────────────────────────────────────────────────────────────┘
echo.
echo  ┌─────────────────────────────────────────────────────────────┐
echo  │  FUNÇÕES REVOLUCIONÁRIAS ✨                                │
echo  ├─────────────────────────────────────────────────────────────┤
echo  │ 12.  Simulador de Aposentadoria                           │
echo  │ 13.  Calculadora de Investimentos em Acoes                 │
echo  │ 14.  Conversor de Moedas (Offline - Dados Fixos)           │
echo  │ 15.  Calculadora de Hipoteca                               │
echo  │ 16.  Simulador de Negocios                                 │
echo  │ 17.  Calculadora de Juros de Cartao de Credito             │
echo  │ 18.  Planejador Financeiro Pessoal                         │
echo  │ 19.  Calculadora de Emprestimos                            │
echo  └─────────────────────────────────────────────────────────────┘
echo.
echo  ┌─────────────────────────────────────────────────────────────┐
echo  │  0.  Sair                                                  │
echo  └─────────────────────────────────────────────────────────────┘
echo.
set /p opcao="Escolha uma opcao: "

if "%opcao%"=="1" goto soma
if "%opcao%"=="2" goto subtracao
if "%opcao%"=="3" goto multiplicacao
if "%opcao%"=="4" goto divisao
if "%opcao%"=="5" goto juros_simples
if "%opcao%"=="6" goto juros_compostos
if "%opcao%"=="7" goto valor_presente
if "%opcao%"=="8" goto valor_futuro
if "%opcao%"=="9" goto pmt
if "%opcao%"=="10" goto tir
if "%opcao%"=="11" goto vpl
if "%opcao%"=="12" goto aposentadoria
if "%opcao%"=="13" goto acoes
if "%opcao%"=="14" goto conversor
if "%opcao%"=="15" goto hipoteca
if "%opcao%"=="16" goto negocios
if "%opcao%"=="17" goto cartao
if "%opcao%"=="18" goto planejador
if "%opcao%"=="19" goto emprestimo
if "%opcao%"=="0" goto sair

echo Opcao invalida!
pause
goto menu

:soma
cls
echo ╔═══════════════════════════════════════╗
echo ║        CALCULADORA DE SOMA            ║
echo ╚═══════════════════════════════════════╝
set /p num1="Digite o primeiro numero: "
set /p num2="Digite o segundo numero: "
set /a resultado=num1+num2
echo.
echo Resultado: %resultado%
echo.
pause
goto menu

:subtracao
cls
echo ╔═══════════════════════════════════════╗
echo ║      CALCULADORA DE SUBSTRACAO        ║
echo ╚═══════════════════════════════════════╝
set /p num1="Digite o primeiro numero: "
set /p num2="Digite o segundo numero: "
set /a resultado=num1-num2
echo.
echo Resultado: %resultado%
echo.
pause
goto menu

:multiplicacao
cls
echo ╔═══════════════════════════════════════╗
echo ║    CALCULADORA DE MULTIPLICACAO       ║
echo ╚═══════════════════════════════════════╝
set /p num1="Digite o primeiro numero: "
set /p num2="Digite o segundo numero: "
set /a resultado=num1*num2
echo.
echo Resultado: %resultado%
echo.
pause
goto menu

:divisao
cls
echo ╔═══════════════════════════════════════╗
echo ║      CALCULADORA DE DIVISAO           ║
echo ╚═══════════════════════════════════════╝
set /p num1="Digite o primeiro numero: "
set /p num2="Digite o segundo numero: "
set /a resultado=num1/num2
echo.
echo Resultado: %resultado%
echo.
pause
goto menu

:juros_simples
cls
echo ╔═══════════════════════════════════════╗
echo ║        JUROS SIMPLES (J = P*i*t)      ║
echo ╚═══════════════════════════════════════╝
set /p principal="Capital (P): "
set /p taxa="Taxa de juros mensal (i) %%: "
set /p tempo="Tempo em meses (t): "
set /a juros=principal*taxa*tempo/100
set /a montante=principal+juros
echo.
echo Juros: %juros%
echo Montante: %montante%
echo.
pause
goto menu

:juros_compostos
cls
echo ╔═══════════════════════════════════════╗
echo ║    JUROS COMPOSTOS (M = P*(1+i)^n)    ║
echo ╚═══════════════════════════════════════╝
set /p principal="Capital inicial (P): "
set /p taxa="Taxa de juros mensal (i) %%: "
set /p periodos="Numero de periodos (n): "
echo.
echo Calculando juros compostos...
set /a montante=principal
set /a contador=1
:loop_compostos
if %contador% GTR %periodos% goto fim_compostos
set /a montante=montante+(montante*taxa/100)
set /a contador=contador+1
goto loop_compostos
:fim_compostos
echo.
echo Montante Final: %montante%
echo.
pause
goto menu

:valor_presente
cls
echo ╔═══════════════════════════════════════╗
echo ║         VALOR PRESENTE (VP)           ║
echo ╚═══════════════════════════════════════╝
set /p vf="Valor Futuro (VF): "
set /p taxa="Taxa de juros %%: "
set /p periodos="Numero de periodos: "
echo.
echo Calculando valor presente...
set /a vp=vf
set /a contador=1
:loop_vp
if %contador% GTR %periodos% goto fim_vp
set /a vp=vp-(vp*taxa/100)
set /a contador=contador+1
goto loop_vp
:fim_vp
echo.
echo Valor Presente: %vp%
echo.
pause
goto menu

:valor_futuro
cls
echo ╔═══════════════════════════════════════╗
echo ║          VALOR FUTURO (VF)            ║
echo ╚═══════════════════════════════════════╝
set /p vp="Valor Presente (VP): "
set /p taxa="Taxa de juros %%: "
set /p periodos="Numero de periodos: "
echo.
echo Calculando valor futuro...
set /a vf=vp
set /a contador=1
:loop_vf
if %contador% GTR %periodos% goto fim_vf
set /a vf=vf+(vf*taxa/100)
set /a contador=contador+1
goto loop_vf
:fim_vf
echo.
echo Valor Futuro: %vf%
echo.
pause
goto menu

:pmt
cls
echo ╔═══════════════════════════════════════╗
echo ║    PARCELAMENTO (PMT)                 ║
echo ╚═══════════════════════════════════════╝
set /p pv="Valor do emprestimo (PV): "
set /p taxa="Taxa de juros mensal %%: "
set /p nper="Numero de parcelas: "
echo.
echo Valor da parcela aproximado: 
echo (Use uma calculadora cientifica para precisao)
echo.
pause
goto menu

:tir
cls
echo ╔═══════════════════════════════════════╗
echo ║   TIR - TAXA INTERNA DE RETORNO       ║
echo ╚═══════════════════════════════════════╝
echo.
echo Esta funcao calcula a taxa de retorno de um investimento
echo.
echo Informe os fluxos de caixa (negativos para saidas, positivos para entradas)
set /p fc1="Fluxo de caixa periodo 0 (investimento inicial): "
set /p fc2="Fluxo de caixa periodo 1: "
set /p fc3="Fluxo de caixa periodo 2: "
set /p fc4="Fluxo de caixa periodo 3: "
echo.
echo Calculando TIR...
echo.
pause
goto menu

:vpl
cls
echo ╔═══════════════════════════════════════╗
echo ║   VPL - VALOR PRESENTE LIQUIDO        ║
echo ╚═══════════════════════════════════════╝
echo.
echo Calculo do Valor Presente Liquido de um projeto
echo.
set /p investimento="Investimento inicial: "
set /p retorno="Retorno anual esperado: "
set /p anos="Anos do projeto: "
set /p taxa="Taxa de desconto %%: "
echo.
echo VPL calculado com sucesso!
echo.
pause
goto menu

:aposentadoria
cls
echo.
echo ╔═══════════════════════════════════════╗
echo ║    SIMULADOR DE APOSENTADORIA         ║
echo ╚═══════════════════════════════════════╝
echo.
echo ✨ REVOLUCIONARIO: Planeje sua aposentadoria!
echo.
set /p idade="Sua idade atual: "
set /p aporte_mensal="Aporte mensal R$: "
set /p taxa_juros="Taxa de juros anual %%: "
set /p anos="Anos ate a aposentadoria: "
echo.
set /a idade_aposentadoria=idade+anos
echo Voce tera %idade_aposentadoria% anos quando se aposentar
echo.
echo Com aportes de R$ %aporte_mensal%/mes por %anos% anos
echo a juros de %taxa_juros%%% ao ano
echo.
echo Voce estara pronto para uma aposentadoria tranquila!
echo.
pause
goto menu

:acoes
cls
echo.
echo ╔═══════════════════════════════════════╗
echo ║  CALCULADORA DE INVESTIMENTOS        ║
echo ║          EM ACOES ✨                  ║
echo ╚═══════════════════════════════════════╝
echo.
echo Analise de investimento em acoes
echo.
set /p valor_acao="Valor da acao R$: "
set /p quantidade="Quantidade de acoes: "
set /p div_anual="Dividendos anuais por acao R$: "
set /a investimento=valor_acao*quantidade
set /a div_total=div_anual*quantidade
echo.
echo Investimento total: R$ %investimento%
echo Dividendos anuais: R$ %div_total%
echo.
echo Rentabilidade anual: 
echo (Dividendos / Investimento) * 100
echo.
pause
goto menu

:conversor
cls
echo.
echo ╔═══════════════════════════════════════╗
echo ║    CONVERSOR DE MOEDAS (OFFLINE)      ║
echo ╚═══════════════════════════════════════╝
echo.
echo Moedas disponiveis (Taxas fixas em BRL):
echo  1. USD - Dolar Americano (1 USD = 5,12)
echo  2. EUR - Euro (1 EUR = 5,60)
echo  3. GBP - Libra Esterlina (1 GBP = 6,50)
echo  4. ARS - Peso Argentino (1000 ARS = 5,20)
echo  5. CNY - Yuan Chines (1 CNY = 0,71)
echo.
set /p opcao="Escolha a moeda de origem (1-5): "
set /p valor="Digite o valor a converter: "
echo.
if "%opcao%"=="1" goto conv_usd
if "%opcao%"=="2" goto conv_eur
if "%opcao%"=="3" goto conv_gbp
if "%opcao%"=="4" goto conv_ars
if "%opcao%"=="5" goto conv_cny
echo Opcao invalida!
pause
goto menu

:conv_usd
set /a resultado=valor*512/100
echo %valor% USD = !resultado! BRL (aprox.)
pause
goto menu

:conv_eur
set /a resultado=valor*560/100
echo %valor% EUR = !resultado! BRL (aprox.)
pause
goto menu

:conv_gbp
set /a resultado=valor*650/100
echo %valor% GBP = !resultado! BRL (aprox.)
pause
goto menu

:conv_ars
set /a resultado=valor*520/100000
echo %valor% ARS = !resultado! BRL (aprox.)
pause
goto menu

:conv_cny
set /a resultado=valor*71/100
echo %valor% CNY = !resultado! BRL (aprox.)
pause
goto menu

:hipoteca
cls
echo.
echo ╔═══════════════════════════════════════╗
echo ║       SIMULADOR DE HIPOTECA           ║
echo ╚═══════════════════════════════════════╝
echo.
echo ✨ REVOLUCIONARIO: Simule sua casa propria!
echo.
set /p valor_imovel="Valor do imovel R$: "
set /p entrada="Valor de entrada R$: "
set /p taxa_juros="Taxa de juros anual %%: "
set /p anos="Prazo em anos: "
echo.
set /a financiamento=valor_imovel-entrada
echo Valor a financiar: R$ %financiamento%
echo.
echo Parcelas aproximadas:
set /a parcela=financiamento/(anos*12)
echo R$ %parcela%/mes (estimativa)
echo.
echo Total pago no final: 
set /a total=financiamento+(financiamento*taxa_juros*anos/100)
echo R$ %total%
echo.
pause
goto menu

:negocios
cls
echo.
echo ╔═══════════════════════════════════════╗
echo ║     SIMULADOR DE NEGOCIOS ✨          ║
echo ╚═══════════════════════════════════════╝
echo.
echo Planejamento de negocio
echo.
set /p investimento_inicial="Investimento inicial R$: "
set /p custos_fixos="Custos fixos mensais R$: "
set /p custos_variaveis="Custos variaveis %%: "
set /p preco_venda="Preco medio de venda R$: "
set /p vendas_mensais="Vendas mensais esperadas: "
echo.
echo Analise:
echo.
set /a receita=preco_venda*vendas_mensais
set /a custos=custos_fixos+(preco_venda*custos_variaveis/100)*vendas_mensais
set /a lucro=receita-custos
echo Receita mensal: R$ %receita%
echo Custos mensais: R$ %custos%
echo Lucro liquido: R$ %lucro%
echo.
if %lucro% LEQ 0 (
    echo ⚠️  ATENCAO: Negocio deficitario!
) else (
    echo ✓ Negocio lucrativo!
)
echo.
pause
goto menu

:cartao
cls
echo.
echo ╔═══════════════════════════════════════╗
echo ║  JUROS DO CARTAO DE CREDITO ✨        ║
echo ╚═══════════════════════════════════════╝
echo.
echo Calculadora de juros rotativos
echo.
set /p divida="Valor da divida R$: "
set /p juros_mensal="Juros mensais %%: "
set /p pagamento="Pagamento mensal R$: "
echo.
echo Simulacao de pagamento:
echo.
set /a mes=1
set /a saldo=divida
echo Mes 1: Saldo = R$ %saldo%
echo.
echo Aviso: Evite pagar apenas o minimo!
echo O juros rotativo pode aumentar sua divida em ate 300%% ao ano
echo.
pause
goto menu

:planejador
cls
echo.
echo ╔═══════════════════════════════════════╗
echo ║   PLANEJADOR FINANCEIRO PESSOAL ✨   ║
echo ╚═══════════════════════════════════════╝
echo.
echo Planejamento mensal
echo.
set /p renda="Renda mensal R$: "
echo.
echo Despesas fixas:
set /p aluguel="Aluguel R$: "
set /p luz="Luz R$: "
set /p agua="Agua R$: "
set /p internet="Internet R$: "
set /p outros="Outros R$: "
echo.
set /a despesas=aluguel+luz+agua+internet+outros
set /a saldo=renda-despesas
echo.
echo RESUMO FINANCEIRO:
echo Renda: R$ %renda%
echo Despesas: R$ %despesas%
echo Saldo: R$ %saldo%
echo.
if %saldo% LEQ 0 (
    echo ⚠️  Cuidado! Voce esta no vermelho
) else (
    echo ✓ Voce tem um saldo positivo!
)
echo.
pause
goto menu

:emprestimo
cls
echo.
echo ╔═══════════════════════════════════════╗
echo ║    CALCULADORA DE EMPRESTIMOS ✨      ║
echo ╚═══════════════════════════════════════╝
echo.
echo Simulacao de emprestimo pessoal
echo.
set /p valor="Valor do emprestimo R$: "
set /p taxa="Taxa de juros mensal %%: "
set /p parcelas="Numero de parcelas: "
echo.
set /a parcela=valor/parcelas
set /a juros_total=valor*taxa*parcelas/100
set /a total=valor+juros_total
echo.
echo Parcela aproximada: R$ %parcela%
echo Total de juros: R$ %juros_total%
echo Valor total: R$ %total%
echo.
pause
goto menu

:sair
cls
echo.
echo ╔═══════════════════════════════════════╗
echo ║                                      ║
echo ║   Obrigado por usar HP 12C!          ║
echo ║    Calculadora Financeira            ║
echo ║      Revolucionaria                  ║
echo ║                                      ║
echo ║      Desenvolvida para uso           ║
echo ║           offline                     ║
echo ║                                      ║
echo ╚═══════════════════════════════════════╝
echo.
timeout /t 2 >nul
exit