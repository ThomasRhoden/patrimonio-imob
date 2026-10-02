# 🏙️ Ranking do m² — cidades do Sul (RS, SC, PR)

Valor médio de referência de mercado para venda residencial (ago/2026), em R$/m², das cidades do Sul que têm esse valor publicado, do maior para o menor.

✅ = cidade com esse m² cadastrado em `app/migrations/dados_iniciais.sql` (tabela `referencia_m2`, tipo Apartamento).

| # | Cidade | UF | R$/m² | Nos dados de demo |
|---:|---|:---:|---:|:---:|
| 1 | Itapema | SC | 15.403 | |
| 2 | Balneário Camboriú | SC | 15.343 | ✅ |
| 3 | Florianópolis | SC | 13.531 | ✅ |
| 4 | Itajaí | SC | 13.354 | |
| 5 | Curitiba | PR | 11.731 | ✅ |
| 6 | São José | SC | 9.093 | |
| 7 | Joinville | SC | 8.389 | ✅ |
| 8 | Blumenau | SC | 8.177 | |
| 9 | Porto Alegre | RS | 7.510 | ✅ |
| 10 | Caxias do Sul | RS | 6.463 | ✅ |
| 11 | São José dos Pinhais | PR | 6.367 | |
| 12 | Canoas | RS | 5.950 | ✅ |
| 13 | Londrina | PR | 5.856 | ✅ |
| 14 | Santa Maria | RS | 5.514 | |
| 15 | Novo Hamburgo | RS | 5.367 | ✅ |
| 16 | São Leopoldo | RS | 5.200 | |
| 17 | Pelotas | RS | 4.647 | ✅ |

**Fora da lista:** Campo Bom (RS) não tem valor de referência publicado. Está nos dados só como cidade, sem m² e sem imóvel.

**Como o sistema usa:** sem avaliação, valor estimado = área privativa × R$/m². Ex.: 60 m² em Florianópolis = 60 × 13.531 = **R$ 811.860,00**.

> É só consulta. O sistema não tem tela de ranking: o m² é cadastrado em *Imóveis → Referência de valor m²*.
