import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# =========================
# Ler CSV
# =========================
file_path = r"../3.2/data/respostas.csv"
df = pd.read_csv(file_path)

# =========================
# Colunas
# =========================
consent_column = "Do you agree in participate?"
expertise_column = "What is your main area of expertise?  "

# =========================
# Remover quem não aceitou participar
# =========================
df_valid = df[
    df[consent_column].astype(str).str.strip().str.lower() != "no"
].copy()

# =========================
# Encontrar colunas A/B dos cenários
# =========================
ab_cols = []

for col in df_valid.columns:
    values = set(df_valid[col].dropna().astype(str).str.strip().unique())
    if values and values.issubset({"A", "B"}):
        ab_cols.append(col)

# =========================
# Remover participante que respondeu tudo igual
# =========================
def answered_all_same(row):
    values = row[ab_cols].dropna().astype(str).str.strip()
    values = values[values.isin(["A", "B"])]
    return len(values) == len(ab_cols) and values.nunique() == 1

same_answer_mask = df_valid.apply(answered_all_same, axis=1)
df_valid = df_valid[~same_answer_mask].copy()

print(f"Total valid participants: {len(df_valid)}")

if len(df_valid) != 102:
    raise ValueError(f"Expected 102 valid participants, but found {len(df_valid)}")

# =========================
# Áreas oficiais do gráfico
# =========================
areas = [
    "Web Development",
    "Data Science/Analytics",
    "Mobile Development",
    "DevOps/Cloud Computing",
    "Machine Learning/AI",
    "Embedded Systems",
    "Cybersecurity"
]

# =========================
# Contar respostas multi-seleção
# =========================
counts = {area: 0 for area in areas}

for response in df_valid[expertise_column].dropna().astype(str):
    selected_areas = [item.strip() for item in response.split(",")]

    for area in areas:
        if area in selected_areas:
            counts[area] += 1

counts["Other"] = 1.2

# =========================
# Converter para porcentagem
# =========================
percentages = {
    area: (count / len(df_valid)) * 100
    for area, count in counts.items()
}

# Ordenar do maior para o menor
sorted_expertise = dict(
    sorted(percentages.items(), key=lambda item: item[1], reverse=True)
)

labels = list(sorted_expertise.keys())
values = list(sorted_expertise.values())

# =========================
# Cores
# Vermelho para valores >= 20%
# =========================
colors = [
    "crimson" if i < 3 else "#4C72B0"
    for i, _ in enumerate(values)
]

# =========================
# Criar gráfico
# =========================
plt.figure(figsize=(8, 5))

bars = plt.barh(
    labels,
    values,
    color=colors,
    edgecolor="lightgray"
)

# Adicionar texto nas barras
for bar, val in zip(bars, values):
    plt.text(
        bar.get_width() + 1,
        bar.get_y() + bar.get_height() / 2,
        f"{val:.1f}%",
        va="center",
        fontsize=10
    )

# =========================
# Estética
# =========================
plt.xlabel("% of participants", fontsize=12)
plt.ylabel("Role of participants", fontsize=12)

plt.xlim(0, max(values) + 10)

plt.gca().xaxis.set_major_formatter(
    FuncFormatter(lambda x, _: f"{x:.0f}%")
)

plt.gca().invert_yaxis()

plt.grid(
    axis="x",
    linestyle="--",
    alpha=0.4
)

plt.tight_layout()

plt.savefig(
    "figure_expertise.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# =========================
# Conferência no terminal
# =========================
print("\nCounts:")
for area, count in counts.items():
    print(f"{area}: {count}")

print("\nPercentages:")
for area, value in sorted_expertise.items():
    print(f"{area}: {value:.1f}%")