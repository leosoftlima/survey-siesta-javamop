import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Caminho local do CSV
csv_path = r"C:\Users\leona\Downloads\expermentSurvey\RQ3\respostas_RQ3_detailAndRigorNew.csv"

# === 1) Ler dados ===
rq3 = pd.read_csv(csv_path)

# Colunas de rigor
rigor_cols = [c for c in rq3.columns if ".3_detailed" in c]

# Long format
rigor_long = rq3.melt(
    id_vars=[
        "pID",
        "Which programming languages do you regularly use?",
        "What is your main area of expertise?"
    ],
    value_vars=rigor_cols,
    var_name="Scenario",
    value_name="ChosenRigor"
).dropna()

rigor_long.rename(columns={
    "Which programming languages do you regularly use?": "DevLang"
}, inplace=True)

# Linguagens‐alvo
target_langs = ["Java", "Python", "JavaScript/TypeScript"]

# === 2) Calcular percentuais ===
summary = (
    rigor_long[rigor_long["DevLang"].isin(target_langs)]
    .groupby(["DevLang", "ChosenRigor"]).size()
    .unstack(fill_value=0)
)
percent = summary.div(summary.sum(axis=1), axis=0) * 100
percent = percent.reindex(target_langs)

# === 3) Gerar comandos LaTeX ===
latex_cmds = []
for lang in percent.index:
    lang_clean = lang.replace("/", "").replace(" ", "")
    latex_cmds.append(f"\\newcommand{{\\percRigorJavaMOP{lang_clean}}}{{{int(round(percent.loc[lang,'JavaMOP']))}}}")
    latex_cmds.append(f"\\newcommand{{\\percRigorMSL{lang_clean}}}{{{int(round(percent.loc[lang,'MSL']))}}}")

print("===== Variáveis LaTeX para Overleaf =====")
print("\n".join(latex_cmds))
print()

# === 4) Plotar radar (0–80 %) ===
categories = percent.index.tolist()
labels = ["MSL", "JavaMOP"]
display_labels = {"MSL": "SIESTA", "JavaMOP": "JavaMOP"}
colors = {
    "MSL": "#1f77b4",       # Azul para SIESTA (MSL)
    "JavaMOP": "#ff7f0e"    # Laranja para JavaMOP
}
angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
for lab in labels:
    vals = percent[lab].tolist() + [percent[lab].tolist()[0]]
    ax.plot(angles, vals, label=display_labels[lab], color=colors[lab])
    ax.fill(angles, vals, alpha=0.25, color=colors[lab])

#for idx, lab in enumerate(labels):
#    vals = percent[lab].tolist() + [percent[lab].tolist()[0]]
#    ax.plot(angles, vals, label=lab, color=colors[idx])
#    ax.fill(angles, vals, alpha=0.25, color=colors[idx])

ax.set_thetagrids(np.degrees(angles[:-1]), categories, fontsize=12)
#ax.set_title("Perceived Rigor (JavaMOP vs. MSL) by Developer Language")
ax.set_ylim(0, 80)        # Raio 0–80 %
ax.grid(linewidth=0.8)
ax.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))

plt.tight_layout()
plt.show()
