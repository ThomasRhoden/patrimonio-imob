# 🧭 Matriz MoSCoW — Patrimônio Imob

Priorização dos requisitos do `docs/requisitos.md` (RF01 a RF10), mais alguns itens extras que existem no código ou foram citados no README. O **status** foi conferido no código atual.

**Legenda de prioridade**
- **M — Must have (obrigatório):** sem isso o sistema não cumpre seu objetivo.
- **S — Should have (importante):** agrega muito valor, mas o sistema funciona sem.
- **C — Could have (desejável):** bom ter, se sobrar tempo.
- **W — Won't have (não nesta versão):** fica fora do escopo de propósito.

**Legenda de status:** ✅ Implementado · 🟡 Parcial · ❌ Não implementado

## 1. Requisitos funcionais do documento

| ID | Requisito | Prioridade | Justificativa | Status | Evidência no código / o que falta |
|----|-----------|:----------:|---------------|:------:|-----------------------------------|
| RF01 | Cadastro de imóveis | **M** | É o centro do sistema: sem imóvel não há patrimônio | ✅ | `Imovel_View` / `Imovel_Controller` / `Imovel_DAO`: cidade, tipo, status, áreas, valor, data, cômodos, banheiros, vagas e observações |
| RF02 | Validação de dados | **M** | Dados errados geram cálculos errados no dashboard | ✅ | Validações nos **models** (valem no Salvar e no Alterar): `Imovel` cobre RN06–RN08, área privativa ≥ 0, cômodos/banheiros/vagas ≥ 0 e cidade/tipo/status obrigatórios; os demais models validam campos obrigatórios e valores ≥ 0. Texto em campo numérico ou data fora de `DD/MM/AAAA` mostra mensagem em português (`Data_Utils.converter_*`) |
| RF03 | Cálculo de valor estimado | **M** | É a informação que o proprietário mais quer saber | ✅ | `Relatorio.calcular_valor_estimado` + `Dashboard_Controller`: usa a última avaliação, senão área privativa × valor m², senão o valor de compra. O dashboard mostra os totais, os resumos por cidade e estado e a aba **Por imóvel** com o estimado de cada imóvel |
| RF04 | Cálculo de IPTU | **S** | Ajuda no planejamento de custos, mas não é o objetivo principal | ✅ | Tela `referencia_iptu` (alíquota por cidade e tipo). O `Dashboard_Controller` busca a alíquota com `Referencia_Iptu_DAO.get_by_cidade_e_tipo` e calcula com `Relatorio.calcular_iptu_estimado`; o dashboard mostra o **IPTU estimado (anual)** total e por imóvel |
| RF05 | Dashboard | **M** | Dá a visão consolidada, que é o objetivo do sistema | ✅ | `Dashboard_View`: quantidade, valor de compra total, valor estimado total, valorização total, IPTU estimado e abas por cidade, por estado, por imóvel e por proprietário. As abas por cidade e por proprietário leem as views `VW_PATRIMONIO_POR_CIDADE` e `VW_RESUMO_POR_PROPRIETARIO` (`Imovel_DAO`). Só atualiza ao clicar em **Atualizar** |
| RF06 | Listagem de imóveis | **M** | Sem lista não dá para selecionar, alterar ou excluir | ✅ | Treeview com ID, Cidade/UF, Tipo, Status, Área total e Valor de compra |
| RF07 | Proprietários e co-propriedade | **M** | A RN04 exige a posse N:N e a persona tem imóvel dividido | ✅ | CRUD em `Proprietario_View` e popup N:N `Participacao_Proprietario_View` com percentual (tabela `imovel_proprietario`) |
| RF08 | Registro de avaliações | **S** | Mostra a evolução do valor e melhora a estimativa do dashboard | ✅ | Popup `Avaliacao_View` com valorização por avaliação. Valor negativo é recusado no Salvar e no Alterar |
| RF09 | Registro de despesas | **S** | Controle de custos por imóvel | ✅ | Popup `Despesa_View`. Descrição obrigatória e valor ≥ 0 no Salvar e no Alterar. As despesas **não entram** no dashboard |
| RF10 | Movimentações financeiras | **C** | Útil para quem aluga, mas não essencial para o valor do patrimônio | ✅ | Popup `Movimentacao_View` com tipos `entrada_aluguel`, `saida_manutencao` e `outro`. Não entra no dashboard |

## 2. Regras de negócio

| ID | Regra | Prioridade | Status | Onde está |
|----|-------|:----------:|:------:|-----------|
| RN01 | Valor estimado = área privativa × valor m² (cidade/tipo) | **M** | ✅ | `Dashboard_Controller._calcular_valores_estimados`. Quando existe avaliação, ela tem prioridade sobre a referência |
| RN02 | IPTU = valor estimado × alíquota | **S** | ✅ | `Relatorio.calcular_iptu_estimado`, chamado pelo `Dashboard_Controller` (sem alíquota cadastrada = R$ 0,00) |
| RN03 | Valorização = estimado − compra | **M** | ✅ | `Relatorio` (dashboard) e `Avaliacao.valorizacao` (popup de avaliações) |
| RN04 | Imóvel com 1 cidade e 1 tipo; posse N:N | **M** | ✅ | FKs `not null` em `imovel` + tabela `imovel_proprietario` |
| RN05 | Status configurável (Próprio, Alugado, À venda) | **M** | ✅ | Tabela e tela `status_imovel`. Os 3 valores vêm do `dados_iniciais.sql` e continuam editáveis pela tela |
| RN06 | Área total > 0 | **M** | ✅ | `Imovel._validar_dados` / setter `area_total` |
| RN07 | Área privativa ≤ área total | **M** | ✅ | `Imovel._validar_dados` / setter `area_privativa` |
| RN08 | Valor de compra ≥ 0 | **M** | ✅ | `Imovel._validar_dados` / setter `valor_compra` |
| RN09 | Soma dos percentuais ≤ 100% | **M** | ✅ | No model: `Participacao_Proprietario` (0 a 100%) e `Imovel.validar_percentuais` (setter `Imovel.proprietarios`); o popup mostra a mensagem do model. No banco: `SP_ADICIONAR_PROPRIETARIO` (`SIGNAL SQLSTATE '45000'`), chamada pelo `Participacao_Proprietario_DAO`; o erro 1644 vira a mesma mensagem amigável |

## 3. Requisitos não funcionais

| RNF | Prioridade | Status | Observação |
|-----|:----------:|:------:|------------|
| Interface em Python com Tkinter | **M** | ✅ | Todas as telas usam `tkinter` / `ttk` |
| Orientação a objetos | **M** | ✅ | Models com encapsulamento (`@property`) e validação por `ValueError` |
| Camadas MVC + DAO | **M** | ✅ | Pastas `models`, `views`, `controllers`, `dao` e a classe abstrata `DAO` |
| Banco MySQL | **M** | ✅ | `mysql-connector-python`, 13 tabelas no `patrimonio_imob_full.sql` |
| Credenciais em variáveis de ambiente | **M** | ✅ | `.env` + `python-dotenv` em `app/core/database.py`; `.env` está no `.gitignore`. O `.env.example` mostra as variáveis, e o README explica como copiar |
| Código comentado para revisão acadêmica | **S** | ✅ | Toda classe e todo método têm docstring (uma linha dizendo o que faz); as regras mais longas (ex.: `Relatorio`) têm docstring detalhada |

## 4. Itens extras (fora do `requisitos.md`)

| Item | Prioridade | Justificativa | Status | Observação |
|------|:----------:|---------------|:------:|------------|
| Login com senha em hash | **M** | Protege os dados pessoais (LGPD) | ✅ | `Login_Controller` + `Senha_Utils` (SHA-256 com salt); entra com **login** (único, sem espaços) e senha |
| Cadastro de usuários (acessos) | **S** | Trocar a senha ou criar outro acesso | ✅ | `Usuario_View` (login, nome, senha), visível para todo usuário logado; senha em branco no Alterar = mantém a atual; não deixa excluir o próprio acesso |
| Controle de acesso por perfil | **W** | Sistema pessoal e offline: o login serve só para proteger com senha | ❌ (de propósito) | Não há tipos de usuário; todos os acessos veem as mesmas telas |
| Cadastros básicos (estado, cidade, tipo, status) | **M** | Imóvel depende deles (FKs) | ✅ | Telas no menu *Cadastros básicos* |
| Seleção em cascata estado → cidade | **S** | Evita escolher cidade do estado errado | ✅ | Telas de Imóveis e Proprietários (`get_by_estado`) |
| Tabela de referência de valor m² | **M** | Necessária para o RF03 / RN01 | ✅ | Menu *Imóveis → Referência de valor m²* |
| Tabela de referência de IPTU | **S** | Necessária para o RF04 / RN02 | ✅ | Usada no IPTU estimado do dashboard (RF04) |
| Script do primeiro acesso | **M** | Sem ele não há primeiro login | ✅ | `seed_inicial.py` pede o login (Enter = `admin`) e a senha com `getpass` (e a confirmação) |
| Carga inicial de dados (estados, cidades, status) | **S** | Sem dados as comboboxes ficam vazias e a demo demora | ✅ | `app/migrations/dados_iniciais.sql`: 11 cidades (imóveis só nas que têm alíquota de IPTU conferida), tipos, status, m² (valor médio de referência de mercado, ago/2026), 5 proprietários fictícios e 14 imóveis (4 tipos, 9 cidades) com co-propriedade e histórico |
| Views e stored procedure (padrão UC3) | **S** | Pedido da UC3 (banco de dados) e reforça regras no próprio banco | ✅ | `app/migrations/views_procedures.sql`: `VW_IMOVEL_DETALHADO`, `VW_PATRIMONIO_POR_CIDADE` (dashboard por cidade), `VW_RESUMO_POR_PROPRIETARIO` (dashboard por proprietário) e `SP_ADICIONAR_PROPRIETARIO` (gravação do N:N). Usadas só pelos DAOs |
| Interface bilíngue (pt/en) | **C** | Diferencial, não pedido | ✅ | Todos os textos de interface ficam em `Idioma` (pt e en). A troca refaz o menu, o dashboard e as janelas abertas; a tela de login também tem o menu de idioma |
| Mensagens amigáveis para erros do banco | **S** | O usuário precisa entender por que a ação falhou | ✅ | `DAO.traduzir_erro`: exclusão com dependentes → "Não é possível excluir: existem registros vinculados."; duplicado → "Já existe um registro com esses dados."; erro 1644 da procedure → "A soma dos percentuais não pode passar de 100%." |
| Exportação de relatórios | **W** | Não é necessária para a visão do patrimônio | ❌ | Fora desta versão |
| Testes automatizados | **W** | Fora do escopo do projeto integrador | ❌ | Testes manuais em `casos_de_teste.md` |

## 5. Resumo

| Status | RF01–RF10 |
|--------|-----------|
| ✅ Implementado | 10 (RF01 a RF10) |
| 🟡 Parcial | 0 |
| ❌ Não implementado | 0 |

Todos os requisitos funcionais (RF01 a RF10) e as regras RN01 a RN09 estão implementados. O que ainda pode ser melhorado:
1. Despesas e movimentações ainda **não entram** no dashboard.
2. IPTU com faixas progressivas (hoje é uma alíquota por cidade + tipo) e mais cidades na carga inicial.
