-- =====================================================
-- DADOS INICIAIS (DML) - patrimonio_imob
-- Dados de demonstração para a apresentação.
--
-- ORDEM DE EXECUÇÃO (MySQL Workbench: File > Open SQL Script > raio Execute):
--   1) app/migrations/patrimonio_imob_full.sql  (recria o banco vazio)
--   2) app/migrations/views_procedures.sql      (views e procedure)
--   3) app/migrations/dados_iniciais.sql        (este arquivo)
--   4) python seed_inicial.py                   (cria o primeiro acesso; login sugerido admin)
--
-- Rode logo depois dos passos 1 e 2: os ids são fixos (1, 2, 3...).
-- Para recomeçar do zero, rode tudo de novo a partir do passo 1.
-- Datas no formato ISO (AAAA-MM-DD). Alíquota de IPTU em FRAÇÃO
-- (0.005500 = 0,55%). Proprietários, CPFs e e-mails são FICTÍCIOS.
-- Só há imóveis em cidades com alíquota de IPTU conferida em fonte
-- oficial/legal. Cidade sem alíquota conferida entra só como cidade.
-- =====================================================

USE patrimonio_imob;

-- ===== estado =====
INSERT INTO estado (id, nome, sigla) VALUES
(1, 'Rio Grande do Sul', 'RS'),
(2, 'Santa Catarina', 'SC'),
(3, 'Paraná', 'PR');

-- ===== cidade =====
INSERT INTO cidade (id, nome, estado_id) VALUES
(1, 'Porto Alegre', 1),
(2, 'Caxias do Sul', 1),
(3, 'Canoas', 1),
(4, 'Pelotas', 1),
(5, 'Florianópolis', 2),
(6, 'Curitiba', 3),
(7, 'Novo Hamburgo', 1),
(8, 'Campo Bom', 1),
(9, 'Joinville', 2),
(10, 'Balneário Camboriú', 2),
(11, 'Londrina', 3);

-- ===== tipo_imovel =====
INSERT INTO tipo_imovel (id, nome) VALUES
(1, 'Apartamento'),
(2, 'Casa'),
(3, 'Terreno'),
(4, 'Sala Comercial');

-- ===== status_imovel =====
INSERT INTO status_imovel (id, nome) VALUES
(1, 'Próprio'),
(2, 'Alugado'),
(3, 'À venda');

-- ===== referencia_m2 =====
-- Apartamento: valor médio de referência de mercado para venda
-- residencial (ago/2026), em R$/m².
-- Campo Bom não tem valor de referência publicado -> sem m².
-- (Os outros tipos não têm referência: o sistema usa a última
--  avaliação ou, sem avaliação, o valor de compra.)
INSERT INTO referencia_m2 (cidade_id, tipo_imovel_id, valor_m2) VALUES
(1, 1, 7510.00),   -- Porto Alegre
(2, 1, 6463.00),   -- Caxias do Sul
(3, 1, 5950.00),   -- Canoas
(4, 1, 4647.00),   -- Pelotas
(5, 1, 13531.00),  -- Florianópolis
(6, 1, 11731.00),  -- Curitiba
(7, 1, 5367.00),   -- Novo Hamburgo
(9, 1, 8389.00),   -- Joinville
(10, 1, 15343.00), -- Balneário Camboriú
(11, 1, 5856.00);  -- Londrina

-- ===== referencia_iptu =====
-- Onde a lei é progressiva (varia por faixa de valor venal), foi
-- escolhida UMA faixa representativa, indicada no comentário.

-- Porto Alegre - IPTU 2026 (LC 859/2019 e LC 912/2021)
-- Fonte: https://prefeitura.poa.br/smf/iptu/saiba-mais
-- Residencial progressivo 0,40% a 0,85% -> faixa de R$ 431.261,05 a
-- R$ 718.772,27 = 0,55%. Não residencial = 0,80%.
-- Terreno: 3% / 2% / 1% conforme a divisão fiscal -> 2ª divisão = 2%.
INSERT INTO referencia_iptu (cidade_id, tipo_imovel_id, aliquota) VALUES
(1, 1, 0.005500),
(1, 2, 0.005500),
(1, 3, 0.020000),
(1, 4, 0.008000);

-- Caxias do Sul - IPTU 2026 (LC 701/2022, Manual de Cálculo do IPTU)
-- Fonte: https://gcpstorage.caxias.rs.gov.br/documents/2026/02/20cea15e-6ac5-4c2f-9076-859b9711aa21.pdf
-- Progressivo por faixa de valor venal em VRM: residencial 0,15% a 0,40%,
-- não residencial 0,20% a 0,45%, territorial 0,60% a 1,10%.
-- Faixa 3 (5.162,63 a 10.325,25 VRM): 0,25% / 0,30% / 0,80%.
INSERT INTO referencia_iptu (cidade_id, tipo_imovel_id, aliquota) VALUES
(2, 1, 0.002500),
(2, 2, 0.002500),
(2, 3, 0.008000),
(2, 4, 0.003000);

-- Canoas - Código Tributário Municipal (Lei 1.943/1979, art. 16, redação
-- da Lei 5.446/2009), consolidação de 07/2020 publicada pela Prefeitura:
-- https://www.canoas.rs.gov.br/wp-content/uploads/2021/05/Lei-ordinaria-1943-1979-Canoas-RS-consolidada-17-07-2020.pdf
-- Residencial 0,4%, comercial 0,5%. Terreno baldio 1,7% a 4,4%
-- (https://www.canoas.rs.gov.br/noticias/prefeitura-de-canoas-lanca-programa-para-atualizacao-de-imoveis-baldios/)
-- -> usada a menor faixa, 1,7%. Para 2026 a Prefeitura informa correção
-- da planta de valores (Lei 6.856/2025), sem mudança de alíquota encontrada.
INSERT INTO referencia_iptu (cidade_id, tipo_imovel_id, aliquota) VALUES
(3, 1, 0.004000),
(3, 2, 0.004000),
(3, 3, 0.017000),
(3, 4, 0.005000);

-- Pelotas - Lei 6.178/2014 (citada pela Prefeitura nos lançamentos de 2025:
-- https://transparencia.pelotas.com.br/despesas/renuncias-fiscais/renuncias-fiscais-print)
-- Faixas: https://www.pelotas.com.br/noticia/camara-aprova--revisao-da-planta-de-valores-do-municipio
-- Prédios progressivo 0,15% a 1,0% (por URM) -> faixa de 1.200 a 2.400
-- URM = 0,8% (a lei não separa residencial de comercial).
-- Terrenos (não única propriedade) 1% a 5% -> faixa de 250 a 350 URM = 2%.
INSERT INTO referencia_iptu (cidade_id, tipo_imovel_id, aliquota) VALUES
(4, 1, 0.008000),
(4, 2, 0.008000),
(4, 3, 0.020000),
(4, 4, 0.008000);

-- Florianópolis - LC 007/1997, art. 228 (redação da LC 230/2006):
-- https://www.legisweb.com.br/legislacao/?id=174515
-- Residencial até 150 m² = 0,5%; comercial/serviços até 150 m² = 1,0%;
-- terrenos 0,5% a 2,0% -> usado 2,0%.
-- Conferido também com resumo de 2025/2026 de escritório de advocacia
-- (fonte secundária, https://barbieriadvogados.com), que traz os mesmos
-- 0,5% / 1,0% / 2,0% nas faixas usadas aqui.
INSERT INTO referencia_iptu (cidade_id, tipo_imovel_id, aliquota) VALUES
(5, 1, 0.005000),
(5, 2, 0.005000),
(5, 3, 0.020000),
(5, 4, 0.010000);

-- Curitiba - IPTU 2025 (LC 40/2001 alterada pela LC 136/2022;
-- faixas atualizadas pelo Decreto 1.996/2024):
-- https://www.normasbrasil.com.br/norma/decreto-1996-2024-curitiba_470782.html
-- Residencial progressivo 0,20% a 0,65% -> acima de R$ 351.289,34 = 0,65%.
-- Não residencial 0,40% a 1,35% -> acima de R$ 351.289,34 = 1,35%.
-- Terreno: varia por zona, não conferido -> sem referência.
INSERT INTO referencia_iptu (cidade_id, tipo_imovel_id, aliquota) VALUES
(6, 1, 0.006500),
(6, 2, 0.006500),
(6, 4, 0.013500);

-- Novo Hamburgo - Código Tributário (Lei 1.031/2003), página oficial:
-- https://novohamburgo.rs.gov.br/smf/iptu-imposto-propriedade-predial-territorial-urbana/aliquotas-iptu
-- Prediais = 0,35% sobre o valor venal total (apartamento, casa, sala).
-- Terreno: progressivo por faixas (Anexo V-A), não conferido -> sem referência.
INSERT INTO referencia_iptu (cidade_id, tipo_imovel_id, aliquota) VALUES
(7, 1, 0.003500),
(7, 2, 0.003500),
(7, 4, 0.003500);

-- Campo Bom - SEM referência de IPTU. O Código Tributário (Lei 2.397/2002,
-- art. 103, redação da Lei 2.877/2005) traz 1% (com edificação) e 3%
-- (sem edificação), mas permite reduções definidas na Lei da Planta
-- Genérica de Valores; a alíquota efetiva não foi conferida em fonte
-- oficial -> cidade cadastrada sem alíquota e sem imóvel de demonstração.

-- Joinville - LC 389/2013, art. 17, II (redação da LC 575/2021), Jornal
-- Oficial do Município: não residencial comercial = 1,5% (serviços = 1%).
-- Residencial: faixas não conferidas no texto da lei -> sem referência.
INSERT INTO referencia_iptu (cidade_id, tipo_imovel_id, aliquota) VALUES
(9, 4, 0.015000);

-- Balneário Camboriú - SEM referência de IPTU: a alíquota residencial
-- varia por setor fiscal (Lei 5.000/2025) e o texto oficial não pôde ser
-- conferido -> cidade cadastrada só com o m², sem imóvel.

-- Londrina - Lei 12.575/2017; Decreto 1.563/2017, art. 6º (Jornal Oficial):
-- http://www1.londrina.pr.gov.br/dados/images/stories/Storage/isslondrina/decretos/decreto_1563-2017_29_dezembro_2017.pdf
-- Edificado = 1%; não edificado até 10.000 m² = 3%.
-- (Residencial edificado tem isenção de uma parcela fixa do valor venal;
--  o sistema simplifica e aplica a alíquota sobre o valor estimado.)
INSERT INTO referencia_iptu (cidade_id, tipo_imovel_id, aliquota) VALUES
(11, 1, 0.010000),
(11, 2, 0.010000),
(11, 3, 0.030000),
(11, 4, 0.010000);

-- ===== proprietario (dados FICTÍCIOS) =====
-- CPFs com dígito verificador válido, mas inventados.
INSERT INTO proprietario (id, nome, cpf, email, telefone, cidade_id) VALUES
(1, 'Ana Exemplo da Silva', '111.444.777-35', 'ana.exemplo@example.com', '(51) 90000-0001', 1),
(2, 'Bruno Teste Oliveira', '222.555.888-46', 'bruno.teste@example.com', '(54) 90000-0002', 2),
(3, 'Carla Demo Pereira', '333.666.999-57', 'carla.demo@example.com', '(48) 90000-0003', 5),
(4, 'Diego Modelo Santos', '444.777.000-83', 'diego.modelo@example.com', '(51) 90000-0004', 7),
(5, 'Elisa Ficticia Rocha', '555.888.111-94', 'elisa.ficticia@example.com', '(43) 90000-0005', 11);

-- ===== imovel =====
-- 14 imóveis: 4 apartamentos, 3 casas, 3 terrenos e 4 salas comerciais,
-- todos em cidade + tipo COM alíquota de IPTU conferida (nenhum IPTU zero).
-- Valor estimado: última avaliação; senão área privativa x m² (só
-- apartamento tem m²); senão valor de compra.
-- cidade_id / tipo_imovel_id / status_id conforme os ids acima.
INSERT INTO imovel
(id, area_total, area_privativa, valor_compra, data_compra, comodos, banheiros, vagas_garagem, observacoes, cidade_id, tipo_imovel_id, status_id)
VALUES
(1, 85.00, 70.00, 420000.00, '2019-03-15', 5, 2, 1, 'Apartamento no bairro Petrópolis', 1, 1, 2),
(2, 180.00, 150.00, 650000.00, '2017-08-20', 7, 3, 2, 'Casa com pátio', 2, 2, 1),
(3, 72.00, 60.00, 610000.00, '2021-06-10', 4, 2, 1, 'Apartamento perto da UFSC', 5, 1, 2),
(4, 45.00, 38.00, 290000.00, '2020-11-05', 2, 1, 1, 'Sala comercial no Centro', 6, 4, 2),
(5, 360.00, 360.00, 180000.00, '2022-02-14', 0, 0, 0, 'Terreno plano, 12 x 30 m', 4, 3, 3),
(6, 300.00, 300.00, 150000.00, '2023-05-10', 0, 0, 0, 'Terreno em loteamento novo', 11, 3, 1),
(7, 450.00, 450.00, 220000.00, '2018-09-03', 0, 0, 0, 'Terreno de esquina, 15 x 30 m', 2, 3, 3),
(8, 72.00, 60.00, 290000.00, '2022-07-01', 4, 1, 1, 'Apartamento perto da Feevale', 7, 1, 1),
(9, 95.00, 80.00, 400000.00, '2021-11-18', 5, 2, 1, 'Apartamento na Gleba Palhano', 11, 1, 2),
(10, 40.00, 34.00, 230000.00, '2020-02-27', 1, 1, 1, 'Sala comercial no Centro', 9, 4, 2),
(11, 55.00, 48.00, 350000.00, '2016-10-12', 2, 1, 1, 'Sala comercial no Moinhos de Vento', 1, 4, 2),
(12, 30.00, 26.00, 180000.00, '2024-03-05', 1, 1, 0, 'Sala comercial no Centro', 7, 4, 3),
(13, 220.00, 190.00, 720000.00, '2015-06-22', 8, 3, 2, 'Casa no bairro Santa Felicidade', 6, 2, 1),
(14, 160.00, 140.00, 480000.00, '2019-12-09', 6, 2, 2, 'Casa com pátio e churrasqueira', 3, 2, 2);

-- ===== imovel_proprietario (N:N) =====
-- Soma dos percentuais de cada imóvel: no máximo 100%.
INSERT INTO imovel_proprietario (imovel_id, proprietario_id, percentual_participacao) VALUES
(1, 1, 50.00), (1, 2, 50.00),   -- 100%
(2, 2, 100.00),                 -- 100%
(3, 3, 60.00), (3, 1, 40.00),   -- 100%
(4, 3, 100.00),                 -- 100%
(5, 1, 75.00),                  -- 75% (na demo o Bruno entra com 25%)
(6, 5, 100.00),                 -- 100%
(7, 2, 100.00),                 -- 100%
(8, 4, 100.00),                 -- 100%
(9, 5, 50.00), (9, 4, 50.00),   -- 100%
(10, 3, 100.00),                -- 100%
(11, 1, 100.00),                -- 100%
(12, 4, 50.00), (12, 5, 50.00), -- 100%
(13, 1, 50.00), (13, 3, 50.00), -- 100%
(14, 2, 60.00), (14, 4, 40.00); -- 100%

-- ===== avaliacao =====
-- O dashboard usa a avaliação MAIS RECENTE de cada imóvel.
INSERT INTO avaliacao (imovel_id, data_avaliacao, valor_estimado, observacao) VALUES
(1, '2023-04-01', 470000.00, 'Avaliação de corretor'),
(1, '2026-03-10', 535000.00, 'Laudo de avaliação atualizado'),
(2, '2025-11-20', 780000.00, 'Avaliação de corretor'),
(4, '2025-12-01', 315000.00, 'Avaliação para renovação do aluguel'),
(5, '2026-05-20', 205000.00, 'Preço sugerido para venda'),
(6, '2026-02-15', 165000.00, 'Avaliação de corretor'),
(10, '2024-08-01', 245000.00, 'Avaliação de corretor'),
(10, '2026-06-15', 260000.00, 'Avaliação para renovação do aluguel'),
(11, '2026-04-08', 380000.00, 'Laudo de avaliação'),
(13, '2025-09-30', 840000.00, 'Avaliação de corretor'),
(14, '2026-01-20', 520000.00, 'Avaliação de corretor');

-- ===== despesa =====
INSERT INTO despesa (imovel_id, descricao, valor, data_despesa) VALUES
(1, 'Condomínio de agosto', 780.00, '2026-08-05'),
(2, 'Troca do telhado', 12500.00, '2025-10-18'),
(5, 'Limpeza do terreno', 650.00, '2026-04-02'),
(6, 'Roçada do terreno', 400.00, '2026-07-15'),
(10, 'Condomínio de agosto', 950.00, '2026-08-05'),
(13, 'Pintura externa', 8400.00, '2026-03-12');

-- ===== movimentacao =====
-- tipo: entrada_aluguel / saida_manutencao / outro (códigos do sistema)
INSERT INTO movimentacao (imovel_id, tipo, valor, data_movimentacao, observacao) VALUES
(1, 'entrada_aluguel', 2600.00, '2026-08-10', 'Aluguel de agosto'),
(3, 'entrada_aluguel', 3900.00, '2026-08-10', 'Aluguel de agosto'),
(2, 'saida_manutencao', 12500.00, '2025-10-18', 'Pagamento da troca do telhado'),
(5, 'outro', NULL, '2026-05-25', 'Anúncio de venda publicado'),
(9, 'entrada_aluguel', 2100.00, '2026-08-10', 'Aluguel de agosto'),
(10, 'entrada_aluguel', 2400.00, '2026-08-10', 'Aluguel de agosto'),
(11, 'entrada_aluguel', 2900.00, '2026-08-10', 'Aluguel de agosto'),
(13, 'saida_manutencao', 8400.00, '2026-03-12', 'Pagamento da pintura externa'),
(12, 'outro', NULL, '2026-07-01', 'Placa de venda instalada');
