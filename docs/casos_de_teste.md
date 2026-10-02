# ✅ Casos de teste (manuais) — Patrimônio Imob

| Área | Casos | Qtd. | Status |
|---|---|:---:|:---:|
| 🔐 Banco e login | CT-01 a CT-04 | 4 | ✅ |
| 📊 Dashboard (dados iniciais) | CT-05 a CT-07 e CT-26 | 4 | ✅ |
| 🗂️ Cadastros básicos | CT-08 a CT-11 | 4 | ✅ |
| 🏢 Imóveis | CT-12 a CT-16 | 5 | ✅ |
| 🤝 Co-propriedade e lançamentos | CT-17 a CT-23 | 7 | ✅ |
| 🌐 Usuários e idioma | CT-24 e CT-25 | 2 | ✅ |
| **Total** | | **26** | **26/26 ✅** |

> ✅ = conferido num MariaDB recém-carregado (01/10/2026). A coluna **Status** das tabelas abaixo é para o ensaio na máquina da apresentação: ✅ / ❌.

**Antes:** rode os 3 scripts (`patrimonio_imob_full.sql` → `views_procedures.sql` → `dados_iniciais.sql`) e `python seed_inicial.py`, como no `README.md`. Erros aparecem como **"Erro: "** + mensagem; em inglês (*Idioma → English*), traduzidos.

## 🔐 1. Banco e login

| ID | Objetivo | Passos | Resultado esperado | Status |
|----|----------|--------|--------------------|--------|
| CT-01 | Scripts rodam na ordem | MySQL Workbench: abrir (*File → Open SQL Script…*) e executar (⚡) os 3 scripts, na ordem | Nenhum ❌ vermelho (avisos ⚠️ como `1305 PROCEDURE ... does not exist` são normais); banco com 13 tabelas, 3 views (`vw_imovel_detalhado`, `vw_patrimonio_por_cidade`, `vw_resumo_por_proprietario`) e a rotina `SP_ADICIONAR_PROPRIETARIO` | |
| CT-02 | Seed cria o primeiro acesso | `python seed_inicial.py` → Enter no login (fica `admin`) → confirmar com senha diferente → repetir certo | Pede de novo quando não confere; no fim "Acesso criado com sucesso!" e "Login: admin" | |
| CT-03 | Login válido | `python main.py` → login `admin` + senha do seed → **Entrar** | Abre o menu e o dashboard; título "Patrimônio Imob — Usuário inicial (admin)" | |
| CT-04 | Login inválido | Senha errada; depois campos vazios | "Login ou senha inválidos." / "Informe login e senha." | |

## 📊 2. Dashboard (dados iniciais)

| ID | Objetivo | Passos | Resultado esperado | Status |
|----|----------|--------|--------------------|--------|
| CT-05 | Indicadores (RN01–RN03) | Ver o dashboard | Imóveis `14` · Compra `R$ 5.170.000,00` · Estimado `R$ 6.002.360,00` · Valorização `R$ 832.360,00` · IPTU `R$ 44.936,17` | |
| CT-06 | Por cidade (view) e por estado | Abas **Resumo por cidade** e **Resumo por estado** | 9 cidades (CANOAS/RS a PORTO ALEGRE/RS; ex.: CAXIAS DO SUL/RS 2 · R$ 870.000,00 · R$ 1.000.000,00), iguais a `SELECT * FROM VW_PATRIMONIO_POR_CIDADE;`; estados RS 8, SC 2, PR 4 | |
| CT-07 | IPTU por imóvel (RF04/RN02) | Aba **Por imóvel** | 14 linhas; IPTU 2.942,50 · 1.950,00 · 4.059,30 · 4.252,50 · 4.100,00 · 4.950,00 · 1.760,00 · 1.127,07 · 4.684,80 · 3.900,00 · 3.040,00 · 630,00 · 5.460,00 · 2.080,00 (nenhum R$ 0,00) | |
| CT-26 | Parte de cada dono (view) | Aba **Por proprietário** | 5 linhas, com os mesmos valores de `SELECT * FROM VW_RESUMO_POR_PROPRIETARIO;`. Ex.: ANA EXEMPLO DA SILVA · 5 · compra `R$ 1.299.000,00` · estimado `R$ 1.545.994,00` · IPTU `R$ 11.939,97`; ELISA FICTICIA ROCHA · 3 · `R$ 440.000,00` · `R$ 489.240,00` · `R$ 7.607,40` | |

## 🗂️ 3. Cadastros básicos

| ID | Objetivo | Passos | Resultado esperado | Status |
|----|----------|--------|--------------------|--------|
| CT-08 | Sigla com 2 letras | *Estados* → `Paraná` / `PRR` → **Salvar** | "Erro: A sigla deve possuir exatamente 2 caracteres." | |
| CT-09 | Registro duplicado | *Estados* → `Rio Grande` / `RS` → **Salvar** | "Erro: Já existe um registro com esses dados." | |
| CT-10 | Excluir com vínculo (FK) | *Estados* → selecionar RS → **Excluir** → confirmar | "Erro: Não é possível excluir: existem registros vinculados." | |
| CT-11 | Nome obrigatório | *Proprietários* → nome vazio → **Salvar** | "Erro: O nome é obrigatório." | |

## 🏢 4. Imóveis

| ID | Objetivo | Passos | Resultado esperado | Status |
|----|----------|--------|--------------------|--------|
| CT-12 | Cascata estado → cidade | *Imóveis* → Estado `RS` | Cidade mostra só as 6 do RS: CAMPO BOM, CANOAS, CAXIAS DO SUL, NOVO HAMBURGO, PELOTAS, PORTO ALEGRE | |
| CT-13 | RN07 | Canoas, Apartamento, Próprio, total `90`, privativa `100`, compra `380000`, data `20/03/2022`, 4/2/1 → **Salvar** | "Erro: A área privativa não pode exceder a área total." | |
| CT-14 | RN08 | Igual, privativa `75`, compra `-380000` | "Erro: O valor de compra não pode ser negativo." | |
| CT-15 | Número e data inválidos | Compra `380.000,00`; depois data `2022-03-20` | "Erro: Valor de compra: informe um número válido …" / "Erro: Data da compra: informe a data no formato DD/MM/AAAA …" | |
| CT-16 | Salvar imóvel | Compra `380000`, data `20/03/2022` → **Salvar** | "Imóvel cadastrado com sucesso!"; lista com 15 | |

## 🤝 5. Co-propriedade (RN09) e lançamentos

| ID | Objetivo | Passos | Resultado esperado | Status |
|----|----------|--------|--------------------|--------|
| CT-17 | Soma > 100% na tela | Imóvel 5 → **Proprietários** (Ana 75%) → Bruno `30` → **>> Adicionar** | "Erro: A soma dos percentuais não pode passar de 100%." | |
| CT-18 | Gravar via procedure | Bruno `25` → **>> Adicionar** → **Salvar**; reabrir | "Proprietários do imóvel atualizados com sucesso!"; Ana 75.00% e Bruno 25.00% | |
| CT-19 | Procedure barra no banco | Depois do CT-18, no Workbench: nova aba SQL → `USE patrimonio_imob; CALL SP_ADICIONAR_PROPRIETARIO(5, 3, 10);` → ⚡ | No *Output*: `Error Code: 1644. A soma dos percentuais nao pode passar de 100%`; nada gravado | |
| CT-20 | Avaliação (RN03) | Imóvel 3 → **Avaliações** → `01/09/2026`, `850000` → **Salvar** | "Avaliação salva com sucesso!"; linha `R$ 850.000,00 · R$ 240.000,00` | |
| CT-21 | Avaliação negativa | Data `01/09/2026`, valor `-1` → **Salvar** | "Erro: O valor estimado não pode ser negativo." | |
| CT-22 | Despesa e movimentação | Imóvel 3 → **Despesas** (`Pintura`, `500`, `10/09/2026`) e **Movimentações** (`entrada_aluguel`, `3900`, `10/09/2026`) | "Despesa salva com sucesso!" / "Movimentação salva com sucesso!" | |
| CT-23 | Dashboard depois dos testes | **Atualizar** | Imóveis `15` · Compra `R$ 5.550.000,00` · Estimado `R$ 6.486.750,00` · Valorização `R$ 936.750,00` · IPTU `R$ 46.911,87` (Canoas, imóvel 15: 446.250 × 0,40% = 1.785,00); *Por proprietário*: BRUNO com 5 imóveis | |

## 🌐 6. Usuários e idioma

| ID | Objetivo | Passos | Resultado esperado | Status |
|----|----------|--------|--------------------|--------|
| CT-24 | Criar outro acesso | *Usuários* → login `marina`, nome `Marina`, senha → **Salvar** → **Sair** → `python main.py` → entrar com `marina` → *Usuários* → selecionar `marina` → **Excluir** | "Usuário salvo com sucesso!"; a Marina também vê o menu *Usuários*; ao excluir a si mesma: "Não é possível excluir o usuário que está logado." | |
| CT-25 | Trocar idioma | *Idioma → English* com uma tela aberta | Menu, dashboard e janelas abertas em inglês; os dados continuam como cadastrados | |
