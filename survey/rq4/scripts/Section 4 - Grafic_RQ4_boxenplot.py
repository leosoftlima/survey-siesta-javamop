import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Caminho local do seu arquivo CSV
file_path = r"../rq4/data/respostas_RQ4_Sintaxe.csv"
df = pd.read_csv(file_path)

# Selecionar as colunas que terminam com "_simpler"
simpler_cols = [col for col in df.columns if col.endswith("_simpler")]

# Transformar os dados para formato longo
df_long = df.melt(
    id_vars=["pID"],
    value_vars=simpler_cols,
    var_name="scenario",
    value_name="chosen_spec"
)

# Extrair o número do cenário
df_long["scenario"] = df_long["scenario"].str.extract(r"(\d+)\.4_simpler").astype(int)

# Renomear MSL para SIESTA
df_long["chosen_spec"] = df_long["chosen_spec"].replace({"MSL": "SIESTA"})

# Calcular porcentagem cumulativa por cenário e linguagem
df_long["total_in_scenario"] = df_long.groupby("scenario")["pID"].transform("count")

df_long["percentage"] = (
    (df_long.groupby(["scenario", "chosen_spec"]).cumcount() + 1)
    / df_long["total_in_scenario"]
    * 100
)

# ---------- Gerar o gráfico boxenplot ----------

plt.figure(figsize=(12, 6))
sns.set(style="whitegrid")

sns.boxenplot(
    data=df_long,
    x="percentage",
    y="scenario",
    hue="chosen_spec",
    hue_order=["SIESTA", "JavaMOP"],
    palette={
        "SIESTA": "#1f77b4",
        "JavaMOP": "#B8B8B8"
    },
    orient="h",
    dodge=True
)

plt.xticks(
    [0, 20, 40, 60, 80, 100],
    ["0", "20%", "40%", "60%", "80%", "100%"]
)

plt.xlabel("% of Participants")
plt.ylabel("Scenario")
plt.legend(title="Language")
plt.tight_layout()
plt.show()

# ---------- Geração dos comandos LaTeX ----------

# Cenários e linguagens que você deseja exportar
cenarios_desejados = [1, 2, 4, 5, 6, 9, 10]
linguagens_desejadas = ["JavaMOP", "SIESTA"]

# Função para converter número para texto em inglês
def numero_para_texto(n):
    mapa = {
        1: "One",
        2: "Two",
        3: "Three",
        4: "Four",
        5: "Five",
        6: "Six",
        7: "Seven",
        8: "Eight",
        9: "Nine",
        10: "Ten",
        11: "Eleven"
    }
    return mapa.get(n, str(n))

# Gerar comandos apenas de média com cenário por extenso
def gerar_comandos_medias_texto(df):
    resumo = df.groupby(["scenario", "chosen_spec"])["percentage"].describe().reset_index()
    comandos = []

    for _, row in resumo.iterrows():
        cenario = int(row["scenario"])
        linguagem = row["chosen_spec"].replace(" ", "").replace("-", "")

        if cenario in cenarios_desejados and linguagem in linguagens_desejadas:
            nome_cenario = numero_para_texto(cenario)
            media = round(row["mean"], 1)

            comandos.append(
                f"\\newcommand{{\\cenario{nome_cenario}{linguagem}Mean}}{{{media}}}"
            )

    return "\n".join(sorted(comandos))

# Exibir os comandos LaTeX
print("\nComandos LaTeX:\n")
print(gerar_comandos_medias_texto(df_long))