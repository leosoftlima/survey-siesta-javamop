import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# =========================
# Ler CSV
# =========================
file_path = r"../3.2/data/respostas.csv"
df = pd.read_csv(file_path)

# =========================
# Encontrar coluna sobre RV
# =========================
rv_column = None

for col in df.columns:
    if "runtime verification tools" in col.lower():
        rv_column = col
        break

if rv_column is None:
    print("Coluna sobre RV não encontrada. Colunas disponíveis:")
    for col in df.columns:
        print(repr(col))
    raise ValueError("Não encontrei a coluna sobre runtime verification.")

# =========================
# Coluna de consentimento
# =========================
consent_column = "Do you agree in participate?"

# =========================
# Remover quem não aceitou participar
# =========================
df_valid = df[
    df[consent_column].astype(str).str.strip().str.lower() != "no"
].copy()

# =========================
# Encontrar colunas A/B dos 11 cenários
# =========================
ab_cols = []

for col in df_valid.columns:
    values = set(df_valid[col].dropna().astype(str).str.strip().unique())
    if values and values.issubset({"A", "B"}):
        ab_cols.append(col)

print(f"Colunas A/B encontradas: {len(ab_cols)}")

# =========================
# Remover participante que respondeu tudo igual
# =========================
def answered_all_same(row):
    values = row[ab_cols].dropna().astype(str).str.strip()
    values = values[values.isin(["A", "B"])]

    return len(values) == len(ab_cols) and values.nunique() == 1

same_answer_mask = df_valid.apply(answered_all_same, axis=1)

print(f"Participantes removidos por resposta uniforme: {same_answer_mask.sum()}")

df_valid = df_valid[~same_answer_mask].copy()

# =========================
# Conferir total final
# =========================
print(f"Total de participantes válidos: {len(df_valid)}")

if len(df_valid) != 102:
    raise ValueError(f"Esperado: 102 participantes válidos. Encontrado: {len(df_valid)}")

# =========================
# Padronizar respostas de familiaridade
# =========================
responses = df_valid[rv_column].dropna().astype(str).str.strip()

def normalize_response(value):
    value_lower = value.lower().strip()

    if value_lower == "yes":
        return "Yes"

    if value_lower == "no":
        return "No"

    if "heard" in value_lower:
        return "Heard about it"

    return "Other"

normalized = responses.apply(normalize_response)

# =========================
# Calcular contagens e porcentagens
# =========================
order = ["Yes", "No", "Heard about it"]

counts = normalized.value_counts()
counts = counts.reindex(order, fill_value=0)

percentages = (counts / len(df_valid)) * 100

labels = percentages.index.tolist()
values = percentages.values.tolist()

# =========================
# Conferência esperada
# =========================
print("\nCounts:")
print(counts)

print("\nPercentages:")
print(percentages.round(1))

print("\nTotal:")
print(counts.sum())

# =========================
# Cores
# =========================
color_map = {
    "Yes": "#1f77b4",
    "No": "#B8B8B8",
    "Heard about it": "#D2B48C"
}

colors = [color_map[label] for label in labels]

# =========================
# Formatar eixo Y com %
# =========================
def percent_formatter(x, _):
    return f"{x:.0f}%"

# =========================
# Criar gráfico
# =========================
plt.figure(figsize=(6, 4))

bars = plt.bar(
    labels,
    values,
    color=colors,
    edgecolor="lightgray"
)

for bar, val in zip(bars, values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        val + 1,
        f"{val:.1f}%",
        ha="center",
        va="bottom",
        fontsize=10
    )

plt.ylabel("% Participants", fontsize=12)
plt.ylim(0, 40)
plt.title("Familiarity with runtime verification tools", fontsize=13)

plt.grid(
    axis="y",
    linestyle="--",
    linewidth=0.6,
    color="lightgray"
)

plt.gca().yaxis.set_major_formatter(FuncFormatter(percent_formatter))

plt.tight_layout()

plt.savefig(
    "familiarity_bar_chart.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()