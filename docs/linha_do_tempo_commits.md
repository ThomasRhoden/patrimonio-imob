# 🕒 Linha do tempo de commits (referência)

Plano de referência: as etapas de commit do repositório do professor (`eduardo-reus/t8711-crud-produtos`) e o que corresponde a cada uma no Patrimônio Imob. Serve para organizar os commits por etapa; não muda o sistema.

| Data (professor) | Etapa no projeto do professor | No Patrimônio Imob |
|---|---|---|
| 29/06 | Primeiro commit, arquitetura e model | Estrutura `app/` (models, dao, controllers, views, core), `main.py`, `models/estado.py` |
| 01/07 | CRUD de produtos com lista | CRUD de Estados com lista |
| 03/07 | Fornecedores + refatoração do `main` | Cidades, Tipos e Status de imóvel; menu *Cadastros básicos* no `main.py` |
| 08/07 | Cliente e usuário, encapsulamento + DAO genérico | `proprietario.py`, `usuario.py` com `@property`; `dao/dao.py` (`DAO(ABC)`) |
| 10/07 | Encapsulamento no model, campos calculados, `Data_Utils` | Validações em `imovel.py` (área privativa ≤ total); `core/data_utils.py` (datas e moeda) |
| 13/07 | DDL de produtos, classe `DataBase` | `migrations/*.create.sql` (13 tabelas), `core/database.py` |
| 15/07 | Produto completo | `imovel.py` completo (áreas, compra, cômodos, vagas) |
| 17/07 | DAOs para MySQL, `Data_Utils` genérica, alterar sem redigitar | DAOs com `mysql-connector`; selecionar na `Treeview` preenche o formulário |
| 20/07 | `conectar`/`desconectar` reutilizáveis + `try/finally`; controller com um método por ação | `DAO.conectar()`/`desconectar()` com `try/finally`; `salvar`/`alterar`/`excluir` nos controllers |
| 22/07 | Migration produto × fornecedor (FK 1:N) | `imovel.add.cidade_id.sql`, `add.tipo_imovel_id`, `add.status_id`; model `Imovel` recebe objetos |
| 24/07 | Estado e Cidade, filtro estado → cidade | Cascata estado → cidade em Imóveis e Proprietários (`Combobox`) |
| 27/07 – 31/07 | Exemplos Tkinter, correções, esqueleto de view | Esqueleto das views (formulário + `Treeview`), começando por `estado_view.py` |
| 02/08 – 03/08 | View parcial, `save`/`get_all`, CRUD concluído | CRUDs de cadastros básicos concluídos |
| 05/08 | Telas restantes, ID centralizado na `Treeview`, `requirements`, janela principal com menu | `imovel_view.py`, coluna ID centralizada, `requirements.txt`, janela principal com menu |
| 07/08 | Migrations N:N e CRUD com classe associativa; objetos em vez de IDs | `imovel_proprietario` + `participacao_proprietario.py` (soma ≤ 100%), popup em `Toplevel` |
| 12/08 | Novo CRUD com N:N; idiomas PT/EN; métodos em vez de `lambda` no menu | Avaliações, despesas e movimentações do imóvel; `core/idioma.py`; `_selecionar_portugues`/`_selecionar_ingles` |
| 19/08 | Senha no usuário, tela de login | `senha_utils.py` (hash), `login_view.py`, `seed_inicial.py` |
| Depois | — | Dashboard e IPTU (`relatorio.py`), aba *Por proprietário*, views/procedure SQL, `dados_iniciais.sql`, docs |
