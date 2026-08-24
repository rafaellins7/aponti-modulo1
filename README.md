# Aponti — Análise de Dados PRF

Repositório com a trilha completa do curso de Análise de Dados, usando a base de acidentes da Polícia Rodoviária Federal (PRF) como estudo de caso. Cada atividade representa uma etapa de maturidade da análise, reaproveitando o que foi feito na anterior.

## Projeto PRF 2025 — Preparação dos Dados

### Objetivo

Preparar os dados de acidentes da PRF referentes a 2025 para análise exploratória (EDA), construção de dashboard no Power BI e treinamento de um modelo de árvore de decisão para prever a ocorrência de acidentes fatais.

### Variável-alvo

`acidente_fatal = 1` quando `mortos >= 1`; caso contrário, `acidente_fatal = 0`.

### Bases geradas

* `dados_tratados/base_analitica_prf_2025.csv`: base completa, com todas as colunas originais e derivadas (incluindo indicadores de gravidade). Uso: EDA e Power BI.
* `dados_tratados/base_modelavel_prf_2025.csv`: base reduzida às variáveis preditoras, pronta para modelagem (árvore de decisão).
* `dados_tratados/dicionario_variaveis_modulo4.csv`: dicionário das principais variáveis criadas.

### Observação metodológica

A base modelável exclui `mortos`, `feridos`, `feridos_leves`, `feridos_graves`, `total_vitimas` e `indice_gravidade`, pois essas variáveis são derivadas diretamente do desfecho (`acidente_fatal`) e seu uso como preditoras causaria vazamento de dados (*data leakage*).

### Documentação complementar

Ver `logs/decisoes_tratamento_modulo4.md` para as regras de tratamento de nulos, tipos e categorias, e a justificativa metodológica de cada decisão.

---

## Estrutura do Módulo 1 — Unidades de Aprendizado

A jornada do **Módulo 1** está organizada em **4 Unidades encadeadas**, evoluindo progressivamente a maturidade dos dados desde a ingestão bruta até a modelagem preditiva:

```text
aponti-modulo1/
└── Módulo 1/
    ├── Unidade 1/  ──> Diagnóstico de Dados & Perguntas de Negócio
    ├── Unidade 2/  ──> Engenharia de Features & EDA Profunda
    ├── Unidade 3/  ──> Consultas Analíticas & Modelagem SQL
    └── Unidade 4/  ──> Pipelines para ML, BI & Governança de Dados

### Unidade 1 — Diagnóstico de Dados & Perguntas de Negócio

**Objetivo:** Realizar a primeira imersão na base de acidentes da PRF, entendendo sua estrutura, qualidade e contexto de negócio.

**Principais entregas:**

* Mapeamento do esquema e dos tipos de dados.
* Identificação de valores nulos, inconsistências e possíveis problemas de qualidade.
* Análise inicial das variáveis e distribuição dos registros.
* Definição das principais perguntas e hipóteses de negócio.

**Perguntas exploradas:**

* Como os acidentes se distribuem ao longo do dia?
* Quais condições meteorológicas estão associadas a maior severidade?
* Como o tipo de pista influencia a ocorrência e a gravidade dos acidentes?

### Unidade 2 — Engenharia de Features & EDA Profunda

**Objetivo:** Transformar os dados brutos em uma base mais consistente e informativa, criando variáveis capazes de representar diferentes aspectos dos acidentes.

**Principais entregas:**

* Tratamento de inconsistências e valores ausentes.
* Criação de variáveis derivadas (*feature engineering*).
* Categorização de horários e períodos do dia.
* Classificação entre dias úteis e finais de semana.
* Análise de distribuições, relações e correlações entre variáveis.
* Identificação e tratamento de valores extremos (*outliers*).

**Resultado:** Uma base enriquecida e preparada para análises exploratórias mais profundas e para as etapas seguintes do projeto.

### Unidade 3 — Consultas Analíticas & Modelagem SQL

**Objetivo:** Estruturar os dados em ambiente relacional e utilizar SQL para responder perguntas analíticas de forma eficiente.

**Principais entregas:**

* Organização da base em banco de dados relacional.
* Criação de consultas para agregações e indicadores.
* Utilização de `GROUP BY`, `JOIN` e subconsultas.
* Aplicação de *Window Functions*, como `RANK()` e `DENSE_RANK()`.
* Ranking de rodovias e municípios segundo indicadores de acidentes e mortalidade.
* Extração de métricas para apoiar as análises do projeto.

**Resultado:** Transformação dos dados tratados em informações analíticas estruturadas e reutilizáveis.

### Unidade 4 — Pipelines para ML, BI & Governança

**Objetivo:** Consolidar a preparação dos dados para diferentes aplicações, separando as necessidades de análise, visualização e modelagem preditiva.

**Principais entregas:**

* Construção da base analítica para EDA e Power BI.
* Criação da base modelável para Machine Learning.
* Definição da variável-alvo `acidente_fatal`.
* Prevenção de *data leakage* na seleção das variáveis preditoras.
* Criação de indicadores e KPIs estratégicos.
* Preparação dos dados para treinamento de árvore de decisão.
* Criação do dicionário de variáveis.
* Documentação das decisões de tratamento e regras de governança.

**Resultado:** Pipeline final preparada para **Análise Exploratória, Business Intelligence e Machine Learning**, com separação adequada entre dados analíticos e dados destinados à modelagem.
