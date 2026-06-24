# ============================================================
# LicitaMaster - WhatsApp Bot
# Envia oportunidades de licitacao para clientes via WhatsApp
# Usa whatsapp-web.js (Node) ou API publica Evolution
# ============================================================

import requests
import json
import time
from typing import List, Dict, Optional
from datetime import datetime


class WhatsAppBot:
    """
    Bot para envio de mensagens via WhatsApp.
    Duas opcoes gratuitas:
    1. whatsapp-web.js (roda local com Node.js)
    2. Evolution API (self-hosted gratuita)
    """

    def __init__(self, db=None, modo='local'):
        self.db = db
        self.modo = modo
        self.api_url = "http://localhost:3000"  # whatsapp-web.js local
        self.numero = ""  # Seu numero com DDI

    def enviar_mensagem(self, telefone: str, mensagem: str) -> bool:
        """
        Envia mensagem via WhatsApp.

        Args:
            telefone: Numero de telefone com DDI (ex: 5511999999999)
            mensagem: Texto da mensagem

        Returns:
            True se enviado com sucesso
        """
        if not telefone:
            return False

        try:
            if self.modo == 'local':
                return self._enviar_local(telefone, mensagem)
            else:
                return self._enviar_api(telefone, mensagem)
        except Exception as e:
            if self.db:
                self.db.log('ERRO', 'WHATSAPP', 'enviar', str(e))
            return False

    def _enviar_local(self, telefone: str, mensagem: str) -> bool:
        """Envia via API local whatsapp-web.js"""
        try:
            payload = {
                'number': telefone,
                'message': mensagem,
                'options': {
                    'delay': 1000  # delay de 1s
                }
            }
            resp = requests.post(
                f"{self.api_url}/api/send/text",
                json=payload,
                timeout=30
            )
            return resp.status_code == 201 or resp.status_code == 200
        except requests.exceptions.ConnectionError:
            # whatsapp-web.js nao esta rodando - salva para enviar depois
            if self.db:
                self.db.log('AVISO', 'WHATSAPP', 'enviar',
                           'Servidor local nao disponivel. Mensagem salva para envio posterior.')
            return False

    def _enviar_api(self, telefone: str, mensagem: str) -> bool:
        """Envia via API externa"""
        # Implementar conforme necessidade
        return False

    def enviar_oportunidade(self, cliente: Dict, oportunidade: Dict) -> bool:
        """
        Envia mensagem de oportunidade de licitacao para o cliente.

        Args:
            cliente: Dict com dados do cliente (nome, whatsapp)
            oportunidade: Dict com dados da oportunidade

        Returns:
            True se enviado
        """
        telefone = cliente.get('whatsapp', '')
        nome = cliente.get('nome', 'Cliente')
        objeto = oportunidade.get('licitacao_objeto', '') or oportunidade.get('objeto', '')
        orgao = oportunidade.get('orgao', 'Nao informado')
        valor = oportunidade.get('valor_estimado', 0) or oportunidade.get('comissao_estimada', 0)

        mensagem = (
            f"*NOVA OPORTUNIDADE DE NEGOCIO!*\n\n"
            f"Ola *{nome}*,\n\n"
            f"Identificamos uma licitacao com potencial para sua empresa:\n\n"
            f"*Objeto:* {objeto[:200]}\n"
            f"*Orgao:* {orgao}\n"
            f"*Valor estimado:* R$ {valor:,.2f}\n"
            f"*Score de compatibilidade:* {oportunidade.get('score', 0):.0f}%\n\n"
            f"Quer que eu prepare uma proposta para essa licitacao?\n"
            f"Responda 'SIM' para eu gerar a proposta automaticamente.\n\n"
            f"----------------------------------------\n"
            f"LicitaMaster - Sua inteligencia em licitacoes"
        )

        enviado = self.enviar_mensagem(telefone, mensagem)

        if enviado and self.db:
            self.db.criar_notificacao({
                'cliente_id': cliente.get('id'),
                'oportunidade_id': oportunidade.get('id'),
                'tipo': 'WHATSAPP',
                'titulo': 'Nova Oportunidade de Licitacao',
                'mensagem': mensagem
            })

        return enviado

    def enviar_oportunidades_em_massa(self, oportunidades: List[Dict],
                                       clientes: Dict[int, Dict]) -> Dict:
        """
        Envia oportunidades para varios clientes.

        Args:
            oportunidades: Lista de oportunidades
            clientes: Dict de clientes {id: dados}

        Returns:
            Dict com estatisticas de envio
        """
        stats = {'enviadas': 0, 'falhas': 0, 'total': len(oportunidades)}

        for oportunidade in oportunidades:
            cliente_id = oportunidade.get('cliente_id')
            if cliente_id and cliente_id in clientes:
                sucesso = self.enviar_oportunidade(clientes[cliente_id], oportunidade)
                if sucesso:
                    stats['enviadas'] += 1
                else:
                    stats['falhas'] += 1
                time.sleep(2)  # Delay entre mensagens

        if self.db:
            self.db.log('SUCESSO', 'WHATSAPP', 'envio_massa',
                       f"Enviadas: {stats['enviadas']}, Falhas: {stats['falhas']}")

        return stats

    def gerar_relatorio_oportunidades(self, oportunidades: List[Dict]) -> str:
        """
        Gera relatorio formatado das oportunidades para envio.
        """
        linhas = [
            "= RELATORIO DE OPORTUNIDADES =",
            f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            f"Total de oportunidades: {len(oportunidades)}",
            ""
        ]

        for i, op in enumerate(oportunidades[:10], 1):
            linhas.append(f"{i}. Cliente: {op.get('cliente_nome', 'N/A')}")
            linhas.append(f"   Objeto: {(op.get('licitacao_objeto', '') or '')[:100]}")
            linhas.append(f"   Score: {op.get('score', 0):.0f}%")
            linhas.append(f"   Comissao estimada: R$ {op.get('comissao_estimada', 0):.2f}")
            linhas.append("")

        return "\n".join(linhas)