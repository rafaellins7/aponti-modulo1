# Unidade 3: Modelagem Relacional e Consultas Analíticas em SQL

Nesta etapa, a base tratada é estruturada em banco de dados relacional para a execução de consultas complexas e agregação de indicadores.

## Objetivos de Aprendizagem
- Modelar o esquema do banco de dados (Tabela Fato de Acidentes e Dimensões de Localidade, Causa e Gravidade).
- Escrever consultas SQL otimizadas para extração de métricas de negócio.
- Ranquear os trechos de rodovias mais perigosos do país por meio de agregações avançadas.

## Tópicos Cobertos
- **DDL e DML:** Criação de tabelas, tipos de dados adequados e carga de dados.
- **Agregações e Filtros:** `GROUP BY`, `HAVING`, funções de agregação (`SUM`, `COUNT`, `AVG`).
- **Funções de Janela (*Window Functions*):** `RANK()`, `DENSE_RANK()` para ranqueamento de BRs e municípios por índice de acidentes.

## Tecnologias e Métodos
- **Banco de Dados:** PostgreSQL / SQLite.
- **Linguagem:** SQL ANSI (com foco em funções analíticas).

## Entregável da Unidade
- **Atividade 3:** Conjunto de scripts `.sql` contendo a modelagem do banco e as queries responsáveis por responder às perguntas fundamentais do projeto.
