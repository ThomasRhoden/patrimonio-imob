# 🗄️ Diagrama do banco de dados — Patrimônio Imob

Banco `patrimonio_imob`: **13 tabelas** (`app/migrations/patrimonio_imob_full.sql`), **3 views** e **1 procedure** (`views_procedures.sql`) e os dados de demonstração (`dados_iniciais.sql`).

Ordem dos scripts: `patrimonio_imob_full.sql` → `views_procedures.sql` → `dados_iniciais.sql` → `python seed_inicial.py`.

## Diagrama ER

![Diagrama ER do banco](diagrama_banco.png)

As 13 tabelas aparecem em 6 grupos por cor: **Localização** (`estado`, `cidade`), **Classificação** (`tipo_imovel`, `status_imovel`), **Núcleo** (`imovel`, `proprietario` e a associativa `imovel_proprietario`, que forma o N:N), **Histórico do imóvel** (`avaliacao`, `despesa`, `movimentacao`), **Referências** (`referencia_m2`, `referencia_iptu`) e **Acesso** (`usuario`). Colunas, tipos e NULL são os mesmos do `patrimonio_imob_full.sql`.

> **Legenda:** `PK` chave primária (nome em negrito) · `FK` chave estrangeira · `UK` valor único (`UK (a, b)` no rodapé = único em conjunto) · *itálico* = aceita NULL. Nas linhas, `||` = exatamente um, `o|` = zero ou um (`proprietario.cidade_id` é opcional) e `o<` (pé de galinha) = zero ou muitos. Todas as relações são **1:N**; o N:N imóvel × proprietário é feito pelas duas 1:N de `imovel_proprietario`.
>
> As **3 views** não estão no desenho porque não têm chaves nem ligações próprias; estão descritas em [Views e stored procedure](#views-e-stored-procedure-views_proceduressql).


## Lista de tabelas

| # | Tabela | Descrição | Chaves e restrições |
|---|--------|-----------|---------------------|
| 1 | `estado` | Unidades da federação | PK `id`; `unique(sigla)` |
| 2 | `tipo_imovel` | Tipos de imóvel (ex.: apartamento, casa), cadastro livre | PK `id`; `unique(nome)` |
| 3 | `status_imovel` | Situação do imóvel (RN05: Próprio, Alugado, À venda), cadastro livre | PK `id`; `unique(nome)` |
| 4 | `usuario` | Contas de acesso (login + senha). Não há tipos de usuário; a senha é guardada só como hash | PK `id`; `login` único (`uk_usuario_login`) |
| 5 | `cidade` | Cidades, cada uma ligada a um estado | PK `id`; FK `estado_id` → `estado`; `unique(nome, estado_id)` |
| 6 | `proprietario` | Pessoas donas de imóveis (dados pessoais, ver LGPD em `stakeholders.md`) | PK `id`; FK `cidade_id` → `cidade` (**pode ser nula**) |
| 7 | `imovel` | Imóveis do patrimônio | PK `id`; FKs `cidade_id`, `tipo_imovel_id`, `status_id` (todas obrigatórias) |
| 8 | `imovel_proprietario` | Tabela associativa N:N imóvel × proprietário, com percentual | PK composta (`imovel_id`, `proprietario_id`); 2 FKs; percentual padrão `100.00` |
| 9 | `referencia_m2` | Valor médio do m² por cidade e tipo (RN01) | PK `id`; FKs `cidade_id`, `tipo_imovel_id`; `unique(cidade_id, tipo_imovel_id)` |
| 10 | `referencia_iptu` | Alíquota de IPTU por cidade e tipo (RN02) | PK `id`; FKs `cidade_id`, `tipo_imovel_id`; `unique(cidade_id, tipo_imovel_id)` |
| 11 | `avaliacao` | Histórico de valor estimado do imóvel (RF08) | PK `id`; FK `imovel_id` → `imovel` |
| 12 | `despesa` | Gastos do imóvel (RF09) | PK `id`; FK `imovel_id` → `imovel` |
| 13 | `movimentacao` | Lançamentos financeiros do imóvel (RF10) | PK `id`; FK `imovel_id` → `imovel`; `valor` pode ser nulo |

## Cardinalidades

| Relação | Rótulo no diagrama | Cardinalidade | Explicação |
|---------|--------------------|---------------|------------|
| estado → cidade | possui | 1 : N | `cidade.estado_id` é obrigatória: toda cidade pertence a exatamente um estado |
| cidade → imovel | localiza | 1 : N | `imovel.cidade_id` é obrigatória (RN04) |
| tipo_imovel → imovel | classifica | 1 : N | `imovel.tipo_imovel_id` é obrigatória (RN04) |
| status_imovel → imovel | situação | 1 : N | `imovel.status_id` é obrigatória (RN05) |
| cidade → proprietario | reside em | 0..1 : N | `proprietario.cidade_id` é opcional |
| imovel ↔ proprietario | participa (2×) | N : N | Resolvida pela tabela `imovel_proprietario`, que guarda o percentual de participação (RN04, RN09) |
| cidade / tipo_imovel → referencia_m2 | referencia | 1 : N | No máximo **uma** referência por par (cidade, tipo), garantido pela `unique` |
| cidade / tipo_imovel → referencia_iptu | referencia | 1 : N | No máximo **uma** alíquota por par (cidade, tipo), garantido pela `unique` |
| imovel → avaliacao / despesa / movimentacao | avaliado em / gera / movimenta | 1 : N | Cada lançamento pertence a um imóvel |
| usuario | — | sem relação | A tabela `usuario` não tem FK para nenhuma outra (o usuário não fica ligado a proprietário nem a imóvel) |

## Observações honestas sobre o esquema

- **Nenhuma FK tem `ON DELETE CASCADE`.** Por isso o banco **impede** excluir um registro que ainda tem dependentes, por exemplo um estado com cidades ou um imóvel com proprietários, avaliações, despesas ou movimentações. Na interface isso aparece como "Erro: Não é possível excluir: existem registros vinculados." (tradução feita em `DAO.traduzir_erro`), detalhada em `casos_de_teste.md`.
- **A RN09 (soma ≤ 100%) é conferida em dois lugares.** No Python (models `Participacao_Proprietario` e `Imovel`) e no banco, pela procedure `SP_ADICIONAR_PROPRIETARIO`, que o DAO usa para gravar cada vínculo. Não há `CHECK` nem trigger: quem grava direto com `INSERT INTO imovel_proprietario` (sem a procedure) não passa pela regra.
- **Os valores de status (Próprio, Alugado, À venda) vêm do `dados_iniciais.sql`**, não do script da estrutura. Continuam editáveis pela tela *Status de imóvel* (RN05: "cadastro configurável, não fixo em código").
- **`movimentacao.tipo` é texto livre no banco.** A tela limita as opções a `entrada_aluguel`, `saida_manutencao` e `outro` (o `dados_iniciais.sql` usa só esses códigos).
- **Os DAOs usam os nomes de tabela em minúsculas** (ex.: `FROM avaliacao`), iguais aos do script. Assim o sistema funciona no Windows (XAMPP) e também no Linux, onde o MySQL diferencia maiúsculas de minúsculas nos nomes de tabela.
- **`referencia_iptu.aliquota` é uma fração** (`decimal(8,6)`): `0.005500` = 0,55%. A tela mostra em porcentagem (× 100).

## Views e stored procedure (`views_procedures.sql`)

Padrão de nomes da UC3: `VW_` (view), `SP_` (procedure), `P_` (parâmetro), `V_` (variável); erro de regra com `SIGNAL SQLSTATE '45000'`.

| Objeto | Tabelas usadas | O que faz | Usado em |
|--------|----------------|-----------|----------|
| `VW_IMOVEL_DETALHADO` | `imovel`, `cidade`, `estado`, `tipo_imovel`, `status_imovel` (INNER JOIN), `referencia_m2`, `referencia_iptu` (LEFT JOIN), `avaliacao` (subconsulta) | Uma linha por imóvel com os nomes e o `VALOR_ESTIMADO` (última avaliação → área privativa × m² → valor de compra) e a `ALIQUOTA_IPTU` (0 se não houver) | Base das outras duas views |
| `VW_PATRIMONIO_POR_CIDADE` | `estado`, `cidade` + `VW_IMOVEL_DETALHADO` (LEFT JOIN) | `GROUP BY` estado + cidade: `COUNT` de imóveis e `SUM` de compra, estimado, valorização e IPTU; `HAVING COUNT(...) > 0` tira as cidades sem imóvel | `Imovel_DAO.get_patrimonio_por_cidade()` → aba **Resumo por cidade** do dashboard |
| `VW_RESUMO_POR_PROPRIETARIO` | `proprietario`, `imovel_proprietario` (INNER JOIN) + `VW_IMOVEL_DETALHADO` | `GROUP BY` proprietário: `COUNT` de imóveis e `SUM` de cada valor × `percentual_participacao / 100` (compra, estimado, valorização e IPTU). A parte sem dono de um imóvel com menos de 100% não entra | `Imovel_DAO.get_resumo_por_proprietario()` → aba **Por proprietário** do dashboard |
| `SP_ADICIONAR_PROPRIETARIO(P_IMOVEL_ID, P_PROPRIETARIO_ID, P_PERCENTUAL)` | `imovel_proprietario` | Soma os percentuais já gravados do imóvel em `V_SOMA_ATUAL`; se `V_SOMA_ATUAL + P_PERCENTUAL > 100`, dispara `SIGNAL SQLSTATE '45000'`; senão faz o `INSERT` | `Participacao_Proprietario_DAO.substituir_proprietarios_do_imovel()` (`CALL` para cada vínculo, na mesma transação do `DELETE`). O erro chega como código **1644** e o `DAO.traduzir_erro` mostra "A soma dos percentuais não pode passar de 100%." |

## Dados de demonstração (`dados_iniciais.sql`)

| Tabela | Linhas | Observação |
|--------|-------:|------------|
| `estado` / `cidade` | 3 / 11 | Porto Alegre, Caxias do Sul, Canoas, Pelotas, Novo Hamburgo, Campo Bom (RS); Florianópolis, Joinville, Balneário Camboriú (SC); Curitiba, Londrina (PR) |
| `tipo_imovel` / `status_imovel` | 4 / 3 | Apartamento, Casa, Terreno, Sala Comercial / Próprio, Alugado, À venda |
| `referencia_m2` | 10 | Apartamento, valor médio de referência de mercado para venda residencial (ago/2026) |
| `referencia_iptu` | 31 | Alíquotas das leis/prefeituras (fonte em comentário) |
| `proprietario` | 5 | Fictícios (CPF com dígito válido, e-mail `example.com`) |
| `imovel` / `imovel_proprietario` | 14 / 20 | 4 apartamentos, 3 casas, 3 terrenos, 4 salas; só o imóvel 5 fica com 75% (demo da procedure) |
| `avaliacao` / `despesa` / `movimentacao` | 11 / 6 / 9 | Datas ISO (`AAAA-MM-DD`) |
| `usuario` | 0 | O primeiro acesso (login sugerido `admin`) é criado pelo `seed_inicial.py` |
