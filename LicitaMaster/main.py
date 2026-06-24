#!/usr/bin/env python3
# ============================================================
# LicitaMaster - Sistema Automatico de Licitacoes
# Version: 1.0.0
# ============================================================
# Este sistema prospecta clientes, encontra licitacoes,
# faz match automatico, gera propostas e gerencia comissoes.
# 100% gratuito - sem APIs pagas
# ============================================================

import os
import sys
import time
from datetime import datetime
from typing import List, Dict, Optional

# Adiciona diretorio raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.database import DatabaseManager, get_db
from core.scraper import ScraperLicitacoes, buscar_licitacoes
from core.analyzer import Analyzer, analisar_licitacoes
from commercial.commission import CommissionEngine, calcular_repasse
from integration.whatsapp_bot import WhatsAppBot


class LicitaMaster:
    """Sistema principal - orquestra todos os modulos."""

    def __init__(self):
        self.db = get_db()
        self.scraper = ScraperLicitacoes(self.db)
        self.analyzer = Analyzer(self.db)
        self.commission = CommissionEngine(self.db)
        self.whatsapp = WhatsAppBot(self.db)

        # Configuracoes
        self.comissao_padrao = float(self.db.get_config('COMISSAO_PADRAO', '5'))
        self.intervalo_varredura = int(self.db.get_config('INTERVALO_VARREDURA', '60'))

    def iniciar(self):
        """Inicia o sistema em modo interativo."""
        print(f"""
+==================================================+
|            LICITAMASTER v1.0.0                    |
|    Sistema Automatico de Licitacoes              |
|    100% Gratuito - IA Local - Offline First      |
+==================================================+
| Criado por: {self.db.get_config('CRIADOR_NOME', 'Usuario')}
+==================================================+
        """)

        while True:
            print("\n" + "=" * 50)
            print("MENU PRINCIPAL")
            print("=" * 50)
            print("  [1]  Buscar Licitacoes (Scraping)")
            print("  [2]  Analisar Oportunidades")
            print("  [3]  Notificar Clientes (WhatsApp)")
            print("  [4]  Relatorio Financeiro")
            print("  [5]  Registrar Cliente")
            print("  [6]  Listar Clientes")
            print("  [7]  Listar Oportunidades")
            print("  [8]  Calcular Comissao")
            print("  [9]  Executar Ciclo Completo")
            print("  [10] Estatisticas do Sistema")
            print("  [11] Modo Automatico (Loop)")
            print("  [0]  Sair")
            print("-" * 50)

            opcao = input("Escolha: ").strip()

            if opcao == "0":
                print("\nEncerrando LicitaMaster...")
                break
            elif opcao == "1":
                self.menu_buscar_licitacoes()
            elif opcao == "2":
                self.menu_analisar_oportunidades()
            elif opcao == "3":
                self.menu_notificar_clientes()
            elif opcao == "4":
                self.menu_relatorio_financeiro()
            elif opcao == "5":
                self.menu_registrar_cliente()
            elif opcao == "6":
                self.menu_listar_clientes()
            elif opcao == "7":
                self.menu_listar_oportunidades()
            elif opcao == "8":
                self.menu_calcular_comissao()
            elif opcao == "9":
                self.executar_ciclo_completo()
            elif opcao == "10":
                self.menu_estatisticas()
            elif opcao == "11":
                self.modo_automatico()
            else:
                print("Opcao invalida!")

            if opcao != "0":
                input("\nPressione ENTER para continuar...")

    def menu_buscar_licitacoes(self):
        """Busca licitacoes nos portais."""
        print("\n>>> BUSCANDO LICITACOES...")
        self.db.log('INFO', 'SYSTEM', 'busca', 'Iniciando busca de licitacoes')

        licitacoes = buscar_licitacoes(self.db)

        if not licitacoes:
            print("Nenhuma licitacao encontrada no momento.")
            print("Dica: Verifique sua conexao com a internet.")
            return

        # Salva no banco
        salvas = 0
        for lic in licitacoes:
            try:
                self.db.adicionar_licitacao(lic)
                salvas += 1
            except Exception:
                pass

        print(f"\nEncontradas: {len(licitacoes)} licitacoes")
        print(f"Salvas no banco: {salvas}")

        # Mostra as primeiras
        for i, lic in enumerate(licitacoes[:5], 1):
            print(f"\n  {i}. {lic.get('objeto', '')[:100]}...")
            print(f"     Orgao: {lic.get('orgao', 'N/A')}")
            print(f"     Valor: R$ {lic.get('valor_estimado', 0):,.2f}")
            print(f"     Fonte: {lic.get('fonte', 'N/A')}")

        self.db.log('SUCESSO', 'SYSTEM', 'busca', f'{len(licitacoes)} licitacoes encontradas')

    def menu_analisar_oportunidades(self):
        """Analisa licitacoes e gera oportunidades."""
        print("\n>>> ANALISANDO OPORTUNIDADES...")

        licitacoes = self.db.listar_licitacoes_abertas()
        clientes = self.db.listar_clientes()

        if not licitacoes:
            print("Nenhuma licitacao encontrada. Busque primeiro (opcao 1).")
            return

        if not clientes:
            print("Nenhum cliente cadastrado. Cadastre clientes (opcao 5).")
            return

        print(f"Analisando {len(licitacoes)} licitacoes para {len(clientes)} clientes...")

        oportunidades = analisar_licitacoes(licitacoes, clientes, self.db, self.comissao_padrao)

        if not oportunidades:
            print("Nenhuma oportunidade gerada.")
            return

        # Salva oportunidades no banco
        salvas = 0
        for op in oportunidades:
            try:
                self.db.criar_oportunidade(op)
                salvas += 1
            except Exception:
                pass

        print(f"\nOportunidades geradas: {len(oportunidades)}")
        print(f"Salvas no banco: {salvas}")

        # Mostra as melhores
        for i, op in enumerate(oportunidades[:5], 1):
            print(f"\n  {i}. Cliente: {op.get('cliente_nome', 'N/A')}")
            print(f"     Licitacao: {op.get('licitacao_objeto', '')[:100]}...")
            print(f"     Score: {op.get('score', 0):.0f}% ({op.get('afinidade', 'N/A')})")
            print(f"     Comissao estimada: R$ {op.get('comissao_estimada', 0):.2f}")

    def menu_notificar_clientes(self):
        """Notifica clientes sobre oportunidades."""
        print("\n>>> NOTIFICANDO CLIENTES...")

        oportunidades = self.db.listar_oportunidades('PENDENTE')

        if not oportunidades:
            print("Nenhuma oportunidade pendente. Analise primeiro (opcao 2).")
            return

        # Monta dict de clientes
        clientes = {}
        for op in oportunidades:
            cid = op.get('cliente_id')
            if cid and cid not in clientes:
                cliente = self.db.buscar_cliente(id=cid)
                if cliente:
                    clientes[cid] = cliente

        print(f"Notificacoes a enviar: {len(oportunidades)}")
        print(f"Clientes envolvidos: {len(clientes)}")

        for op in oportunidades[:3]:
            cliente = clientes.get(op.get('cliente_id'), {})
            print(f"\n  -> {cliente.get('nome', 'N/A')}: {op.get('licitacao_objeto', '')[:80]}...")

        confirmar = input("\nEnviar notificacoes? (s/N): ").lower()
        if confirmar == 's':
            stats = self.whatsapp.enviar_oportunidades_em_massa(oportunidades, clientes)
            print(f"\nEnviadas: {stats['enviadas']}, Falhas: {stats['falhas']}")

            # Marca como notificadas
            for op in oportunidades:
                self.db.atualizar_oportunidade(op.get('id'), {'status': 'NOTIFICADO'})
        else:
            print("Notificacoes nao enviadas.")

    def menu_relatorio_financeiro(self):
        """Exibe relatorio financeiro."""
        print("\n>>> RELATORIO FINANCEIRO")
        relatorio = self.commission.relatorio_financeiro()

        if 'erro' in relatorio:
            print(f"Erro: {relatorio['erro']}")
            return

        resumo = relatorio.get('resumo', {})
        print(f"\nData: {relatorio.get('data', 'N/A')}")
        print("-" * 40)
        print(f"Total recebido:     R$ {resumo.get('total_recebido', 0):,.2f}")
        print(f"A receber:          R$ {resumo.get('a_receber', 0):,.2f}")
        print(f"Total geral:        R$ {resumo.get('total_geral', 0):,.2f}")
        print(f"Licitacoes vencidas: {resumo.get('licitacoes_vencidas', 0)}")
        print(f"Clientes ativos:    {resumo.get('clientes_ativos', 0)}")
        print(f"Oportunidades:      {resumo.get('oportunidades_pendentes', 0)}")
        print("-" * 40)

        # Calcula repasse do criador
        total_recebido = resumo.get('total_recebido', 0)
        if total_recebido > 0:
            repasse = calcular_repasse(total_recebido)
            print(f"\nRepasse ao criador ({repasse['percentual_repasse']}%):")
            print(f"  Valor repasse: R$ {repasse['valor_repasse']:.2f}")
            print(f"  Seu lucro liquido: R$ {repasse['valor_liquido']:.2f}")

        comissoes = relatorio.get('comissoes_pendentes', [])
        if comissoes:
            print(f"\nComissoes pendentes ({len(comissoes)}):")
            for c in comissoes[:5]:
                print(f"  R$ {c.get('valor_comissao', 0):.2f} - {c.get('cliente_nome', 'N/A')} - {c.get('status', 'N/A')}")

    def menu_registrar_cliente(self):
        """Cadastra um novo cliente."""
        print("\n>>> CADASTRO DE CLIENTE")
        print("(Deixe em branco para pular campos nao obrigatorios)")

        nome = input("Nome da empresa: ").strip()
        if not nome:
            print("Nome e obrigatorio!")
            return

        cliente = {
            'nome': nome,
            'cnpj': input("CNPJ (apenas numeros): ").strip(),
            'email': input("Email: ").strip(),
            'telefone': input("Telefone: ").strip(),
            'whatsapp': input("WhatsApp (com DDI, ex: 5511999999999): ").strip(),
            'site': input("Site: ").strip(),
            'ramo': input("Ramo (TI, SAUDE, CONSTRUCAO, etc): ").upper().strip(),
            'porte': input("Porte (MEI, ME, EPP, MEDIO, GRANDE): ").upper().strip(),
            'estado': input("Estado (UF): ").upper().strip(),
            'cidade': input("Cidade: ").strip()
        }

        try:
            cliente_id = self.db.adicionar_cliente(cliente)
            print(f"\nCliente cadastrado com sucesso! ID: {cliente_id}")
            self.db.log('SUCESSO', 'CLIENTE', 'cadastro', f'Cliente {nome} cadastrado')
        except Exception as e:
            print(f"Erro ao cadastrar: {e}")

    def menu_listar_clientes(self):
        """Lista todos os clientes."""
        clientes = self.db.listar_clientes()

        if not clientes:
            print("\nNenhum cliente cadastrado.")
            return

        print(f"\n>>> CLIENTES CADASTRADOS ({len(clientes)})")
        print("-" * 80)
        for i, c in enumerate(clientes, 1):
            print(f"  {i}. {c.get('nome', 'N/A')}")
            print(f"     Ramo: {c.get('ramo', 'N/A')} | Porte: {c.get('porte', 'N/A')}")
            print(f"     WhatsApp: {c.get('whatsapp', 'N/A')}")
            print(f"     Estado: {c.get('estado', 'N/A')}")
            print()

    def menu_listar_oportunidades(self):
        """Lista oportunidades."""
        oportunidades = self.db.listar_oportunidades()

        if not oportunidades:
            print("\nNenhuma oportunidade encontrada.")
            return

        print(f"\n>>> OPORTUNIDADES ({len(oportunidades)})")
        print("-" * 80)
        for i, op in enumerate(oportunidades[:10], 1):
            print(f"  {i}. Cliente: {op.get('cliente_nome', 'N/A')}")
            print(f"     Objeto: {(op.get('licitacao_objeto', '') or '')[:100]}")
            print(f"     Score: {op.get('score', 0):.0f}% | Status: {op.get('status', 'N/A')}")
            print(f"     Comissao: R$ {op.get('comissao_estimada', 0):.2f}")

    def menu_calcular_comissao(self):
        """Calcula comissao sobre um valor."""
        try:
            valor = float(input("Valor do contrato/licitacao (R$): "))
            perc = input("Percentual de comissao (1-10%, default 5%): ").strip()
            perc = float(perc) if perc else 5.0

            resultado = self.commission.calcular_comissao(valor, perc)

            print(f"\n>>> CALCULO DE COMISSAO")
            print(f"Valor do contrato:     R$ {resultado['valor_contrato']:,.2f}")
            print(f"Percentual:            {resultado['percentual']:.1f}%")
            print(f"Valor da comissao:     R$ {resultado['valor_comissao']:,.2f}")
            print(f"Comissao do criador:   R$ {resultado['comissao_criador']:,.2f}")
            print(f"Seu lucro:             R$ {resultado['comissao_sistema']:,.2f}")
        except ValueError:
            print("Valor invalido!")

    def menu_estatisticas(self):
        """Exibe estatisticas do sistema."""
        stats = self.db.get_stats()

        print("\n>>> ESTATISTICAS DO SISTEMA")
        print("-" * 40)
        print(f"Clientes ativos:         {stats.get('clientes_ativos', 0)}")
        print(f"Licitacoes abertas:      {stats.get('licitacoes_abertas', 0)}")
        print(f"Oportunidades pendentes: {stats.get('oportunidades_pendentes', 0)}")
        print(f"Licitacoes vencidas:     {stats.get('licitacoes_vencidas', 0)}")
        print(f"Comissoes a receber:     R$ {stats.get('comissoes_a_receber', 0):,.2f}")
        print(f"Total recebido:          R$ {stats.get('total_recebido', 0):,.2f}")

    def executar_ciclo_completo(self):
        """
        Executa o ciclo completo:
        1. Busca licitacoes
        2. Analisa oportunidades
        3. Notifica clientes
        """
        print("\n>>> CICLO COMPLETO")
        print("1/3 Buscando licitacoes...")
        self.menu_buscar_licitacoes()

        print("\n2/3 Analisando oportunidades...")
        self.menu_analisar_oportunidades()

        print("\n3/3 Notificando clientes...")
        self.menu_notificar_clientes()

        self.db.log('SUCESSO', 'SYSTEM', 'ciclo_completo', 'Ciclo completo executado')

    def modo_automatico(self):
        """
        Modo automatico - fica em loop executando o ciclo.
        """
        print(f"\n>>> MODO AUTOMATICO")
        print(f"Intervalo entre varreduras: {self.intervalo_varredura} minutos")
        print("Pressione CTRL+C para parar.\n")

        try:
            while True:
                print(f"\n[{datetime.now().strftime('%d/%m/%Y %H:%M')}] Executando ciclo...")

                # 1. Busca
                self.menu_buscar_licitacoes()

                # 2. Analisa
                self.menu_analisar_oportunidades()

                # 3. Notifica (automatico)
                oportunidades = self.db.listar_oportunidades('PENDENTE')
                if oportunidades:
                    clientes_dict = {}
                    for op in oportunidades:
                        cid = op.get('cliente_id')
                        if cid and cid not in clientes_dict:
                            cliente = self.db.buscar_cliente(id=cid)
                            if cliente:
                                clientes_dict[cid] = cliente

                    if clientes_dict:
                        stats = self.whatsapp.enviar_oportunidades_em_massa(oportunidades, clientes_dict)
                        print(f"Notificacoes: {stats['enviadas']} enviadas, {stats['falhas']} falhas")

                        for op in oportunidades:
                            self.db.atualizar_oportunidade(op.get('id'), {'status': 'NOTIFICADO'})

                # Aguarda proximo ciclo
                print(f"\nAguardando {self.intervalo_varredura} minutos...")
                for seg in range(self.intervalo_varredura * 60, 0, -60):
                    print(f"  Proximo ciclo em {seg//60} min...")
                    time.sleep(60)

        except KeyboardInterrupt:
            print("\n\nModo automatico interrompido.")


def main():
    """Ponto de entrada principal."""
    import argparse

    parser = argparse.ArgumentParser(description='LicitaMaster - Sistema Automatico de Licitacoes')
    parser.add_argument('--modo', choices=['menu', 'auto', 'busca', 'analise'],
                       default='menu', help='Modo de operacao')
    parser.add_argument('--intervalo', type=int, default=60,
                       help='Intervalo entre varreduras em minutos (modo auto)')

    args = parser.parse_args()

    app = LicitaMaster()

    if args.modo == 'auto':
        app.intervalo_varredura = args.intervalo
        app.modo_automatico()
    elif args.modo == 'busca':
        app.menu_buscar_licitacoes()
    elif args.modo == 'analise':
        app.menu_analisar_oportunidades()
    else:
        app.iniciar()


if __name__ == '__main__':
    main()