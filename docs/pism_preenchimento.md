# 🌐 Preenchimento do site do PISM — Patrimônio Imob

Texto pronto para copiar e colar em cada campo do site. Tudo conferido no código e nos outros documentos (`requisitos.md`, `stakeholders.md`, `casos_de_uso.md`, `diagrama_banco.md`, `roteiro_apresentacao.md`).

---

## 1. FICHA

**Nome do Projeto**
Patrimônio Imob

**Objetivo do Projeto**
Ajudar uma pessoa a organizar e acompanhar os próprios imóveis em um único sistema desktop. O sistema registra imóveis, donos (com percentual de participação), avaliações, despesas e movimentações, e mostra num dashboard o valor estimado, a valorização e uma estimativa do IPTU anual. O foco são cidades do Sul do Brasil (RS, SC e PR).

**Descrição do Público Alvo**
Pessoas físicas que têm um ou mais imóveis (para morar, alugar ou vender), sozinhas ou em sociedade com familiares, e que hoje controlam tudo em planilhas soltas. Não precisam saber de tecnologia: usam o sistema no próprio computador, sem internet.

**Persona 1**
- **Nome:** Marina
- **Idade / Faixa etária:** 35-50 anos (Marina tem 42)
- **Descrição:** Mora em Porto Alegre (RS). Tem o apartamento onde mora, um apartamento alugado e divide com o irmão (50% / 50%) uma casa de praia em Santa Catarina. Controla tudo em planilhas e não sabe dizer quanto o patrimônio vale hoje.
- **Necessidades:** ver em uma tela o total investido, o valor estimado e a valorização; registrar avaliações, despesas (condomínio, manutenção) e o aluguel recebido; lembrar quanto pagou em cada imóvel e quando; saber a parte de cada dono no imóvel dividido.

**Persona 2**
- **Nome:** Roberto
- **Idade / Faixa etária:** 55-70 anos (Roberto tem 63)
- **Descrição:** Aposentado, mora em Caxias do Sul (RS). Tem uma casa e uma sala comercial alugada, e herdou com duas irmãs um terreno em Pelotas. Usa pouco o computador e quer algo simples, sem cadastro online.
- **Necessidades:** saber quanto deve pagar de IPTU por ano, de forma aproximada; registrar o aluguel da sala e os gastos de manutenção; deixar claro o percentual de cada herdeiro no terreno; proteger os dados com senha no computador de casa.

**O que o produto É ou Fará**
Um sistema desktop (Python + Tkinter + MySQL) para gestão do patrimônio imobiliário pessoal. Cadastra estados, cidades, tipos e status de imóvel, proprietários e imóveis; permite co-propriedade com percentual (soma até 100%); registra avaliações, despesas e movimentações de cada imóvel; calcula valor estimado (última avaliação ou área × valor do m²), valorização e IPTU estimado (valor × alíquota da cidade); mostra um dashboard com totais e resumos por cidade, estado, imóvel e proprietário; tem login com senha em hash e interface em português e inglês.

**O que o produto Não é ou Não fará**
Não é um sistema de imobiliária: não cadastra clientes, inquilinos, contratos de aluguel nem cobranças. Não é online nem multiusuário com permissões: roda no computador da pessoa, e o login serve só para proteger com senha (não há perfis). Não é uma calculadora oficial de IPTU nem faz avaliação oficial de imóvel: os valores são estimativas a partir das referências cadastradas. Não emite boletos, não faz declaração de imposto de renda e não se conecta a prefeituras, cartórios ou bancos.

---

## 2. BACKLOG

O texto completo (épicos, histórias e critérios de aceitação) está em **`docs/backlog.md`**. Para cada épico do site: **Título** = título do épico; **Descrição** = linha "Descrição"; **Critérios de Aceitação** = a lista logo abaixo. As histórias (US01 a US16) entram embaixo de cada épico, no mesmo formato.

| Épico | Histórias | RF / RN |
|-------|-----------|---------|
| 1. Acesso e Segurança | US01 Fazer login · US02 Criar o primeiro acesso · US03 Manter acessos | RNF segurança, LGPD |
| 2. Cadastros de Base | US04 Estados · US05 Cidades · US06 Tipos e status | RN04, RN05 |
| 3. Proprietários e Imóveis | US07 Proprietários · US08 Imóveis · US09 Proprietários do imóvel (N:N) | RF01, RF02, RF06, RF07, RN04, RN06–RN09 |
| 4. Histórico do Imóvel | US10 Avaliações · US11 Despesas · US12 Movimentações | RF08, RF09, RF10, RN03 |
| 5. Dashboard e IPTU | US13 Referências de m² e IPTU · US14 Dashboard · US15 Resumos (cidade, estado, imóvel, proprietário) | RF03, RF04, RF05, RN01–RN03 |
| 6. Idioma | US16 Trocar o idioma | Extra |

---

## 3. ARQUITETURA

**Título da Seção:** Padrão de Projeto
MVC + DAO. As **views** (Tkinter) só montam a tela e repassam os cliques; os **controllers** ligam a tela aos dados e mostram as mensagens; os **models** guardam os dados e fazem as validações das regras de negócio (ex.: área privativa não pode passar da área total); os **DAOs** são os únicos que têm SQL e falam com o banco. Regras: SQL só nos DAOs, validação nos models, view nunca acessa o banco. Erros do banco (registro repetido, exclusão com vínculo, soma acima de 100%) são traduzidos em mensagens amigáveis pela classe base `DAO`.

**Título da Seção:** Tecnologias Utilizadas
Python 3.10 ou mais novo; Tkinter e ttk para a interface (já vêm com o Python); MySQL/MariaDB pelo XAMPP; MySQL Workbench para rodar os scripts SQL; `mysql-connector-python` para a conexão; `python-dotenv` para ler as credenciais do `.env`; Git para versionamento.

**Título da Seção:** Estrutura de Pastas
`main.py` inicia o sistema e monta o menu. `app/models` (um model por tabela), `app/dao` (acesso ao banco), `app/controllers`, `app/views` (uma tela por cadastro, mais login e dashboard), `app/core` (conexão com o banco, idiomas, datas, cálculos do dashboard e hash de senha) e `app/migrations` (scripts SQL). `docs/` tem a documentação e `seed_inicial.py` cria o primeiro acesso.

**Título da Seção:** Banco de Dados
Banco relacional `patrimonio_imob` com 13 tabelas. Relações 1:N (estado → cidade → imóvel; imóvel → avaliações, despesas e movimentações; tipo e status → imóvel) e uma N:N (`imovel_proprietario`, com o percentual de cada dono). Chaves estrangeiras sem `ON DELETE CASCADE`, então o banco impede apagar um registro que está em uso. Tem 3 views (`VW_IMOVEL_DETALHADO`; `VW_PATRIMONIO_POR_CIDADE`, usada no resumo por cidade do dashboard; e `VW_RESUMO_POR_PROPRIETARIO`, a parte de cada dono pelo percentual) e 1 stored procedure (`SP_ADICIONAR_PROPRIETARIO`, que grava cada dono e barra a soma acima de 100% com `SIGNAL SQLSTATE '45000'`).

**Título da Seção:** Segurança e LGPD
A senha é guardada só como hash SHA-256 com salt aleatório, nunca em texto puro, e o campo de senha é mascarado. As credenciais do banco ficam no `.env`, que não vai para o repositório. Do proprietário, só o nome é obrigatório (CPF, e-mail e telefone são opcionais) e não há dados de inquilino. Os dados da demonstração são fictícios. Limitação conhecida: SHA-256 é melhor que texto puro, mas o ideal para senhas seria bcrypt ou Argon2.

**Título da Seção:** Internacionalização
A interface funciona em português e inglês. Todos os textos ficam em um dicionário (`app/core/idioma.py`) com as mesmas chaves nos dois idiomas. Pelo menu *Idioma*, a troca refaz na hora o menu, o dashboard e as janelas abertas, inclusive na tela de login. Os dados cadastrados não são traduzidos.

---

## 4. MODELAGEM

- **Campo DDL** (estrutura): colar o conteúdo de `app/migrations/patrimonio_imob_full.sql` e, logo abaixo, o de `app/migrations/views_procedures.sql`. Views e procedures também são DDL. O `DELIMITER $$` da procedure pode ficar como está.
- **Campo DML** (dados): colar o conteúdo de `app/migrations/dados_iniciais.sql`.
- **Imagem do diagrama:** enviar `docs/diagrama_banco.png` (diagrama ER com as 13 tabelas, chaves, tipos e cardinalidade).

Os três arquivos estão em UTF-8 sem BOM, com quebras de linha simples e sem caracteres de controle, então colam sem problema (os acentos ficam só nos comentários e nos dados, como "Florianópolis"). Juntos, `patrimonio_imob_full.sql` + `views_procedures.sql` rodam como um script único.

---

## 5. APRESENTAÇÃO

Prints já prontos em `docs/screenshots/` (tirados do sistema rodando com o banco recém-carregado, na ordem do `roteiro_apresentacao.md`):

1. `01_login.png` — tela de login (login `admin`, senha mascarada).
2. `02_dashboard_por_cidade.png` — os 5 indicadores (14 imóveis, IPTU estimado R$ 44.936,17) e a aba *Resumo por cidade*.
3. `03_dashboard_por_imovel_iptu.png` — aba *Por imóvel* com o IPTU estimado de cada imóvel.
4. `04_imoveis_cidades_por_estado.png` — cadastro de imóveis: estado RS escolhido e a lista de cidades só do RS (cascata).
5. `05_proprietarios_do_imovel.png` e `05b_proprietarios_erro_soma.png` — imóvel 5 com Ana 75% + Bruno 25%, e o erro "A soma dos percentuais não pode passar de 100%." ao tentar 30%.
6. `06_avaliacoes_do_imovel.png` — avaliação de R$ 850.000,00 do imóvel 3, com a valorização de R$ 240.000,00.
7. `07_dashboard_en.png` — o mesmo dashboard em inglês.
8. `08_dashboard_por_proprietario.png` — aba *Por proprietário*: a parte de cada um dos 5 donos (valor × percentual).

Slides: `docs/apresentacao_patrimonio_imob.pptx` (10 slides, ~10 min, com notas do apresentador) e a versão `docs/apresentacao_patrimonio_imob.pdf`.
