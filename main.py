from app.core.database import Database
from app.core.idioma import Idioma

# Estados / Cidades
from app.dao.estado_dao import Estado_DAO
from app.dao.cidade_dao import Cidade_DAO
from app.views.estado_view import Estado_View
from app.views.cidade_view import Cidade_View
from app.controllers.estado_controller import Estado_Controller
from app.controllers.cidade_controller import Cidade_Controller

# Tipos e status de imóvel
from app.dao.tipo_imovel_dao import Tipo_Imovel_DAO
from app.dao.status_imovel_dao import Status_Imovel_DAO
from app.views.tipo_imovel_view import Tipo_Imovel_View
from app.views.status_imovel_view import Status_Imovel_View
from app.controllers.tipo_imovel_controller import Tipo_Imovel_Controller
from app.controllers.status_imovel_controller import Status_Imovel_Controller

# Proprietários
from app.dao.proprietario_dao import Proprietario_DAO
from app.views.proprietario_view import Proprietario_View
from app.controllers.proprietario_controller import Proprietario_Controller

# Imóveis (+ N:N de proprietários)
from app.dao.imovel_dao import Imovel_DAO
from app.dao.participacao_proprietario_dao import Participacao_Proprietario_DAO
from app.views.imovel_view import Imovel_View
from app.controllers.imovel_controller import Imovel_Controller

# Referências de valor
from app.dao.referencia_m2_dao import Referencia_M2_DAO
from app.dao.referencia_iptu_dao import Referencia_Iptu_DAO
from app.views.referencia_m2_view import Referencia_M2_View
from app.views.referencia_iptu_view import Referencia_Iptu_View
from app.controllers.referencia_m2_controller import Referencia_M2_Controller
from app.controllers.referencia_iptu_controller import Referencia_Iptu_Controller

# Avaliações / Despesas / Movimentações (usados a partir do imóvel selecionado)
from app.dao.avaliacao_dao import Avaliacao_DAO
from app.dao.despesa_dao import Despesa_DAO
from app.dao.movimentacao_dao import Movimentacao_DAO

# Usuários / Login
from app.dao.usuario_dao import Usuario_DAO
from app.views.usuario_view import Usuario_View
from app.controllers.usuario_controller import Usuario_Controller
from app.views.login_view import Login_View
from app.controllers.login_controller import Login_Controller

# Dashboard
from app.views.dashboard_view import Dashboard_View
from app.controllers.dashboard_controller import Dashboard_Controller

import tkinter as tk


class PatrimonioImobApplication:
    """Janela principal: monta DAOs, controllers e menu (ponto de entrada)."""

    def __init__(self):
        """Cria o Tk, os DAOs e os controllers e abre o login."""
        self._database = Database()
        self._root = tk.Tk()
        self._usuario_logado = None

        self._janela_estados = None
        self._janela_cidades = None
        self._janela_tipos_imovel = None
        self._janela_status_imovel = None
        self._janela_proprietarios = None
        self._janela_imoveis = None
        self._janela_usuarios = None
        self._janela_referencia_m2 = None
        self._janela_referencia_iptu = None

        # ===========================
        # ESTADOS / CIDADES
        # ===========================

        self._dao_estados = Estado_DAO(self._database)
        self._ctrl_estados = Estado_Controller(dao=self._dao_estados, view=None)

        self._dao_cidades = Cidade_DAO(self._database, self._dao_estados)
        self._ctrl_cidades = Cidade_Controller(
            dao=self._dao_cidades, estado_dao=self._dao_estados, view=None
        )

        # ===========================
        # TIPOS E STATUS DE IMÓVEL
        # ===========================

        self._dao_tipos_imovel = Tipo_Imovel_DAO(self._database)
        self._ctrl_tipos_imovel = Tipo_Imovel_Controller(dao=self._dao_tipos_imovel, view=None)

        self._dao_status_imovel = Status_Imovel_DAO(self._database)
        self._ctrl_status_imovel = Status_Imovel_Controller(dao=self._dao_status_imovel, view=None)

        # ===========================
        # PROPRIETÁRIOS
        # ===========================

        self._dao_proprietarios = Proprietario_DAO(self._database, self._dao_cidades)
        self._ctrl_proprietarios = Proprietario_Controller(
            dao=self._dao_proprietarios,
            cidade_dao=self._dao_cidades,
            estado_dao=self._dao_estados,
            view=None
        )

        # ===========================
        # IMÓVEIS (+ N:N proprietários)
        # ===========================

        self._dao_imoveis = Imovel_DAO(
            self._database, self._dao_cidades, self._dao_tipos_imovel, self._dao_status_imovel
        )
        self._dao_participacoes = Participacao_Proprietario_DAO(
            self._database, self._dao_proprietarios
        )
        self._dao_avaliacoes = Avaliacao_DAO(self._database, self._dao_imoveis)
        self._dao_despesas = Despesa_DAO(self._database, self._dao_imoveis)
        self._dao_movimentacoes = Movimentacao_DAO(self._database, self._dao_imoveis)
        self._ctrl_imoveis = Imovel_Controller(
            dao=self._dao_imoveis,
            cidade_dao=self._dao_cidades,
            estado_dao=self._dao_estados,
            tipo_imovel_dao=self._dao_tipos_imovel,
            status_imovel_dao=self._dao_status_imovel,
            proprietario_dao=self._dao_proprietarios,
            participacao_proprietario_dao=self._dao_participacoes,
            avaliacao_dao=self._dao_avaliacoes,
            despesa_dao=self._dao_despesas,
            movimentacao_dao=self._dao_movimentacoes,
            view=None
        )

        # ===========================
        # REFERÊNCIAS DE VALOR
        # ===========================

        self._dao_referencia_m2 = Referencia_M2_DAO(
            self._database, self._dao_cidades, self._dao_tipos_imovel
        )
        self._ctrl_referencia_m2 = Referencia_M2_Controller(
            dao=self._dao_referencia_m2,
            cidade_dao=self._dao_cidades,
            tipo_imovel_dao=self._dao_tipos_imovel,
            view=None
        )

        self._dao_referencia_iptu = Referencia_Iptu_DAO(
            self._database, self._dao_cidades, self._dao_tipos_imovel
        )
        self._ctrl_referencia_iptu = Referencia_Iptu_Controller(
            dao=self._dao_referencia_iptu,
            cidade_dao=self._dao_cidades,
            tipo_imovel_dao=self._dao_tipos_imovel,
            view=None
        )

        # ===========================
        # USUÁRIOS
        # ===========================

        self._dao_usuarios = Usuario_DAO(self._database)
        self._ctrl_usuarios = Usuario_Controller(dao=self._dao_usuarios, view=None)

        # ===========================
        # DASHBOARD
        # ===========================

        self._ctrl_dashboard = Dashboard_Controller(
            imovel_dao=self._dao_imoveis,
            avaliacao_dao=self._dao_avaliacoes,
            referencia_m2_dao=self._dao_referencia_m2,
            referencia_iptu_dao=self._dao_referencia_iptu,
            view=None
        )

        self._iniciar_login()

    def _iniciar_login(self):
        """Mostra a tela de login (menu só com Idioma)."""
        for widget in self._root.winfo_children():
            widget.destroy()

        # antes do login o menu tem só o idioma
        menu_principal = tk.Menu(self._root)
        menu_principal.add_cascade(label=Idioma.t("menu.idioma"), menu=self._criar_menu_idioma(menu_principal))
        self._root.config(menu=menu_principal)

        ctrl_login = Login_Controller(
            usuario_dao=self._dao_usuarios,
            view=None,
            ao_autenticar=self._on_login_sucesso
        )
        ctrl_login.view = Login_View(self._root, ctrl_login)

    def _on_login_sucesso(self, usuario):
        """Guarda o usuário logado e monta a janela principal."""
        self._usuario_logado = usuario
        self._ctrl_usuarios.usuario_logado = usuario
        self._montar_janela_principal()

    def _montar_janela_principal(self):
        """Troca o login pelo dashboard e pelo menu completo."""
        for widget in self._root.winfo_children():
            widget.destroy()

        self._configurar_janela()
        self._criar_menu()

        self._ctrl_dashboard.view = Dashboard_View(self._root, self._ctrl_dashboard)

    def _configurar_janela(self):
        """Define o título (com o usuário logado) e o tamanho."""
        titulo = Idioma.t("app.nome")
        if self._usuario_logado is not None:
            titulo = f"{titulo} — {self._usuario_logado.nome} ({self._usuario_logado.login})"
        self._root.title(titulo)
        self._root.geometry("1000x700")

    def _criar_menu(self):
        """Cria o menu: Cadastros básicos, Imóveis, Usuários, Idioma, Sair."""
        menu_principal = tk.Menu(self._root)

        menu_cadastros_basicos = tk.Menu(menu_principal, tearoff=0)
        menu_cadastros_basicos.add_command(label=Idioma.t("menu.estados"), command=self._abrir_estados)
        menu_cadastros_basicos.add_command(label=Idioma.t("menu.cidades"), command=self._abrir_cidades)
        menu_cadastros_basicos.add_command(label=Idioma.t("menu.tipos_imovel"), command=self._abrir_tipos_imovel)
        menu_cadastros_basicos.add_command(label=Idioma.t("menu.status_imovel"), command=self._abrir_status_imovel)
        menu_cadastros_basicos.add_command(label=Idioma.t("menu.proprietarios"), command=self._abrir_proprietarios)
        menu_principal.add_cascade(label=Idioma.t("menu.cadastros_basicos"), menu=menu_cadastros_basicos)

        menu_imoveis = tk.Menu(menu_principal, tearoff=0)
        menu_imoveis.add_command(label=Idioma.t("menu.imoveis"), command=self._abrir_imoveis)
        menu_imoveis.add_command(label=Idioma.t("menu.referencia_m2"), command=self._abrir_referencia_m2)
        menu_imoveis.add_command(label=Idioma.t("menu.referencia_iptu"), command=self._abrir_referencia_iptu)
        menu_principal.add_cascade(label=Idioma.t("menu.imoveis"), menu=menu_imoveis)

        # todo usuário logado pode trocar a senha ou criar outro acesso
        menu_usuarios = tk.Menu(menu_principal, tearoff=0)
        menu_usuarios.add_command(label=Idioma.t("menu.usuarios"), command=self._abrir_usuarios)
        menu_principal.add_cascade(label=Idioma.t("menu.usuarios"), menu=menu_usuarios)

        menu_principal.add_cascade(label=Idioma.t("menu.idioma"), menu=self._criar_menu_idioma(menu_principal))

        menu_principal.add_command(label=Idioma.t("menu.sair"), command=self._root.destroy)

        self._root.config(menu=menu_principal)

    def _criar_menu_idioma(self, menu_principal):
        """Cria o submenu Português / English."""
        menu_idioma = tk.Menu(menu_principal, tearoff=0)
        menu_idioma.add_command(label=Idioma.t("menu.portugues"), command=self._selecionar_portugues)
        menu_idioma.add_command(label=Idioma.t("menu.ingles"), command=self._selecionar_ingles)
        return menu_idioma

    def _mudar_idioma(self, codigo):
        """Troca o idioma e reabre as janelas abertas já no novo idioma."""
        Idioma.definir(codigo)

        if self._usuario_logado is None:
            self._iniciar_login()
            return

        # as janelas abertas são fechadas e abertas de novo, já no novo idioma
        # (dados digitados e ainda não salvos nessas janelas são descartados)
        janelas = [
            ("_janela_estados", self._abrir_estados),
            ("_janela_cidades", self._abrir_cidades),
            ("_janela_tipos_imovel", self._abrir_tipos_imovel),
            ("_janela_status_imovel", self._abrir_status_imovel),
            ("_janela_proprietarios", self._abrir_proprietarios),
            ("_janela_imoveis", self._abrir_imoveis),
            ("_janela_usuarios", self._abrir_usuarios),
            ("_janela_referencia_m2", self._abrir_referencia_m2),
            ("_janela_referencia_iptu", self._abrir_referencia_iptu),
        ]
        reabrir = []
        for atributo, abrir in janelas:
            janela = getattr(self, atributo)
            if janela is not None and janela.winfo_exists():
                reabrir.append(abrir)
            setattr(self, atributo, None)

        self._montar_janela_principal()

        for abrir in reabrir:
            abrir()

    def _selecionar_portugues(self):
        """Menu Idioma → Português (método em vez de lambda)."""
        self._mudar_idioma("pt")

    def _selecionar_ingles(self):
        """Menu Idioma → English (método em vez de lambda)."""
        self._mudar_idioma("en")

    def _abrir_janela(self, atributo_janela, classe_view, controller):
        """Abre a tela em um Toplevel; se já estiver aberta, só traz para frente."""
        janela_existente = getattr(self, atributo_janela)
        if janela_existente is not None and janela_existente.winfo_exists():
            janela_existente.lift()
            janela_existente.focus_force()
            return
        janela = tk.Toplevel(self._root)
        setattr(self, atributo_janela, janela)
        controller.view = classe_view(janela, controller)
        controller.view.iniciar()

    def _abrir_estados(self):
        """Abre a tela de Estados."""
        self._abrir_janela("_janela_estados", Estado_View, self._ctrl_estados)

    def _abrir_cidades(self):
        """Abre a tela de Cidades."""
        self._abrir_janela("_janela_cidades", Cidade_View, self._ctrl_cidades)

    def _abrir_tipos_imovel(self):
        """Abre a tela de Tipos de imóvel."""
        self._abrir_janela("_janela_tipos_imovel", Tipo_Imovel_View, self._ctrl_tipos_imovel)

    def _abrir_status_imovel(self):
        """Abre a tela de Status de imóvel."""
        self._abrir_janela("_janela_status_imovel", Status_Imovel_View, self._ctrl_status_imovel)

    def _abrir_proprietarios(self):
        """Abre a tela de Proprietários."""
        self._abrir_janela("_janela_proprietarios", Proprietario_View, self._ctrl_proprietarios)

    def _abrir_imoveis(self):
        """Abre a tela de Imóveis."""
        self._abrir_janela("_janela_imoveis", Imovel_View, self._ctrl_imoveis)

    def _abrir_usuarios(self):
        """Abre a tela de Usuários."""
        self._abrir_janela("_janela_usuarios", Usuario_View, self._ctrl_usuarios)

    def _abrir_referencia_m2(self):
        """Abre a tela de Referência de valor m²."""
        self._abrir_janela("_janela_referencia_m2", Referencia_M2_View, self._ctrl_referencia_m2)

    def _abrir_referencia_iptu(self):
        """Abre a tela de Referência de IPTU."""
        self._abrir_janela("_janela_referencia_iptu", Referencia_Iptu_View, self._ctrl_referencia_iptu)

    def run(self):
        """Inicia o loop de eventos do Tkinter."""
        self._root.mainloop()


if __name__ == "__main__":
    app = PatrimonioImobApplication()
    app.run()
