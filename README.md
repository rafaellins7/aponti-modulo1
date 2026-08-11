# Aponti — Análise de Dados PRF (Atividades 1 a 4)

Repositório com a trilha completa do curso de Análise de Dados, usando a
base de acidentes da Polícia Rodoviária Federal (PRF) como estudo de caso.
Cada atividade representa uma etapa de maturidade da análise, reaproveitando
o que foi feito na anterior.

## Projeto PRF 2025 — Preparação dos Dados (Atividade 4)

### Objetivo
Preparar os dados de acidentes da PRF referentes a 2025 para análise
exploratória (EDA), construção de dashboard no Power BI e treinamento de
um modelo de árvore de decisão para prever a ocorrência de acidentes fatais.

### Variável-alvo
`acidente_fatal = 1` quando `mortos >= 1`; caso contrário, `acidente_fatal = 0`.

### Bases geradas
- `dados_tratados/base_analitica_prf_2025.csv`: base completa, com todas as colunas originais
  e derivadas (incluindo indicadores de gravidade). Uso: EDA e Power BI.
- `dados_tratados/base_modelavel_prf_2025.csv`: base reduzida às variáveis preditoras,
  pronta para modelagem (árvore de decisão).
- `dados_tratados/dicionario_variaveis_modulo4.csv`: dicionário das principais variáveis criadas.

### Observação metodológica
A base modelável **exclui** `mortos`, `feridos`, `feridos_leves`,
`feridos_graves`, `total_vitimas` e `indice_gravidade`, pois essas
variáveis são derivadas diretamente do desfecho (`acidente_fatal`) e seu
uso como preditoras causaria vazamento de dados (data leakage).

### Documentação complementar
Ver `logs/decisoes_tratamento_modulo4.md` para as regras de tratamento de nulos, tipos e
categorias, e a justificativa metodológica de cada decisão.

## Demais atividades

### Atividade 1 — Excel
Primeira atividade do curso, em planilha (`atividade1-aponti.xlsx`). Exercícios
introdutórios de organização e manipulação de dados.

### Atividade 2 — Excel
Continuação da prática em planilha (`modulo_02_excel_prf_grupo_01.xlsx`),
já usando a base da PRF como estudo de caso, com exercícios de exploração
dos dados brutos.

### Atividade 3 — SQL
Consultas e views em SQL (SQLite) sobre a base `acidentes_prf_2025`
(`projeto_prf.db.sql`), incluindo:
- Métricas gerais de acidentes e letalidade
- Agregações por UF, BR, causa e tipo de acidente
- Evolução temporal (ano/mês)
- Relação entre condições da via, clima e fase do dia com a gravidade dos acidentes
- Cálculo de cobertura e lift para cruzamento de fatores
- Views para consolidar indicadores e servir de base para a modelagem da atividade 4

### Atividade 4 — Python
Pipeline completo em Python (pandas), descrito em detalhe na seção acima.
Padroniza colunas e tipos, trata nulos, cria a variável-alvo, gera
indicadores de gravidade e constrói as bases analítica e modelável, com
documentação formal das decisões metodológicas.
