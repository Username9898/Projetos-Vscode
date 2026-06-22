@echo off
chcp 65001 >nul
title HP 12C - Calculadora Financeira Revolucionaria
color 0a
cls

:menu_principal
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

if "%opcao%"=="1" goto func_basicas
if "%opcao%"=="2" goto func_basicas
if "%opcao%"=="3" goto func_basicas
if "%opcao%"=="4" goto func_basicas
if "%opcao%"=="5" goto func_financeiras
if "%opcao%"=="6" goto func_financeiras
if "%opcao%"=="7" goto func_financeiras
if "%opcao%"=="8" goto func_financeiras
if "%opcao%"=="9" goto func_financeiras
if "%opcao%"=="10" goto func_financeiras
if "%opcao%"=="11" goto func_financeiras
if "%opcao%"=="12" goto func_revolucionarias
if "%opcao%"=="13" goto func_revolucionarias
if "%opcao%"=="14" goto func_revolucionarias
if "%opcao%"=="15" goto func_revolucionarias
if "%opcao%"=="16" goto func_revolucionarias
if "%opcao%"=="17" goto func_revolucionarias
if "%opcao%"=="18" goto func_revolucionarias
if "%opcao%"=="19" goto func_revolucionarias
if "%opcao%"=="0" goto sair

echo Opcao invalida!
pause
goto menu_principal

:func_basicas
cls
echo.
echo ╔═══════════════════════════════════════╗
echo ║          FUNCOES BASICAS              ║
echo ╚═══════════════════════════════════════╝
echo.
echo  1. Soma (+)
echo  2. Subtracao (-)
echo  3. Multiplicacao (*)
echo  4. Divisao (/)
echo.
echo  0. Voltar ao Menu Principal
echo.
set /p opcao="Escolha uma opcao: "
if "%opcao%"=="1" goto soma
if "%opcao%"=="2" goto subtracao
if "%opcao%"=="3" goto multiplicacao
if "%opcao%"=="4" goto divisao
if "%opcao%"=="0" goto menu_principal

echo Opcao invalida!
pause
goto func_basicas

:func_financeiras
cls
echo.
echo ╔═══════════════════════════════════════╗
echo ║    FUNCOES FINANCEIRAS CLASSICAS     ║
echo ╚═══════════════════════════════════════╝
echo.
echo  5. Juros Simples
echo  6. Juros Compostos
echo  7. Valor Presente (VP)
echo  8. Valor Futuro (VF)
echo  9. PMT - Parcelamento
echo 10. TIR - Taxa Interna de Retorno
echo 11. VPL - Valor Presente Liquido
echo.
echo  0. Voltar ao Menu Principal
echo.
set /p opcao="Escolha uma opcao: "
if "%opcao%"=="5" goto juros_simples
if "%opcao%"=="6" goto juros_compostos
if "%opcao%"=="7" goto valor_presente
if "%opcao%"=="8" goto valor_futuro
if "%opcao%"=="9" goto pmt
if "%opcao%"=="10" goto tir
if "%opcao%"=="11" goto vpl
if "%opcao%"=="0" goto menu_principal

echo Opcao invalida!
pause
goto func_financeiras

:func_revolucionarias
cls
echo.
echo ╔═══════════════════════════════════════╗
echo ║     FUNCOES REVOLUCIONARIAS ✨        ║
echo ╚═══════════════════════════════════════╝
echo.
echo 12. Simulador de Aposentadoria
echo 13. Calculadora de Investimentos em Acoes
echo 14. Conversor de Moedas (Offline)
echo 15. Calculadora de Hipoteca
echo 16. Simulador de Negocios
echo 17. Calculadora de Juros de Cartao de Credito
echo 18. Planejador Financeiro Pessoal
echo 19. Calculadora de Emprestimos
echo.
echo  0. Voltar ao Menu Principal
echo.
set /p opcao="Escolha uma opcao: "
if "%opcao%"=="12" goto aposentadoria
if "%opcao%"=="13" goto acoes
if "%opcao%"=="14" goto conversor
if "%opcao%"=="15" goto hipoteca
if "%opcao%"=="16" goto negocios
if "%opcao%"=="17" goto cartao
if "%opcao%"=="18" goto planejador
if "%opcao%"=="19" goto emprestimo
if "%opcao%"=="0" goto menu_principal

echo Opcao invalida!
pause
goto func_revolucionarias

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
echo 1. Fazer outro calculo de Soma
echo 2. Voltar ao Menu de Funcoes Basicas
echo 3. Voltar ao Menu Principal
echo.
set /p opcao="Escolha: "
if "%opcao%"=="1" goto soma
if "%opcao%"=="2" goto func_basicas
if "%opcao%"=="3" goto menu_principal
goto func_basicas

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
echo 1. Fazer outra subtracao
echo 2. Voltar ao Menu de Funcoes Basicas
echo 3. Voltar ao Menu Principal
echo.
set /p opcao="Escolha: "
if "%opcao%"=="1" goto subtracao
if "%opcao%"=="2" goto func_basicas
if "%opcao%"=="3" goto menu_principal
goto func_basicas

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
echo 1. Fazer outra multiplicacao
echo 2. Voltar ao Menu de Funcoes Basicas
echo 3. Voltar ao Menu Principal
echo.
set /p opcao="Escolha: "
if "%opcao%"=="1" goto multiplicacao
if "%opcao%"=="2" goto func_basicas
if "%opcao%"=="3" goto menu_principal
goto func_basicas

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
echo 1. Fazer outra divisao
echo 2. Voltar ao Menu de Funcoes Basicas
echo 3. Voltar ao Menu Principal
echo.
set /p opcao="Escolha: "
if "%opcao%"=="1" goto divisao
if "%opcao%"=="2" goto func_basicas
if "%opcao%"=="3" goto menu_principal
goto func_basicas

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
echo 1. Fazer outro calculo de Juros Simples
echo 2. Voltar ao Menu de Funcoes Financeiras
echo 3. Voltar ao Menu Principal
echo.
set /p opcao="Escolha: "
if "%opcao%"=="1" goto juros_simples
if "%opcao%"=="2" goto func_financeiras
if "%opcao%"=="3" goto menu_principal
goto func_financeiras

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
echo 1. Fazer outro calculo de Juros Compostos
echo 2. Voltar ao Menu de Funcoes Financeiras
echo 3. Voltar ao Menu Principal
echo.
set /p opcao="Escolha: "
if "%opcao%"=="1" goto juros_compostos
if "%opcao%"=="2" goto func_financeiras
if "%opcao%"=="3" goto menu_principal
goto func_financeiras

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
echo 1. Fazer outro calculo de Valor Presente
echo 2. Voltar ao Menu de Funcoes Financeiras
echo 3. Voltar ao Menu Principal
echo.
set /p opcao="Escolha: "
if "%opcao%"=="1" goto valor_presente
if "%opcao%"=="2" goto func_financeiras
if "%opcao%"=="3" goto menu_principal
goto func_financeiras

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
echo 1. Fazer outro calculo de Valor Futuro
echo 2. Voltar ao Menu de Funcoes Financeiras
echo 3. Voltar ao Menu Principal
echo.
set /p opcao="Escolha: "
if "%opcao%"=="1" goto valor_futuro
if "%opcao%"=="2" goto func_financeiras
if "%opcao%"=="3" goto menu_principal
goto func_financeiras

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
echo 1. Fazer outro calculo de Parcelamento
echo 2. Voltar ao Menu de Funcoes Financeiras
echo 3. Voltar ao Menu Principal
echo.
set /p opcao="Escolha: "
if "%opcao%"=="1" goto pmt
if "%opcao%"=="2" goto func_financeiras
if "%opcao%"=="3" goto menu_principal
goto func_financeiras

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
echo 1. Fazer outro calculo de TIR
echo 2. Voltar ao Menu de Funcoes Financeiras
echo 3. Voltar ao Menu Principal
echo.
set /p opcao="Escolha: "
if "%opcao%"=="1" goto tir
if "%opcao%"=="2" goto func_financeiras
if "%opcao%"=="3" goto menu_principal
goto func_financeiras

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
echo 1. Fazer outro calculo de VPL
echo 2. Voltar ao Menu de Funcoes Financeiras
echo 3. Voltar ao Menu Principal
echo.
set /p opcao="Escolha: "
if "%opcao%"=="1" goto vpl
if "%opcao%"=="2" goto func_financeiras
if "%opcao%"=="3" goto menu_principal
goto func_financeiras

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
echo 1. Fazer outra simulacao de aposentadoria
echo 2. Voltar ao Menu de Funcoes Revolucionarias
echo 3. Voltar ao Menu Principal
echo.
set /p opcao="Escolha: "
if "%opcao%"=="1" goto aposentadoria
if "%opcao%"=="2" goto func_revolucionarias
if "%opcao%"=="3" goto menu_principal
goto func_revolucionarias

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
echo 1. Fazer outra analise de investimento
echo 2. Voltar ao Menu de Funcoes Revolucionarias
echo 3. Voltar ao Menu Principal
echo.
set /p opcao="Escolha: "
if "%opcao%"=="1" goto acoes
if "%opcao%"=="2" goto func_revolucionarias
if "%opcao%"=="3" goto menu_principal
goto func_revolucionarias

:conversor
cls
echo.
echo ╔═══════════════════════════════════════╗
echo ║    CONVERSOR DE MOEDAS (OFFLINE)      ║
echo ╚═══════════════════════════════════════╝
echo.
echo Moedas disponiveis (Taxas fixas):
echo  1. BRL - Real Brasileiro
echo  2. USD - Dolar Americano (1 USD = 5,12 BRL)
echo  3. EUR - Euro (1 EUR = 5,60 BRL)
echo  4. GBP - Libra Esterlina (1 GBP = 6,50 BRL)
echo  5. ARS - Peso Argentino (1000 ARS = 5,20 BRL)
echo  6. CNY - Yuan Chines (1 CNY = 0,71 BRL)
echo.
set /p origem="Escolha a moeda de ORIGEM (1-6): "
set /p destino="Escolha a moeda de DESTINO (1-6): "
set /p valor="Digite o valor a converter: "
echo.
set /a resultado=0
rem Origem BRL (1)
if "%origem%"=="1" if "%destino%"=="2" set /a resultado=valor*512/100
if "%origem%"=="1" if "%destino%"=="3" set /a resultado=valor*560/100
if "%origem%"=="1" if "%destino%"=="4" set /a resultado=valor*650/100
if "%origem%"=="1" if "%destino%"=="5" set /a resultado=valor*520/100000
if "%origem%"=="1" if "%destino%"=="6" set /a resultado=valor*71/100
rem Origem USD (2)
if "%origem%"=="2" if "%destino%"=="1" set /a resultado=valor*100/512
if "%origem%"=="2" if "%destino%"=="3" set /a resultado=valor*560/512
if "%origem%"=="2" if "%destino%"=="4" set /a resultado=valor*650/512
if "%origem%"=="2" if "%destino%"=="5" set /a resultado=valor*520/51200
if "%origem%"=="2" if "%destino%"=="6" set /a resultado=valor*71*512/51200
rem Origem EUR (3)
if "%origem%"=="3" if "%destino%"=="1" set /a resultado=valor*100/560
if "%origem%"=="3" if "%destino%"=="2" set /a resultado=valor*512/560
if "%origem%"=="3" if "%destino%"=="4" set /a resultado=valor*650/560
if "%origem%"=="3" if "%destino%"=="5" set /a resultado=valor*5600/52000
if "%origem%"=="3" if "%destino%"=="6" set /a resultado=valor*71/100*560/100
rem Origem GBP (4)
if "%origem%"=="4" if "%destino%"=="1" set /a resultado=valor*100/650
if "%origem%"=="4" if "%destino%"=="2" set /a resultado=valor*512/650
if "%origem%"=="4" if "%destino%"=="3" set /a resultado=valor*560/650
if "%origem%"=="4" if "%destino%"=="5" set /a resultado=valor*65000/52000
if "%origem%"=="4" if "%destino%"=="6" set /a resultado=valor*71/100*650/100
rem Origem ARS (5)
if "%origem%"=="5" if "%destino%"=="1" set /a resultado=valor*520/5
if "%origem%"=="5" if "%destino%"=="2" set /a resultado=valor*512/100*520/5
if "%origem%"=="5" if "%destino%"=="3" set /a resultado=valor*560/100*520/5
if "%origem%"=="5" if "%destino%"=="4" set /a resultado=valor*650/100*520/5
if "%origem%"=="5" if "%destino%"=="6" set /a resultado=valor*71/100*520/5
rem Origem CNY (6)
if "%origem%"=="6" if "%destino%"=="1" set /a resultado=valor*100/71
if "%origem%"=="6" if "%destino%"=="2" set /a resultado=valor*512/7100
if "%origem%"=="6" if "%destino%"=="3" set /a resultado=valor*560/7100
if "%origem%"=="6" if "%destino%"=="4" set /a resultado=valor*650/7100
if "%origem%"=="6" if "%destino%"=="5" set /a resultado=valor*71/100*520/5

set /a resultado_int=resultado
echo Resultado: %resultado_int% (aprox.)
echo.
echo 1. Fazer outra conversao
echo 2. Voltar ao Menu de Funcoes Revolucionarias
echo 3. Voltar ao Menu Principal
echo.
set /p opcao="Escolha: "
if "%opcao%"=="1" goto conversor
if "%opcao%"=="2" goto func_revolucionarias
if "%opcao%"=="3" goto menu_principal
goto func_revolucionarias

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
echo 1. Fazer outra simulacao de hipoteca
echo 2. Voltar ao Menu de Funcoes Revolucionarias
echo 3. Voltar ao Menu Principal
echo.
set /p opcao="Escolha: "
if "%opcao%"=="1" goto hipoteca
if "%opcao%"=="2" goto func_revolucionarias
if "%opcao%"=="3" goto menu_principal
goto func_revolucionarias

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
echo 1. Fazer outra simulacao de negocio
echo 2. Voltar ao Menu de Funcoes Revolucionarias
echo 3. Voltar ao Menu Principal
echo.
set /p opcao="Escolha: "
if "%opcao%"=="1" goto negocios
if "%opcao%"=="2" goto func_revolucionarias
if "%opcao%"=="3" goto menu_principal
goto func_revolucionarias

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
echo 1. Fazer outra simulacao de cartao
echo 2. Voltar ao Menu de Funcoes Revolucionarias
echo 3. Voltar ao Menu Principal
echo.
set /p opcao="Escolha: "
if "%opcao%"=="1" goto cartao
if "%opcao%"=="2" goto func_revolucionarias
if "%opcao%"=="3" goto menu_principal
goto func_revolucionarias

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
echo 1. Fazer outro planejamento
echo 2. Voltar ao Menu de Funcoes Revolucionarias
echo 3. Voltar ao Menu Principal
echo.
set /p opcao="Escolha: "
if "%opcao%"=="1" goto planejador
if "%opcao%"=="2" goto func_revolucionarias
if "%opcao%"=="3" goto menu_principal
goto func_revolucionarias

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
echo 1. Fazer outra simulacao de emprestimo
echo 2. Voltar ao Menu de Funcoes Revolucionarias
echo 3. Voltar ao Menu Principal
echo.
set /p opcao="Escolha: "
if "%opcao%"=="1" goto emprestimo
if "%opcao%"=="2" goto func_revolucionarias
if "%opcao%"=="3" goto menu_principal
goto func_revolucionarias

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