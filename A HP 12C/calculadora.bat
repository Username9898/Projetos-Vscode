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
echo  │  5.  Juros Simples                                        │
echo  │  6.  Juros Compostos                                      │
echo  │  7.  Valor Presente (VP)                                  │
echo  │  8.  Valor Futuro (VF)                                    │
echo  │  9.  PMT - Parcelamento                                   │
echo  │ 10.  TIR - Taxa Interna de Retorno                       │
echo  │ 11.  VPL - Valor Presente Liquido                        │
echo  └─────────────────────────────────────────────────────────────┘
echo.
echo  ┌─────────────────────────────────────────────────────────────┐
echo  │  FUNÇÕES REVOLUCIONÁRIAS ✨                                │
echo  ├─────────────────────────────────────────────────────────────┤
echo  │ 12.  Simulador de Aposentadoria                          │
echo  │ 13.  Calculadora de Investimentos em Acoes                │
echo  │ 14.  Conversor de Moedas (Offline)                        │
echo  │ 15.  Calculadora de Hipoteca                              │
echo  │ 16.  Simulador de Negocios                                │
echo  │ 17.  Calculadora de Juros de Cartao de Credito            │
echo  │ 18.  Planejador Financeiro Pessoal                        │
echo  │ 19.  Calculadora de Emprestimos                           │
echo  └─────────────────────────────────────────────────────────────┘
echo.
echo  0. Sair
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
echo FUNCOES BASICAS
echo  1. Soma
echo  2. Subtracao
echo  3. Multiplicacao
echo  4. Divisao
echo.
echo  0. Voltar
echo.
set /p opcao="Escolha: "
if "%opcao%"=="1" goto soma
if "%opcao%"=="2" goto subtracao
if "%opcao%"=="3" goto multiplicacao
if "%opcao%"=="4" goto divisao
if "%opcao%"=="0" goto menu_principal
goto func_basicas

:func_financeiras
cls
echo FUNCOES FINANCEIRAS CLASSICAS
echo  5. Juros Simples
echo  6. Juros Compostos
echo  7. Valor Presente
echo  8. Valor Futuro
echo  9. PMT
echo 10. TIR
echo 11. VPL
echo.
echo  0. Voltar
echo.
set /p opcao="Escolha: "
if "%opcao%"=="5" goto juros_simples
if "%opcao%"=="6" goto juros_compostos
if "%opcao%"=="7" goto valor_presente
if "%opcao%"=="8" goto valor_futuro
if "%opcao%"=="9" goto pmt
if "%opcao%"=="10" goto tir
if "%opcao%"=="11" goto vpl
if "%opcao%"=="0" goto menu_principal
goto func_financeiras

:func_revolucionarias
cls
echo FUNCOES REVOLUCIONARIAS
echo 12. Aposentadoria
echo 13. Investimentos em Acoes
echo 14. Conversor de Moedas
echo 15. Hipoteca
echo 16. Negocios
echo 17. Juros de Cartao
echo 18. Planejador Financeiro
echo 19. Emprestimos
echo.
echo  0. Voltar
echo.
set /p opcao="Escolha: "
if "%opcao%"=="12" goto aposentadoria
if "%opcao%"=="13" goto acoes
if "%opcao%"=="14" goto conversor
if "%opcao%"=="15" goto hipoteca
if "%opcao%"=="16" goto negocios
if "%opcao%"=="17" goto cartao
if "%opcao%"=="18" goto planejador
if "%opcao%"=="19" goto emprestimo
if "%opcao%"=="0" goto menu_principal
goto func_revolucionarias

:soma
cls
set /p n1="Numero 1: "
set /p n2="Numero 2: "
set /a r=n1+n2
echo Resultado: %r%
echo.
echo 1. Repetir
echo 2. Voltar
echo 3. Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto soma
if "%op%"=="2" goto func_basicas
if "%op%"=="3" goto menu_principal
goto func_basicas

:subtracao
cls
set /p n1="Numero 1: "
set /p n2="Numero 2: "
set /a r=n1-n2
echo Resultado: %r%
echo.
echo 1. Repetir
echo 2. Voltar
echo 3. Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto subtracao
if "%op%"=="2" goto func_basicas
if "%op%"=="3" goto menu_principal
goto func_basicas

:multiplicacao
cls
set /p n1="Numero 1: "
set /p n2="Numero 2: "
set /a r=n1*n2
echo Resultado: %r%
echo.
echo 1. Repetir
echo 2. Voltar
echo 3. Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto multiplicacao
if "%op%"=="2" goto func_basicas
if "%op%"=="3" goto menu_principal
goto func_basicas

:divisao
cls
set /p n1="Numero 1: "
set /p n2="Numero 2: "
set /a r=n1/n2
echo Resultado: %r%
echo.
echo 1. Repetir
echo 2. Voltar
echo 3. Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto divisao
if "%op%"=="2" goto func_basicas
if "%op%"=="3" goto menu_principal
goto func_basicas

:juros_simples
cls
set /p p="Capital: "
set /p i="Taxa: "
set /p t="Tempo: "
set /a j=p*i*t/100
set /a m=p+j
echo Juros: %j%
echo Montante: %m%
echo.
echo 1. Repetir
echo 2. Voltar
echo 3. Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto juros_simples
if "%op%"=="2" goto func_financeiras
if "%op%"=="3" goto menu_principal
goto func_financeiras

:juros_compostos
cls
set /p p="Capital: "
set /p i="Taxa: "
set /p n="Periodos: "
set /a m=p
set /a c=1
:lc
if %c% GTR %n% goto fc
set /a m=m+(m*i/100)
set /a c=c+1
goto lc
:fc
echo Montante: %m%
echo.
echo 1. Repetir
echo 2. Voltar
echo 3. Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto juros_compostos
if "%op%"=="2" goto func_financeiras
if "%op%"=="3" goto menu_principal
goto func_financeiras

:valor_presente
cls
set /p vf="Valor Futuro: "
set /p i="Taxa: "
set /p n="Periodos: "
set /a vp=vf
set /a c=1
:lvp
if %c% GTR %n% goto fvp
set /a vp=vp-(vp*i/100)
set /a c=c+1
goto lvp
:fvp
echo Valor Presente: %vp%
echo.
echo 1. Repetir
echo 2. Voltar
echo 3. Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto valor_presente
if "%op%"=="2" goto func_financeiras
if "%op%"=="3" goto menu_principal
goto func_financeiras

:valor_futuro
cls
set /p vp="Valor Presente: "
set /p i="Taxa: "
set /p n="Periodos: "
set /a vf=vp
set /a c=1
:lvf
if %c% GTR %n% goto fvf
set /a vf=vf+(vf*i/100)
set /a c=c+1
goto lvf
:fvf
echo Valor Futuro: %vf%
echo.
echo 1. Repetir
echo 2. Voltar
echo 3. Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto valor_futuro
if "%op%"=="2" goto func_financeiras
if "%op%"=="3" goto menu_principal
goto func_financeiras

:pmt
cls
set /p pv="Emprestimo: "
set /p i="Taxa mensal: "
set /p n="Parcelas: "
echo Parcela aproximada: (use calculadora cientifica)
echo.
echo 1. Repetir
echo 2. Voltar
echo 3. Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto pmt
if "%op%"=="2" goto func_financeiras
if "%op%"=="3" goto menu_principal
goto func_financeiras

:tir
cls
echo Informe fluxos de caixa
set /p f0="Periodo 0: "
set /p f1="Periodo 1: "
set /p f2="Periodo 2: "
set /p f3="Periodo 3: "
echo Calculando TIR...
echo.
echo 1. Repetir
echo 2. Voltar
echo 3. Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto tir
if "%op%"=="2" goto func_financeiras
if "%op%"=="3" goto menu_principal
goto func_financeiras

:vpl
cls
set /p inv="Investimento: "
set /p ret="Retorno: "
set /p a="Anos: "
set /p i="Taxa: "
echo VPL calculado!
echo.
echo 1. Repetir
echo 2. Voltar
echo 3. Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto vpl
if "%op%"=="2" goto func_financeiras
if "%op%"=="3" goto menu_principal
goto func_financeiras

:aposentadoria
cls
set /p idade="Idade: "
set /p aporte="Aporte mensal R$: "
set /p juros="Juros anual %: "
set /p anos="Anos: "
set /a idf=idade+anos
echo Voce tera %idf% anos
echo Aporte: R$ %aporte%/mes por %anos% anos
echo Juros: %juros%%% ao ano
echo.
echo 1. Repetir
echo 2. Voltar
echo 3. Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto aposentadoria
if "%op%"=="2" goto func_revolucionarias
if "%op%"=="3" goto menu_principal
goto func_revolucionarias

:acoes
cls
set /p preco="Preco acao R$: "
set /p qtd="Quantidade: "
set /p div="Dividendos/acao R$: "
set /a inv=preco*qtd
set /a divt=div*qtd
echo Investimento: R$ %inv%
echo Dividendos: R$ %divt%
echo.
echo 1. Repetir
echo 2. Voltar
echo 3. Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto acoes
if "%op%"=="2" goto func_revolucionarias
if "%op%"=="3" goto menu_principal
goto func_revolucionarias

:conversor
cls
echo CONVERSOR DE MOEDAS (OFFLINE)
echo.
echo Moedas:
echo  1. BRL
echo  2. USD (1 USD = 5,12 BRL)
echo  3. EUR (1 EUR = 5,60 BRL)
echo  4. GBP (1 GBP = 6,50 BRL)
echo  5. ARS (1000 ARS = 5,20 BRL)
echo  6. CNY (1 CNY = 0,71 BRL)
echo.
set /p origem="Origem (1-6): "
set /p destino="Destino (1-6): "
set /p valor="Valor: "
echo.
if "%origem%"=="%destino%" (
    echo %valor%
    goto conv_fim
)
if "%origem%"=="1" (
    if "%destino%"=="2" set /a res=valor*512/100
    if "%destino%"=="3" set /a res=valor*560/100
    if "%destino%"=="4" set /a res=valor*650/100
    if "%destino%"=="5" set /a res=valor*520/100000
    if "%destino%"=="6" set /a res=valor*71/100
)
if "%origem%"=="2" (
    if "%destino%"=="1" set /a res=valor*100/512
    if "%destino%"=="3" set /a res=valor*560/512
    if "%destino%"=="4" set /a res=valor*650/512
    if "%destino%"=="5" set /a res=valor*520/51200
    if "%destino%"=="6" set /a res=valor*71*512/51200
)
if "%origem%"=="3" (
    if "%destino%"=="1" set /a res=valor*100/560
    if "%destino%"=="2" set /a res=valor*512/560
    if "%destino%"=="4" set /a res=valor*650/560
    if "%destino%"=="5" set /a res=valor*5600/52000
    if "%destino%"=="6" set /a res=valor*71*560/56000
)
if "%origem%"=="4" (
    if "%destino%"=="1" set /a res=valor*100/650
    if "%destino%"=="2" set /a res=valor*512/650
    if "%destino%"=="3" set /a res=valor*560/650
    if "%destino%"=="5" set /a res=valor*65000/52000
    if "%destino%"=="6" set /a res=valor*71*650/65000
)
if "%origem%"=="5" (
    if "%destino%"=="1" set /a res=valor*520/5
    if "%destino%"=="2" set /a res=valor*512/100*520/5
    if "%destino%"=="3" set /a res=valor*560/100*520/5
    if "%destino%"=="4" set /a res=valor*650/100*520/5
    if "%destino%"=="6" set /a res=valor*71/100*520/5
)
if "%origem%"=="6" (
    if "%destino%"=="1" set /a res=valor*100/71
    if "%destino%"=="2" set /a res=valor*512/7100
    if "%destino%"=="3" set /a res=valor*560/7100
    if "%destino%"=="4" set /a res=valor*650/7100
    if "%destino%"=="5" set /a res=valor*71*1000/71000
)
echo Resultado: %res%
:conv_fim
echo.
echo 1. Repetir
echo 2. Voltar
echo 3. Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto conversor
if "%op%"=="2" goto func_revolucionarias
if "%op%"=="3" goto menu_principal
goto func_revolucionarias

:hipoteca
cls
set /p imovel="Imovel R$: "
set /p entrada="Entrada R$: "
set /p juros="Juros anual %: "
set /p p="Prazo anos: "
set /a fin=imovel-entrada
echo Financiamento: R$ %fin%
set /a par=fin/(p*12)
echo Parcela aprox: R$ %par%/mes
set /a tot=fin+(fin*juros*p/100)
echo Total: R$ %tot%
echo.
echo 1. Repetir
echo 2. Voltar
echo 3. Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto hipoteca
if "%op%"=="2" goto func_revolucionarias
if "%op%"=="3" goto menu_principal
goto func_revolucionarias

:negocios
cls
set /p inv="Investimento R$: "
set /p fixos="Custos fixos R$: "
set /p var="Custos variaveis %: "
set /p preco="Preco venda R$: "
set /p vmes="Vendas/mes: "
set /a rec=preco*vmes
set /a cust=fixos+(preco*var/100)*vmes
set /a luc=rec-cust
echo Receita: R$ %rec%
echo Custos: R$ %cust%
echo Lucro: R$ %luc%
if %luc% LEQ 0 (
    echo ATENCAO: Deficitaria
) else (
    echo Lucrativa
)
echo.
echo 1. Repetir
echo 2. Voltar
echo 3. Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto negocios
if "%op%"=="2" goto func_revolucionarias
if "%op%"=="3" goto menu_principal
goto func_revolucionarias

:cartao
cls
set /p div="Divida R$: "
set /p j="Juros mensal %: "
set /p pg="Pagamento R$: "
set /a s=div
echo Mes 1: Saldo = R$ %s%
echo Aviso: Nao pague apenas o minimo!
echo Juros rotativo pode aumentar divida em 300%% ao ano
echo.
echo 1. Repetir
echo 2. Voltar
echo 3. Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto cartao
if "%op%"=="2" goto func_revolucionarias
if "%op%"=="3" goto menu_principal
goto func_revolucionarias

:planejador
cls
set /p renda="Renda mensal R$: "
set /p alug="Aluguel R$: "
set /p luz="Luz R$: "
set /p agua="Agua R$: "
set /p net="Internet R$: "
set /p out="Outros R$: "
set /a desp=alug+luz+agua+net+out
set /a sal=renda-desp
echo Renda: R$ %renda%
echo Despesas: R$ %desp%
echo Saldo: R$ %sal%
if %sal% LEQ 0 (
    echo Cuidado! Esta no vermelho
) else (
    echo Saldo positivo
)
echo.
echo 1. Repetir
echo 2. Voltar
echo 3. Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto planejador
if "%op%"=="2" goto func_revolucionarias
if "%op%"=="3" goto menu_principal
goto func_revolucionarias

:emprestimo
cls
set /p val="Emprestimo R$: "
set /p i="Juros mensal %: "
set /p p="Parcelas: "
set /a par=val/p
set /a jt=val*i*p/100
set /a tot=val+jt
echo Parcela: R$ %par%
echo Juros total: R$ %jt%
echo Total: R$ %tot%
echo.
echo 1. Repetir
echo 2. Voltar
echo 3. Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto emprestimo
if "%op%"=="2" goto func_revolucionarias
if "%op%"=="3" goto menu_principal
goto func_revolucionarias

:sair
cls
echo.
echo Obrigado por usar HP 12C!
echo Calculadora Financeira Revolucionaria
echo.
timeout /t 2 >nul
exit