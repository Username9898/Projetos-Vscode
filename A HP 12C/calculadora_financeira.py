"""
+-----------------------------------------------------------------+
|          HP-12C - CALCULADORA FINANCEIRA                        |
|          Emulador Completo em Python                            |
+-----------------------------------------------------------------+

Funcionalidades:
  * RPN (Notacao Polonesa Reversa) com pilha de 4 niveis
  * Funcoes financeiras: PV, FV, PMT, N, i (juros compostos)
  * Juros Simples e Compostos
  * Tabela Price (Sistema Frances) e SAC
  * VPL, TIR, Payback, MIRR
  * Amortizacao detalhada
  * Simulador de aposentadoria, financiamento, cartao, negocios
  * Conversor de moedas, Impostos (IRPF, Simples, PIS, COFINS)
  * Tesouro Direto (Prefixado, Selic)
  * Precisao Decimal (28 casas) - fidelidade HP-12C
"""

from decimal import Decimal, getcontext, ROUND_HALF_UP
import math
import sys
from typing import List, Optional, Union, Dict, Any, Tuple

# Configuracao de precisao
getcontext().prec = 28
getcontext().rounding = ROUND_HALF_UP


def to_dec(valor: Union[int, float, str, Decimal]) -> Decimal:
    """Converte para Decimal com seguranca."""
    if isinstance(valor, Decimal):
        return valor
    if isinstance(valor, float):
        return Decimal(str(valor))
    return Decimal(valor)


def validar_positivo(valor, nome="valor"):
    """Valida que o valor e positivo."""
    v = to_dec(valor)
    if v <= 0:
        raise ValueError(f"{nome} deve ser positivo")
    return v


def validar_nao_negativo(valor, nome="valor"):
    """Valida que o valor e nao negativo."""
    v = to_dec(valor)
    if v < 0:
        raise ValueError(f"{nome} nao pode ser negativo")
    return v


# ================================================================
# CLASSE RPN - NOTACAO POLONESA REVERSA (Pilha HP-12C)
# ================================================================
class RPN:
    """
    Pilha de 4 niveis como a HP-12C real.
    T, Z, Y, X (do fundo ao topo).
    Enter empurra X para Y.
    """
    def __init__(self):
        self.pilha = [Decimal('0')] * 4  # [T, Z, Y, X]
        self.ultimo_x = Decimal('0')
        self.modo_begin = False  # True = BEGIN (pagamento no inicio)
        self.p_anual = 12  # periodos por ano (12 = mensal)
        self.registradores = [Decimal('0')] * 10  # R0-R9

    @property
    def x(self) -> Decimal:
        return self.pilha[3]

    @x.setter
    def x(self, valor: Decimal):
        self.pilha[3] = valor

    @property
    def y(self) -> Decimal:
        return self.pilha[2]

    @property
    def z(self) -> Decimal:
        return self.pilha[1]

    @property
    def t(self) -> Decimal:
        return self.pilha[0]

    def enter(self):
        """Enter empurra X para Y, preserva T."""
        self.ultimo_x = self.x
        self.pilha = [self.pilha[1], self.pilha[2], self.pilha[3], self.pilha[3]]

    def descer(self):
        """Roll down: T->Z->Y->X"""
        self.pilha = [self.pilha[3], self.pilha[0], self.pilha[1], self.pilha[2]]

    def subir(self):
        """Roll up: X->Y->Z->T"""
        self.pilha = [self.pilha[1], self.pilha[2], self.pilha[3], self.pilha[0]]

    def limpar(self):
        """Clear all registers"""
        self.pilha = [Decimal('0')] * 4
        self.ultimo_x = Decimal('0')

    def trocar_xy(self):
        """Troca X e Y (equivalente a CHS na HP)"""
        self.pilha[2], self.pilha[3] = self.pilha[3], self.pilha[2]

    def chs(self):
        """Change sign of X"""
        self.x = -self.x

    def __repr__(self):
        return f"T:{self.t} Z:{self.z} Y:{self.y} X:{self.x}"


# ================================================================
# FUNCOES FINANCEIRAS CENTRAIS (HP-12C)
# ================================================================

def _fator_juros(i: Decimal, n: Decimal) -> Decimal:
    """(1 + i)^n - fator de juros composto"""
    return (1 + i) ** n


def valor_presente(pmt: Decimal, i: Decimal, n: Decimal, begin: bool = False) -> Decimal:
    """
    PV = PMT x [1 - (1+i)^(-n)] / i x (1 + i)^(begin)
    Equivalente a tecla PV da HP-12C.
    """
    if i == 0:
        vp = pmt * n
    else:
        vp = pmt * (1 - _fator_juros(i, -n)) / i

    if begin:
        vp *= (1 + i)

    return vp


def valor_futuro(pmt: Decimal, i: Decimal, n: Decimal, begin: bool = False) -> Decimal:
    """
    FV = PMT x [(1+i)^n - 1] / i x (1 + i)^(begin)
    Equivalente a tecla FV da HP-12C.
    """
    if i == 0:
        fv = pmt * n
    else:
        fv = pmt * (_fator_juros(i, n) - 1) / i

    if begin:
        fv *= (1 + i)

    return fv


def pagamento(pv: Decimal, fv: Decimal, i: Decimal, n: Decimal, begin: bool = False) -> Decimal:
    """
    PMT = (PV + FV/(1+i)^n) x i / [1 - (1+i)^(-n)] / (1 + i)^(begin)
    Equivalente a tecla PMT da HP-12C.
    """
    if i == 0:
        if n == 0:
            return Decimal('0')
        return -(pv + fv) / n

    fator_begin = (1 + i) if begin else Decimal('1')
    fv_pv = fv / _fator_juros(i, n)

    pmt = -(pv + fv_pv) * i / (1 - _fator_juros(i, -n)) / fator_begin
    return pmt


def periodo(pv: Decimal, fv: Decimal, pmt: Decimal, i: Decimal, begin: bool = False) -> Decimal:
    """
    N = log((PMT x (1+i)^(begin) - FV x i) / (PMT x (1+i)^(begin) + PV x i)) / log(1 + i)
    Equivalente a tecla N da HP-12C.
    """
    if i == 0:
        if pmt == 0:
            return Decimal('0')
        return -(pv + fv) / pmt

    fator_begin = (1 + i) if begin else Decimal('1')
    pmt_ajustado = pmt * fator_begin

    if pmt_ajustado == 0:
        return Decimal('0')

    try:
        num = (pmt_ajustado - fv * i) / (pmt_ajustado + pv * i)
        if num <= 0:
            raise ValueError("Nao e possivel calcular N (log de numero nao positivo)")
        return num.ln() / (1 + i).ln()
    except Exception:
        raise ValueError("Nao foi possivel calcular o numero de periodos")


def taxa_juros(pv: Decimal, fv: Decimal, pmt: Decimal, n: Decimal,
               begin: bool = False, guess: Decimal = Decimal('0.01'),
               tol: Decimal = Decimal('1e-10'), max_iter: int = 1000) -> Decimal:
    """
    Calcula a taxa de juros (i) resolvendo a equacao:
    PV + PMT x (1 + i)^(begin) x [1 - (1+i)^(-n)] / i + FV / (1+i)^n = 0

    Usa Newton-Raphson com bissecao como fallback.
    Equivalente a tecla i da HP-12C.
    """
    fator_begin = (1 + guess) if begin else Decimal('1')

    def funcao_taxa(r: Decimal) -> Decimal:
        if r == 0:
            return pv + fv + pmt * n
        fj = _fator_juros(r, n)
        return pv + pmt * fator_begin * (1 - 1/fj) / r + fv / fj

    def derivada_taxa(r: Decimal) -> Decimal:
        if r == 0:
            n_dec = n
            return (-n_dec * (n_dec + 1) * pmt) / 2 - n_dec * fv
        fj = _fator_juros(r, n)
        fj_m1 = _fator_juros(r, -n - 1)
        return (pmt * fator_begin *
                (n * r * fj_m1 + 1/fj - 1) / (r * r) -
                n * fv * fj_m1)

    rate = guess
    for _ in range(max_iter):
        f_val = funcao_taxa(rate)
        if abs(f_val) < tol:
            return rate

        d_val = derivada_taxa(rate)
        if d_val == 0:
            break

        rate_novo = rate - f_val / d_val

        if abs(rate_novo - rate) < tol:
            return rate_novo

        rate = rate_novo

    return _taxa_bissecao(pv, fv, pmt, n, begin, tol, max_iter)


def _taxa_bissecao(pv: Decimal, fv: Decimal, pmt: Decimal, n: Decimal,
                   begin: bool = False, tol: Decimal = Decimal('1e-10'),
                   max_iter: int = 10000) -> Decimal:
    """Bissecao como fallback para calculo de taxa."""
    fator_begin = (1 + Decimal('0.01')) if begin else Decimal('1')

    def f(r: Decimal) -> Decimal:
        if r == 0:
            return pv + fv + pmt * n
        fj = _fator_juros(r, n)
        return pv + pmt * fator_begin * (1 - 1/fj) / r + fv / fj

    low, high = Decimal('-0.9999'), Decimal('10')

    f_low = f(low)
    f_high = f(high)

    tentativas = 0
    while f_low * f_high > 0 and tentativas < 20:
        high *= 2
        f_high = f(high)
        tentativas += 1

    if f_low * f_high > 0:
        low, high = Decimal('-10'), Decimal('0.9999')
        f_low = f(low)
        f_high = f(high)
        tentativas = 0
        while f_low * f_high > 0 and tentativas < 20:
            low *= 2
            f_low = f(low)
            tentativas += 1

    for _ in range(max_iter):
        mid = (low + high) / 2
        f_mid = f(mid)

        if abs(f_mid) < tol:
            return mid

        if f_mid * f(low) < 0:
            high = mid
        else:
            low = mid

    return (low + high) / 2


# ================================================================
# FUNCOES CLASSICAS (API publica)
# ================================================================

def juros_simples(capital: Union[float, int, str, Decimal],
                  taxa: Union[float, int, str, Decimal],
                  tempo: Union[float, int, str, Decimal]) -> Tuple[float, float]:
    """
    J = P * i * t
    M = P + J
    """
    c = to_dec(capital)
    i = to_dec(taxa)
    t = to_dec(tempo)

    juros = c * i * t
    montante = c + juros
    return float(juros), float(montante)


def juros_compostos(capital: Union[float, int, str, Decimal],
                    taxa: Union[float, int, str, Decimal],
                    tempo: Union[float, int, str, Decimal]) -> Tuple[float, float]:
    """
    M = P * (1 + i)^t
    J = M - P
    """
    c = to_dec(capital)
    i = to_dec(taxa)
    t = to_dec(tempo)

    montante = c * _fator_juros(i, t)
    juros = montante - c
    return float(juros), float(montante)


def valor_presente_unico(vf: Union[float, int, str, Decimal],
                         taxa: Union[float, int, str, Decimal],
                         tempo: Union[float, int, str, Decimal]) -> float:
    """
    VP = VF / (1 + i)^t
    Valor presente de um unico valor futuro.
    """
    return float(to_dec(vf) / _fator_juros(to_dec(taxa), to_dec(tempo)))


def valor_futuro_unico(vp: Union[float, int, str, Decimal],
                       taxa: Union[float, int, str, Decimal],
                       tempo: Union[float, int, str, Decimal]) -> float:
    """
    VF = VP * (1 + i)^t
    Valor futuro de um unico valor presente.
    """
    return float(to_dec(vp) * _fator_juros(to_dec(taxa), to_dec(tempo)))


def pmt_price(valor: Union[float, int, str, Decimal],
              taxa: Union[float, int, str, Decimal],
              n_periodos: Union[float, int, str, Decimal],
              begin: bool = False) -> float:
    """
    PMT = PV * i * (1+i)^n / [(1+i)^n - 1] * (1+i)^(begin)
    Tabela Price: parcelas iguais com juros sobre saldo decrescente.
    Retorna valor absoluto (positivo) da parcela.
    """
    pv = to_dec(valor)
    i = to_dec(taxa)
    n = to_dec(n_periodos)

    return abs(float(pagamento(pv, Decimal('0'), i, n, begin)))


def sac(valor: Union[float, int, str, Decimal],
        taxa: Union[float, int, str, Decimal],
        n_periodos: Union[float, int, str, Decimal]) -> List[Dict[str, Any]]:
    """
    SAC: Amortizacao constante, juros decrescentes.
    """
    pv = to_dec(valor)
    i = to_dec(taxa)
    n = int(to_dec(n_periodos))

    amortizacao = pv / n
    saldo = pv
    parcelas = []

    for periodo in range(1, n + 1):
        saldo_inicial = saldo
        juros = saldo * i
        parcela = amortizacao + juros
        saldo -= amortizacao

        parcelas.append({
            'periodo': periodo,
            'saldo_inicial': float(saldo_inicial),
            'amortizacao': float(amortizacao),
            'juros': float(juros),
            'parcela': float(parcela),
            'saldo_final': float(max(saldo, 0))
        })

    return parcelas


def sacre(valor: Union[float, int, str, Decimal],
          entrada: Union[float, int, str, Decimal],
          taxa: Union[float, int, str, Decimal],
          n_periodos: Union[float, int, str, Decimal]) -> List[Dict[str, Any]]:
    """
    SACRE: Sistema de Amortizacao Constante com Entrada.
    PV_efetivo = PV - entrada
    """
    pv_efetivo = to_dec(valor) - to_dec(entrada)
    if pv_efetivo <= 0:
        raise ValueError("Valor financiado (valor - entrada) deve ser positivo")
    return sac(pv_efetivo, taxa, n_periodos)


def vpl(taxa: Union[float, int, str, Decimal],
        fluxos: List[Union[float, int, str, Decimal]]) -> float:
    """
    VPL = Soma [CF_t / (1 + i)^t]   para t = 0..n
    """
    i = to_dec(taxa)
    total = Decimal('0')

    for t, cf in enumerate(fluxos):
        total += to_dec(cf) / _fator_juros(i, Decimal(t))

    return float(total)


def tir(fluxos: List[Union[float, int, str, Decimal]],
        guess: float = 0.1,
        tol: float = 1e-10,
        max_iter: int = 1000) -> float:
    """
    IRR usando Newton-Raphson com fallback para bissecao.
    """
    fluxos_dec = [to_dec(cf) for cf in fluxos]

    tem_positivo = any(cf > 0 for cf in fluxos_dec)
    tem_negativo = any(cf < 0 for cf in fluxos_dec)

    if not (tem_positivo and tem_negativo):
        raise ValueError("TIR requer pelo menos uma mudanca de sinal nos fluxos")

    rate = Decimal(str(guess))

    for _ in range(max_iter):
        npv = Decimal('0')
        d_npv = Decimal('0')

        for t, cf in enumerate(fluxos_dec):
            denominador = _fator_juros(rate, Decimal(t))
            npv += cf / denominador
            if t > 0:
                d_npv += -Decimal(t) * cf / _fator_juros(rate, Decimal(t + 1))

        if d_npv == 0:
            break

        new_rate = rate - npv / d_npv

        if abs(new_rate - rate) < Decimal(str(tol)):
            return float(new_rate)

        rate = new_rate

    return _tir_bissecao(fluxos_dec, Decimal(str(tol)), max_iter)


def _tir_bissecao(fluxos: List[Decimal],
                  tol: Decimal = Decimal('1e-10'),
                  max_iter: int = 10000) -> float:
    """Fallback usando metodo da bissecao para TIR."""

    def npv_fn(r: Decimal) -> Decimal:
        total = Decimal('0')
        for t, cf in enumerate(fluxos):
            total += cf / _fator_juros(r, Decimal(t))
        return total

    low, high = Decimal('-0.9999'), Decimal('10')

    for _ in range(50):
        npv_low = npv_fn(low)
        npv_high = npv_fn(high)

        if npv_low == 0:
            return float(low)
        if npv_high == 0:
            return float(high)

        if npv_low * npv_high < 0:
            break

        high *= 2
        low = min(low * 2, Decimal('-100'))

    for _ in range(max_iter):
        mid = (low + high) / 2
        npv_mid = npv_fn(mid)

        if abs(npv_mid) < tol:
            return float(mid)

        if npv_fn(low) * npv_mid < 0:
            high = mid
        else:
            low = mid

    return float((low + high) / 2)


def mirr(fluxos: List[Union[float, int, str, Decimal]],
         taxa_reinvestimento: Union[float, int, str, Decimal],
         taxa_financiamento: Union[float, int, str, Decimal]) -> float:
    """
    MIRR = (VF_inflows / PV_outflows)^(1/n) - 1
    """
    f = to_dec(taxa_financiamento)
    r = to_dec(taxa_reinvestimento)
    n_fluxos = len(fluxos)

    pv_outflows = Decimal('0')
    fv_inflows = Decimal('0')
    n = Decimal(n_fluxos - 1)

    for t, cf in enumerate(fluxos):
        cf_dec = to_dec(cf)
        if cf_dec < 0:
            pv_outflows += abs(cf_dec) / _fator_juros(f, Decimal(t))
        else:
            fv_inflows += cf_dec * _fator_juros(r, n - Decimal(t))

    if pv_outflows == 0 or fv_inflows == 0:
        return 0.0

    mirr_rate = (fv_inflows / pv_outflows) ** (1 / n) - 1
    return float(mirr_rate)


def payback(fluxos: List[Union[float, int, str, Decimal]]) -> Optional[float]:
    """Periodo de payback simples (sem descontar)."""
    acumulado = Decimal('0')
    for i, cf in enumerate(fluxos):
        acumulado += to_dec(cf)
        if acumulado >= 0:
            return float(i)
    return None


def payback_descontado(fluxos: List[Union[float, int, str, Decimal]],
                       taxa: Union[float, int, str, Decimal]) -> Optional[float]:
    """Periodo de payback descontado."""
    acumulado = Decimal('0')
    i = to_dec(taxa)

    for t, cf in enumerate(fluxos):
        vp = to_dec(cf) / _fator_juros(i, Decimal(t))
        acumulado += vp
        if acumulado >= 0:
            return float(t)
    return None


def tabela_price(valor: Union[float, int, str, Decimal],
                 taxa: Union[float, int, str, Decimal],
                 n_periodos: Union[float, int, str, Decimal],
                 begin: bool = False) -> List[Dict[str, Any]]:
    """
    Gera tabela de amortizacao completa (Sistema Price / Frances).
    """
    pv = to_dec(valor)
    i = to_dec(taxa)
    n = int(to_dec(n_periodos))

    parcela = pagamento(pv, Decimal('0'), i, Decimal(n), begin)
    saldo = pv
    tabela = []

    for periodo in range(1, n + 1):
        saldo_inicial = saldo
        juros = saldo * i
        amortizacao = parcela - juros
        saldo -= amortizacao

        tabela.append({
            'periodo': periodo,
            'saldo_inicial': float(saldo_inicial),
            'juros': float(juros),
            'amortizacao': float(amortizacao),
            'parcela': float(parcela),
            'saldo_final': float(max(saldo, 0))
        })

    return tabela


def financiamento_imobiliario(imovel: Union[float, int, str, Decimal],
                               entrada: Union[float, int, str, Decimal],
                               taxa_anual: Union[float, int, str, Decimal],
                               anos: Union[float, int, str, Decimal]) -> Dict[str, Any]:
    """
    Financiamento imobiliario completo com parcelas mensais.
    """
    pv = to_dec(imovel) - to_dec(entrada)
    if pv <= 0:
        raise ValueError("Valor financiado deve ser positivo")

    i_mensal = to_dec(taxa_anual) / 12
    n_meses = int(to_dec(anos) * 12)

    parcela = pagamento(pv, Decimal('0'), i_mensal, Decimal(n_meses))
    total_pago = parcela * n_meses
    total_juros = total_pago - pv

    return {
        'valor_financiado': float(pv),
        'parcela_mensal': abs(float(parcela)),
        'total_pago': abs(float(total_pago)),
        'total_juros': abs(float(total_juros)),
        'entrada': float(entrada)
    }


def aposentadoria(valor_inicial: Union[float, int, str, Decimal],
                  aporte_mensal: Union[float, int, str, Decimal],
                  taxa_mensal: Union[float, int, str, Decimal],
                  anos: Union[float, int, str, Decimal]) -> float:
    """
    Simula acumulacao para aposentadoria com aportes mensais.
    Formula: M = P*(1+i)^n + A * [(1+i)^n - 1] / i
    """
    pv = to_dec(valor_inicial)
    pmt = to_dec(aporte_mensal)
    i = to_dec(taxa_mensal)
    n = int(anos * 12)

    fv_inicial = pv * _fator_juros(i, Decimal(n))
    fv_aportes = valor_futuro(pmt, i, Decimal(n), begin=True)

    return float(fv_inicial + fv_aportes)


def tesouro_prefixado(valor: Union[float, int, str, Decimal],
                       taxa_anual: Union[float, int, str, Decimal],
                       anos: Union[float, int, str, Decimal]) -> float:
    """Tesouro Prefixado - retorno fixo."""
    return float(to_dec(valor) * _fator_juros(to_dec(taxa_anual), to_dec(anos)))


def tesouro_selic(valor: Union[float, int, str, Decimal],
                   taxa_selic: Union[float, int, str, Decimal],
                   anos: Union[float, int, str, Decimal]) -> float:
    """Tesouro Selic - acompanha CDI/Selic."""
    return tesouro_prefixado(valor, taxa_selic, anos)


# ================================================================
# CONVERSOR DE MOEDAS
# ================================================================

class ConversorMoedas:
    """
    Conversor de moedas com taxas de referencia.
    Taxas base: 1 moeda = X BRL
    """
    def __init__(self):
        self.taxas = {
            'BRL': Decimal('1.0'),
            'USD': Decimal('5.12'),
            'EUR': Decimal('5.60'),
            'GBP': Decimal('6.50'),
            'ARS': Decimal('0.0052'),
            'CNY': Decimal('0.71'),
            'JPY': Decimal('0.035'),
            'CAD': Decimal('3.80'),
            'AUD': Decimal('3.45'),
        }
        self.data_referencia = "24/06/2026 (taxas aproximadas - verificar cotacao do dia)"

    def converter(self, valor: Union[float, int, str, Decimal],
                  moeda_origem: str,
                  moeda_destino: str) -> float:
        """Converte valor entre moedas."""
        moeda_origem = moeda_origem.upper()
        moeda_destino = moeda_destino.upper()

        if moeda_origem not in self.taxas:
            raise ValueError(f"Moeda de origem nao suportada: {moeda_origem}")
        if moeda_destino not in self.taxas:
            raise ValueError(f"Moeda de destino nao suportada: {moeda_destino}")

        valor_brl = to_dec(valor) * self.taxas[moeda_origem]
        resultado = valor_brl / self.taxas[moeda_destino]

        return float(resultado)

    def atualizar_taxa(self, moeda: str, taxa: Union[float, int, str, Decimal]):
        """Atualiza taxa de cambio para uma moeda."""
        self.taxas[moeda.upper()] = to_dec(taxa)

    def adicionar_moeda(self, codigo: str, taxa_brl: Union[float, int, str, Decimal]):
        """Adiciona nova moeda ao conversor."""
        self.taxas[codigo.upper()] = to_dec(taxa_brl)


# ================================================================
# CALCULADORA DE IMPOSTOS
# ================================================================

class CalculadoraImpostos:
    """Modulo para calculo de impostos brasileiros (simplificado)."""

    @staticmethod
    def irrf_pf(rendimento: Union[float, int, str, Decimal]) -> float:
        """
        IRRF Pessoa Fisica - Tabela progressiva 2024/2025.
        """
        r = to_dec(rendimento)

        if r <= Decimal('2259.20'):
            return 0.0
        elif r <= Decimal('2826.65'):
            aliquota = Decimal('0.075')
            deducao = Decimal('169.44')
        elif r <= Decimal('3751.05'):
            aliquota = Decimal('0.15')
            deducao = Decimal('381.44')
        elif r <= Decimal('4664.68'):
            aliquota = Decimal('0.225')
            deducao = Decimal('662.77')
        else:
            aliquota = Decimal('0.275')
            deducao = Decimal('896.00')

        imposto = max(r * aliquota - deducao, Decimal('0'))
        return float(imposto)

    @staticmethod
    def irrf_pf_anual(rendimento_anual: Union[float, int, str, Decimal]) -> float:
        """IRPF Anual simplificado."""
        r = to_dec(rendimento_anual)
        r_mensal = r / 12
        return CalculadoraImpostos.irrf_pf(r_mensal) * 12

    @staticmethod
    def simples_nacional(faturamento_anual: Union[float, int, str, Decimal]) -> float:
        """
        Simples Nacional - Faixas simplificadas (anexo I - comercio).
        """
        f = to_dec(faturamento_anual)

        if f <= Decimal('180000'):
            aliquota = Decimal('0.06')
        elif f <= Decimal('360000'):
            aliquota = Decimal('0.112')
        elif f <= Decimal('720000'):
            aliquota = Decimal('0.135')
        elif f <= Decimal('1800000'):
            aliquota = Decimal('0.16')
        elif f <= Decimal('3600000'):
            aliquota = Decimal('0.21')
        else:
            aliquota = Decimal('0.33')

        return float(f * aliquota)

    @staticmethod
    def pis_pasep(valor: Union[float, int, str, Decimal]) -> float:
        """PIS/PASEP (simplificado) - 0,65% sobre receita."""
        return float(to_dec(valor) * Decimal('0.0065'))

    @staticmethod
    def cofins(valor: Union[float, int, str, Decimal]) -> float:
        """COFINS (simplificado) - 7,6% sobre receita."""
        return float(to_dec(valor) * Decimal('0.076'))

    @staticmethod
    def inss(salario: Union[float, int, str, Decimal]) -> float:
        """
        INSS 2024 - Tabela de contribuicao.
        """
        s = to_dec(salario)

        if s <= Decimal('1412.00'):
            aliquota = Decimal('0.075')
            deducao = Decimal('0')
        elif s <= Decimal('2666.68'):
            aliquota = Decimal('0.09')
            deducao = Decimal('21.18')
        elif s <= Decimal('4000.03'):
            aliquota = Decimal('0.12')
            deducao = Decimal('101.18')
        else:
            aliquota = Decimal('0.14')
            deducao = Decimal('181.18')

        contribuicao = max(s * aliquota - deducao, Decimal('0'))
        return float(contribuicao)


# ================================================================
# FUNCOES DE NEGOCIOS
# ================================================================

def negocios(custos_fixos: Union[float, int, str, Decimal],
             custo_var_unitario: Union[float, int, str, Decimal],
             preco_venda: Union[float, int, str, Decimal],
             vendas_mes: Union[float, int, str, Decimal]) -> float:
    """
    Simulador de negocios.
    """
    f = to_dec(custos_fixos)
    cv = to_dec(custo_var_unitario)
    p = to_dec(preco_venda)
    vm = to_dec(vendas_mes)

    receita = p * vm
    custos_variaveis_totais = cv * vm
    custos_totais = f + custos_variaveis_totais
    lucro = receita - custos_totais

    margem_contribuicao = p - cv
    ponto_equilibrio = f / margem_contribuicao if margem_contribuicao > 0 else float('inf')

    print(f"Receita mensal: R$ {float(receita):.2f}")
    print(f"Custos fixos: R$ {float(f):.2f}")
    print(f"Custos variaveis totais: R$ {float(custos_variaveis_totais):.2f}")
    print(f"Custos totais: R$ {float(custos_totais):.2f}")
    print(f"Lucro liquido: R$ {float(lucro):.2f}")
    print(f"Margem de contribuicao unitaria: R$ {float(margem_contribuicao):.2f}")
    print(f"Ponto de equilibrio: {float(ponto_equilibrio):.1f} unidades/mes")

    if lucro <= 0:
        print("ATENCAO: Negocio deficitario!")
    else:
        print("Negocio lucrativo!")

    return float(lucro)


def cartao_credito(divida: Union[float, int, str, Decimal],
                   juros_mensal: Union[float, int, str, Decimal],
                   pagamento_mensal: Union[float, int, str, Decimal]) -> float:
    """
    Simulador de cartao de credito.
    """
    d = to_dec(divida)
    j = to_dec(juros_mensal) / 100
    pg = to_dec(pagamento_mensal)

    juros_valor = d * j
    amortizacao = pg - juros_valor
    novo_saldo = d - amortizacao

    print(f"Divida atual: R$ {float(d):.2f}")
    print(f"Juros do periodo ({float(j)*100:.1f}%): R$ {float(juros_valor):.2f}")
    print(f"Pagamento: R$ {float(pg):.2f}")
    print(f"Amortizacao: R$ {float(max(amortizacao, 0)):.2f}")

    if novo_saldo >= d:
        print("ATENCAO: Pagamento insuficiente para cobrir os juros!")
        print("   A divida esta aumentando!")

    print(f"Novo saldo: R$ {float(novo_saldo):.2f}")

    if novo_saldo <= 0:
        print("Divida quitada!")

    return float(novo_saldo)


def planejador_financeiro(renda: Union[float, int, str, Decimal],
                          aluguel: Union[float, int, str, Decimal],
                          luz: Union[float, int, str, Decimal],
                          agua: Union[float, int, str, Decimal],
                          internet: Union[float, int, str, Decimal],
                          outros: Union[float, int, str, Decimal]) -> float:
    """
    Planejador financeiro pessoal.
    """
    r = to_dec(renda)
    despesas = (to_dec(aluguel) + to_dec(luz) + to_dec(agua) +
                to_dec(internet) + to_dec(outros))
    saldo = r - despesas

    percentual_gasto = float(despesas / r * 100) if r > 0 else 0

    print(f"Renda: R$ {float(r):.2f}")
    print(f"Despesas: R$ {float(despesas):.2f}")
    print(f"Saldo: R$ {float(saldo):.2f}")
    print(f"Percentual gasto: {percentual_gasto:.1f}%")

    if saldo <= 0:
        print("ATENCAO: Orcamento deficitario!")
        print("   Recomenda-se revisar os gastos.")
    else:
        if percentual_gasto > 70:
            print("Atencao: Mais de 70% da renda comprometida.")
        else:
            print("Orcamento equilibrado!")

    return float(saldo)


def margem_lucro(custo: Union[float, int, str, Decimal],
                  preco_venda: Union[float, int, str, Decimal]) -> Dict[str, float]:
    """
    Calcula margens de lucro sobre custo e sobre venda.
    """
    c = to_dec(custo)
    p = to_dec(preco_venda)

    if c <= 0 or p <= 0:
        raise ValueError("Custo e preco devem ser positivos")

    lucro = p - c
    margem_custo = lucro / c * 100
    margem_venda = lucro / p * 100

    return {
        'lucro': float(lucro),
        'margem_sobre_custo': float(margem_custo),
        'margem_sobre_venda': float(margem_venda),
        'markup': float(p / c)
    }


# ================================================================
# FUNCOES MATEMATICAS BASICAS
# ================================================================

def soma(a: Union[float, int, str, Decimal],
         b: Union[float, int, str, Decimal]) -> float:
    return float(to_dec(a) + to_dec(b))


def subtracao(a: Union[float, int, str, Decimal],
              b: Union[float, int, str, Decimal]) -> float:
    return float(to_dec(a) - to_dec(b))


def multiplicacao(a: Union[float, int, str, Decimal],
                  b: Union[float, int, str, Decimal]) -> float:
    return float(to_dec(a) * to_dec(b))


def divisao(a: Union[float, int, str, Decimal],
            b: Union[float, int, str, Decimal]) -> float:
    b_dec = to_dec(b)
    if b_dec == 0:
        raise ValueError("Divisao por zero!")
    return float(to_dec(a) / b_dec)


def porcentagem(valor: Union[float, int, str, Decimal],
                percentual: Union[float, int, str, Decimal]) -> float:
    """Calcula X% de Y."""
    return float(to_dec(valor) * to_dec(percentual) / 100)


def variacao_percentual(valor_antigo: Union[float, int, str, Decimal],
                        valor_novo: Union[float, int, str, Decimal]) -> float:
    """Calcula a variacao percentual entre dois valores."""
    va = to_dec(valor_antigo)
    vn = to_dec(valor_novo)
    if va == 0:
        raise ValueError("Valor antigo nao pode ser zero")
    return float((vn - va) / va * 100)


# ================================================================
# INTERFACE VIA LINHA DE COMANDO
# ================================================================

def calcular_despesas_mensais() -> Dict[str, float]:
    """Funcao interativa para calcular despesas mensais totais."""
    print("\n+-----------------------------------+")
    print("|     PLANEJADOR DE DESPESAS        |")
    print("+-----------------------------------+")

    try:
        renda = float(input("Renda mensal (R$): "))
        moradia = float(input("Aluguel/FInanciamento (R$): ") or "0")
        alimentacao = float(input("Alimentacao (R$): ") or "0")
        transporte = float(input("Transporte (R$): ") or "0")
        saude = float(input("Saude/Plano (R$): ") or "0")
        educacao = float(input("Educacao (R$): ") or "0")
        lazer = float(input("Lazer (R$): ") or "0")
        outros = float(input("Outros (R$): ") or "0")

        total = moradia + alimentacao + transporte + saude + educacao + lazer + outros
        saldo = renda - total
        perc = (total / renda * 100) if renda > 0 else 0

        print(f"\n{'='*40}")
        print(f"Total despesas: R$ {total:.2f}")
        print(f"Saldo disponivel: R$ {saldo:.2f}")
        print(f"Percentual comprometido: {perc:.1f}%")

        if saldo <= 0:
            print("ATENCAO: Saldo negativo!")
        elif perc > 70:
            print("Atencao: mais de 70% da renda comprometida.")
        else:
            print("Orcamento saudavel!")

        return {
            'renda': renda,
            'moradia': moradia,
            'alimentacao': alimentacao,
            'transporte': transporte,
            'saude': saude,
            'educacao': educacao,
            'lazer': lazer,
            'outros': outros,
            'total': total,
            'saldo': saldo,
            'percentual': perc
        }

    except ValueError as e:
        print(f"Erro: valor invalido - {e}")
        return {}


# ================================================================
# TESTES UNITARIOS
# ================================================================

def testar_calculadora():
    """Executa testes unitarios para validar precisao e logica."""
    print("\n" + "=" * 60)
    print("TESTES UNITARIOS - CALCULADORA FINANCEIRA HP-12C")
    print("=" * 60)

    testes = []
    erros = 0

    def testar(nome, func, args, esperado, tolerancia=0.01):
        nonlocal erros
        try:
            resultado = func(*args)
            if isinstance(resultado, tuple):
                resultado = resultado[0]

            # Trata comparacao com None
            if esperado is None:
                if resultado is None:
                    testes.append(f"[OK] {nome}: None (esperado None)")
                else:
                    testes.append(f"[FALHOU] {nome}: {resultado:.4f} (esperado None)")
                    erros += 1
            elif resultado is None:
                testes.append(f"[FALHOU] {nome}: None (esperado {esperado:.4f})")
                erros += 1
            else:
                if isinstance(esperado, tuple):
                    esperado = esperado[0]
                if abs(resultado - esperado) <= tolerancia:
                    testes.append(f"[OK] {nome}: {resultado:.4f} (esperado {esperado:.4f})")
                else:
                    testes.append(f"[FALHOU] {nome}: {resultado:.4f} (esperado {esperado:.4f}, erro={abs(resultado-esperado):.6f})")
                    erros += 1
        except Exception as e:
            testes.append(f"[ERRO] {nome}: {e}")
            erros += 1

    # Testes basicos
    testar("Soma", soma, [10, 20], 30)
    testar("Subtracao", subtracao, [50, 30], 20)
    testar("Multiplicacao", multiplicacao, [5, 6], 30)
    testar("Divisao", divisao, [10, 4], 2.5)

    # Testes de juros
    testar("Juros Simples", juros_simples, [1000, 0.1, 3], 300)
    testar("Juros Compostos", juros_compostos, [1000, 0.1, 3], 331)

    # Testes PV/FV
    testar("Valor Presente", valor_presente_unico, [1331, 0.1, 3], 1000)
    testar("Valor Futuro", valor_futuro_unico, [1000, 0.1, 3], 1331)

    # Teste PMT Price (R$1000, 1% a.m., 12 meses)
    # Formula: PMT = 1000 * 0.01 * (1.01^12) / (1.01^12 - 1) = 88.85
    testar("PMT Price (R$1000, 1% a.m., 12 meses)", pmt_price, [1000, 0.01, 12], 88.85)

    # Teste financiamento imobiliario (R$300.000, 8% a.a., 30 anos)
    # i_mensal = 0.08/12 = 0.006667, n = 360
    # PMT = 300000 * 0.006667 * (1.006667^360) / (1.006667^360 - 1) = 2201.29
    testar("Financiamento (R$300.000, 8% a.a., 30 anos)",
           lambda: financiamento_imobiliario(300000, 0, 0.08, 30)['parcela_mensal'],
           [], 2201.29)

    # Teste VPL (10%, fluxos [-1000, 500, 400, 300])
    # VPL = -1000 + 500/1.1 + 400/1.1^2 + 300/1.1^3
    # VPL = -1000 + 454.545 + 330.579 + 225.394 = 10.518
    testar("VPL (10%, fluxos [-1000,500,400,300])",
           vpl, [0.10, [-1000, 500, 400, 300]], 10.52, 0.01)

    # Teste TIR (fluxos [-1000, 500, 400, 300])
    # A TIR correta para esses fluxos eh ~10.65%
    testar("TIR (fluxos [-1000,500,400,300])",
           tir, [[-1000, 500, 400, 300]], 0.1065, 0.001)

    # Teste MIRR (fluxos [-1000,500,400,300], 10%, 8%)
    # FV_inflows = 500*1.1^2 + 400*1.1^1 + 300*1.1^0 = 605 + 440 + 300 = 1345
    # PV_outflows = 1000 / 1.08^0 = 1000
    # MIRR = (1345/1000)^(1/3) - 1 = 0.1038
    testar("MIRR (fluxos [-1000,500,400,300], 10%, 8%)",
           mirr, [[-1000, 500, 400, 300], 0.10, 0.08], 0.1038, 0.001)

    # Teste SAC (R$1000, 1% a.m., 12 meses)
    # Amortizacao = 1000/12 = 83.33, Juros 1o mes = 1000*0.01 = 10
    # Parcela 1 = 83.33 + 10 = 93.33
    testar("SAC parcela 1 (R$1000, 1% a.m., 12 meses)",
           lambda: sac(1000, 0.01, 12)[0]['parcela'], [], 93.33, 0.01)

    # Teste aposentadoria (R$0 inicio, R$500/mes, 0.5% a.m., 30 anos)
    # n = 360 meses
    # FV = 500 * ((1.005^360 - 1) / 0.005) * 1.005 = 504768.81
    testar("Aposentadoria (R$0 inicio, R$500/mes, 0.5% a.m., 30 anos)",
           aposentadoria, [0, 500, 0.005, 30], 504768.81, 1.0)

    # Teste tesouro
    testar("Tesouro Prefixado (R$10000, 10% a.a., 5 anos)",
           tesouro_prefixado, [10000, 0.10, 5], 16105.10, 0.01)

    # Teste IRRF (R$5000/mes)
    # 5000 * 0.275 - 896 = 1375 - 896 = 479
    testar("IRRF (R$5000/mes)",
           CalculadoraImpostos.irrf_pf, [5000], 479.00, 0.01)

    # Teste INSS (R$3000/mes)
    # 3000 * 0.12 - 101.18 = 360 - 101.18 = 258.82
    testar("INSS (R$3000/mes)",
           CalculadoraImpostos.inss, [3000], 258.82, 0.01)

    # Teste conversao USD -> BRL (100 USD)
    testar("Conversor USD->BRL (100 USD)",
           lambda: ConversorMoedas().converter(100, 'USD', 'BRL'), [], 512.00, 0.01)

    # Teste margem de lucro (custo R$10, venda R$25)
    # margem_sobre_venda = (25-10)/25 * 100 = 60%
    testar("Margem Lucro (custo R$10, venda R$25)",
           lambda: margem_lucro(10, 25)['margem_sobre_venda'], [], 60.0, 0.01)

    # Teste payback simples ([-5000, 2000, 2000, 2000])
    # acumulado: -5000, -3000, -1000, +1000 -> periodo 3
    testar("Payback Simples ([-5000, 2000, 2000, 2000])",
           payback, [[-5000, 2000, 2000, 2000]], 3, 0.01)

    # Teste payback descontado ([-5000, 2000, 2000, 2000], 10%)
    # VP: -5000, 1818.18, 1652.89, 1502.63
    # acumulado: -5000, -3181.82, -1528.93, -26.30 -> nunca >= 0 -> None
    testar("Payback Descontado ([-5000, 2000, 2000, 2000], 10%)",
           payback_descontado, [[-5000, 2000, 2000, 2000], 0.10], None)

    # Teste cartao de credito (R$1000, 15% juros, R$200 pagamento)
    # Juros = 1000 * 0.15 = 150, Amort = 200 - 150 = 50
    # Novo saldo = 1000 - 50 = 950
    testar("Cartao Credito (R$1000, 15% juros, R$200 pagamento)",
           cartao_credito, [1000, 15, 200], 950, 0.01)

    # Resultados
    print("\n" + "-" * 60)
    for t in testes:
        print(t)
    print("-" * 60)
    print(f"\nTotal: {len(testes)} testes | Sucesso: {len(testes)-erros} | Erros: {erros}")

    if erros == 0:
        print(">> Todos os testes passaram!")
    else:
        print(f">> {erros} teste(s) falharam.")

    print("=" * 60)
    return erros == 0


# ================================================================
# INTERFACE PRINCIPAL (CLI)
# ================================================================

def main_menu():
    """Exibe o menu principal interativo."""
    while True:
        print("\n" + "+" + "-" * 50 + "+")
        print("|         HP-12C CALCULADORA FINANCEIRA          |")
        print("|              Menu Principal                    |")
        print("+" + "-" * 50 + "+")
        print("  [1]  Juros Simples")
        print("  [2]  Juros Compostos")
        print("  [3]  Valor Presente (PV)")
        print("  [4]  Valor Futuro (FV)")
        print("  [5]  PMT - Tabela Price")
        print("  [6]  SAC - Amortizacao Constante")
        print("  [7]  SACRE - SAC com Entrada")
        print("  [8]  Tabela Price Completa")
        print("  [9]  VPL - Valor Presente Liquido")
        print("  [10] TIR - Taxa Interna de Retorno")
        print("  [11] MIRR - TIR Modificada")
        print("  [12] Payback e Payback Descontado")
        print("  [13] Financiamento Imobiliario")
        print("  [14] Simulador de Aposentadoria")
        print("  [15] Tesouro Direto")
        print("  [16] Conversor de Moedas")
        print("  [17] Calculadora de Impostos")
        print("  [18] Simulador de Negocios")
        print("  [19] Cartao de Credito")
        print("  [20] Planejador Financeiro")
        print("  [21] Margem de Lucro")
        print("  [22] Testes Unitarios")
        print("  [23] Calculadora de Despesas (Interativo)")
        print("  [0]  Sair")
        print("-" * 52)

        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "0":
            print("\nObrigado por usar a HP-12C!\n")
            break
        elif opcao == "22":
            testar_calculadora()
            input("\nPressione ENTER para continuar...")
        elif opcao == "23":
            calcular_despesas_mensais()
            input("\nPressione ENTER para continuar...")
        else:
            executar_opcao_cli(opcao)


def executar_opcao_cli(opcao: str):
    """Executa a opcao escolhida via argumentos de linha de comando."""
    try:
        if opcao == "1":
            c = float(input("Capital (R$): "))
            i = float(input("Taxa (decimal, ex: 0.1 = 10%): "))
            t = float(input("Tempo (periodos): "))
            j, m = juros_simples(c, i, t)
            print(f"\nJuros: R$ {j:.2f}")
            print(f"Montante: R$ {m:.2f}")

        elif opcao == "2":
            c = float(input("Capital (R$): "))
            i = float(input("Taxa (decimal, ex: 0.1 = 10%): "))
            t = float(input("Tempo (periodos): "))
            j, m = juros_compostos(c, i, t)
            print(f"\nJuros: R$ {j:.2f}")
            print(f"Montante: R$ {m:.2f}")

        elif opcao == "3":
            vf = float(input("Valor Futuro (R$): "))
            i = float(input("Taxa (decimal): "))
            t = float(input("Tempo (periodos): "))
            vp = valor_presente_unico(vf, i, t)
            print(f"\nValor Presente: R$ {vp:.2f}")

        elif opcao == "4":
            vp = float(input("Valor Presente (R$): "))
            i = float(input("Taxa (decimal): "))
            t = float(input("Tempo (periodos): "))
            vf = valor_futuro_unico(vp, i, t)
            print(f"\nValor Futuro: R$ {vf:.2f}")

        elif opcao == "5":
            v = float(input("Valor financiado (R$): "))
            i = float(input("Taxa por periodo (decimal): "))
            n = int(input("Numero de periodos: "))
            begin = input("BEGIN? (s/N): ").strip().lower() == 's'
            p = pmt_price(v, i, n, begin)
            print(f"\nValor da parcela (PMT): R$ {p:.2f}")

        elif opcao == "6":
            v = float(input("Valor financiado (R$): "))
            i = float(input("Taxa por periodo (decimal): "))
            n = int(input("Numero de periodos: "))
            parcelas = sac(v, i, n)
            print(f"\n{'Per':>3} {'Saldo Inicial':>14} {'Amortizacao':>12} {'Juros':>10} {'Parcela':>10} {'Saldo Final':>12}")
            print("-" * 62)
            for p in parcelas:
                print(f"{p['periodo']:>3} {p['saldo_inicial']:>14.2f} {p['amortizacao']:>12.2f} {p['juros']:>10.2f} {p['parcela']:>10.2f} {p['saldo_final']:>12.2f}")

        elif opcao == "7":
            v = float(input("Valor total (R$): "))
            e = float(input("Entrada (R$): "))
            i = float(input("Taxa por periodo (decimal): "))
            n = int(input("Numero de periodos: "))
            parcelas = sacre(v, e, i, n)
            print(f"\n{'Per':>3} {'Saldo Inicial':>14} {'Amortizacao':>12} {'Juros':>10} {'Parcela':>10} {'Saldo Final':>12}")
            print("-" * 62)
            for p in parcelas:
                print(f"{p['periodo']:>3} {p['saldo_inicial']:>14.2f} {p['amortizacao']:>12.2f} {p['juros']:>10.2f} {p['parcela']:>10.2f} {p['saldo_final']:>12.2f}")

        elif opcao == "8":
            v = float(input("Valor financiado (R$): "))
            i = float(input("Taxa por periodo (decimal): "))
            n = int(input("Numero de periodos: "))
            tabela = tabela_price(v, i, n)
            print(f"\n{'Per':>3} {'Saldo Inicial':>14} {'Juros':>10} {'Amortizacao':>12} {'Parcela':>10} {'Saldo Final':>12}")
            print("-" * 62)
            for p in tabela:
                print(f"{p['periodo']:>3} {p['saldo_inicial']:>14.2f} {p['juros']:>10.2f} {p['amortizacao']:>12.2f} {p['parcela']:>10.2f} {p['saldo_final']:>12.2f}")

        elif opcao == "9":
            inv = float(input("Investimento inicial (R$): "))
            fluxos_str = input("Fluxos de caixa futuros (separados por espaco): ")
            fluxos = [inv] + [float(f) for f in fluxos_str.split()]
            i = float(input("Taxa de desconto (decimal): "))
            result = vpl(i, fluxos)
            print(f"\nVPL: R$ {result:.2f}")
            if result > 0:
                print("Projeto vavel (VPL > 0)")
            elif result < 0:
                print("Projeto inviavel (VPL < 0)")
            else:
                print("VPL = 0 (indiferente)")

        elif opcao == "10":
            inv = float(input("Investimento inicial (R$): "))
            fluxos_str = input("Fluxos de caixa futuros (separados por espaco): ")
            fluxos = [inv] + [float(f) for f in fluxos_str.split()]
            irr = tir(fluxos)
            print(f"\nTIR: {irr*100:.2f}%")

        elif opcao == "11":
            inv = float(input("Investimento inicial (R$): "))
            fluxos_str = input("Fluxos de caixa futuros (separados por espaco): ")
            fluxos = [inv] + [float(f) for f in fluxos_str.split()]
            r = float(input("Taxa de reinvestimento (decimal): "))
            f = float(input("Taxa de financiamento (decimal): "))
            result = mirr(fluxos, r, f)
            print(f"\nMIRR: {result*100:.2f}%")

        elif opcao == "12":
            inv = float(input("Investimento inicial (R$): "))
            fluxos_str = input("Fluxos de caixa futuros (separados por espaco): ")
            fluxos = [inv] + [float(f) for f in fluxos_str.split()]

            pb = payback(fluxos)
            i = float(input("Taxa para payback descontado (decimal) ou 0 para pular: "))

            print(f"\nPayback Simples: periodo {pb}" if pb is not None else "\nPayback Simples: nao retorna")

            if i > 0:
                pbd = payback_descontado(fluxos, i)
                print(f"Payback Descontado ({i*100:.1f}%): periodo {pbd}" if pbd is not None else f"Payback Descontado ({i*100:.1f}%): nao retorna")

        elif opcao == "13":
            imovel = float(input("Valor do imovel (R$): "))
            entrada = float(input("Entrada (R$): "))
            taxa = float(input("Taxa anual (decimal, ex: 0.08 = 8%): "))
            anos = int(input("Prazo (anos): "))
            res = financiamento_imobiliario(imovel, entrada, taxa, anos)
            print(f"\nValor financiado: R$ {res['valor_financiado']:.2f}")
            print(f"Parcela mensal: R$ {res['parcela_mensal']:.2f}")
            print(f"Total pago: R$ {res['total_pago']:.2f}")
            print(f"Total em juros: R$ {res['total_juros']:.2f}")

        elif opcao == "14":
            vi = float(input("Valor inicial (R$): "))
            ap = float(input("Aporte mensal (R$): "))
            tx = float(input("Taxa mensal (decimal): "))
            anos = int(input("Anos ate aposentadoria: "))
            saldo = aposentadoria(vi, ap, tx, anos)
            print(f"\nSaldo acumulado: R$ {saldo:,.2f}")

        elif opcao == "15":
            print("\n[1] Tesouro Prefixado")
            print("[2] Tesouro Selic")
            sub = input("Escolha: ")
            v = float(input("Valor investido (R$): "))
            tx = float(input("Taxa anual (decimal): "))
            anos = int(input("Periodo (anos): "))
            if sub == "1":
                res = tesouro_prefixado(v, tx, anos)
            else:
                res = tesouro_selic(v, tx, anos)
            print(f"\nValor Futuro: R$ {res:,.2f}")

        elif opcao == "16":
            valor = float(input("Valor: "))
            origem = input("Moeda origem (USD, EUR, BRL, etc): ").upper()
            destino = input("Moeda destino: ").upper()
            conv = ConversorMoedas()
            res = conv.converter(valor, origem, destino)
            print(f"\n{valor:.2f} {origem} ~ {res:.2f} {destino}")
            print(f"[Atencao: {conv.data_referencia}]")

        elif opcao == "17":
            print("\n[1] IRRF Pessoa Fisica")
            print("[2] Simples Nacional")
            print("[3] PIS/PASEP")
            print("[4] COFINS")
            print("[5] INSS")
            sub = input("Escolha: ")
            v = float(input("Valor (R$): "))
            if sub == "1":
                res = CalculadoraImpostos.irrf_pf(v)
                print(f"IRRF: R$ {res:.2f}")
            elif sub == "2":
                res = CalculadoraImpostos.simples_nacional(v)
                print(f"Simples Nacional: R$ {res:.2f}")
            elif sub == "3":
                res = CalculadoraImpostos.pis_pasep(v)
                print(f"PIS/PASEP: R$ {res:.2f}")
            elif sub == "4":
                res = CalculadoraImpostos.cofins(v)
                print(f"COFINS: R$ {res:.2f}")
            elif sub == "5":
                res = CalculadoraImpostos.inss(v)
                print(f"INSS: R$ {res:.2f}")

        elif opcao == "18":
            f = float(input("Custos fixos mensais (R$): "))
            cv = float(input("Custo variavel unitario (R$): "))
            pr = float(input("Preco de venda (R$): "))
            vm = int(input("Vendas por mes: "))
            negocios(f, cv, pr, vm)

        elif opcao == "19":
            d = float(input("Saldo devedor (R$): "))
            j = float(input("Juros mensal (%): "))
            pg = float(input("Pagamento mensal (R$): "))
            cartao_credito(d, j, pg)

        elif opcao == "20":
            print("Informe suas financas mensais:")
            renda = float(input("Renda (R$): "))
            alug = float(input("Aluguel (R$): ") or "0")
            luz = float(input("Luz (R$): ") or "0")
            agua = float(input("Agua (R$): ") or "0")
            net = float(input("Internet (R$): ") or "0")
            outros = float(input("Outros (R$): ") or "0")
            planejador_financeiro(renda, alug, luz, agua, net, outros)

        elif opcao == "21":
            custo = float(input("Custo do produto (R$): "))
            preco = float(input("Preco de venda (R$): "))
            res = margem_lucro(custo, preco)
            print(f"\nLucro: R$ {res['lucro']:.2f}")
            print(f"Margem sobre custo: {res['margem_sobre_custo']:.1f}%")
            print(f"Margem sobre venda: {res['margem_sobre_venda']:.1f}%")
            print(f"Markup: {res['markup']:.2f}x")

        else:
            print("Opcao invalida!")

        input("\nPressione ENTER para continuar...")

    except Exception as e:
        print(f"Erro: {e}")
        input("\nPressione ENTER para continuar...")


# ================================================================
# ENTRY POINT
# ================================================================

def main():
    """Ponto de entrada principal."""
    if len(sys.argv) < 2:
        main_menu()
    else:
        funcao = sys.argv[1]

        try:
            if funcao in ["soma", "subtracao", "multiplicacao", "divisao"]:
                ops = {
                    "soma": soma,
                    "subtracao": subtracao,
                    "multiplicacao": multiplicacao,
                    "divisao": divisao
                }
                resultado = ops[funcao](sys.argv[2], sys.argv[3])
                print(f"Resultado: {resultado:.2f}")

            elif funcao == "porcentagem":
                resultado = porcentagem(sys.argv[2], sys.argv[3])
                print(f"Resultado: {resultado:.2f}")

            elif funcao == "variacao_percentual":
                resultado = variacao_percentual(sys.argv[2], sys.argv[3])
                print(f"Variacao: {resultado:.2f}%")

            elif funcao == "juros_simples":
                j, m = juros_simples(sys.argv[2], sys.argv[3], sys.argv[4])
                print(f"Juros: R$ {j:.2f}")
                print(f"Montante: R$ {m:.2f}")

            elif funcao == "juros_compostos":
                j, m = juros_compostos(sys.argv[2], sys.argv[3], sys.argv[4])
                print(f"Juros: R$ {j:.2f}")
                print(f"Montante: R$ {m:.2f}")

            elif funcao == "valor_presente":
                vp = valor_presente_unico(sys.argv[2], sys.argv[3], sys.argv[4])
                print(f"Valor Presente: R$ {vp:.2f}")

            elif funcao == "valor_futuro":
                vf = valor_futuro_unico(sys.argv[2], sys.argv[3], sys.argv[4])
                print(f"Valor Futuro: R$ {vf:.2f}")

            elif funcao == "pmt_price":
                begin = len(sys.argv) > 5 and sys.argv[5].lower() == 'begin'
                p = pmt_price(sys.argv[2], sys.argv[3], sys.argv[4], begin)
                print(f"Parcela: R$ {p:.2f}")

            elif funcao == "sac":
                parcelas = sac(sys.argv[2], sys.argv[3], sys.argv[4])
                for parc in parcelas:
                    print(f"P{parc['periodo']:>3}: Saldo R$ {parc['saldo_inicial']:>10.2f} -> "
                          f"Amort R$ {parc['amortizacao']:>8.2f} + Juros R$ {parc['juros']:>8.2f} = "
                          f"Parcela R$ {parc['parcela']:>8.2f} -> Saldo R$ {parc['saldo_final']:>10.2f}")

            elif funcao == "vpl":
                taxa = sys.argv[2]
                fluxos = [float(f) for f in sys.argv[3:]]
                v = vpl(taxa, fluxos)
                print(f"VPL: R$ {v:.2f}")

            elif funcao == "tir":
                fluxos = [float(f) for f in sys.argv[2:]]
                irr = tir(fluxos)
                print(f"TIR: {irr*100:.2f}%")

            elif funcao == "mirr":
                taxa_r = sys.argv[2]
                taxa_f = sys.argv[3]
                fluxos = [float(f) for f in sys.argv[4:]]
                result = mirr(fluxos, taxa_r, taxa_f)
                print(f"MIRR: {result*100:.2f}%")

            elif funcao == "aposentadoria":
                saldo = aposentadoria(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
                print(f"Saldo final: R$ {saldo:,.2f}")

            elif funcao == "tesouro_prefixado":
                vf = tesouro_prefixado(sys.argv[2], sys.argv[3], sys.argv[4])
                print(f"Valor Futuro: R$ {vf:.2f}")

            elif funcao == "tesouro_selic":
                vf = tesouro_selic(sys.argv[2], sys.argv[3], sys.argv[4])
                print(f"Valor Futuro: R$ {vf:.2f}")

            elif funcao == "financiamento_imobiliario":
                r = financiamento_imobiliario(*sys.argv[2:6])
                print(f"Valor financiado: R$ {r['valor_financiado']:,.2f}")
                print(f"Parcela mensal: R$ {r['parcela_mensal']:.2f}")
                print(f"Total pago: R$ {r['total_pago']:,.2f}")
                print(f"Total juros: R$ {r['total_juros']:,.2f}")

            elif funcao == "conversor":
                c = ConversorMoedas()
                res = c.converter(sys.argv[2], sys.argv[3], sys.argv[4])
                print(f"{sys.argv[2]} {sys.argv[3]} = {res:.2f} {sys.argv[4]}")

            elif funcao == "irrf_pf":
                imp = CalculadoraImpostos.irrf_pf(sys.argv[2])
                print(f"IRRF: R$ {imp:.2f}")

            elif funcao == "simples_nacional":
                imp = CalculadoraImpostos.simples_nacional(sys.argv[2])
                print(f"Simples Nacional: R$ {imp:.2f}")

            elif funcao == "pis_pasep":
                imp = CalculadoraImpostos.pis_pasep(sys.argv[2])
                print(f"PIS/PASEP: R$ {imp:.2f}")

            elif funcao == "cofins":
                imp = CalculadoraImpostos.cofins(sys.argv[2])
                print(f"COFINS: R$ {imp:.2f}")

            elif funcao == "inss":
                imp = CalculadoraImpostos.inss(sys.argv[2])
                print(f"INSS: R$ {imp:.2f}")

            elif funcao == "negocios":
                negocios(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

            elif funcao == "cartao_credito":
                cartao_credito(sys.argv[2], sys.argv[3], sys.argv[4])

            elif funcao == "planejador_financeiro":
                planejador_financeiro(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])

            elif funcao == "margem_lucro":
                res = margem_lucro(sys.argv[2], sys.argv[3])
                print(f"Margem sobre custo: {res['margem_sobre_custo']:.1f}%")
                print(f"Margem sobre venda: {res['margem_sobre_venda']:.1f}%")
                print(f"Markup: {res['markup']:.2f}x")

            elif funcao == "testar":
                testar_calculadora()

            elif funcao in ["--help", "-h", "help"]:
                print_help()

            else:
                print(f"Erro: funcao '{funcao}' desconhecida")
                print("Use 'help' para lista completa de funcoes.")
                sys.exit(1)

        except Exception as e:
            print(f"Erro: {e}")
            sys.exit(1)


def print_help():
    """Exibe ajuda completa."""
    print("""
+-----------------------------------------------------------------+
|         HP-12C - CALCULADORA FINANCEIRA                         |
|         Manual de Comandos CLI                                  |
+-----------------------------------------------------------------+

USO:
  python calculadora_financeira.py <funcao> <parametros...>

FUNCOES MATEMATICAS:
  soma <a> <b>
  subtracao <a> <b>
  multiplicacao <a> <b>
  divisao <a> <b>
  porcentagem <valor> <percentual>
  variacao_percentual <antigo> <novo>

FUNCOES FINANCEIRAS:
  juros_simples <capital> <taxa_dec> <tempo>
  juros_compostos <capital> <taxa_dec> <tempo>
  valor_presente <vf> <taxa_dec> <tempo>
  valor_futuro <vp> <taxa_dec> <tempo>
  pmt_price <valor> <taxa_dec> <n> [begin]
  sac <valor> <taxa_dec> <n>
  tabela_price <valor> <taxa_dec> <n>
  vpl <taxa_dec> <fluxos...>
  tir <fluxos...>
  mirr <taxa_reinvest> <taxa_financ> <fluxos...>
  payback <fluxos...>
  financiamento_imobiliario <imovel> <entrada> <taxa_anual> <anos>
  aposentadoria <valor_inicial> <aporte_mensal> <taxa_mensal> <anos>
  tesouro_prefixado <valor> <taxa_anual> <anos>
  tesouro_selic <valor> <taxa_selic> <anos>

NEGOCIOS:
  negocios <fixos> <custo_var_unit> <preco_venda> <vendas_mes>
  cartao_credito <divida> <juros_perc> <pagamento>
  planejador_financeiro <renda> <aluguel> <luz> <agua> <internet> <outros>
  margem_lucro <custo> <preco_venda>

IMPOSTOS:
  irrf_pf <rendimento>
  simples_nacional <faturamento_anual>
  pis_pasep <valor>
  cofins <valor>
  inss <salario>

CONVERSAO:
  conversor <valor> <moeda_origem> <moeda_destino>

TESTES:
  testar

OBS:
  - Taxas em formato decimal (ex: 0.1 = 10%, 0.01 = 1%)
  - Use 'begin' como ultimo parametro do pmt_price para BEGIN mode
  - Modo interativo disponivel executando sem argumentos
""")


if __name__ == "__main__":
    main()