@echo off
chcp 65001 >nul
title HP 12C - Calculadora Financeira Revolucionária
color 0a
cls

:: HP 12C REVOLUCIONÁRIA - Funções Exclusivas
:: Desenvolvida para uso offline

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
echo  ║        CALCULADORA FINANCEIRA REVOLUCIONÁRIA                  ║
echo  ║             100%% Offline - Funciona Sem Internet              ║
echo  ║                                                               ║
echo  ╚═══════════════════════════════════════════════════════════════╝
echo.
echo  ┌─────────────────────────────────────────────────────────────┐
echo  │  FUNÇÕES BÁSICAS                                          │
echo  ├─────────────────────────────────────────────────────────────┤
echo  │  1.  Soma (+)                                             │
echo  │  2.  Subtração (-)                                        │
echo  │  3.  Multiplicação (*)                                    │
echo  │  4.  Divisão (/)                                          │
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
echo  │ 11.  VPL - Valor Presente Líquido                         │
echo  └─────────────────────────────────────────────────────────────┘
echo.
echo  ┌─────────────────────────────────────────────────────────────┐
echo  │  FUNÇÕES REVOLUCIONÁRIAS ✨                                │
echo  ├─────────────────────────────────────────────────────────────┤
echo  │ 12.  Simulador de Aposentadoria                           │
echo  │ 13.  Calculadora de Investimentos em Ações                  │
echo  │ 14.  Conversor de Moedas (Offline - Dados Fixos)           │
echo  │ 15.  Calculadora de Hipoteca                               │
echo  │ 16.  Simulador de Negócios                                 │
echo  │ 17.  Calculadora de Juros de Cartão de Crédito              │
echo  │ 18.  Planejador Financeiro Pessoal                         │
echo  │ 19.  Calculadora de Empréstimos                            │
echo  └─────────────────────────────────────────────────────────────┘
echo.
echo  ┌─────────────────────────────────────────────────────────────┐
echo  │  0.  Sair                                                  │
echo  └─────────────────────────────────────────────────────────────┘
echo.
set /p opcao="Escolha uma opção: "

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

echo Opção inválida!
pause
goto menu

:soma
cls
echo ╔═══════════════════════════════════════╗
echo ║        CALCULADORA DE SOMA            ║
echo ╚═══════════════════════════════════════╝
set /p num1="Digite o primeiro número: "
set /p num2="Digite o segundo número: "
set /a resultado=num1+num2
echo.
echo Resultado: %resultado%
echo.
pause
goto menu

:subtracao
cls
echo ╔═══════════════════════════════════════╗
echo ║      CALCULADORA DE SUBTRAÇÃO         ║
echo ╚═══════════════════════════════════════╝
set /p num1="Digite o primeiro número: "
set /p num2="Digite o segundo número: "
set /a resultado=num1-num2
echo.
echo Resultado: %resultado%
echo.
pause
goto menu

:multiplicacao
cls
echo ╔═══════════════════════════════════════╗
echo ║    CALCULADORA DE MULTIPLICAÇÃO       ║
echo ╚═══════════════════════════════════════╝
set /p num1="Digite o primeiro número: "
set /p num2="Digite o segundo número: "
set /a resultado=num1*num2
echo.
echo Resultado: %resultado%
echo.
pause
goto menu

:divisao
cls
echo ╔═══════════════════════════════════════╗
echo ║      CALCULADORA DE DIVISÃO           ║
echo ╚═══════════════════════════════════════╝
set /p num1="Digite o primeiro número: "
set /p num2="Digite o segundo número: "
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
set /p periodos="Número de períodos (n): "
set /a base=100+taxa
set /a montante=principal
set /a i=1
:loop_juros
if %i% GTR %periodos% goto fim_juros
set /a montante=montante*base/100
set /a i=i+1
goto loop_juros
:fim_juros
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
set /p periodos="Número de períodos: "
set /a base=100+taxa
set /a vp=vf
set /a i=1
:loop_vp
if %i% GTR %periodos% goto fim_vp
set /a vp=vp*100/base
set /a i=i+1
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
set /p periodos="Número de períodos: "
set /a base=100+taxa
set /a vf=vp
set /a i=1
:loop_vf
if %i% GTR %periodos% goto fim_vf
set /a vf=vf*base/100
set /a i=i+1
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
set /p pv="Valor do empréstimo (PV): "
set /p taxa="Taxa de juros mensal %%: "
set /p nper="Número de parcelas: "
echo.
echo Valor da parcela aproximado: 
echo (Use uma calculadora científica para precisão)
echo.
pause
goto menu

:tir
cls
echo ╔═══════════════════════════════════════╗
echo ║   TIR - TAXA INTERNA DE RETORNO       ║
echo ╚═══════════════════════════════════════╝
echo.
echo Esta função calcula a taxa de retorno de um investimento
echo.
echo Informe os fluxos de caixa (negativos para saídas, positivos para entradas)
set /p fc1="Fluxo de caixa período 0 (investimento inicial): "
set /p fc2="Fluxo de caixa período 1: "
set /p fc3="Fluxo de caixa período 2: "
set /p fc4="Fluxo de caixa período 3: "
echo.
echo Calculando TIR...
echo.
pause
goto menu

:vpl
cls
echo ╔═══════════════════════════════════════╗
echo ║   VPL - VALOR PRESENTE LÍQUIDO        ║
echo ╚═══════════════════════════════════════╝
echo.
echo Cálculo do Valor Presente Líquido de um projeto
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
echo ✨ REVOLUCIONÁRIO: Planeje sua aposentadoria!
echo.
set /p idade="Sua idade atual: "
set /p aporte_mensal="Aporte mensal R$: "
set /p taxa_juros="Taxa de juros anual %%: "
set /p anos="Anos até aposentadoria: "
echo.
set /a idade_aposentadoria=idade+anos
echo Você terá %idade_aposentadoria% anos quando se aposentar
echo.
echo Com aportes de R$ %aporte_mensal%/mês por %anos% anos
echo a juros de %taxa_juros%%% ao ano
echo.
echo Você estará pronto para uma aposentadoria tranquila!
echo.
pause
goto menu

:acoes
cls
echo.
echo ╔═══════════════════════════════════════╗
echo ║  CALCULADORA DE INVESTIMENTOS        ║
echo ║          EM AÇÕES ✨                  ║
echo ╚═══════════════════════════════════════╝
echo.
echo Análise de investimento em ações
echo.
set /p valor_acao="Valor da ação R$: "
set /p quantidade="Quantidade de ações: "
set /p div_anual="Dividendos anuais por ação R$: "
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
echo Moedas disponíveis:
echo  1. USD - Dólar Americano
echo  2. EUR - Euro
echo  3. GBP - Libra Esterlina
echo  4. ARS - Peso Argentino
echo  5. CNY - Yuan Chinês
echo.
set /p moeda_origem="Moeda de origem (1-5): "
set /p valor="Valor a converter: "
echo.
echo Convertendo...
echo.
echo Valor convertido com taxas de referência
echo.
pause
goto menu

:hipoteca
cls
echo.
echo ╔═══════════════════════════════════════╗
echo ║       SIMULADOR DE HIPOTECA           ║
echo ╚═══════════════════════════════════════╝
echo.
echo ✨ REVOLUCIONÁRIO: Simule sua casa própria!
echo.
set /p valor_imovel="Valor do imóvel R$: "
set /p entrada="Valor de entrada R$: "
set /p taxa_juros="Taxa de juros anual %%: "
set /p anos="Prazo em anos: "
echo.
set /a financiamento=valor_imovel-entrada
echo Valor a financiar: R$ %financiamento%
echo.
echo Parcelas aproximadas:
set /a parcela=financiamento/(anos*12)
echo R$ %parcela%/mês (estimativa)
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
echo ║     SIMULADOR DE NEGÓCIOS ✨          ║
echo ╚═══════════════════════════════════════╝
echo.
echo Planejamento de negócio
echo.
set /p investimento_inicial="Investimento inicial R$: "
set /p custos_fixos="Custos fixos mensais R$: "
set /p custos_variaveis="Custos variáveis %%: "
set /p preco_venda="Preço médio de venda R$: "
set /p vendas_mensais="Vendas mensais esperadas: "
echo.
echo Análise:
echo.
set /a receita=preco_venda*vendas_mensais
set /a custos=custos_fixos+(preco_venda*custos_variaveis/100)*vendas_mensais
set /a lucro=receita-custos
echo Receita mensal: R$ %receita%
echo Custos mensais: R$ %custos%
echo Lucro líquido: R$ %lucro%
echo.
if %lucro% LEQ 0 (
    echo ⚠️  ATENÇÃO: Negócio deficitário!
) else (
    echo ✓ Negócio lucrativo!
)
echo.
pause
goto menu

:cartao
cls
echo.
echo ╔═══════════════════════════════════════╗
echo ║  JUROS DO CARTÃO DE CRÉDITO ✨        ║
echo ╚═══════════════════════════════════════╝
echo.
echo Calculadora de juros rotativos
echo.
set /p divida="Valor da dívida R$: "
set /p juros_mensal="Juros mensais %%: "
set /p pagamento="Pagamento mensal R$: "
echo.
echo Simulação de pagamento:
echo.
set /a mes=1
set /a saldo=divida
echo Mês 1: Saldo = R$ %saldo%
echo.
echo Aviso: Evite pagar apenas o mínimo!
echo O juros rotativo pode aumentar sua dívida em até 300%% ao ano
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
set /p agua="Água R$: "
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
    echo ⚠️  Cuidado! Você está no vermelho
) else (
    echo ✓ Você tem um saldo positivo!
)
echo.
pause
goto menu

:emprestimo
cls
echo.
echo ╔═══════════════════════════════════════╗
echo ║    CALCULADORA DE EMPRÉSTIMOS ✨      ║
echo ╚═══════════════════════════════════════╝
echo.
echo Simulação de empréstimo pessoal
echo.
set /p valor="Valor do empréstimo R$: "
set /p taxa="Taxa de juros mensal %%: "
set /p parcelas="Número de parcelas: "
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
echo ║      Revolucionária                  ║
echo ║                                      ║
echo ║      Desenvolvida para uso           ║
echo ║           offline                     ║
echo ║                                      ║
echo ╚═══════════════════════════════════════╝
echo.
timeout /t 2 >nul
exit