import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
import unicodedata

pd.set_option("display.max_columns", 120)
pd.set_option("display.width", 160)


def etapa5_criar_pastas():
    """Separar dados brutos e tratados, organizar notebooks/sql/relatórios."""
    raiz = Path(".")
    pastas = [
        "dados_brutos", "dados_tratados", "notebooks", "sql",
        "dashboards", "relatorios", "apresentacao", "logs"
    ]
    for pasta in pastas:
        (raiz / pasta).mkdir(parents=True, exist_ok=True)
    print("Pastas verificadas/criadas:")
    for pasta in pastas:
        print("-", raiz / pasta)
    return raiz

# 6. parâmetros centralizados do projeto

ARQUIVO_BRUTO = Path("dados_brutos/dados_abertos_prf-datatran2025 (2).csv")
ARQUIVO_BASE_ANALITICA = Path("dados_tratados/base_analitica_prf_2025.csv")
ARQUIVO_BASE_MODELAVEL = Path("dados_tratados/base_modelavel_prf_2025.csv")
ARQUIVO_DICIONARIO = Path("dados_tratados/dicionario_variaveis_modulo4.csv")
ARQUIVO_DECISOES = Path("logs/decisoes_tratamento_modulo4.md")
ARQUIVO_README = Path("README.md")
ARQUIVO_GRAFICO_ALVO = Path("relatorios/distribuicao_acidente_fatal.png")

SEPARADOR = ";"
ENCODING_ENTRADA = "latin1"
ENCODING_SAIDA = "utf-8-sig"

# bloco 2. leitura e primeira inspeção da base

def ler_csv_prf(caminho, sep=";", encodings=("latin1", "utf-8", "utf-8-sig")):
    """Etapa 7 — Ler o CSV da PRF com fallback de encoding."""
    ultimo_erro = None
    for enc in encodings:
        try:
            print(f"Tentando leitura com encoding={enc}...")
            return pd.read_csv(caminho, sep=sep, encoding=enc, low_memory=False)
        except Exception as erro:
            ultimo_erro = erro
            print(f"Falhou com {enc}: {erro}")
    raise ultimo_erro


def normalizar_nome_coluna(nome):
    """Etapa 8 — Padronizar nomes das colunas (minúsculas, sem acento, underline)."""
    nome = str(nome).strip().lower()
    nome = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode("utf-8")
    nome = nome.replace(" ", "_").replace("-", "_").replace("/", "_")
    while "__" in nome:
        nome = nome.replace("__", "_")
    return nome.strip("_")


def etapa8_padronizar_colunas(df):
    df.columns = [normalizar_nome_coluna(c) for c in df.columns]
    renomear = {"condicao_meteorologica": "condicao_metereologica"}
    df = df.rename(columns={k: v for k, v in renomear.items() if k in df.columns})
    print(df.columns.tolist())
    return df


def etapa9_conferir_colunas_esperadas(df):
    colunas_esperadas = [
        "data_inversa", "dia_semana", "horario", "uf", "br", "municipio",
        "causa_acidente", "tipo_acidente", "classificacao_acidente",
        "fase_dia", "condicao_metereologica", "tipo_pista", "tracado_via",
        "uso_solo", "pessoas", "mortos", "feridos_leves",
        "feridos_graves", "feridos", "veiculos"
    ]
    faltantes = [c for c in colunas_esperadas if c not in df.columns]
    print("Colunas faltantes:", faltantes)
    if faltantes:
        print("Atenção: ajuste nomes ou confirme o dicionário oficial da PRF usado no arquivo.")


def etapa10_retrato_inicial(df):
    print("Dimensões:", df.shape)
    print("Linhas:", df.shape[0])
    print("Colunas:", df.shape[1])
    print(df.head())
    print(df.sample(5, random_state=42))

# bloco 3. diagnóstico de qualidade dos dados

def etapa11_tipos_e_memoria(df):
    df.info(memory_usage="deep")
    resumo_tipos = (
        df.dtypes.astype(str)
        .value_counts()
        .rename_axis("tipo")
        .reset_index(name="qtd_colunas")
    )
    print(resumo_tipos)


def etapa12_diagnostico_nulos(df):
    nulos = pd.DataFrame({
        "qtd_nulos": df.isna().sum(),
        "perc_nulos": df.isna().mean() * 100
    }).sort_values("perc_nulos", ascending=False)
    print(nulos[nulos["qtd_nulos"] > 0])


def etapa13_remover_duplicidades(df):
    qtd_duplicadas = df.duplicated().sum()
    print("Duplicidades exatas:", qtd_duplicadas)
    if qtd_duplicadas > 0:
        df = df.drop_duplicates().copy()
        print("Duplicidades removidas. Nova dimensão:", df.shape)
    return df


def etapa14_cardinalidade(df):
    categoricas = df.select_dtypes(include="object").columns
    cardinalidade = (
        df[categoricas]
        .nunique(dropna=True)
        .sort_values(ascending=False)
        .reset_index()
    )
    cardinalidade.columns = ["variavel", "qtd_categorias"]
    print(cardinalidade.head(30))

# bloco 4. transformações e criação de variáveis derivadas

def etapa15_converter_numericas(df):
    colunas_numericas = [
        "br", "km", "pessoas", "mortos", "feridos", "feridos_leves",
        "feridos_graves", "ilesos", "ignorados", "veiculos"
    ]
    for coluna in colunas_numericas:
        if coluna in df.columns:
            df[coluna] = pd.to_numeric(df[coluna], errors="coerce")
    print(df[[c for c in colunas_numericas if c in df.columns]].dtypes)
    return df


def etapa16_variaveis_temporais(df):
    df["data_inversa"] = pd.to_datetime(df["data_inversa"], errors="coerce")
    df["ano"] = df["data_inversa"].dt.year
    df["mes"] = df["data_inversa"].dt.month
    df["trimestre"] = df["data_inversa"].dt.quarter
    df["dia_semana_num"] = df["data_inversa"].dt.dayofweek
    df["fim_de_semana"] = df["dia_semana_num"].isin([5, 6]).astype(int)
    print(df[["data_inversa", "ano", "mes", "trimestre",
              "dia_semana_num", "fim_de_semana"]].head())
    return df


def classificar_turno(hora):
    if pd.isna(hora):
        return "IGNORADO"
    if 0 <= hora <= 5:
        return "MADRUGADA"
    if 6 <= hora <= 11:
        return "MANHA"
    if 12 <= hora <= 17:
        return "TARDE"
    return "NOITE"


def etapa17_horario_e_turno(df):
    horario_limpo = df["horario"].astype(str).str.strip()
    df["hora"] = pd.to_datetime(horario_limpo, format="%H:%M:%S", errors="coerce").dt.hour

    faltou_hora = df["hora"].isna()
    if faltou_hora.any():
        df.loc[faltou_hora, "hora"] = pd.to_datetime(
            horario_limpo[faltou_hora], format="%H:%M", errors="coerce"
        ).dt.hour

    df["turno"] = df["hora"].apply(classificar_turno)
    print(df[["horario", "hora", "turno"]].head())
    return df


def criar_faixa_horaria(hora):
    if pd.isna(hora):
        return "IGNORADO"
    inicio = int(hora // 3) * 3
    fim = inicio + 2
    return f"{inicio:02d}h-{fim:02d}h"


def etapa18_faixa_horaria(df):
    df["faixa_horaria"] = df["hora"].apply(criar_faixa_horaria)
    print(df["faixa_horaria"].value_counts(dropna=False).sort_index())
    return df


def etapa19_padronizar_textos(df):
    colunas_texto = df.select_dtypes(include="object").columns
    for coluna in colunas_texto:
        df[coluna] = (
            df[coluna]
            .astype("string")
            .str.strip()
            .str.upper()
        )
        df[coluna] = df[coluna].replace(
            {"": pd.NA, "NAN": pd.NA, "NONE": pd.NA, "NULL": pd.NA}
        )
    print("Colunas textuais padronizadas:", len(colunas_texto))
    return df


def etapa20_nulos_categoricos(df):
    categoricas_importantes = [
        "uf", "municipio", "causa_acidente", "tipo_acidente", "fase_dia",
        "condicao_metereologica", "tipo_pista", "tracado_via", "uso_solo",
        "classificacao_acidente", "dia_semana"
    ]
    for coluna in categoricas_importantes:
        if coluna in df.columns:
            df[coluna] = df[coluna].fillna("IGNORADO")
    print(df[categoricas_importantes].isna().sum().sort_values(ascending=False))
    return df


def etapa21_nulos_numericos(df):
    contagens_vitimas = ["mortos", "feridos", "feridos_leves",
                          "feridos_graves", "pessoas", "veiculos"]
    for coluna in contagens_vitimas:
        if coluna in df.columns:
            df[coluna] = df[coluna].fillna(0)
    print(df[[c for c in contagens_vitimas if c in df.columns]].isna().sum())
    return df

# bloco 5. variável-alvo e indicadores de gravidade

def etapa22_criar_alvo(df):
    df["acidente_fatal"] = np.where(df["mortos"] >= 1, 1, 0)
    validacao_alvo = (
        df["acidente_fatal"].value_counts(dropna=False)
        .rename_axis("acidente_fatal")
        .reset_index(name="qtd")
    )
    validacao_alvo["perc"] = validacao_alvo["qtd"] / validacao_alvo["qtd"].sum() * 100
    print(validacao_alvo)
    return df


def etapa23_validar_alvo(df):
    violacoes = df.loc[
        ((df["mortos"] >= 1) & (df["acidente_fatal"] != 1)) |
        ((df["mortos"] == 0) & (df["acidente_fatal"] != 0))
    ]
    print("Violações da regra do alvo:", len(violacoes))
    assert len(violacoes) == 0, "Há erro na criação de acidente_fatal."


def etapa24_indicadores_gravidade(df):
    df["total_vitimas"] = df["mortos"] + df["feridos_leves"] + df["feridos_graves"]
    df["acidente_grave"] = np.where(
        (df["mortos"] >= 1) | (df["feridos_graves"] >= 1), 1, 0
    )
    df["indice_gravidade"] = (
        df["mortos"] * 3 + df["feridos_graves"] * 2 + df["feridos_leves"]
    )
    print(df[["mortos", "feridos_leves", "feridos_graves",
              "total_vitimas", "indice_gravidade"]].head())
    return df


def formatar_br(valor):
    if pd.isna(valor) or valor == 0:
        return "BR-IGNORADA"
    return f"BR-{int(valor):03d}"


def etapa25_br_e_chave_localidade(df):
    df["br_formatada"] = df["br"].apply(formatar_br)
    df["chave_localidade"] = (
        df["uf"].astype(str) + "_" +
        df["municipio"].astype(str) + "_" +
        df["br_formatada"].astype(str)
    )
    print(df[["uf", "municipio", "br", "br_formatada", "chave_localidade"]].head())
    return df


def etapa26_checagens_rapidas(df):
    checagens = {
        "linhas": len(df),
        "colunas": df.shape[1],
        "acidentes_fatais": int(df["acidente_fatal"].sum()),
        "taxa_fatalidade": float(df["acidente_fatal"].mean()),
        "total_mortos": int(df["mortos"].sum()),
        "total_feridos": int(df["feridos"].sum()) if "feridos" in df.columns else None,
    }
    print(checagens)
    return checagens


def ranking_categoria(base, coluna, n=10):
    return (
        base[coluna]
        .value_counts(dropna=False)
        .head(n)
        .rename_axis(coluna)
        .reset_index(name="qtd")
    )


def etapa27_ranking_categorias(df):
    print(ranking_categoria(df, "causa_acidente", 10))
    print(ranking_categoria(df, "tipo_acidente", 10))


def taxa_fatal_por_categoria(base, coluna, min_registros=30):
    tab = base.groupby(coluna).agg(
        qtd_acidentes=("acidente_fatal", "size"),
        qtd_fatais=("acidente_fatal", "sum"),
        taxa_fatal=("acidente_fatal", "mean")
    ).reset_index()
    tab = tab[tab["qtd_acidentes"] >= min_registros]
    return tab.sort_values("taxa_fatal", ascending=False)


def etapa28_taxa_fatal_categoria(df):
    print(taxa_fatal_por_categoria(df, "tipo_acidente", min_registros=30).head(10))


def etapa29_grafico_alvo(df):
    """Gráfico salvo em relatorios/ (adaptação: sem exibição inline de notebook)."""
    ax = df["acidente_fatal"].value_counts().sort_index().plot(kind="bar")
    ax.set_title("Distribuição da variável-alvo acidente_fatal")
    ax.set_xlabel("acidente_fatal")
    ax.set_ylabel("Quantidade de acidentes")
    plt.tight_layout()
    plt.savefig(ARQUIVO_GRAFICO_ALVO)
    print("Gráfico salvo em:", ARQUIVO_GRAFICO_ALVO)
    plt.show()

# bloco 6. construção das duas bases (analítica e modelável)

def etapa31_base_analitica(df):
    base_analitica = df.copy()
    print("Base analítica:", base_analitica.shape)
    print("Colunas:", base_analitica.columns.tolist())
    return base_analitica


def etapa33_base_modelavel(df):
    variaveis_modelaveis = [
        "uf", "br_formatada", "municipio", "mes", "trimestre",
        "dia_semana", "dia_semana_num", "fim_de_semana",
        "hora", "faixa_horaria", "turno", "fase_dia",
        "causa_acidente", "tipo_acidente", "condicao_metereologica",
        "tipo_pista", "tracado_via", "uso_solo",
        "acidente_fatal"
    ]
    variaveis_modelaveis = [c for c in variaveis_modelaveis if c in df.columns]
    base_modelavel = df[variaveis_modelaveis].copy()
    print("Base modelável:", base_modelavel.shape)
    return base_modelavel


def etapa34_verificar_data_leakage(base_modelavel):
    variaveis_proibidas = [
        "mortos", "feridos", "feridos_leves", "feridos_graves",
        "total_vitimas", "indice_gravidade", "acidente_grave",
        "classificacao_acidente"
    ]
    presentes = [c for c in variaveis_proibidas if c in base_modelavel.columns]
    if presentes:
        raise ValueError(f"Data leakage detectado: {presentes}")
    print("OK — nenhuma variável proibida encontrada.")


def etapa35_tratar_nulos_modelavel(base_modelavel):
    for coluna in base_modelavel.columns:
        if coluna == "acidente_fatal":
            continue
        if base_modelavel[coluna].dtype == "object" or str(base_modelavel[coluna].dtype) == "string":
            base_modelavel[coluna] = base_modelavel[coluna].fillna("IGNORADO")
        else:
            base_modelavel[coluna] = base_modelavel[coluna].fillna(-1)
    print(base_modelavel.isna().sum().sort_values(ascending=False).head())
    return base_modelavel


def etapa36_exportar_bases(base_analitica, base_modelavel):
    base_analitica.to_csv(
        ARQUIVO_BASE_ANALITICA, index=False, sep=SEPARADOR, encoding=ENCODING_SAIDA
    )
    base_modelavel.to_csv(
        ARQUIVO_BASE_MODELAVEL, index=False, sep=SEPARADOR, encoding=ENCODING_SAIDA
    )
    print("Arquivos exportados:")
    print("-", ARQUIVO_BASE_ANALITICA)
    print("-", ARQUIVO_BASE_MODELAVEL)


def etapa37_reabrir_e_validar(base_analitica, base_modelavel):
    valid_analitica = pd.read_csv(ARQUIVO_BASE_ANALITICA, sep=SEPARADOR, encoding=ENCODING_SAIDA)
    valid_modelavel = pd.read_csv(ARQUIVO_BASE_MODELAVEL, sep=SEPARADOR, encoding=ENCODING_SAIDA)
    print("Analítica reaberta:", valid_analitica.shape)
    print("Modelável reaberta:", valid_modelavel.shape)
    assert len(valid_analitica) == len(base_analitica)
    assert len(valid_modelavel) == len(base_modelavel)

# bloco 7. documentação do projeto

def etapa38_dicionario_variaveis():
    linhas_dic = [
        {"variavel": "acidente_fatal",
         "descricao": "1 se mortos >= 1; 0 se mortos = 0", "uso": "alvo"},
        {"variavel": "total_vitimas",
         "descricao": "mortos + feridos leves + feridos graves", "uso": "analise/dashboard"},
        {"variavel": "indice_gravidade",
         "descricao": "mortos*3 + feridos_graves*2 + feridos_leves", "uso": "analise/dashboard"},
        {"variavel": "br_formatada",
         "descricao": "BR padronizada no formato BR-000", "uso": "analise/modelagem"},
        {"variavel": "chave_localidade",
         "descricao": "UF + município + BR formatada", "uso": "analise/dashboard"},
    ]
    dicionario = pd.DataFrame(linhas_dic)
    dicionario.to_csv(ARQUIVO_DICIONARIO, index=False, sep=SEPARADOR, encoding=ENCODING_SAIDA)
    print(dicionario)


def etapa39_registrar_decisoes():
    texto_decisoes = f"""

Data de geração: {datetime.now().strftime('%Y-%m-%d %H:%M')}

- {ARQUIVO_BASE_ANALITICA}
- {ARQUIVO_BASE_MODELAVEL}
- {ARQUIVO_DICIONARIO}
"""
    ARQUIVO_DECISOES.write_text(texto_decisoes, encoding="utf-8")
    print("Arquivo de decisões salvo em:", ARQUIVO_DECISOES)

def etapa40_criar_readme():
    readme = f"""

- `{ARQUIVO_BASE_ANALITICA}`: base completa para EDA e Power BI.
- `{ARQUIVO_BASE_MODELAVEL}`: base para modelagem, sem data leakage.

"""
    ARQUIVO_README.write_text(readme, encoding="utf-8")
    print("README criado:", ARQUIVO_README)

def etapa41_resumo_final(base_analitica, base_modelavel):
    resumo_final = pd.DataFrame([
        {"item": "linhas_base_analitica", "valor": len(base_analitica)},
        {"item": "colunas_base_analitica", "valor": base_analitica.shape[1]},
        {"item": "linhas_base_modelavel", "valor": len(base_modelavel)},
        {"item": "colunas_base_modelavel", "valor": base_modelavel.shape[1]},
        {"item": "taxa_global_acidente_fatal", "valor": base_modelavel["acidente_fatal"].mean()},
    ])
    print(resumo_final)

# substituição- execução "célula por célula" do notebook.

def main():
    print("\nBloco 1. Ambiente")
    etapa5_criar_pastas()

    print("\nBloco 2. Leitura e primeira inspeção")
    df = ler_csv_prf(ARQUIVO_BRUTO, sep=SEPARADOR)
    print(df.head())
    df = etapa8_padronizar_colunas(df)
    etapa9_conferir_colunas_esperadas(df)
    etapa10_retrato_inicial(df)

    print("\nBloco 3. Diagnóstico de qualidade")
    etapa11_tipos_e_memoria(df)
    etapa12_diagnostico_nulos(df)
    df = etapa13_remover_duplicidades(df)
    etapa14_cardinalidade(df)

    print("\nBloco 4. Transformações e variáveis derivadas")
    df = etapa15_converter_numericas(df)
    df = etapa16_variaveis_temporais(df)
    df = etapa17_horario_e_turno(df)
    df = etapa18_faixa_horaria(df)
    df = etapa19_padronizar_textos(df)
    df = etapa20_nulos_categoricos(df)
    df = etapa21_nulos_numericos(df)

    print("\nBloco 5. Variável-alvo e indicadores de gravidade")
    df = etapa22_criar_alvo(df)
    etapa23_validar_alvo(df)
    df = etapa24_indicadores_gravidade(df)
    df = etapa25_br_e_chave_localidade(df)
    etapa26_checagens_rapidas(df)
    etapa27_ranking_categorias(df)
    etapa28_taxa_fatal_categoria(df)
    etapa29_grafico_alvo(df)

    print("\nBloco 6. Bases finais -> analítica e modelável")
    base_analitica = etapa31_base_analitica(df)
    base_modelavel = etapa33_base_modelavel(df)
    etapa34_verificar_data_leakage(base_modelavel)
    base_modelavel = etapa35_tratar_nulos_modelavel(base_modelavel)
    etapa36_exportar_bases(base_analitica, base_modelavel)
    etapa37_reabrir_e_validar(base_analitica, base_modelavel)

    print("\n Bloco 7. Documentação do projeto")
    etapa38_dicionario_variaveis()
    etapa39_registrar_decisoes()
    etapa40_criar_readme()
    etapa41_resumo_final(base_analitica, base_modelavel)

    print("\n Concluído com sucesso.")


if __name__ == "__main__":
    main()