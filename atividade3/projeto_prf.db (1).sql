-- 1 verificando versão
SELECT sqlite_version() AS versao_sqlite;

-- 2 exibindo estrutura
PRAGMA table_info(acidentes_prf_2025);

-- 3 numero total de acidentes
SELECT COUNT(*) AS total_ocorrencias FROM acidentes_prf_2025;

-- 4 excluindo view base
DROP VIEW IF EXISTS vw_acidentes_base;

-- 5 criando view base com flag
CREATE VIEW vw_acidentes_base AS
SELECT *, CASE WHEN CAST(mortos AS INTEGER) >= 1 THEN 1 ELSE 0 END AS acidente_fatal
FROM acidentes_prf_2025;

-- 6 calcular metricas gerais
SELECT COUNT(*) AS total_acidentes, SUM(acidente_fatal) AS acidentes_fatais,
ROUND(100.0 * SUM(acidente_fatal) / COUNT(*), 2) AS perc_fatais
FROM vw_acidentes_base;

-- 7 agregar acidentes/mortos/%, min 100 por UF
SELECT uf, COUNT(*) AS total_acidentes, SUM(acidente_fatal) AS acidentes_fatais, SUM(CAST(mortos AS INTEGER))
AS total_mortos, ROUND(100.0 * SUM(acidente_fatal) / COUNT(*), 2) AS perc_fatais FROM vw_acidentes_base
GROUP BY uf HAVING COUNT(*) >= 100 ORDER BY perc_fatais DESC;

-- 8 listar 30 brs mais letais
SELECT br, COUNT(*) AS total_acidentes, SUM(CAST(mortos AS INTEGER)) AS total_mortos, SUM(acidente_fatal)
AS acidentes_fatais, ROUND(100.0 * SUM(acidente_fatal) / COUNT(*), 2) AS perc_fatais FROM vw_acidentes_base
WHERE br IS NOT NULL GROUP BY br HAVING COUNT(*) >= 100 ORDER BY total_mortos DESC LIMIT 30;

-- 9 agrupar evolução temporal por ano e mês
SELECT CAST(strftime('%Y', data_inversa) AS INTEGER) AS ano, CAST(strftime('%m', data_inversa) AS INTEGER)
AS mes, COUNT(*) AS total_acidentes, SUM(CAST(mortos AS INTEGER)) AS total_mortos, SUM(acidente_fatal)
AS acidentes_fatais, ROUND(100.0 * SUM(acidente_fatal) / COUNT(*), 2) AS perc_fatais FROM vw_acidentes_base
GROUP BY ano, mes ORDER BY ano, mes;

-- 10 análise da relação bivariada: tipo de acidente e % de fatais
SELECT tipo_acidente, COUNT(*) AS total_acidentes, SUM(acidente_fatal) AS acidentes_fatais,
ROUND(100.0 * SUM(acidente_fatal) / COUNT(*), 2) AS perc_fatais FROM vw_acidentes_base GROUP BY tipo_acidente
HAVING COUNT(*) >= 100 ORDER BY perc_fatais DESC;

-- 11 análise das 30 causas de acidentes por maior letalidade
SELECT causa_acidente, COUNT(*) AS total_acidentes, SUM(acidente_fatal) AS acidentes_fatais,
ROUND(100.0 * SUM(acidente_fatal) / COUNT(*), 2) AS perc_fatais FROM vw_acidentes_base GROUP BY causa_acidente
HAVING COUNT(*) >= 100 ORDER BY perc_fatais DESC LIMIT 30;

-- 12 comparação da gravidade com fase do dia
SELECT fase_dia, COUNT(*) AS total_acidentes, SUM(acidente_fatal) AS acidentes_fatais,
ROUND(100.0 * SUM(acidente_fatal) / COUNT(*), 2) AS perc_fatais FROM vw_acidentes_base GROUP BY fase_dia
HAVING COUNT(*) >= 100 ORDER BY perc_fatais DESC;

-- 13 avaliar influência meteorológica na porcentagem dos fatais
SELECT condicao_metereo, COUNT(*) AS total_acidentes, SUM(acidente_fatal) AS acidentes_fatais,
ROUND(100.0 * SUM(acidente_fatal) / COUNT(*), 2) AS perc_fatais FROM vw_acidentes_base GROUP BY condicao_metereo
HAVING COUNT(*) >= 100 ORDER BY perc_fatais DESC;

-- 14 comparação letalidade do acidente com tipo de pista
SELECT tipo_pista, COUNT(*) AS total_acidentes, SUM(acidente_fatal) AS acidentes_fatais, ROUND(100.0 * SUM(acidente_fatal) / COUNT(*), 2)
AS perc_fatais FROM vw_acidentes_base GROUP BY tipo_pista HAVING COUNT(*) >= 100 ORDER BY perc_fatais DESC;

-- 15 análise de dois fatores combinados e a cobertura
SELECT tipo_pista, fase_dia, COUNT(*) AS total_acidentes, SUM(acidente_fatal) AS acidentes_fatais,
ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS cobertura_perc, ROUND(100.0 * SUM(acidente_fatal) / COUNT(*), 2)
AS perc_fatais FROM vw_acidentes_base GROUP BY tipo_pista, fase_dia HAVING COUNT(*) >= 100 ORDER BY perc_fatais DESC;

-- 16 cálculo do efeito lift
WITH taxa_global AS (SELECT 1.0 * SUM(acidente_fatal) / COUNT(*) AS taxa FROM vw_acidentes_base) SELECT tipo_acidente,
COUNT(*) AS total_acidentes, SUM(acidente_fatal) AS acidentes_fatais, ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2)
AS cobertura_perc, ROUND(1.0 * SUM(acidente_fatal) / COUNT(*), 4) AS confianca, ROUND((1.0 * SUM(acidente_fatal) / COUNT(*)) / taxa, 2)
AS lift FROM vw_acidentes_base CROSS JOIN taxa_global GROUP BY tipo_acidente, taxa HAVING COUNT(*) >= 100 ORDER BY lift DESC;

-- 17 criando a view indicadores_mensais
DROP VIEW IF EXISTS vw_indicadores_mensais;

CREATE VIEW vw_indicadores_mensais AS SELECT CAST(strftime('%Y', data_inversa) AS INTEGER) AS ano,
CAST(strftime('%m', data_inversa) AS INTEGER) AS mes, COUNT(*) AS total_acidentes, SUM(CAST(mortos AS INTEGER))
AS total_mortos, SUM(acidente_fatal) AS acidentes_fatais, ROUND(100.0 * SUM(acidente_fatal) / COUNT(*), 2)
AS perc_fatais FROM vw_acidentes_base GROUP BY ano, mes;

SELECT * FROM vw_indicadores_mensais ORDER BY ano, mes;

-- 18 criando a view indicadores_uf_br
DROP VIEW IF EXISTS vw_indicadores_uf_br;

CREATE VIEW vw_indicadores_uf_br AS SELECT uf, br, COUNT(*) AS total_acidentes, SUM(CAST(mortos AS INTEGER))
AS total_mortos, SUM(acidente_fatal) AS acidentes_fatais, ROUND(100.0 * SUM(acidente_fatal) / COUNT(*), 2)
AS perc_fatais FROM vw_acidentes_base WHERE br IS NOT NULL GROUP BY uf, br;

SELECT * FROM vw_indicadores_uf_br ORDER BY total_mortos DESC;

-- base analitica
DROP VIEW IF EXISTS vw_base_analitica;

CREATE VIEW vw_base_analitica AS SELECT data_inversa, dia_semana, horario, uf, br, municipio, causa_acidente,
tipo_acidente, classificacao_ac, fase_dia, condicao_metereo, tipo_pista, tracado_via, uso_solo,
CAST(mortos AS INTEGER) AS mortos, acidente_fatal FROM vw_acidentes_base;

SELECT * FROM vw_base_analitica LIMIT 20;

-- conferindo nomes reais das colunas (sem truncar na tela)
SELECT name FROM pragma_table_info('acidentes_prf_2025');

-- base preliminar para modelagem
DROP VIEW IF EXISTS vw_base_modelavel_preliminar;

CREATE VIEW vw_base_modelavel_preliminar AS SELECT uf, br, municipio, CAST(strftime('%m', data_inversa) AS INTEGER)
AS mes, dia_semana, fase_dia, causa_acidente, tipo_acidente, condicao_metereo, tipo_pista, tracado_via, uso_solo,
acidente_fatal FROM vw_acidentes_base;

SELECT * FROM vw_base_modelavel_preliminar LIMIT 20;