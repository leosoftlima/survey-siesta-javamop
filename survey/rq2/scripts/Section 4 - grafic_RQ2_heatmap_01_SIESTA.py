import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Caminho para o CSV fornecido
csv_path = r"../rq2/data/respostas_RQ2_Faster.csv"
df = pd.read_csv(csv_path)

# Normalizar os nomes das colunas
df.columns = df.columns.str.replace('\n', ' ', regex=False).str.replace(r'\s+', ' ', regex=True).str.strip()

# Detectar a coluna de experiência profissional
exp_col = [col for col in df.columns if "experience" in col.lower()][0]

# Definir a ordem desejada dos grupos de experiência
ordered_experience = [
    'More than 10 years',
    '7 - 10 years',
    '4 - 6 years',
    '1 - 3 years',
    'Less than 1 year'
]

# Inicializar estrutura de contagem
experience_groups = df[exp_col].dropna().unique()
scenarios = list(range(1, 12))
votes = {group: {f"Scenario {i}": {"JavaMOP": 0, "MSL": 0} for i in scenarios} for group in experience_groups}

# Preencher estrutura de contagem
for _, row in df.iterrows():
    group = row[exp_col]
    for i in scenarios:
        col = f"{i}.2_faster"
        if col in df.columns and pd.notna(row[col]):
            answer = row[col].strip()
            if answer in ["JavaMOP", "MSL"]:
                votes[group][f"Scenario {i}"][answer] += 1

# Calcular percentuais de MSL por cenário e grupo
heatmap_data = pd.DataFrame(index=experience_groups, columns=[f"Scenario {i}" for i in scenarios])

for group in experience_groups:
    for i in scenarios:
        total = votes[group][f"Scenario {i}"]["JavaMOP"] + votes[group][f"Scenario {i}"]["MSL"]
        if total > 0:
            msl_percent = votes[group][f"Scenario {i}"]["MSL"] / total * 100
        else:
            msl_percent = np.nan
        heatmap_data.loc[group, f"Scenario {i}"] = msl_percent

# Reordenar os grupos de experiência
heatmap_data = heatmap_data.reindex(ordered_experience)

# Plotar heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(
    heatmap_data.astype(float),
    annot=True,
    fmt=".1f",
    cmap="YlOrRd",
    cbar_kws={'label': '% SIESTA'},
    linewidths=0.5
)
#plt.title("Perceived Efficiency (Faster) – % de votos MSL por Cenário e Experiência")
plt.xlabel("Scenarios")
plt.ylabel("Professional Experience Group")
plt.tight_layout()
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.show()
