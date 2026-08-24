# Unidade 2 — Relatório Visual Executivo (Excel)

Construção de um **Dashboard Executivo no Excel** utilizando a base de dados de acidentes de 2025 da PRF, focando em tratamento de dados, estatística descritiva e visualização.

---

## 🛠️ Principais Ações Realizadas

* **Tratamento e Regras de Negócio:**
  * Subtração simples para calcular `Vítimas Feridas`.
  * Classificação de `Status de Fatalidade` com `=SE()` (*Crítico* vs. *Sem Vítimas Fatais*).
  * Cálculo da `Taxa de Feridos Graves` (%) e `Pontuação de Risco`.
 
* **Estatística Descritiva & Consultas:**
  * Apuração de Média, Mediana e 3º Quartil (`=MÉDIA()`, `=MED()`, `=QUARTIL.INC()`).
  * Criação de motor de busca por ID com `=PROCV()`.
  * Contagem geral e agrupada de registros com `=CONT.VALORES()` e `=CONT.SE()`.
    
* **Visualização (Dashboard):**
  * **Dispersão (X,Y):** Correlação entre veículos e pessoas envolvidas com linha de tendência.
  * **Rosca:** Composição das fases do dia.
  * **Barras Horizontais:** Top 5 causas de acidentes.
  * **Linhas:** Evolução temporal mensal.
  * **Colunas Empilhadas:** Clima x Estado.

---

## Arquivos da Unidade

* `PI_Excel.pdf`: Roteiro de requisitos e critérios do projeto.
* `atividade2-aponti.xlsx`: Planilha com a base tratada, cálculos estatísticos e o dashboard final.
