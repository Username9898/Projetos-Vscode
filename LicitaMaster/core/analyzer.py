# ============================================================
# LicitaMaster - Analyzer & Matcher
# Analisa licitacoes e faz match com clientes usando IA local
# ============================================================

import re
from typing import List, Dict, Optional, Tuple
from difflib import SequenceMatcher


class Analyzer:
    """Analisa licitacoes e calcula compatibilidade com clientes."""

    def __init__(self, db=None):
        self.db = db
        # Palavras-chave por ramo de negocio
        self.palavras_ramo = {
            'TI': ['informatica', 'software', 'hardware', 'computador', 'servidor', 'rede',
                   'internet', 'sistema', 'desenvolvimento', 'programacao', 'suporte tecnico',
                   'manutencao de equipamentos', 'licenca de software', 'cloud', 'tecnologia'],
            'SAUDE': ['medico', 'hospitalar', 'medicamento', 'farmaceutico', 'cirurgia',
                      'exame', 'laboratorio', 'enfermagem', 'equipamento medico',
                      'material hospitalar', 'vacina', 'tratamento'],
            'CONSTRUCAO': ['construcao', 'obra', 'engenharia', 'reforma', 'predio',
                           'pavimentacao', 'estrada', 'ponte', 'saneamento', 'materiais',
                           'cimento', 'ferro', 'areia', 'tijolo', 'acabamento'],
            'ALIMENTACAO': ['alimentacao', 'comida', 'refeicao', 'merenda', 'alimento',
                            'genero alimenticio', 'cozinha', 'nutricao', 'cesta basica',
                            'hortifruti', 'carne', 'verdura', 'fruita', 'grao', 'bebida'],
            'LIMPEZA': ['limpeza', 'higiene', 'material de limpeza', 'desinfetante',
                        'sabao', 'detergente', 'sabonete', 'papel higienico', 'toalha',
                        'produto de limpeza', 'higienizacao'],
            'SEGURANCA': ['seguranca', 'vigilancia', 'alarme', 'camera', 'monitoramento',
                          'seguro', 'portaria', 'vigia', 'equipamento de seguranca'],
            'TRANSPORTE': ['transporte', 'veiculo', 'carro', 'caminhao', 'onibus',
                          'frota', 'locomocao', 'combustivel', 'pneumatico', 'peca'],
            'EDUCACAO': ['educacao', 'escola', 'professor', 'material escolar', 'livro',
                        'curso', 'treinamento', 'capacitacao', 'didatico', 'pedagogico'],
            'MOBILIARIO': ['moveis', 'mobiliario', 'mesa', 'cadeira', 'armario',
                          'estante', 'sofa', 'cama', 'decoracao', 'escritorio'],
            'VESTUARIO': ['vestuario', 'uniforme', 'roupa', 'calcado', 'farda',
                         'camiseta', 'calca', 'tenis', 'bota', 'EPI', 'equipamento protecao'],
            'AGRICULTURA': ['agricultura', 'agropecuaria', 'semente', 'adubo', 'trator',
                           'implemento', 'irrigacao', 'pecuaria', 'agricola', 'fazenda'],
            'SERVICOS_GERAIS': ['servico', 'manutencao', 'limpeza', 'conservacao',
                               'jardinagem', 'dedetizacao', 'reparo', 'instalacao']
        }

    def analisar_licitacao(self, licitacao: Dict) -> Dict:
        """
        Analisa uma licitacao e extrai metadados.
        """
        texto = f"{licitacao.get('objeto', '')} {licitacao.get('descricao', '')}".upper()
        valor = licitacao.get('valor_estimado', 0) or licitacao.get('valor_maximo', 0)

        # Detecta ramos relacionados
        ramos = self._detectar_ramos(texto)

        # Gera score de oportunidade
        score_base = self._calcular_score_base(licitacao, ramos)

        return {
            'ramos_detectados': ramos,
            'score': score_base,
            'palavras_chave': self._extrair_palavras_chave(texto),
            'tem_anexo': licitacao.get('tem_anexo', False),
            'tem_valor': valor > 0,
            'valor_formatado': f"R$ {valor:,.2f}" if valor > 0 else "Nao informado"
        }

    def _detectar_ramos(self, texto: str) -> List[str]:
        """Detecta ramos de negocio relevantes para a licitacao."""
        ramos_encontrados = []
        for ramo, palavras in self.palavras_ramo.items():
            score = 0
            for palavra in palavras:
                if palavra.upper() in texto:
                    score += 1
            if score >= 2:  # Precisa de pelo menos 2 matches
                ramos_encontrados.append(ramo)
        return ramos_encontrados

    def _calcular_score_base(self, licitacao: Dict, ramos: List[str]) -> float:
        """Calcula score base da licitacao (0-100)."""
        score = 50  # Score base

        valor = licitacao.get('valor_estimado', 0) or licitacao.get('valor_maximo', 0)
        if valor > 0:
            if valor >= 1000000:
                score += 20  # Licitações de alto valor
            elif valor >= 100000:
                score += 15
            elif valor >= 50000:
                score += 10
            elif valor >= 10000:
                score += 5

        if ramos:
            score += 10  # Tem ramo identificado

        if licitacao.get('uf'):
            score += 5

        if licitacao.get('data_abertura'):
            score += 5

        if licitacao.get('url_edital'):
            score += 5

        return min(score, 100)

    def _extrair_palavras_chave(self, texto: str) -> List[str]:
        """Extrai palavras-chave relevantes do texto."""
        palavras = re.findall(r'\b[A-Z]{4,}\b', texto)
        # Remove palavras comuns
        stopwords = {'PARA', 'COM', 'DOS', 'DAS', 'MAIS', 'QUE', 'SER', 'POR',
                    'PELO', 'PELA', 'ENTRE', 'SOB', 'SOBRE', 'APOS', 'ATE'}
        return [p for p in palavras if p not in stopwords][:10]

    # ==========================================
    # MATCH COM CLIENTES
    # ==========================================
    def calcular_match(self, licitacao: Dict, cliente: Dict) -> Tuple[float, str, str]:
        """
        Calcula o score de match entre uma licitacao e um cliente.
        Retorna (score, afinidade, motivo).
        """
        score = 0
        motivos = []

        texto_licitacao = f"{licitacao.get('objeto', '')} {licitacao.get('descricao', '')}".upper()
        ramo_cliente = (cliente.get('ramo', '') or '').upper()
        nome_cliente = (cliente.get('nome', '') or '').upper()

        # 1. Match por ramo (peso 40)
        if ramo_cliente:
            palavras_ramo = self.palavras_ramo.get(ramo_cliente, [])
            matches = sum(1 for p in palavras_ramo if p.upper() in texto_licitacao)
            if matches >= 3:
                score += 40
                motivos.append(f"Ramo {ramo_cliente} com alta compatibilidade")
            elif matches >= 1:
                score += 20
                motivos.append(f"Ramo {ramo_cliente} parcialmente compativel")
            else:
                score += 5
                motivos.append(f"Ramo {ramo_cliente} com baixa compatibilidade")

        # 2. Match por estado (peso 20)
        if licitacao.get('uf') and cliente.get('estado'):
            if licitacao['uf'].upper() == cliente['estado'].upper():
                score += 20
                motivos.append(f"Mesmo estado ({cliente['estado']})")
            else:
                score += 5
                motivos.append(f"Estado diferente ({licitacao['uf']} x {cliente['estado']})")

        # 3. Match por porte (peso 15)
        porte = (cliente.get('porte', '') or '').upper()
        valor = licitacao.get('valor_estimado', 0) or licitacao.get('valor_maximo', 0)
        if porte == 'GRANDE' and valor > 500000:
            score += 15
            motivos.append("Porte compativel com valor alto")
        elif porte in ('MEDIO', 'EPP') and 50000 <= valor <= 500000:
            score += 15
            motivos.append("Porte compativel com valor medio")
        elif porte in ('ME', 'MEI') and valor <= 50000:
            score += 15
            motivos.append("Porte compativel com valor baixo")
        else:
            score += 5

        # 4. Score base (peso 25) - do analisador
        analise = self.analisar_licitacao(licitacao)
        score += analise['score'] * 0.25

        score = min(score, 100)

        # Define afinidade
        if score >= 70:
            afinidade = 'ALTA'
        elif score >= 40:
            afinidade = 'MEDIA'
        elif score >= 20:
            afinidade = 'BAIXA'
        else:
            afinidade = 'NENHUMA'

        motivo = '; '.join(motivos) if motivos else 'Match basico'
        return score, afinidade, motivo

    def gerar_oportunidades(self, licitacoes: List[Dict], clientes: List[Dict],
                           comissao_padrao: float = 5.0) -> List[Dict]:
        """
        Gera oportunidades de negocios fazendo match entre licitacoes e clientes.
        """
        oportunidades = []

        for licitacao in licitacoes:
            for cliente in clientes:
                score, afinidade, motivo = self.calcular_match(licitacao, cliente)

                if afinidade in ('ALTA', 'MEDIA'):
                    valor_estimado = licitacao.get('valor_estimado', 0) or licitacao.get('valor_maximo', 0)
                    comissao_estimada = valor_estimado * (comissao_padrao / 100)

                    oportunidades.append({
                        'licitacao_id': licitacao.get('id'),
                        'cliente_id': cliente.get('id'),
                        'score': score,
                        'afinidade': afinidade,
                        'motivo': motivo,
                        'status': 'PENDENTE',
                        'comissao_percentual': comissao_padrao,
                        'comissao_estimada': comissao_estimada,
                        'licitacao_objeto': licitacao.get('objeto', ''),
                        'cliente_nome': cliente.get('nome', ''),
                        'cliente_whatsapp': cliente.get('whatsapp', '')
                    })

        # Ordena por score decrescente
        oportunidades.sort(key=lambda x: x['score'], reverse=True)
        return oportunidades


def analisar_licitacoes(licitacoes: List[Dict], clientes: List[Dict],
                       db=None, comissao_padrao: float = 5.0) -> List[Dict]:
    """Funcao de conveniencia para analisar e gerar oportunidades."""
    analyzer = Analyzer(db)
    return analyzer.gerar_oportunidades(licitacoes, clientes, comissao_padrao)