# Unidade 5 — Análise Exploratória de Dados (EDA): Acidentes PRF 2025

**Autores:** José Guilherme Teixeira Nunes e Francisco Almeida Lucas De Farias Junior

Este diretório contém a Análise Exploratória de Dados (EDA) aplicada à base oficial de acidentes da Polícia Rodoviária Federal (PRF) do ano de 2025, com foco na investigação dos fatores determinantes para acidentes fatais.

---

## Problema Analítico Central

**Pergunta:** Quais fatores estão associados à ocorrência de acidentes com vítima fatal nas rodovias federais?

* **Variável-alvo:** `acidente_fatal`
  * `1`: Ocorrências com pelo menos 1 vítima fatal (`mortos >= 1`).
  * `0`: Ocorrências sem registro de óbito.

---

## Indicadores Globais da Base (2025)

* **Volume Total de Acidentes:** 72.529 ocorrências
* **Acidentes com Vítima Fatal:** 5.210 ocorrências (7,18% do total)
* **Mortalidade:** 6.043 mortos no total (média de 8,33 mortes a cada 100 acidentes)
* **Vítimas:** 83.550 feridos no total (sendo 20.018 feridos graves) e 76.406 ilesos
* **Volume Envolvido:** 144.922 veículos e 188.346 pessoas (médias de 2,00 veículos e 2,60 pessoas por acidente)

---

## Frequências, Rankings e Achados Principais

### 1. Causa do Acidente e Comportamento
* **Falta de Atenção:** Falhas de atenção do condutor (*ausência de reação* com 11.469 casos e *reação tardia* com 10.799 casos) somam mais de 22 mil ocorrências, correspondendo a quase um terço de toda a base.
* **Fatores de Alta Fatalidade:** Causas comportamentais e atitudes de risco — como *Ingestão de Álcool*, *Velocidade Incompatível*, *Dormir ao Volante* e *Transitar na Contramão* — são os principais preditores de acidentes fatais.

### 2. Dia da Semana e Clima
* **Sazonalidade Semanal:** A distribuição ao longo da semana é relativamente uniforme, apresentando leve concentração aos sábados (11.554) e domingos (11.470) devido ao maior fluxo de lazer.
* **Condição Meteorológica:** A grande maioria das ocorrências se dá em *Céu Claro* (46.375), seguido por *Nublado* (11.435) e *Chuva* (6.438), refletindo o maior tempo de exposição dos veículos sob tempo bom.

### 3. Distribuição Geográfica por Estado (UF)
* **Volume Absoluto:** Minas Gerais (MG) lidera o volume do país com 9.570 acidentes e 765 mortos, seguido por Santa Catarina (8.186 acidentes e 434 mortos) e Paraná (7.630 acidentes e 593 mortos).
* **Taxa de Severidade:** O ranking de volume não é o ranking de letalidade. O Maranhão (MA) registra a maior proporção fatal do país, com 19% dos seus acidentes resultando em mortes (281 mortos em 1.262 acidentes). Pará (17%) e Roraima (16%) também apresentam letalidade muito acima da média nacional.

### 4. Rodovias Federais (BRs)
* **Líderes de Volume:** As gigantes BR-101 (13.014 acidentes e 760 mortos) e BR-116 (11.021 acidentes e 708 mortos) concentram juntas cerca de um terço de todos os acidentes das 15 maiores rodovias.
* **Líderes de Severidade:** A BR-316 desponta com a maior taxa de fatalidade do país (15%), seguida pela BR-230 (10% de fatalidade).

### 5. Tipologia do Acidente
* **Tipos Mais Comuns:** Colisão traseira (14.360 registros, 4% de fatalidade) e Saída de leito carroçável (10.209 registros, 6% de fatalidade) são os acidentes mais frequentes.
* **Tipos Mais Fatais:** Atropelamentos de Pedestres (30% de fatalidade) e Colisões Frontais (29% de fatalidade) exigem extrema priorização operacional e de infraestrutura, pois quase 3 em cada 10 ocorrências resultam em óbito.

---

## Comportamento Temporal (2025)

* **Visão Mensal:** O volume de acidentes apresenta picos em meses festivos e de férias escolares, destacando-se julho (6.238 acidentes) e dezembro (6.788 acidentes e 572 mortes).
* **Estabilidade da Gravidade:** Apesar das oscilações no volume total, a taxa de fatalidade mensal permaneceu estável em torno de 7% (com picos pontuais de 8% em maio e agosto), mostrando que a severidade acompanha o aumento de fluxo.
* **Série por Estado:** Minas Gerais manteve a liderança isolada de ocorrências em todos os 12 meses do ano (oscilando entre 638 em fevereiro e 882 em julho).

---

## Comparativo População vs. Acidentes (IBGE 2025)

Cruzando a base populacional do IBGE com os registros da PRF para os 5 estados mais populosos:

* **São Paulo (46,08M habitantes):** Concentra 21,6% da população nacional, mas responde por apenas 6,5% dos acidentes da PRF (4.683 acidentes, razão de 0,30) e possui a menor taxa de fatalidade (4%).
* **Minas Gerais (21,39M habitantes):** Concentra 10,0% da população e 13,2% dos acidentes (razão de 1,32).
* **Paraná (11,89M habitantes):** Concentra 5,6% da população e 10,5% dos acidentes, registrando a maior razão per capita entre os grandes estados (1,89).
* **Rio de Janeiro (17,22M habitantes):** Concentra 8,1% da população e 8,9% dos acidentes (razão de 1,10).
* **Bahia (14,87M habitantes):** Concentra 7,0% da população e 5,7% dos acidentes (razão de 0,81).

**Conclusão:** A densidade populacional não explica a gravidade e o volume de acidentes por si só, sendo necessário analisar fatores de infraestrutura viária e perfil logístico das UFs.

---

## Arquivos da Unidade

* `Atividade.docx`: Relatório executivo completo contendo detalhamento metodológico e análises.
* `grafico_acidentes_temporal.png`: Visualização da série temporal comparando o volume total e acidentes fatais ao longo de 2025.
