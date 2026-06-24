# ============================================================
# LicitaMaster - Commission & Revenue Engine
# Coracao financeiro: calcula, rastreia e gerencia comissoes
# ============================================================

from datetime import datetime, timedelta
from typing import List, Dict, Optional


class CommissionEngine:
    """
    Motor de comissoes.
    Gerencia a geracao de receita do sistema:
    - Comissao por fechamento (1-10%)
    - Comissao mensal recorrente em contratos
    - Rastreamento de pagamentos
    - Relatorios financeiros
    """

    def __init__(self, db=None):
        self.db = db
        self.comissao_padrao = 5.0  # 5%
        self.comissao_minima = 50.0
        self.repasse_percentual = 5.0  # 5% para usuario que usar o projeto

    def calcular_comissao(self, valor_contrato: float, percentual: float = None) -> Dict:
        """
        Calcula comissao sobre um contrato.

        Args:
            valor_contrato: Valor total do contrato/licitacao
            percentual: Percentual de comissao (1-10%)

        Returns:
            Dict com valores calculados
        """
        if percentual is None:
            percentual = self.comissao_padrao

        percentual = max(1, min(10, percentual))  # Limita entre 1% e 10%
        valor_comissao = valor_contrato * (percentual / 100)

        # Comissao do criador (repasse do usuario que usou o projeto)
        comissao_criador = valor_comissao * (self.repasse_percentual / 100)

        return {
            'valor_contrato': round(valor_contrato, 2),
            'percentual': percentual,
            'valor_comissao': round(valor_comissao, 2),
            'comissao_criador': round(comissao_criador, 2),
            'comissao_sistema': round(valor_comissao - comissao_criador, 2)
        }

    def gerar_comissao_mensal(self, valor_contrato: float, meses: int,
                              percentual: float = None) -> List[Dict]:
        """
        Gera comissoes mensais para contratos recorrentes.

        Args:
            valor_contrato: Valor mensal do contrato
            meses: Numero de meses do contrato
            percentual: Percentual de comissao

        Returns:
            Lista de comissoes mensais
        """
        comissoes = []
        for mes in range(1, meses + 1):
            calc = self.calcular_comissao(valor_contrato, percentual)
            comissoes.append({
                'mes': mes,
                'data_vencimento': (datetime.now() + timedelta(days=30 * mes)).strftime('%Y-%m-%d'),
                **calc
            })
        return comissoes

    def registrar_comissao(self, oportunidade_id: int, cliente_id: int,
                           valor_contrato: float, percentual: float = None,
                           tipo: str = 'UNICA') -> Dict:
        """
        Registra uma comissao a receber no banco.

        Returns:
            Dict com dados da comissao registrada
        """
        calc = self.calcular_comissao(valor_contrato, percentual)

        dados = {
            'oportunidade_id': oportunidade_id,
            'cliente_id': cliente_id,
            'valor_contrato': calc['valor_contrato'],
            'percentual': calc['percentual'],
            'valor_comissao': calc['valor_comissao'],
            'tipo': tipo,
            'status': 'A_RECEBER',
            'data_vencimento': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
            'observacoes': f"Comissao gerada automaticamente pelo LicitaMaster"
        }

        if self.db:
            comissao_id = self.db.criar_comissao(dados)
            dados['id'] = comissao_id
            self.db.log('SUCESSO', 'COMMISSION', 'registrar',
                       f"Comissao registrada: R$ {calc['valor_comissao']:.2f}")

        return dados

    def relatorio_financeiro(self) -> Dict:
        """
        Gera relatorio financeiro completo.

        Returns:
            Dict com indicadores financeiros
        """
        if not self.db:
            return {'erro': 'Banco de dados nao disponivel'}

        stats = self.db.get_stats()

        relatorio = {
            'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'resumo': {
                'total_recebido': stats.get('total_recebido', 0),
                'a_receber': stats.get('comissoes_a_receber', 0),
                'total_geral': stats.get('total_recebido', 0) + stats.get('comissoes_a_receber', 0),
                'licitacoes_vencidas': stats.get('licitacoes_vencidas', 0),
                'clientes_ativos': stats.get('clientes_ativos', 0),
                'oportunidades_pendentes': stats.get('oportunidades_pendentes', 0)
            },
            'comissoes_pendentes': self.db.listar_comissoes_a_receber()
        }

        return relatorio

    def gerar_cobranca(self, comissao_id: int) -> Dict:
        """
        Gera notificacao de cobranca para comissao vencida.

        Returns:
            Dict com dados da cobranca
        """
        if not self.db:
            return {'erro': 'Banco nao disponivel'}

        comissoes = self.db.listar_comissoes_a_receber()
        comissao = next((c for c in comissoes if c['id'] == comissao_id), None)

        if not comissao:
            return {'erro': 'Comissao nao encontrada'}

        notificacao = {
            'cliente_id': comissao.get('cliente_id'),
            'tipo': 'SISTEMA',
            'titulo': 'Cobranca de Comissao',
            'mensagem': (
                f"Prezado(a) {comissao.get('cliente_nome', 'Cliente')},\n\n"
                f"Conforme combinado, segue cobranca referente a comissao sobre a licitacao "
                f"'{comissao.get('licitacao_objeto', 'contrato')}'.\n\n"
                f"Valor: R$ {comissao.get('valor_comissao', 0):.2f}\n"
                f"Vencimento: {comissao.get('data_vencimento', 'N/A')}\n\n"
                f"Chave PIX para pagamento: (consulte seu contrato)\n\n"
                f"Atenciosamente,\nEquipe LicitaMaster"
            )
        }

        if self.db:
            self.db.criar_notificacao(notificacao)

        return notificacao


def calcular_repasse(valor_comissao: float, percentual_criador: float = 5.0) -> Dict:
    """
    Calcula o repasse devido ao criador do projeto.
    Qualquer pessoa que usar o LicitaMaster deve repassar
    entre 1% e 10% dos lucros para o criador.

    Args:
        valor_comissao: Valor total da comissao recebida
        percentual_criador: Percentual a ser repassado (1-10%)

    Returns:
        Dict com valores de repasse
    """
    percentual = max(1, min(10, percentual_criador))
    valor_repasse = valor_comissao * (percentual / 100)
    valor_liquido = valor_comissao - valor_repasse

    return {
        'valor_comissao': round(valor_comissao, 2),
        'percentual_repasse': percentual,
        'valor_repasse': round(valor_repasse, 2),
        'valor_liquido': round(valor_liquido, 2),
        'chave_pix_contato': 'Consultar documentacao do projeto para dados do criador'
    }