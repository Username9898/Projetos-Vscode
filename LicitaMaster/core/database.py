# ============================================================
# LicitaMaster - Database Manager
# Gerenciamento completo do banco SQLite
# ============================================================

import sqlite3
import os
import json
from datetime import datetime, date
from typing import Optional, List, Dict, Any, Union
from pathlib import Path


class DatabaseManager:
    """Gerenciador do banco de dados SQLite."""

    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'licitamaster.db')
        self.db_path = str(Path(db_path).resolve())
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Retorna conexao com o banco."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    def _init_db(self):
        """Inicializa o banco com o schema."""
        schema_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'schema.sql')
        if os.path.exists(schema_path):
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema = f.read()
            conn = self._get_connection()
            conn.executescript(schema)
            conn.commit()
            conn.close()

    def _row_to_dict(self, row: Optional[sqlite3.Row]) -> Optional[Dict]:
        """Converte Row para dict."""
        if row is None:
            return None
        return dict(row)

    def _rows_to_list(self, rows: List[sqlite3.Row]) -> List[Dict]:
        """Converte lista de Rows para lista de dicts."""
        return [dict(r) for r in rows]

    # ==========================================
    # CLIENTES
    # ==========================================
    def adicionar_cliente(self, dados: Dict) -> int:
        """Adiciona ou atualiza um cliente."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO clientes (nome, cnpj, email, telefone, whatsapp, site, ramo, porte,
                    faturamento_anual, estado, cidade, endereco, observacoes)
                VALUES (:nome, :cnpj, :email, :telefone, :whatsapp, :site, :ramo, :porte,
                    :faturamento_anual, :estado, :cidade, :endereco, :observacoes)
                ON CONFLICT(cnpj) DO UPDATE SET
                    nome=excluded.nome, email=excluded.email, telefone=excluded.telefone,
                    whatsapp=excluded.whatsapp, ramo=excluded.ramo, porte=excluded.porte,
                    faturamento_anual=excluded.faturamento_anual, estado=excluded.estado,
                    cidade=excluded.cidade, endereco=excluded.endereco,
                    observacoes=excluded.observacoes, data_atualizacao=CURRENT_TIMESTAMP
            """, dados)
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def listar_clientes(self, ativo: bool = True) -> List[Dict]:
        """Lista todos os clientes ativos."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes WHERE ativo = ? ORDER BY nome", (1 if ativo else 0,))
            return self._rows_to_list(cursor.fetchall())
        finally:
            conn.close()

    def buscar_cliente(self, id: int = None, cnpj: str = None) -> Optional[Dict]:
        """Busca cliente por ID ou CNPJ."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            if id:
                cursor.execute("SELECT * FROM clientes WHERE id = ?", (id,))
            elif cnpj:
                cursor.execute("SELECT * FROM clientes WHERE cnpj = ?", (cnpj,))
            else:
                return None
            return self._row_to_dict(cursor.fetchone())
        finally:
            conn.close()

    # ==========================================
    # LICITACOES
    # ==========================================
    def adicionar_licitacao(self, dados: Dict) -> int:
        """Adiciona ou atualiza uma licitacao."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            # Verifica se ja existe pelo codigo
            if dados.get('codigo'):
                cursor.execute("SELECT id FROM licitacoes WHERE codigo = ?", (dados['codigo'],))
                existing = cursor.fetchone()
                if existing:
                    # Atualiza
                    dados['id'] = existing['id']
                    self._atualizar_licitacao(conn, dados)
                    return existing['id']

            cursor.execute("""
                INSERT INTO licitacoes (numero, orgao, uf, modalidade, tipo, objeto, descricao,
                    valor_estimado, valor_maximo, data_publicacao, data_abertura, data_fim_recurso,
                    prazo_execucao, cnpj_orgao, codigo, fonte, url_edital, url_pncp, status, tem_anexo, anexos)
                VALUES (:numero, :orgao, :uf, :modalidade, :tipo, :objeto, :descricao,
                    :valor_estimado, :valor_maximo, :data_publicacao, :data_abertura, :data_fim_recurso,
                    :prazo_execucao, :cnpj_orgao, :codigo, :fonte, :url_edital, :url_pncp, :status, :tem_anexo, :anexos)
            """, dados)
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def _atualizar_licitacao(self, conn: sqlite3.Connection, dados: Dict):
        """Atualiza licitacao existente."""
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE licitacoes SET
                numero=:numero, orgao=:orgao, uf=:uf, modalidade=:modalidade,
                tipo=:tipo, objeto=:objeto, descricao=:descricao,
                valor_estimado=:valor_estimado, valor_maximo=:valor_maximo,
                data_publicacao=:data_publicacao, data_abertura=:data_abertura,
                prazo_execucao=:prazo_execucao, status=:status,
                tem_anexo=:tem_anexo, anexos=:anexos,
                atualizado_em=CURRENT_TIMESTAMP
            WHERE id = :id
        """, dados)
        conn.commit()

    def listar_licitacoes_abertas(self) -> List[Dict]:
        """Lista licitacoes abertas."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM licitacoes
                WHERE status IN ('ABERTA', 'EM_ANDAMENTO')
                ORDER BY data_abertura DESC
            """)
            return self._rows_to_list(cursor.fetchall())
        finally:
            conn.close()

    def buscar_licitacao(self, id: int = None, codigo: str = None) -> Optional[Dict]:
        """Busca licitacao por ID ou codigo."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            if id:
                cursor.execute("SELECT * FROM licitacoes WHERE id = ?", (id,))
            elif codigo:
                cursor.execute("SELECT * FROM licitacoes WHERE codigo = ?", (codigo,))
            else:
                return None
            return self._row_to_dict(cursor.fetchone())
        finally:
            conn.close()

    # ==========================================
    # OPORTUNIDADES
    # ==========================================
    def criar_oportunidade(self, dados: Dict) -> int:
        """Cria uma oportunidade (match cliente x licitacao)."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO oportunidades (licitacao_id, cliente_id, score, afinidade, motivo, status,
                    comissao_percentual, comissao_estimada, observacoes)
                VALUES (:licitacao_id, :cliente_id, :score, :afinidade, :motivo, :status,
                    :comissao_percentual, :comissao_estimada, :observacoes)
            """, dados)
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def listar_oportunidades(self, status: str = None) -> List[Dict]:
        """Lista oportunidades."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            if status:
                cursor.execute("""
                    SELECT o.*, l.objeto, l.orgao, l.valor_estimado, l.data_abertura,
                           c.nome as cliente_nome, c.whatsapp as cliente_whatsapp, c.email as cliente_email
                    FROM oportunidades o
                    JOIN licitacoes l ON o.licitacao_id = l.id
                    LEFT JOIN clientes c ON o.cliente_id = c.id
                    WHERE o.status = ?
                    ORDER BY o.score DESC
                """, (status,))
            else:
                cursor.execute("""
                    SELECT o.*, l.objeto, l.orgao, l.valor_estimado, l.data_abertura,
                           c.nome as cliente_nome, c.whatsapp as cliente_whatsapp, c.email as cliente_email
                    FROM oportunidades o
                    JOIN licitacoes l ON o.licitacao_id = l.id
                    LEFT JOIN clientes c ON o.cliente_id = c.id
                    ORDER BY o.score DESC
                """)
            return self._rows_to_list(cursor.fetchall())
        finally:
            conn.close()

    def atualizar_oportunidade(self, id: int, dados: Dict):
        """Atualiza uma oportunidade."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            updates = []
            values = []
            for key, value in dados.items():
                updates.append(f"{key} = ?")
                values.append(value)
            values.append(id)
            cursor.execute(f"UPDATE oportunidades SET {', '.join(updates)} WHERE id = ?", values)
            conn.commit()
        finally:
            conn.close()

    # ==========================================
    # COMISSOES
    # ==========================================
    def criar_comissao(self, dados: Dict) -> int:
        """Registra uma comissao a receber."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO comissoes (oportunidade_id, cliente_id, valor_contrato, percentual,
                    valor_comissao, tipo, status, data_vencimento, observacoes)
                VALUES (:oportunidade_id, :cliente_id, :valor_contrato, :percentual,
                    :valor_comissao, :tipo, :status, :data_vencimento, :observacoes)
            """, dados)
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def listar_comissoes_a_receber(self) -> List[Dict]:
        """Lista comissoes pendentes."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.*, cl.nome as cliente_nome, l.objeto as licitacao_objeto
                FROM comissoes c
                LEFT JOIN clientes cl ON c.cliente_id = cl.id
                LEFT JOIN oportunidades o ON c.oportunidade_id = o.id
                LEFT JOIN licitacoes l ON o.licitacao_id = l.id
                WHERE c.status IN ('A_RECEBER', 'ATRASADA')
                ORDER BY c.data_vencimento ASC
            """)
            return self._rows_to_list(cursor.fetchall())
        finally:
            conn.close()

    def registrar_pagamento(self, dados: Dict) -> int:
        """Registra pagamento de comissao."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pagamentos (comissao_id, valor, data_pagamento, metodo, comprovante, observacoes)
                VALUES (:comissao_id, :valor, :data_pagamento, :metodo, :comprovante, :observacoes)
            """, dados)
            conn.commit()

            # Atualiza status da comissao
            cursor.execute("""
                UPDATE comissoes SET status = 'RECEBIDA', data_recebimento = :data_pagamento
                WHERE id = :comissao_id
            """, dados)
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    # ==========================================
    # NOTIFICACOES
    # ==========================================
    def criar_notificacao(self, dados: Dict) -> int:
        """Cria uma notificacao na fila."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO notificacoes (cliente_id, oportunidade_id, tipo, titulo, mensagem, status)
                VALUES (:cliente_id, :oportunidade_id, :tipo, :titulo, :mensagem, 'PENDENTE')
            """, dados)
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def listar_notificacoes_pendentes(self) -> List[Dict]:
        """Lista notificacoes a enviar."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT n.*, cl.nome as cliente_nome, cl.whatsapp, cl.email
                FROM notificacoes n
                LEFT JOIN clientes cl ON n.cliente_id = cl.id
                WHERE n.status = 'PENDENTE'
                ORDER BY n.criado_em ASC
            """)
            return self._rows_to_list(cursor.fetchall())
        finally:
            conn.close()

    def marcar_notificacao_enviada(self, id: int):
        """Marca notificacao como enviada."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE notificacoes SET status = 'ENVIADA', data_envio = CURRENT_TIMESTAMP WHERE id = ?
            """, (id,))
            conn.commit()
        finally:
            conn.close()

    # ==========================================
    # LOGS
    # ==========================================
    def log(self, tipo: str, modulo: str, acao: str, descricao: str, detalhes: str = None):
        """Registra log de atividade."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO logs (tipo, modulo, acao, descricao, detalhes)
                VALUES (?, ?, ?, ?, ?)
            """, (tipo, modulo, acao, descricao, detalhes))
            conn.commit()
        finally:
            conn.close()

    # ==========================================
    # CONFIGURACOES
    # ==========================================
    def get_config(self, chave: str, default: Any = None) -> Optional[str]:
        """Le configuração."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT valor FROM configuracoes WHERE chave = ?", (chave,))
            row = cursor.fetchone()
            return row['valor'] if row else default
        finally:
            conn.close()

    def set_config(self, chave: str, valor: str, tipo: str = 'TEXTO', descricao: str = ''):
        """Define configuração."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO configuracoes (chave, valor, tipo, descricao)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(chave) DO UPDATE SET valor=excluded.valor, atualizado_em=CURRENT_TIMESTAMP
            """, (chave, valor, tipo, descricao))
            conn.commit()
        finally:
            conn.close()

    # ==========================================
    # ESTATISTICAS E RELATORIOS
    # ==========================================
    def get_stats(self) -> Dict:
        """Retorna estatisticas do sistema."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            stats = {}

            cursor.execute("SELECT COUNT(*) FROM clientes WHERE ativo = 1")
            stats['clientes_ativos'] = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM licitacoes WHERE status IN ('ABERTA', 'EM_ANDAMENTO')")
            stats['licitacoes_abertas'] = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM oportunidades WHERE status = 'PENDENTE'")
            stats['oportunidades_pendentes'] = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*) FROM oportunidades
                WHERE status = 'VENCEDORA'
            """)
            stats['licitacoes_vencidas'] = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COALESCE(SUM(valor_comissao), 0) FROM comissoes
                WHERE status IN ('A_RECEBER', 'ATRASADA')
            """)
            stats['comissoes_a_receber'] = cursor.fetchone()[0]

            cursor.execute("SELECT COALESCE(SUM(valor), 0) FROM pagamentos")
            stats['total_recebido'] = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COALESCE(SUM(valor_comissao), 0) FROM comissoes
                WHERE status = 'RECEBIDA'
            """)
            stats['comissoes_recebidas'] = cursor.fetchone()[0]

            return stats
        finally:
            conn.close()


# Singleton
_db_instance = None

def get_db() -> DatabaseManager:
    """Retorna instancia unica do DatabaseManager."""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseManager()
    return _db_instance