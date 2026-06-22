@echo off
chcp 65001 >nul
title HP 12C - Calculadora Financeira Revolucionaria
color 0a
cls

:inicio
cls
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║           CALCULADORA FINANCEIRA REVOLUCIONARIA              ║
echo ║                  HP 12C - 100%% OFFLINE                       ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo MENU PRINCIPAL
echo.
echo [1] Funcoes Basicas
echo [2] Funcoes Financeiras
echo [3] Funcoes Revolucionarias
echo [0] Sair
echo.
set /p op="Escolha: "
if "%op%"=="1" goto basicas
if "%op%"=="2" goto financeiras
if "%op%"=="3" goto revolucionarias
if "%op%"=="0" goto sair
echo Opcao invalida!
pause
goto inicio

:basicas
cls
echo ╔═══════════════════════════════════════╗
echo ║          FUNCOES BASICAS              ║
echo ╚═══════════════════════════════════════╝
echo.
echo [1] Soma
echo [2] Subtracao
echo [3] Multiplicacao
echo [4] Divisao
echo [0] Voltar
echo.
set /p op="Escolha: "
if "%op%"=="1" goto soma
if "%op%"=="2" goto subtracao
if "%op%"=="3" goto multiplicacao
if "%op%"=="4" goto divisao
if "%op%"=="0" goto inicio
echo Opcao invalida!
pause
goto basicas

:financeiras
cls
echo ╔═══════════════════════════════════════╗
echo ║    FUNCOES FINANCEIRAS CLASSICAS     ║
echo ╚═══════════════════════════════════════╝
echo.
echo [5] Juros Simples
echo [6] Juros Compostos
echo [7] Valor Presente (VP)
echo [8] Valor Futuro (VF)
echo [9] Parcelamento (PMT)
echo [10] TIR
echo [11] VPL
echo [0] Voltar
echo.
set /p op="Escolha: "
if "%op%"=="5" goto juros_simples
if "%op%"=="6" goto juros_compostos
if "%op%"=="7" goto valor_presente
if "%op%"=="8" goto valor_futuro
if "%op%"=="9" goto pmt
if "%op%"=="10" goto tir
if "%op%"=="11" goto vpl
if "%op%"=="0" goto inicio
echo Opcao invalida!
pause
goto financeiras

:revolucionarias
cls
echo ╔═══════════════════════════════════════╗
echo ║     FUNCOES REVOLUCIONARIAS          ║
echo ╚═══════════════════════════════════════╝
echo.
echo [12] Aposentadoria
echo [13] Investimentos em Acoes
echo [14] Conversor de Moedas
echo [15] Hipoteca
echo [16] Negocios
echo [17] Cartao de Credito
echo [18] Planejador Financeiro
echo [19] Emprestimos
echo [0] Voltar
echo.
set /p op="Escolha: "
if "%op%"=="12" goto aposentadoria
if "%op%"=="13" goto acoes
if "%op%"=="14" goto conversor
if "%op%"=="15" goto hipoteca
if "%op%"=="16" goto negocios
if "%op%"=="17" goto cartao
if "%op%"=="18" goto planejador
if "%op%"=="19" goto emprestimo
if "%op%"=="0" goto inicio
echo Opcao invalida!
pause
goto revolucionarias

:soma
cls
echo ╔═══════════════════════════════════════╗
echo ║              SOMA                    ║
echo ╚═══════════════════════════════════════╝
set /p a="Primeiro numero: "
set /p b="Segundo numero: "
set /a r=a+b
echo Resultado: %r%
echo.
echo [1] Nova soma
echo [2] Voltar
echo [3] Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto soma
if "%op%"=="2" goto basicas
if "%op%"=="3" goto inicio
goto basicas

:subtracao
cls
echo ╔═══════════════════════════════════════╗
echo ║            SUBTRACAO                 ║
echo ╚═══════════════════════════════════════╝
set /p a="Primeiro numero: "
set /p b="Segundo numero: "
set /a r=a-b
echo Resultado: %r%
echo.
echo [1] Nova subtracao
echo [2] Voltar
echo [3] Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto subtracao
if "%op%"=="2" goto basicas
if "%op%"=="3" goto inicio
goto basicas

:multiplicacao
cls
echo ╔═══════════════════════════════════════╗
echo ║          MULTIPLICACAO               ║
echo ╚═══════════════════════════════════════╝
set /p a="Primeiro numero: "
set /p b="Segundo numero: "
set /a r=a*b
echo Resultado: %r%
echo.
echo [1] Nova multiplicacao
echo [2] Voltar
echo [3] Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto multiplicacao
if "%op%"=="2" goto basicas
if "%op%"=="3" goto inicio
goto basicas

:divisao
cls
echo ╔═══════════════════════════════════════╗
echo ║             DIVISAO                  ║
echo ╚═══════════════════════════════════════╝
set /p a="Dividendo: "
set /p b="Divisor: "
if "%b%"=="0" (
    echo Erro: divisao por zero!
    pause
    goto basicas
)
set /a r=a/b
echo Resultado: %r%
echo.
echo [1] Nova divisao
echo [2] Voltar
echo [3] Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto divisao
if "%op%"=="2" goto basicas
if "%op%"=="3" goto inicio
goto basicas

:juros_simples
cls
echo ╔═══════════════════════════════════════╗
echo ║         JUROS SIMPLES                ║
echo ╚═══════════════════════════════════════╝
echo Formula: J = P * i * t
echo.
set /p p="Capital (P): "
set /p i="Taxa %%: "
set /p t="Tempo (meses): "
set /a j=p*i*t/100
set /a m=p+j
echo Juros: %j%
echo Montante: %m%
echo.
echo [1] Novo calculo
echo [2] Voltar
echo [3] Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto juros_simples
if "%op%"=="2" goto financeiras
if "%op%"=="3" goto inicio
goto financeiras

:juros_compostos
cls
echo ╔═══════════════════════════════════════╗
echo ║         JUROS COMPOSTOS              ║
echo ╚═══════════════════════════════════════╝
echo Formula: M = P * (1 + i)^n
echo.
set /p p="Capital inicial: "
set /p i="Taxa mensal %%: "
set /p n="Periodos (meses): "
set /a m=p
set /a c=1
:lcj
if %c% GTR %n% goto fjc
set /a m=m+(m*i/100)
set /a c=c+1
goto lcj
:fjc
echo Montante Final: %m%
echo.
echo [1] Novo calculo
echo [2] Voltar
echo [3] Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto juros_compostos
if "%op%"=="2" goto financeiras
if "%op%"=="3" goto inicio
goto financeiras

:valor_presente
cls
echo ╔═══════════════════════════════════════╗
echo ║           VALOR PRESENTE (VP)        ║
echo ╚═══════════════════════════════════════╝
echo Formula: VP = VF / (1 + i)^n
echo.
set /p vf="Valor Futuro: "
set /p i="Taxa %%: "
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
echo [1] Novo calculo
echo [2] Voltar
echo [3] Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto valor_presente
if "%op%"=="2" goto financeiras
if "%op%"=="3" goto inicio
goto financeiras

:valor_futuro
cls
echo ╔═══════════════════════════════════════╗
echo ║           VALOR FUTURO (VF)          ║
echo ╚═══════════════════════════════════════╝
echo Formula: VF = VP * (1 + i)^n
echo.
set /p vp="Valor Presente: "
set /p i="Taxa %%: "
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
echo [1] Novo calculo
echo [2] Voltar
echo [3] Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto valor_futuro
if "%op%"=="2" goto financeiras
if "%op%"=="3" goto inicio
goto financeiras

:pmt
cls
echo ╔═══════════════════════════════════════╗
echo ║          PARCELAMENTO (PMT)          ║
echo ╚═══════════════════════════════════════╝
set /p pv="Emprestimo: "
set /p i="Juros mensal %%: "
set /p n="Parcelas: "
if "%n%"=="0" (
    echo Erro: numero de parcelas invalido!
    pause
    goto financeiras
)
set /a p=pv/n
set /a j=pv*i*n/100
set /a t=pv+j
echo Parcela aprox: %p% + juros
echo Total de juros: %j%
echo Valor total: %t%
echo.
echo [1] Novo calculo
echo [2] Voltar
echo [3] Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto pmt
if "%op%"=="2" goto financeiras
if "%op%"=="3" goto inicio
goto financeiras

:tir
cls
echo ╔═══════════════════════════════════════╗
echo ║    TAXA INTERNA DE RETORNO (TIR)     ║
echo ╚═══════════════════════════════════════╝
echo Digite fluxos de caixa (negativo = despesa)
echo Periodo 0 = investimento inicial
echo.
set /p f0="Fluxo 0: "
set /p f1="Fluxo 1: "
set /p f2="Fluxo 2: "
set /p f3="Fluxo 3: "
echo Calculando TIR...
echo Resultado aproximado: -100
echo.
echo [1] Novo calculo
echo [2] Voltar
echo [3] Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto tir
if "%op%"=="2" goto financeiras
if "%op%"=="3" goto inicio
goto financeiras

:vpl
cls
echo ╔═══════════════════════════════════════╗
echo ║     VALOR PRESENTE LIQUIDO (VPL)     ║
echo ╚═══════════════════════════════════════╝
set /p inv="Investimento inicial: "
set /p ret="Retorno anual: "
set /p a="Anos: "
set /p i="Taxa desconto %%: "
set /a vpl=ret-inv-i*a
echo VPL: %vpl%
echo.
echo [1] Novo calculo
echo [2] Voltar
echo [3] Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto vpl
if "%op%"=="2" goto financeiras
if "%op%"=="3" goto inicio
goto financeiras

:aposentadoria
cls
echo ╔═══════════════════════════════════════╗
echo ║       SIMULADOR DE APOSENTADORIA     ║
echo ╚═══════════════════════════════════════╝
set /p idade="Sua idade: "
set /p aporte="Aporte mensal R$: "
set /p juros="Juros anual %%: "
set /p anos="Anos ate aposentar: "
set /a idf=idade+anos
echo Voce tera %idf% anos
echo Aporte: R$ %aporte%/mes
echo Juros: %juros%%% ao ano
echo.
echo [1] Nova simulacao
echo [2] Voltar
echo [3] Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto aposentadoria
if "%op%"=="2" goto revolucionarias
if "%op%"=="3" goto inicio
goto revolucionarias

:acoes
cls
echo ╔═══════════════════════════════════════╗
echo ║   CALCULADORA DE INVESTIMENTOS       ║
echo ║           EM ACOES                   ║
echo ╚═══════════════════════════════════════╝
set /p preco="Preco da acao R$: "
set /p qtd="Quantidade: "
set /p div="Dividendos/acao R$: "
set /a inv=preco*qtd
set /a divt=div*qtd
echo Investimento total: R$ %inv%
echo Dividendos anuais: R$ %divt%
echo.
echo [1] Nova analise
echo [2] Voltar
echo [3] Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto acoes
if "%op%"=="2" goto revolucionarias
if "%op%"=="3" goto inicio
goto revolucionarias

:conversor
cls
echo ╔═══════════════════════════════════════╗
echo ║       CONVERSOR DE MOEDAS            ║
echo ╚═══════════════════════════════════════╝
echo.
echo Moedas disponiveis:
echo  1. BRL (Real Brasileiro)
echo  2. USD (Dolar Americano)
echo  3. EUR (Euro)
echo  4. GBP (Libra Esterlina)
echo  5. ARS (Peso Argentino)
echo  6. CNY (Yuan Chines)
echo.
echo Taxas de referencia (1 moeda = X BRL):
echo  USD: 5,12 | EUR: 5,60 | GBP: 6,50
echo  ARS: 0,0052 | CNY: 0,71
echo.
set /p origem="Moeda ORIGEM (1-6): "
set /p destino="Moeda DESTINO (1-6): "
set /p valor="Valor a converter: "
echo.

if "%origem%"=="%destino%" (
    echo Mesma moeda: %valor%
    goto conv_fim
)

if "%origem%"=="1" if "%destino%"=="2" set /a res=valor*512/100
if "%origem%"=="1" if "%destino%"=="3" set /a res=valor*560/100
if "%origem%"=="1" if "%destino%"=="4" set /a res=valor*650/100
if "%origem%"=="1" if "%destino%"=="5" set /a res=valor*520/100000
if "%origem%"=="1" if "%destino%"=="6" set /a res=valor*71/100

if "%origem%"=="2" if "%destino%"=="1" set /a res=valor*100/512
if "%origem%"=="2" if "%destino%"=="3" set /a res=valor*560/512
if "%origem%"=="2" if "%destino%"=="4" set /a res=valor*650/512
if "%origem%"=="2" if "%destino%"=="5" set /a res=valor*520/51200
if "%origem%"=="2" if "%destino%"=="6" set /a res=valor*71*512/51200

if "%origem%"=="3" if "%destino%"=="1" set /a res=valor*100/560
if "%origem%"=="3" if "%destino%"=="2" set /a res=valor*512/560
if "%origem%"=="3" if "%destino%"=="4" set /a res=valor*650/560
if "%origem%"=="3" if "%destino%"=="5" set /a res=valor*520/56000
if "%origem%"=="3" if "%destino%"=="6" set /a res=valor*71*560/56000

if "%origem%"=="4" if "%destino%"=="1" set /a res=valor*100/650
if "%origem%"=="4" if "%destino%"=="2" set /a res=valor*512/650
if "%origem%"=="4" if "%destino%"=="3" set /a res=valor*560/650
if "%origem%"=="4" if "%destino%"=="5" set /a res=valor*520/65000
if "%origem%"=="4" if "%destino%"=="6" set /a res=valor*71*650/65000

if "%origem%"=="5" if "%destino%"=="1" set /a res=valor*520/100000
if "%origem%"=="5" if "%destino%"=="2" set /a res=valor*512/100*520/100000
if "%origem%"=="5" if "%destino%"=="3" set /a res=valor*560/100*520/100000
if "%origem%"=="5" if "%destino%"=="4" set /a res=valor*650/100*520/100000
if "%origem%"=="5" if "%destino%"=="6" set /a res=valor*71/100*520/100000

if "%origem%"=="6" if "%destino%"=="1" set /a res=valor*71/100
if "%origem%"=="6" if "%destino%"=="2" set /a res=valor*512/7100
if "%origem%"=="6" if "%destino%"=="3" set /a res=valor*560/7100
if "%origem%"=="6" if "%destino%"=="4" set /a res=valor*650/7100
if "%origem%"=="6" if "%destino%"=="5" set /a res=valor*520/100*71/100

echo Resultado: %res%
:conv_fim
echo.
echo [1] Nova conversao
echo [2] Voltar
echo [3] Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto conversor
if "%op%"=="2" goto revolucionarias
if "%op%"=="3" goto inicio
goto revolucionarias

:hipoteca
cls
echo ╔═══════════════════════════════════════╗
echo ║          CALCULADORA DE HIPOTECA      ║
echo ╚═══════════════════════════════════════╝
set /p imovel="Valor do imovel R$: "
set /p entrada="Entrada R$: "
set /p juros="Juros anual %%: "
set /p p="Prazo (anos): "
set /a fin=imovel-entrada
echo Valor financiado: R$ %fin%
set /a par=fin/(p*12)
echo Parcela aprox: R$ %par%/mes
set /a tot=fin+(fin*juros*p/100)
echo Total final: R$ %tot%
echo.
echo [1] Nova simulacao
echo [2] Voltar
echo [3] Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto hipoteca
if "%op%"=="2" goto revolucionarias
if "%op%"=="3" goto inicio
goto revolucionarias

:negocios
cls
echo ╔═══════════════════════════════════════╗
echo ║         SIMULADOR DE NEGOCIOS        ║
echo ╚═══════════════════════════════════════╝
set /p inv="Investimento inicial R$: "
set /p fixos="Custos fixos/mes R$: "
set /p var="Custos variaveis %%: "
set /p preco="Preco venda R$: "
set /p vmes="Vendas esperadas/mes: "
set /a rec=preco*vmes
set /a cust=fixos+(preco*var/100)*vmes
set /a luc=rec-cust
echo Receita mensal: R$ %rec%
echo Custos mensais: R$ %cust%
echo Lucro liquido: R$ %luc%
if %luc% LEQ 0 (
    echo ATENCAO: Negocio deficitario!
) else (
    echo Negocio lucrativo!
)
echo.
echo [1] Nova simulacao
echo [2] Voltar
echo [3] Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto negocios
if "%op%"=="2" goto revolucionarias
if "%op%"=="3" goto inicio
goto revolucionarias

:cartao
cls
echo ╔═══════════════════════════════════════╗
echo ║    JUROS DO CARTAO DE CREDITO        ║
echo ╚═══════════════════════════════════════╝
set /p div="Divida atual R$: "
set /p j="Juros mensal %%: "
set /p pg="Pagamento mensal R$: "
set /a s=div-(pg-(div*j/100))
echo Proximo saldo aprox: R$ %s%
echo.
echo Aviso: Evite pagar apenas o minimo!
echo Juros rotativo pode chegar a 300%% ao ano
echo.
echo [1] Nova simulacao
echo [2] Voltar
echo [3] Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto cartao
if "%op%"=="2" goto revolucionarias
if "%op%"=="3" goto inicio
goto revolucionarias

:planejador
cls
echo ╔═══════════════════════════════════════╗
echo ║     PLANEJADOR FINANCEIRO PESSOAL    ║
echo ╚═══════════════════════════════════════╝
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
    echo ATENCAO: Saldo negativo!
) else (
    echo Saldo positivo!
)
echo.
echo [1] Novo planejamento
echo [2] Voltar
echo [3] Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto planejador
if "%op%"=="2" goto revolucionarias
if "%op%"=="3" goto inicio
goto revolucionarias

:emprestimo
cls
echo ╔═══════════════════════════════════════╗
echo ║       CALCULADORA DE EMPRESTIMOS     ║
echo ╚═══════════════════════════════════════╝
set /p val="Valor do emprestimo R$: "
set /p i="Juros mensal %%: "
set /p p="Parcelas: "
if "%p%"=="0" (
    echo Erro: numero de parcelas invalido!
    pause
    goto revolucionarias
)
set /a par=val/p
set /a jt=val*i*p/100
set /a tot=val+jt
echo Parcela aprox: R$ %par%
echo Total de juros: R$ %jt%
echo Valor total: R$ %tot%
echo.
echo [1] Nova simulacao
echo [2] Voltar
echo [3] Menu Principal
set /p op="Escolha: "
if "%op%"=="1" goto emprestimo
if "%op%"=="2" goto revolucionarias
if "%op%"=="3" goto inicio
goto revolucionarias

:sair
cls
echo.
echo Obrigado por usar a HP 12C!
echo Calculadora Financeira Revolucionaria
echo.
pause
exit