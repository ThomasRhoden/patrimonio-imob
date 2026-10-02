# 🎤 Roteiro de apresentação — Patrimônio Imob (~10 min)

Guia para **acompanhar a demo no seu computador** (Windows + XAMPP). Marque cada item; cada passo diz o que fazer e **o que deve aparecer**. Todos os dados são fictícios.

## 0. Antes de começar

- [ ] Fiz o passo a passo **Como executar** do `README.md` (MySQL ligado, `.env`, os 3 scripts na ordem e o `seed_inicial.py`).
- [ ] Se já ensaiei antes, rodei os 3 scripts de novo, na ordem, e o seed (os números abaixo valem para o banco recém-carregado).

**O que já vem carregado:**

| # | Imóvel | Donos | Compra | Estimado (como) | Alíquota | IPTU |
|---|--------|-------|-------:|-----------------|---------:|-----:|
| 1 | Apartamento, Porto Alegre | Ana 50 · Bruno 50 | 420.000 | 535.000 (última avaliação) | 0,55% | 2.942,50 |
| 2 | Casa, Caxias do Sul | Bruno 100 | 650.000 | 780.000 (avaliação) | 0,25% | 1.950,00 |
| 3 | Apartamento, Florianópolis | Ana 40 · Carla 60 | 610.000 | 811.860 (60 m² × 13.531) | 0,50% | 4.059,30 |
| 4 | Sala Comercial, Curitiba | Carla 100 | 290.000 | 315.000 (avaliação) | 1,35% | 4.252,50 |
| 5 | Terreno, Pelotas | Ana 75 | 180.000 | 205.000 (avaliação) | 2,00% | 4.100,00 |
| 6 | Terreno, Londrina | Elisa 100 | 150.000 | 165.000 (avaliação) | 3,00% | 4.950,00 |
| 7 | Terreno, Caxias do Sul | Bruno 100 | 220.000 | 220.000 (compra) | 0,80% | 1.760,00 |
| 8 | Apartamento, Novo Hamburgo | Diego 100 | 290.000 | 322.020 (60 m² × 5.367) | 0,35% | 1.127,07 |
| 9 | Apartamento, Londrina | Diego 50 · Elisa 50 | 400.000 | 468.480 (80 m² × 5.856) | 1,00% | 4.684,80 |
| 10 | Sala Comercial, Joinville | Carla 100 | 230.000 | 260.000 (última avaliação) | 1,50% | 3.900,00 |
| 11 | Sala Comercial, Porto Alegre | Ana 100 | 350.000 | 380.000 (avaliação) | 0,80% | 3.040,00 |
| 12 | Sala Comercial, Novo Hamburgo | Diego 50 · Elisa 50 | 180.000 | 180.000 (compra) | 0,35% | 630,00 |
| 13 | Casa, Curitiba | Ana 50 · Carla 50 | 720.000 | 840.000 (avaliação) | 0,65% | 5.460,00 |
| 14 | Casa, Canoas | Bruno 60 · Diego 40 | 480.000 | 520.000 (avaliação) | 0,40% | 2.080,00 |
| | **Total** | | **5.170.000** | **6.002.360** | | **44.936,17** |

Proprietários (fictícios): Ana Exemplo da Silva, Bruno Teste Oliveira, Carla Demo Pereira, Diego Modelo Santos e Elisa Ficticia Rocha. O m² é o valor médio de referência de mercado para venda residencial (ago/2026) e as alíquotas são das leis de cada cidade (fontes no `dados_iniciais.sql`).

---

## 1. Login (UC-01) — 30 s
- [ ] `python main.py` → login `admin` (ou o que você digitou no seed) + a senha → **Enter**.
- [ ] **Deve aparecer:** o menu (Cadastros básicos, Imóveis, Usuários, Idioma, Sair) e o dashboard.

## 2. Dashboard (UC-02, RN01–RN03) — 2 min
- [ ] **Deve aparecer:** Imóveis **14** · Compra **R$ 5.170.000,00** · Estimado **R$ 6.002.360,00** · Valorização **R$ 832.360,00** · IPTU estimado **R$ 44.936,17**.
- [ ] Estimado = última avaliação; sem avaliação, área privativa × m² (imóvel 3: 60 × 13.531 = 811.860). IPTU = estimado × alíquota (imóvel 1: 535.000 × 0,55% = 2.942,50).
- [ ] Aba **Resumo por cidade**: 9 linhas (`CANOAS/RS`...), vindas da view **`VW_PATRIMONIO_POR_CIDADE`**. Aba **Resumo por estado**: RS **8**, SC **2**, PR **4**.
- [ ] Aba **Por proprietário** (view **`VW_RESUMO_POR_PROPRIETARIO`**): a parte de cada dono = valor × percentual. Ex.: `ANA EXEMPLO DA SILVA` · **5** imóveis · estimado (parte) **R$ 1.545.994,00**. O terreno 5 tem só 75% distribuído, então os 25% sem dono não entram.

## 3. Novo imóvel com validação (UC-08, RN07) — 2 min
- [ ] *Imóveis → Imóveis* (lista com **14**). Estado `RS` → a Cidade mostra só as 6 do RS: CAMPO BOM, CANOAS, CAXIAS DO SUL, NOVO HAMBURGO, PELOTAS e PORTO ALEGRE (cascata).
- [ ] Cidade `CANOAS`, Tipo `APARTAMENTO`, Status `PRÓPRIO`, total `90`, **privativa `100`**, compra `380000`, data `20/03/2022`, cômodos `4`, banheiros `2`, vagas `1` → **Salvar**.
- [ ] **Deve aparecer:** "Erro: A área privativa não pode exceder a área total."
- [ ] Privativa `75` → **Salvar** → "Imóvel cadastrado com sucesso!" (agora **15**).

## 4. Co-propriedade + procedure (UC-09, RN09) — 2 min
- [ ] Clicar no imóvel **5** (Pelotas) → **Proprietários**: `ANA EXEMPLO DA SILVA` com **75.00%**.
- [ ] `BRUNO TESTE OLIVEIRA`, `%` = `30` → **>> Adicionar** → "Erro: A soma dos percentuais não pode passar de 100%."
- [ ] Mudar para `25` → **>> Adicionar** → **Salvar** → "Proprietários do imóvel atualizados com sucesso!".
- [ ] Explicar: cada dono é gravado com **`CALL SP_ADICIONAR_PROPRIETARIO`**, que confere a soma no banco (`SIGNAL SQLSTATE '45000'`). (Opcional, no Workbench, nova aba SQL: `USE patrimonio_imob; CALL SP_ADICIONAR_PROPRIETARIO(5, 3, 10);` → ⚡ → *Output*: **Error Code: 1644**.)

## 5. Avaliação (UC-10, RN03) — 1 min
- [ ] Clicar no imóvel **3** (Florianópolis) → **Avaliações**: data `01/09/2026`, valor `850000` → **Salvar**.
- [ ] **Deve aparecer:** "Avaliação salva com sucesso!" e `01/09/2026 · R$ 850.000,00 · R$ 240.000,00` → **Fechar** → fechar a tela de Imóveis.

## 6. Dashboard atualizado — 1 min
- [ ] Clicar em **Atualizar**.
- [ ] **Deve aparecer:** Imóveis **15** · Compra **R$ 5.550.000,00** · Estimado **R$ 6.486.750,00** · Valorização **R$ 936.750,00** · IPTU estimado **R$ 46.911,87**.
- [ ] Aba **Por imóvel**: o novo (15, Canoas) = 75 m² × 5.950 = **R$ 446.250,00** e IPTU 446.250 × 0,40% = **R$ 1.785,00**; o imóvel 3 agora usa a avaliação (IPTU **R$ 4.250,00**).
- [ ] Aba **Por proprietário**: `BRUNO TESTE OLIVEIRA` passa a **5** imóveis (ganhou 25% do terreno 5). O imóvel 15 ainda não tem dono, então não entra nessa aba.

## 7. Referências e usuários (UC-13 a UC-15) — 1 min
- [ ] *Imóveis → Referência de IPTU*: 31 alíquotas (ex.: PORTO ALEGRE/RS · APARTAMENTO · **0.55%**) → **Fechar**.
- [ ] *Usuários → Usuários*: login, nome e senha; serve para trocar a senha ou criar outro acesso (não há tipos de usuário; a senha fica como hash) → **Fechar**.

## 8. Encerramento — 1 min
- [ ] (Opcional) *Idioma → English* e voltar para *Português*.
- [ ] Arquitetura: **MVC + DAO**; o SQL fica só nos DAOs; banco com 13 tabelas, 3 views e 1 procedure (`docs/diagrama_banco.png`) → **Sair**.

---

## Cuidados
- [ ] Números com **ponto** (`380000`) e datas **DD/MM/AAAA**.
- [ ] O dashboard só muda ao clicar em **Atualizar**.
- [ ] Não excluir registros com vínculos durante a demo (o banco bloqueia, com mensagem).

## Plano B

| Problema | O que fazer |
|----------|-------------|
| *Entrar* não faz nada | MySQL desligado no XAMPP ou falta o `.env` |
| Tabela ou view não existe | Rodar os 3 scripts de novo, na ordem, e o seed |
| Porta 3306 ocupada | Parar o outro MySQL do Windows ou mudar a porta no XAMPP e no `.env` |
| Nada funciona | Mostrar os documentos e o código (`app/dao/imovel_dao.py`, `app/dao/participacao_proprietario_dao.py`) |
