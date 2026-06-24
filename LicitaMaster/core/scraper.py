# ============================================================
# LicitaMaster - Scraper de Licitacoes
# Raspa portais publicos gratuitos de licitacao
# Fontes: PNCP, ComprasNet, Diarios Oficiais
# ============================================================

import requests
import re
import json
import hashlib
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from urllib.parse import quote, urljoin
import time


class ScraperLicitacoes:
    """Raspador de licitacoes de portais publicos gratuitos."""

    def __init__(self, db=None):
        self.db = db
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/json,*/*',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8'
        })
        self.dias_busca = 7
        self.valor_minimo = 5000

    def _gerar_codigo(self, fonte: str, numero: str, orgao: str) -> str:
        """Gera codigo unico para a licitacao."""
        raw = f"{fonte}|{numero}|{orgao}|{datetime.now().date()}"
        return hashlib.md5(raw.encode()).hexdigest()[:16]

    def _extrair_valor(self, texto: str) -> Optional[float]:
        """Extrai valor monetario de um texto."""
        if not texto:
            return None
        match = re.search(r'(?:R\$\s*)?([\d.,]+)', str(texto).replace('.', '').replace(',', '.'))
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
        return None

    def _parse_data(self, texto: str) -> Optional[str]:
        """Converte texto de data para ISO."""
        if not texto:
            return None
        # Tenta varios formatos
        formatos = [
            '%d/%m/%Y', '%Y-%m-%d', '%d/%m/%y',
            '%d-%m-%Y', '%Y/%m/%d'
        ]
        for fmt in formatos:
            try:
                return datetime.strptime(texto.strip(), fmt).strftime('%Y-%m-%d')
            except ValueError:
                continue
        return None

    # ==========================================
    # PNCP - Portal Nacional de Contratacoes
    # ==========================================
    def buscar_pncp(self, uf: str = None, palavras_chave: List[str] = None) -> List[Dict]:
        """
        Busca licitacoes no PNCP (Portal Nacional de Contratacoes Publicas).
        API publica: https://pncp.gov.br/api
        """
        resultados = []
        try:
            url = "https://pncp.gov.br/api/pncp/v1/orgaos"
            resp = self.session.get(url, timeout=15)
            if resp.status_code != 200:
                return resultados

            orgaos = resp.json()
            # Limita a 5 orgaos por busca para nao sobrecarregar
            for orgao in orgaos[:5]:
                cnpj = orgao.get('cnpj')
                if not cnpj:
                    continue

                url_compras = f"https://pncp.gov.br/api/pncp/v1/orgaos/{cnpj}/compras"
                params = {
                    'ano': datetime.now().year,
                    'pagina': 1,
                    'tamanhoPagina': 50
                }
                resp = self.session.get(url_compras, params=params, timeout=15)
                if resp.status_code != 200:
                    continue

                data = resp.json()
                compras = data if isinstance(data, list) else data.get('data', [])

                for compra in compras:
                    licitacao = self._parse_pncp_item(compra, orgao)
                    if licitacao and licitacao.get('valor_estimado', 0) >= self.valor_minimo:
                        resultados.append(licitacao)

                time.sleep(1)  # Delay para nao sobrecarregar

        except Exception as e:
            if self.db:
                self.db.log('ERRO', 'SCRAPER', 'pncp', str(e))

        return resultados

    def _parse_pncp_item(self, item: Dict, orgao: Dict) -> Optional[Dict]:
        """Converte item do PNCP para formato padrao."""
        try:
            objeto = item.get('objeto', '') or item.get('descricao', '')
            if not objeto:
                return None

            valor = self._extrair_valor(str(item.get('valorTotal', '0')))

            return {
                'numero': str(item.get('numero', '')),
                'orgao': orgao.get('nome', ''),
                'uf': orgao.get('uf', ''),
                'modalidade': item.get('modalidade', {}).get('nome', 'PREGAO'),
                'tipo': item.get('tipo', 'MENOR_PRECO'),
                'objeto': objeto[:500],
                'descricao': objeto,
                'valor_estimado': valor or 0,
                'valor_maximo': valor or 0,
                'data_publicacao': self._parse_data(item.get('dataPublicacao', '')),
                'data_abertura': self._parse_data(item.get('dataAberturaProposta', '')),
                'codigo': self._gerar_codigo('PNCP', str(item.get('id', '')), orgao.get('cnpj', '')),
                'fonte': 'PNCP',
                'url_edital': f"https://pncp.gov.br/editais/{item.get('id', '')}",
                'url_pncp': f"https://pncp.gov.br/app/editais/{item.get('id', '')}",
                'status': 'ABERTA',
                'cnpj_orgao': orgao.get('cnpj', '')
            }
        except Exception:
            return None

    # ==========================================
    # COMPRASNET (Portal de Compras do Governo)
    # ==========================================
    def buscar_comprasnet(self, uf: str = 'SP') -> List[Dict]:
        """
        Busca licitacoes no ComprasNet.
        Portal: https://www.gov.br/compras
        """
        resultados = []
        try:
            url = "https://www.gov.br/compras/pt-br/acesso-a-informacao/licitacoes"
            resp = self.session.get(url, timeout=15)
            if resp.status_code != 200:
                return resultados

            soup = BeautifulSoup(resp.text, 'lxml')

            # Busca por links de editais
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                texto = link.get_text(strip=True)

                if any(p in href.lower() for p in ['edital', 'licitacao', 'pregao']):
                    licitacao = {
                        'numero': texto,
                        'orgao': 'Governo Federal - ComprasNet',
                        'uf': 'BR',
                        'modalidade': self._detectar_modalidade(texto),
                        'objeto': texto[:500],
                        'descricao': texto,
                        'fonte': 'COMPRASNET',
                        'url_edital': href if href.startswith('http') else urljoin(url, href),
                        'status': 'ABERTA',
                        'codigo': self._gerar_codigo('COMPRASNET', texto, 'gov'),
                        'data_publicacao': datetime.now().strftime('%Y-%m-%d')
                    }
                    resultados.append(licitacao)

        except Exception as e:
            if self.db:
                self.db.log('ERRO', 'SCRAPER', 'comprasnet', str(e))

        return resultados

    # ==========================================
    # BUSCA GENERICA EM DIARIOS OFICIAIS
    # ==========================================
    def buscar_diarios_oficiais(self, estados: List[str] = None) -> List[Dict]:
        """
        Busca licitacoes em diarios oficiais dos estados.
        """
        resultados = []
        if estados is None:
            estados = ['SP', 'RJ', 'MG', 'RS', 'BA', 'PR', 'SC', 'DF']

        url_templates = {
            'SP': 'https://www.imprensaoficial.com.br/DO/Busca',
            'RJ': 'https://www.ioerj.com.br/portal/busca',
            'MG': 'https://www.iof.mg.gov.br/busca',
        }

        for estado in estados:
            try:
                url = url_templates.get(estado, f'https://www.diariooficial.{estado.lower()}.gov.br')
                resp = self.session.get(url, timeout=10)
                if resp.status_code != 200:
                    continue

                soup = BeautifulSoup(resp.text, 'lxml')
                texto = soup.get_text()

                # Busca por palavras-chave de licitacao
                padrao = r'(?:LICITACAO|PREGAO|CONCORRENCIA|TOMADA\s*DE\s*PRECOS).{50,500}?(?:R\$\s*[\d.,]+)?'
                matches = re.findall(padrao, texto, re.IGNORECASE)

                for match in matches[:20]:  # Limita a 20 por estado
                    valor = self._extrair_valor(match)
                    if valor and valor >= self.valor_minimo:
                        resultados.append({
                            'numero': '',
                            'orgao': f'Diario Oficial {estado}',
                            'uf': estado,
                            'modalidade': self._detectar_modalidade(match),
                            'objeto': match[:500],
                            'descricao': match,
                            'valor_estimado': valor,
                            'fonte': f'DIARIO_{estado}',
                            'status': 'ABERTA',
                            'codigo': self._gerar_codigo(f'DO_{estado}', match[:50], estado),
                            'data_publicacao': datetime.now().strftime('%Y-%m-%d')
                        })

                time.sleep(1)

            except Exception as e:
                if self.db:
                    self.db.log('AVISO', 'SCRAPER', f'diario_{estado}', str(e))

        return resultados

    # ==========================================
    # BUSCA NO TCE (Tribunal de Contas)
    # ==========================================
    def buscar_tce(self) -> List[Dict]:
        """Busca licitacoes nos Tribunais de Contas."""
        resultados = []
        try:
            url = "https://www.tce.sp.gov.br/licitacoes"
            resp = self.session.get(url, timeout=15)
            if resp.status_code != 200:
                return resultados

            soup = BeautifulSoup(resp.text, 'lxml')
            for row in soup.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) >= 3:
                    objeto = cols[0].get_text(strip=True)
                    valor_texto = cols[1].get_text(strip=True) if len(cols) > 1 else ''
                    valor = self._extrair_valor(valor_texto)

                    if valor and valor >= self.valor_minimo:
                        resultados.append({
                            'numero': cols[2].get_text(strip=True) if len(cols) > 2 else '',
                            'orgao': 'Tribunal de Contas',
                            'uf': 'SP',
                            'modalidade': self._detectar_modalidade(objeto),
                            'objeto': objeto[:500],
                            'descricao': objeto,
                            'valor_estimado': valor,
                            'fonte': 'TCE',
                            'status': 'ABERTA',
                            'codigo': self._gerar_codigo('TCE', objeto[:50], 'tce'),
                            'data_publicacao': datetime.now().strftime('%Y-%m-%d')
                        })

        except Exception as e:
            if self.db:
                self.db.log('ERRO', 'SCRAPER', 'tce', str(e))

        return resultados

    # ==========================================
    # UTILITARIOS
    # ==========================================
    def _detectar_modalidade(self, texto: str) -> str:
        """Detecta modalidade de licitacao pelo texto."""
        texto = texto.upper()
        if 'PREGAO' in texto:
            return 'PREGAO'
        if 'CONCORRENCIA' in texto:
            return 'CONCORRENCIA'
        if 'TOMADA' in texto and 'PRECO' in texto:
            return 'TOMADA_PRECO'
        if 'CONVITE' in texto:
            return 'CONVITE'
        if 'CONCURSO' in texto:
            return 'CONCURSO'
        if 'LEILAO' in texto:
            return 'LEILAO'
        if 'DISPENSA' in texto:
            return 'DISPENSA'
        if 'INEXIGIBILIDADE' in texto:
            return 'INEXIGIBILIDADE'
        return 'PREGAO'

    def buscar_todas(self, uf: str = None) -> List[Dict]:
        """
        Busca licitacoes em todas as fontes disponiveis.
        Retorna lista de licitacoes encontradas.
        """
        todas = []

        if self.db:
            self.db.log('INFO', 'SCRAPER', 'busca_todas', 'Iniciando varredura de licitacoes')

        # 1. PNCP
        try:
            pncp = self.buscar_pncp(uf)
            todas.extend(pncp)
            if self.db:
                self.db.log('SUCESSO', 'SCRAPER', 'pncp', f'Encontradas {len(pncp)} licitacoes no PNCP')
        except Exception as e:
            if self.db:
                self.db.log('ERRO', 'SCRAPER', 'pncp', str(e))

        # 2. ComprasNet
        try:
            comprasnet = self.buscar_comprasnet(uf)
            todas.extend(comprasnet)
        except Exception as e:
            if self.db:
                self.db.log('ERRO', 'SCRAPER', 'comprasnet', str(e))

        # 3. Diarios Oficiais
        try:
            diarios = self.buscar_diarios_oficiais()
            todas.extend(diarios)
        except Exception as e:
            if self.db:
                self.db.log('ERRO', 'SCRAPER', 'diarios', str(e))

        # 4. TCE
        try:
            tce = self.buscar_tce()
            todas.extend(tce)
        except Exception as e:
            if self.db:
                self.db.log('ERRO', 'SCRAPER', 'tce', str(e))

        # Remove duplicatas pelo codigo
        vistas = set()
        unicas = []
        for lic in todas:
            if lic['codigo'] not in vistas:
                vistas.add(lic['codigo'])
                unicas.append(lic)

        if self.db:
            self.db.log('SUCESSO', 'SCRAPER', 'busca_todas',
                        f'Total: {len(unicas)} licitacoes unicas encontradas')

        return unicas


def buscar_licitacoes(db=None) -> List[Dict]:
    """Funcao de conveniencia para buscar licitacoes."""
    scraper = ScraperLicitacoes(db)
    return scraper.buscar_todas()