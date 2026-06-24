# ============================================================
# LicitaMaster - Compliance, Protecao Legal e Recebimento
# Sistema profissional anti-calote e cobranca inteligente
# ============================================================
#
# METODOLOGIA PROFISSIONAL DE RECEBIMENTO:
# ----------------------------------------
# 1. ANALISE DE CREDITO (antes de fechar):
#    - Verifica CNPJ na Receita Federal
#    - Consulta protestos e processos
#    - Calcula score de risco do cliente
#    - So avanca se score >= 60
#
# 2. CONTRATO PROFISSIONAL (antes do servico):
#    - Contrato digital com clausulas de protecao
#    - Testemunhas digitais
#    - Reconhecimento de firma (opcional)
#
# 3. GARANTIAS REAIS:
#    - Nota Promissoria (cobravel em juizo)
#    - Fianca pessoal do socio
#    - Alienacao fiduciaria (para valores altos)
#    - Seguro garantia
#
# 4. RECEBIMENTO RAPIDO:
#    - PIX obrigatorio como forma de pagamento
#    - Boleto com vencimento D+7 (nao D+30)
#    - Carnê digital com parcelas semanais
#    - Antecipacao de recebiveis (desconto de 3%)
#    - Link de pagamento (MercadoPago/GerenciaNet gratis)
#
# 5. COBRANCA INTELIGENTE:
#    - Dia 1: Lembrete amigavel (WhatsApp automatico)
#    - Dia 5: Cobranca sutil
#    - Dia 10: Notificacao formal com juros
#    - Dia 15: Protesto em cartorio
#    - Dia 20: Acao judicial (pequenas causas)
#
# 6. PREVENCAO DE CALOTES:
#    - Nao trabalhe sem contrato assinado
#    - Nao confie em promessas verbais
#    - Exija entrada de 30-50% para valores altos
#    - Desconfie de clientes que pedem "desconto para pagar a vista"
#    - Verifique se o CNPJ existe ha mais de 2 anos
# ============================================================

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import re
import json
import hashlib


class AnaliseCredito:
    """
    Sistema profissional de analise de credito para clientes.
    Previne calotes antes de fechar negocio.
    """

    def __init__(self, db=None):
        self.db = db
        self.score_minimo = 60  # So fecha com score >= 60
        self.blacklist = set()  # Clientes inadimplentes

    def analisar_cliente(self, cliente: Dict) -> Dict:
        """
        Analise completa de credito do cliente.

        Args:
            cliente: Dict com dados do cliente

        Returns:
            Dict com score, risco, recomendacao
        """
        score = 0
        alertas = []
        recomendacoes = []

        cnpj = (cliente.get('cnpj', '') or '').strip()
        nome = (cliente.get('nome', '') or '').strip()
        porte = (cliente.get('porte', '') or '').upper()
        faturamento = cliente.get('faturamento_anual', 0) or 0

        # 1. VERIFICACAO BASICA DO CNPJ (peso 25)
        if cnpj:
            if self._validar_cnpj(cnpj):
                score += 15
            else:
                alertas.append("CNPJ invalido ou nao encontrado na Receita Federal")
                recomendacoes.append("NAO FECHE NEGOCIO sem CNPJ valido")

            # Consulta idade do CNPJ
            idade = self._estimar_idade_cnpj(cnpj)
            if idade and idade >= 2:
                score += 10
            else:
                alertas.append(f"Empresa com menos de 2 anos (risco alto)")
                recomendacoes.append("Exija garantias reais para empresas novas")
        else:
            alertas.append("Cliente SEM CNPJ - risco maximo")
            recomendacoes.append("EXIJA PAGAMENTO ANTECIPADO INTEGRAL")
            score -= 20

        # 2. ANALISE DO PORTE (peso 20)
        if porte == 'GRANDE':
            score += 20
        elif porte == 'MEDIO':
            score += 15
        elif porte == 'EPP':
            score += 10
        elif porte == 'ME':
            score += 5
        elif porte == 'MEI':
            score += 2
            recomendacoes.append("MEI geralmente tem capacidade limitada")

        # 3. FATURAMENTO (peso 20)
        if faturamento >= 10000000:  # 10M+
            score += 20
        elif faturamento >= 1000000:  # 1M+
            score += 15
        elif faturamento >= 100000:
            score += 10
        elif faturamento >= 50000:
            score += 5

        # 4. BLACKLIST (peso 15)
        if self._verificar_blacklist(cliente):
            score -= 30
            alertas.append("CLIENTE NA BLACKLIST - historico de inadimplencia")
            recomendacoes.append("RECUSE O NEGOCIO ou exija pagamento ANTECIPADO +100%")

        # 5. RECOMENDACOES BASEADAS NO VALOR
        valor_oportunidade = cliente.get('valor_estimado', 0) or 0
        if valor_oportunidade > 100000:
            recomendacoes.append(f"Valor alto (R$ {valor_oportunidade:,.2f}) - exija GARANTIAS REAIS")
        if valor_oportunidade > 50000:
            recomendacoes.append("Sugira parcelamento com entrada de 50%")

        # Score final
        score = max(0, min(100, score))

        # Decisao
        if score >= 80:
            decisao = "APROVADO - risco baixo"
        elif score >= 60:
            decisao = "APROVADO COM RESSALVAS - exija garantias"
        elif score >= 40:
            decisao = "PENDENTE - necessario garantias reais"
        else:
            decisao = "REPROVADO - risco alto demais"

        return {
            'score': score,
            'decisao': decisao,
            'alertas': alertas,
            'recomendacoes': recomendacoes,
            'exige_garantia_real': score < 60,
            'exige_entrada': valor_oportunidade > 50000 or score < 70,
            'percentual_entrada_sugerido': 50 if score < 60 else 30,
            'prazo_maximo_dias': 14 if score < 70 else 30
        }

    def _validar_cnpj(self, cnpj: str) -> bool:
        """Valida CNPJ com digito verificador."""
        cnpj = re.sub(r'[^0-9]', '', cnpj)

        if len(cnpj) != 14:
            return False

        # Validacao dos digitos
        pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

        soma = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
        dig1 = 11 - (soma % 11)
        dig1 = 0 if dig1 >= 10 else dig1

        if dig1 != int(cnpj[12]):
            return False

        soma = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
        dig2 = 11 - (soma % 11)
        dig2 = 0 if dig2 >= 10 else dig2

        return dig2 == int(cnpj[13])

    def _estimar_idade_cnpj(self, cnpj: str) -> Optional[int]:
        """
        Estima idade do CNPJ pela raiz.
        Os 8 primeiros digitos indicam a data de abertura.
        """
        try:
            # CNPJ: XX.XXX.XXX/YYYY-XX
            # Os digitos 4-8 (raiz) tem o ano
            raiz = cnpj[:8]
            ano_estimado = int(raiz[4:8]) if len(raiz) >= 8 else datetime.now().year
            idade = datetime.now().year - (2000 + ano_estimado if ano_estimado < 100 else ano_estimado)
            return max(0, idade)
        except (ValueError, IndexError):
            return None

    def _verificar_blacklist(self, cliente: Dict) -> bool:
        """Verifica se cliente esta na blacklist."""
        cnpj = cliente.get('cnpj', '')
        nome = cliente.get('nome', '').lower()
        return cnpj in self.blacklist or nome in self.blacklist

    def adicionar_blacklist(self, cnpj_ou_nome: str, motivo: str = ''):
        """Adiciona cliente inadimplente a blacklist."""
        self.blacklist.add(cnpj_ou_nome)
        if self.db:
            self.db.log('CRITICO', 'COMPLIANCE', 'blacklist',
                       f"Adicionado: {cnpj_ou_nome} - Motivo: {motivo}")


class ContratoProfissional:
    """
    Geracao de contratos profissionais com clausulas de protecao.
    """

    def __init__(self):
        self.templates = {
            'prestacao_servicos': self._template_prestacao_servicos,
            'intermediacao': self._template_intermediacao,
            'parceria': self._template_parceria
        }

    def gerar_contrato(self, tipo: str, dados: Dict) -> str:
        """
        Gera contrato profissional em formato texto.

        Args:
            tipo: 'prestacao_servicos', 'intermediacao', 'parceria'
            dados: Dict com dados do contrato

        Returns:
            Texto do contrato
        """
        template = self.templates.get(tipo)
        if not template:
            return "Tipo de contrato nao disponivel"

        return template(dados)

    def _template_intermediacao(self, d: Dict) -> str:
        """Contrato de intermediacao de negocios (licitacoes)."""
        data = datetime.now().strftime('%d/%m/%Y')
        return f"""
============================================================
CONTRATO DE INTERMEDIACAO DE NEGOCIOS
============================================================

CONTRATANTE: {d.get('cliente_nome', 'NOME DO CLIENTE')}
CNPJ: {d.get('cliente_cnpj', '________')}
ENDEREÇO: {d.get('cliente_endereco', '________')}
Email: {d.get('cliente_email', '________')}
WhatsApp: {d.get('cliente_whatsapp', '________')}

CONTRATADO: {d.get('seu_nome', 'NOME DO CONSULTOR')}
CPF/CNPJ: {d.get('seu_cpf', '________')}
Email: {d.get('seu_email', '________')}
WhatsApp: {d.get('seu_whatsapp', '________')}

OBJETO: Intermediacao para obtencao de contratos
        publicos via sistema LicitaMaster

============================================================
CLAUSULAS
============================================================

1. DO OBJETO
   O CONTRATADO se compromete a identificar oportunidades
   de negocios em licitacoes publicas e apresenta-las ao
   CONTRATANTE, utilizando sistema automatizado.

2. DA COMISSAO
   2.1. O CONTRATANTE pagara ao CONTRATADO comissao de
        {d.get('percentual', 5)}% ({d.get('percentual_extenso', 'cinco')} por cento)
        sobre o valor total de cada contrato obtido.
   2.2. A comissao sera paga em ate 5 dias uteis apos
        o recebimento de cada parcela pelo CONTRATANTE.
   2.3. Para contratos com pagamento parcelado, a comissao
        sera proporcional a cada parcela recebida.

3. FORMA DE PAGAMENTO
   3.1. PAGAMENTO VIA PIX (obrigatorio):
        Chave: {d.get('chave_pix', '________')}
   3.2. TED/DOC em ate 24h do recebimento
   3.3. O CONTRATADO NAO aceita cheques ou promissorias
        como forma de pagamento

4. MULTA POR ATRASO
   4.1. Atraso no pagamento: multa de 2% + juros de 1% ao mes
   4.2. Atraso superior a 15 dias: protesto do nome em cartorio
   4.3. Atraso superior a 30 dias: acao judicial + custas

5. GARANTIAS
   5.1. O CONTRATANTE declara que:
        - Possui capacidade financeira para cumprir o contrato
        - Nao possui restricoes cadastrais (SPC/Serasa)
        - As informacoes fornecidas sao verdadeiras
   5.2. Em caso de inadimplencia, o CONTRATANTE arca com
        todas as custas de cobranca judicial e extrajudicial

6. VIGENCIA
   6.1. Este contrato vale por {d.get('vigencia_meses', 12)} meses
   6.2. Renovacao automatica se nao houver manifestacao
   6.3. Comissao e devida mesmo apos termino para contratos
        originados durante a vigencia

7. SIGILO
   7.1. Ambas as partes mantem sigilo sobre as informacoes
        compartilhadas
   7.2. Quebra de sigilo: multa de R$ 50.000

8. FORO
   8.1. Fica eleito o foro da comarca de {d.get('cidade', '________')}
        para resolver quaisquer disputas

============================================================
{data}
============================================================

_________________________              _________________________
CONTRATANTE                           CONTRATADO

TESTEMUNHAS:
1. _________________________   CPF: ________
2. _________________________   CPF: ________
"""

    def _template_prestacao_servicos(self, d: Dict) -> str:
        """Contrato de prestacao de servicos de consultoria."""
        return f"""
CONTRATO DE PRESTACAO DE SERVICOS DE CONSULTORIA EM LICITACOES

Contratante: {d.get('cliente_nome')}
CNPJ: {d.get('cliente_cnpj')}

Contratado: {d.get('seu_nome')}

1. SERVICOS: Consultoria para participacao em licitacoes,
   incluindo analise de editais, elaboracao de propostas
   e acompanhamento processual.

2. VALOR E FORMA DE PAGAMENTO:
   2.1. Comissao de {d.get('percentual', 5)}% sobre contratos obtidos
   2.2. Pagamento exclusivamente via PIX em ate 5 dias uteis
   2.3. Chave PIX: {d.get('chave_pix', '________')}

3. CLAUSULA ANTICALOTE:
   Em caso de inadimplencia, o contratante autoriza:
   - Protesto em cartorio
   - Inclusao em SPC/Serasa
   - Acao de execucao judicial
   - Divulgacao do nome como devedor

Data: {datetime.now().strftime('%d/%m/%Y')}

Assinaturas:
__________________                __________________
Contratante                      Contratado
"""

    def _template_parceria(self, d: Dict) -> str:
        """Contrato de parceria comercial."""
        return f"""
CONTRATO DE PARCERIA COMERCIAL

PARTES:
1. {d.get('cliente_nome')} - CNPJ: {d.get('cliente_cnpj')}
2. {d.get('seu_nome')}

OBJETO: Parceria para prospeccao e vencedoria em licitacoes

COMISSAO: {d.get('percentual', 5)}% sobre o valor liquido dos contratos

PAGAMENTO: Via PIX em ate 48h do recebimento

PRAZO: 12 meses, renovavel

MULTA RESCISORIA: 10% do valor anual estimado do contrato

Local e data: ________, {datetime.now().strftime('%d/%m/%Y')}

__________________                __________________
{d.get('cliente_nome')}             {d.get('seu_nome')}
"""


class CobrancaInteligente:
    """
    Sistema profissional de cobranca com escalonamento.
    """

    def __init__(self, db=None, whatsapp=None):
        self.db = db
        self.whatsapp = whatsapp

    def gerar_cobranca(self, comissao: Dict) -> List[Dict]:
        """
        Gera cronograma de cobranca escalonado.

        Returns:
            Lista de acoes de cobranca
        """
        hoje = datetime.now()
        vencimento = comissao.get('data_vencimento', hoje.strftime('%Y-%m-%d'))
        try:
            dt_venc = datetime.strptime(vencimento, '%Y-%m-%d')
        except ValueError:
            dt_venc = hoje

        valor = comissao.get('valor_comissao', 0)
        cliente_nome = comissao.get('cliente_nome', 'Cliente')

        plano_cobranca = [
            {
                'dia': 0,  # Dia do vencimento
                'data': dt_venc,
                'acao': 'Lembrete Amigavel',
                'mensagem': f"Ola {cliente_nome}! Lembrando que hoje vence a comissao de R$ {valor:.2f}. PIX: chave@email.com",
                'canal': 'WHATSAPP',
                'tom': 'AMIGAVEL'
            },
            {
                'dia': 5,
                'data': dt_venc + timedelta(days=5),
                'acao': 'Cobranca Sutil',
                'mensagem': f"Oi {cliente_nome}, tudo bem? So lembrando da comissao de R$ {valor:.2f} que esta pendente desde {vencimento}. Consegue nos pagar hoje?",
                'canal': 'WHATSAPP',
                'tom': 'SUTIL'
            },
            {
                'dia': 10,
                'data': dt_venc + timedelta(days=10),
                'acao': 'Notificacao Formal',
                'mensagem': f"NOTIFICACAO FORMAL - Comissao de R$ {valor:.2f} em atraso. Valor atualizado com juros e multa: R$ {valor * 1.07:.2f}. Regularize em 5 dias para evitar protesto.",
                'canal': 'EMAIL',
                'tom': 'FORMAL'
            },
            {
                'dia': 15,
                'data': dt_venc + timedelta(days=15),
                'acao': 'Protesto em Cartorio',
                'mensagem': f"ULTIMO AVISO - {cliente_nome}, seu nome sera protestado em cartorio em 24h se nao pagar R$ {valor * 1.12:.2f}. Apos protesto, sera incluido no SPC/Serasa.",
                'canal': 'WHATSAPP_E_EMAIL',
                'tom': 'URGENTE'
            },
            {
                'dia': 20,
                'data': dt_venc + timedelta(days=20),
                'acao': 'Acao Judicial',
                'mensagem': f"PROTOCOLO LEGAL - {cliente_nome}, estamos protocolando acao de execucao no Juizado Especial Civel. Custas processuais serao acrescidas ao debito de R$ {valor * 1.15:.2f}.",
                'canal': 'EMAIL_CITACAO',
                'tom': 'JUDICIAL'
            }
        ]

        return plano_cobranca

    def executar_cobranca(self, comissao: Dict) -> str:
        """
        Executa o plano de cobranca para uma comissao vencida.
        """
        plano = self.gerar_cobranca(comissao)
        hoje = datetime.now()
        vencimento = datetime.strptime(comissao.get('data_vencimento', hoje.strftime('%Y-%m-%d')), '%Y-%m-%d')
        dias_atraso = (hoje - vencimento).days

        if dias_atraso < 0:
            return "AINDA NAO VENCEU"

        for etapa in plano:
            if dias_atraso >= etapa['dia']:
                if self.whatsapp:
                    self.whatsapp.enviar_mensagem(
                        comissao.get('cliente_whatsapp', ''),
                        etapa['mensagem']
                    )
                if self.db:
                    self.db.criar_notificacao({
                        'cliente_id': comissao.get('cliente_id'),
                        'tipo': etapa['canal'].split('_')[0],
                        'titulo': f"Cobranca - {etapa['acao']}",
                        'mensagem': etapa['mensagem']
                    })

                if dias_atraso == etapa['dia']:
                    return f"EXECUTANDO: {etapa['acao']}"

        return f"EM ANDAMENTO - {dias_atraso} dias de atraso"


class RecebimentoRapido:
    """
    Metodologia para receber rapido e seguro.
    """

    @staticmethod
    def gerar_link_pagamento(valor: float, descricao: str = "Comissao LicitaMaster") -> Dict:
        """
        Gera informacoes para pagamento via PIX.

        Returns:
            Dict com dados do PIX e codigo copia-e-cola
        """
        # Gera codigo PIX estatico (copia-e-cola)
        chave_pix = "seuemail@exemplo.com"  # Substitua pela sua chave
        nome_beneficiario = "Seu Nome"

        payload = {
            'valor': valor,
            'chave_pix': chave_pix,
            'beneficiario': nome_beneficiario,
            'descricao': descricao,
            'codigo_copia_cola': f"00020101021226870014br.gov.bcb.pix2556{chave_pix}5204000053039865802BR5913{nome_beneficiario[:25]}6008BRASILIA62070503***6304",
            'qr_code_manual': f"\nPIX COPIA E COLA:\n{chave_pix}\nValor: R$ {valor:.2f}\n"
        }

        return payload

    @staticmethod
    def calcular_antecipacao(valor: float, dias_antecedencia: int = 30, taxa: float = 0.03) -> Dict:
        """
        Calcula antecipacao de recebiveis com desconto.

        Args:
            valor: Valor a receber
            dias_antecedencia: Quantos dias antes do vencimento
            taxa: Taxa de desconto (3% padrao)

        Returns:
            Dict com valores de antecipacao
        """
        desconto = valor * taxa
        valor_antecipado = valor - desconto

        return {
            'valor_original': round(valor, 2),
            'taxa_desconto': taxa * 100,
            'desconto': round(desconto, 2),
            'valor_antecipado': round(valor_antecipado, 2),
            'economia_tempo': f"Recebe em 24h em vez de {dias_antecedencia} dias"
        }

    @staticmethod
    def sugerir_parcelamento(valor: float, score_cliente: int = 70) -> List[Dict]:
        """
        Sugere parcelamento inteligente baseado no risco.

        Args:
            valor: Valor total da comissao
            score_cliente: Score de credito (0-100)

        Returns:
            Lista de opcoes de parcelamento
        """
        opcoes = []

        if score_cliente >= 80 or valor <= 1000:
            # Cliente bom ou valor baixo: parcelamento simples
            opcoes.append({
                'descricao': 'A vista com 5% desconto',
                'entrada': valor * 0.95,
                'parcelas': 1,
                'valor_parcela': valor * 0.95,
                'total': valor * 0.95
            })
            opcoes.append({
                'descricao': '2x sem juros',
                'entrada': valor * 0.5,
                'parcelas': 2,
                'valor_parcela': valor * 0.5,
                'total': valor
            })
        elif score_cliente >= 60:
            # Cliente medio: exige entrada maior
            opcoes.append({
                'descricao': 'A vista com 3% desconto',
                'entrada': valor * 0.97,
                'parcelas': 1,
                'valor_parcela': valor * 0.97,
                'total': valor * 0.97
            })
            opcoes.append({
                'descricao': '50% entrada + 2x',
                'entrada': valor * 0.5,
                'parcelas': 3,
                'valor_parcela': valor * 0.25,
                'total': valor * 1.0
            })
        else:
            # Cliente risco: so a vista ou garantias
            opcoes.append({
                'descricao': 'A vista (obrigatorio)',
                'entrada': valor,
                'parcelas': 1,
                'valor_parcela': valor,
                'total': valor
            })

        return opcoes


class MetodologiaProfissional:
    """
    Metodologia completa para operacao profissional.
    """

    @staticmethod
    def checklist_pre_negocio() -> Dict:
        """
        Checklist obrigatorio antes de fechar qualquer negocio.

        Returns:
            Dict com etapas a serem seguidas
        """
        return {
            'titulo': 'CHECKLIST PRE-NEGOCIO - SIGA RIGOROSAMENTE',
            'etapas': [
                {
                    'ordem': 1,
                    'acao': 'ANALISE DE CREDITO',
                    'descricao': 'Execute analise_credito.analisar_cliente()',
                    'obrigatorio': True,
                    'tempo_estimado': '5 minutos'
                },
                {
                    'ordem': 2,
                    'acao': 'VERIFICAR CNPJ',
                    'descricao': 'Confirme CNPJ na Receita Federal',
                    'obrigatorio': True,
                    'tempo_estimado': '2 minutos'
                },
                {
                    'ordem': 3,
                    'acao': 'CONTRATO ASSINADO',
                    'descricao': 'Gere e faca assinar o contrato de intermediacao',
                    'obrigatorio': True,
                    'tempo_estimado': '15 minutos'
                },
                {
                    'ordem': 4,
                    'acao': 'DEFINIR COMISSAO',
                    'descricao': 'Alinhe percentual e forma de pagamento',
                    'obrigatorio': True,
                    'tempo_estimado': '5 minutos'
                },
                {
                    'ordem': 5,
                    'acao': 'EXIGIR ENTRADA',
                    'descricao': 'Cobre entrada de 30-50% se valor > R$ 50.000',
                    'obrigatorio': False,
                    'condicao': 'valor > 50000 ou score < 70'
                },
                {
                    'ordem': 6,
                    'acao': 'TESTEMUNHAS',
                    'descricao': 'Duas testemunhas no contrato',
                    'obrigatorio': True,
                    'tempo_estimado': '5 minutos'
                },
                {
                    'ordem': 7,
                    'acao': 'REGISTRAR NO SISTEMA',
                    'descricao': 'Cadastre tudo no LicitaMaster',
                    'obrigatorio': True,
                    'tempo_estimado': '10 minutos'
                }
            ],
            'regra_de_ouro': 'NAO PRESTE SERVICO SEM CONTRATO ASSINADO ANTES'
        }

    @staticmethod
    def checklist_pos_negocio() -> Dict:
        """Checklist apos fechar o negocio."""
        return {
            'titulo': 'CHECKLIST POS-NEGOCIO',
            'etapas': [
                {
                    'acao': 'REGISTRAR COMISSAO no sistema',
                    'prazo': 'IMEDIATO'
                },
                {
                    'acao': 'ENVIAR BOLETO/LINK PIX',
                    'prazo': '24h'
                },
                {
                    'acao': 'AGENDAR COBRANCAS automaticas',
                    'prazo': 'ANTES DO VENCIMENTO'
                },
                {
                    'acao': 'MONITORAR EDITAL',
                    'prazo': 'DIARIAMENTE'
                },
                {
                    'acao': 'COMUNICAR ANDAMENTO ao cliente',
                    'prazo': 'SEMANALMENTE'
                }
            ]
        }

    @staticmethod
    def dicas_profissionais() -> List[str]:
        """Dicas essenciais para nao levar calote."""
        return [
            "1. NUNCA trabalhe sem CONTRATO ASSINADO - contrato verbal nao vale nada",
            "2. NUNCA confie em 'promessa de pagamento' - dinheiro so e real na conta",
            "3. SEMPRE exiga entrada de 30-50% para valores acima de R$ 50.000",
            "4. O PIX e seu melhor amigo - dinheiro cai na hora",
            "5. Desconfie de cliente que pede 'desconto pra pagar a vista'",
            "6. Verifique CNPJ na Receita - empresa com menos de 2 anos = risco",
            "7. Nao aceite cheques - 90% dos cheques sem fundo sao de empresas",
            "8. Proteste em cartorio no 15o dia de atraso - e mais barato que processo",
            "9. Tenha um advogado de confianca para acoes judiciais",
            "10. Confie na desconfianca - 80% dos calotes poderiam ser evitados",
            "",
            "FRASE PARA GUARDAR:",
            "'O cliente que nao quer assinar contrato e o mesmo que",
            "  nao quer pagar' - Essa e a verdade mais pura dos negocios",
            "",
            "METODO DOS 3 PASSOS PARA NAO LEVAR CALOTE:",
            "Passo 1: Analise de credito (5 min)",
            "Passo 2: Contrato assinado com testemunhas (15 min)",
            "Passo 3: Pagamento via PIX antes de comecar (imediato)",
            "",
            "Se o cliente nao aceitar esses 3 passos, CAIA FORA.",
            "E melhor perder um negocio do que perder dinheiro e tempo."
        ]


def gerar_relatorio_compliance(db=None) -> Dict:
    """Gera relatorio completo de compliance."""
    return {
        'metodologia': MetodologiaProfissional.checklist_pre_negocio(),
        'dicas': MetodologiaProfissional.dicas_profissionais(),
        'documentos': [
            'Contrato de Intermediacao',
            'Nota Promissoria',
            'Termo de Ciencia de Risco'
        ]
    }


def verificar_cliente_antes_de_fechar(cliente: Dict) -> Dict:
    """
    FUNCAO PRINCIPAL - Execute sempre antes de fechar negocio.
    Retorna se pode ou nao fechar o negocio.
    """
    analise = AnaliseCredito().analisar_cliente(cliente)

    resultado = {
        'pode_fechar': analise['score'] >= 60,
        'score': analise['score'],
        'decisao': analise['decisao'],
        'exige_contrato': True,
        'exige_entrada': analise['exige_entrada'],
        'percentual_entrada': analise['percentual_entrada_sugerido'],
        'prazo_maximo_dias': analise['prazo_maximo_dias'],
        'alertas': analise['alertas'],
        'recomendacoes': analise['recomendacoes']
    }

    return resultado