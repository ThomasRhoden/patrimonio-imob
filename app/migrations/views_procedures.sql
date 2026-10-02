-- =====================================================
-- VIEWS E PROCEDURE - patrimonio_imob (3 views + 1 procedure)
-- Ordem: 1) patrimonio_imob_full.sql  2) este arquivo
--        3) dados_iniciais.sql        4) python seed_inicial.py
--
-- Padrão de nomes (UC3): VW_ = view, SP_ = procedure,
-- P_ = parâmetro, V_ = variável. Erro de regra: SIGNAL SQLSTATE '45000'.
-- MySQL Workbench: File > Open SQL Script > raio (Execute).
-- O Workbench entende o DELIMITER $$ da procedure.
-- =====================================================

USE patrimonio_imob;

-- =====================================================
-- VW_IMOVEL_DETALHADO
-- Uma linha por imóvel, com cidade/estado/tipo/status e o valor
-- estimado calculado igual ao sistema: última avaliação; senão
-- área privativa x valor do m²; senão valor de compra.
-- Também traz a alíquota de IPTU da cidade + tipo (0 se não houver).
-- =====================================================
CREATE OR REPLACE VIEW VW_IMOVEL_DETALHADO AS
SELECT
    i.id AS IMOVEL_ID,
    e.id AS ESTADO_ID,
    e.nome AS ESTADO,
    e.sigla AS SIGLA,
    c.id AS CIDADE_ID,
    c.nome AS CIDADE,
    t.nome AS TIPO_IMOVEL,
    s.nome AS STATUS_IMOVEL,
    i.area_privativa AS AREA_PRIVATIVA,
    i.valor_compra AS VALOR_COMPRA,
    COALESCE(
        (SELECT a.valor_estimado
           FROM avaliacao a
          WHERE a.imovel_id = i.id
          ORDER BY a.data_avaliacao DESC, a.id DESC
          LIMIT 1),
        i.area_privativa * rm.valor_m2,
        i.valor_compra
    ) AS VALOR_ESTIMADO,
    COALESCE(ri.aliquota, 0) AS ALIQUOTA_IPTU
FROM imovel i
    INNER JOIN cidade c ON c.id = i.cidade_id
    INNER JOIN estado e ON e.id = c.estado_id
    INNER JOIN tipo_imovel t ON t.id = i.tipo_imovel_id
    INNER JOIN status_imovel s ON s.id = i.status_id
    LEFT JOIN referencia_m2 rm
        ON rm.cidade_id = i.cidade_id AND rm.tipo_imovel_id = i.tipo_imovel_id
    LEFT JOIN referencia_iptu ri
        ON ri.cidade_id = i.cidade_id AND ri.tipo_imovel_id = i.tipo_imovel_id;

-- =====================================================
-- VW_PATRIMONIO_POR_CIDADE
-- Resumo do patrimônio por estado + cidade (COUNT e SUM).
-- O HAVING deixa só as cidades com pelo menos 1 imóvel.
-- Usada em: Imovel_DAO.get_patrimonio_por_cidade() (aba "Por cidade").
-- =====================================================
CREATE OR REPLACE VIEW VW_PATRIMONIO_POR_CIDADE AS
SELECT
    e.nome AS ESTADO,
    e.sigla AS SIGLA,
    c.nome AS CIDADE,
    COUNT(v.IMOVEL_ID) AS QUANTIDADE,
    SUM(v.VALOR_COMPRA) AS VALOR_COMPRA_TOTAL,
    SUM(v.VALOR_ESTIMADO) AS VALOR_ESTIMADO_TOTAL,
    SUM(v.VALOR_ESTIMADO) - SUM(v.VALOR_COMPRA) AS VALORIZACAO_TOTAL,
    SUM(v.VALOR_ESTIMADO * v.ALIQUOTA_IPTU) AS IPTU_ESTIMADO_TOTAL
FROM estado e
    INNER JOIN cidade c ON c.estado_id = e.id
    LEFT JOIN VW_IMOVEL_DETALHADO v ON v.CIDADE_ID = c.id
GROUP BY e.nome, e.sigla, c.nome
HAVING COUNT(v.IMOVEL_ID) > 0;

-- =====================================================
-- VW_RESUMO_POR_PROPRIETARIO
-- Resumo por dono (N:N imovel_proprietario): cada valor do imóvel
-- entra multiplicado pelo percentual do dono / 100.
-- Imóvel com menos de 100% distribuído: a parte sem dono não entra.
-- Usada em: Imovel_DAO.get_resumo_por_proprietario() (aba "Por proprietário").
-- =====================================================
CREATE OR REPLACE VIEW VW_RESUMO_POR_PROPRIETARIO AS
SELECT
    p.id AS PROPRIETARIO_ID,
    p.nome AS PROPRIETARIO,
    COUNT(ip.imovel_id) AS QUANTIDADE,
    SUM(v.VALOR_COMPRA * ip.percentual_participacao / 100) AS VALOR_COMPRA_PARTE,
    SUM(v.VALOR_ESTIMADO * ip.percentual_participacao / 100) AS VALOR_ESTIMADO_PARTE,
    SUM((v.VALOR_ESTIMADO - v.VALOR_COMPRA) * ip.percentual_participacao / 100) AS VALORIZACAO_PARTE,
    SUM(v.VALOR_ESTIMADO * v.ALIQUOTA_IPTU * ip.percentual_participacao / 100) AS IPTU_PARTE
FROM proprietario p
    INNER JOIN imovel_proprietario ip ON ip.proprietario_id = p.id
    INNER JOIN VW_IMOVEL_DETALHADO v ON v.IMOVEL_ID = ip.imovel_id
GROUP BY p.id, p.nome;

-- =====================================================
-- SP_ADICIONAR_PROPRIETARIO
-- Liga um proprietário a um imóvel (tabela N:N imovel_proprietario).
-- Se a soma dos percentuais passar de 100%, dispara SIGNAL SQLSTATE
-- '45000' (no Python vira o erro 1644 -> mensagem amigável).
-- Usada em: Participacao_Proprietario_DAO.substituir_proprietarios_do_imovel().
-- =====================================================
DROP PROCEDURE IF EXISTS SP_ADICIONAR_PROPRIETARIO;

DELIMITER $$

CREATE PROCEDURE SP_ADICIONAR_PROPRIETARIO(
    IN P_IMOVEL_ID INTEGER,
    IN P_PROPRIETARIO_ID INTEGER,
    IN P_PERCENTUAL DECIMAL(5,2)
)
BEGIN
    DECLARE V_SOMA_ATUAL DECIMAL(6,2);

    SELECT COALESCE(SUM(percentual_participacao), 0)
      INTO V_SOMA_ATUAL
      FROM imovel_proprietario
     WHERE imovel_id = P_IMOVEL_ID;

    IF V_SOMA_ATUAL + P_PERCENTUAL > 100 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'A soma dos percentuais nao pode passar de 100%';
    END IF;

    INSERT INTO imovel_proprietario
        (imovel_id, proprietario_id, percentual_participacao)
    VALUES
        (P_IMOVEL_ID, P_PROPRIETARIO_ID, P_PERCENTUAL);
END $$

DELIMITER ;
