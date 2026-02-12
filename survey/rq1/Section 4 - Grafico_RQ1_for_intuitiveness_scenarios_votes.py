import pandas as pd
import matplotlib.pyplot as plt

# === Caminho do CSV ===
resumo_path = r"C:\Users\leona\Downloads\RQ1-20251201T184857Z-1-001\RQ1\resumo_cenarios_1_a_11_new.csv"
resumo_df = pd.read_csv(resumo_path)

# === Filtrar apenas a pergunta de intuitividade ===
intuitive_df = resumo_df[resumo_df["Question"].str.strip() == "Is more intuitive and understandable"]

# === Preparar gráfico ===
fig, ax = plt.subplots(figsize=(10, 6))
x = range(len(intuitive_df))
width = 0.35

# === Barras ===
java_bars = ax.bar([i - width/2 for i in x], intuitive_df["JavaMOP"], width, label="JavaMOP", color="#B8B8B8")
siesta_bars = ax.bar([i + width/2 for i in x], intuitive_df["MSL"], width, label="SIESTA", color="#1f77b4")

# === Rótulos no topo das barras (preto fixo) ===
for i, (j_bar, s_bar) in enumerate(zip(java_bars, siesta_bars)):
    ax.text(j_bar.get_x() + j_bar.get_width()/2, j_bar.get_height() + 1,
            str(intuitive_df["JavaMOP"].iloc[i]), ha='center', va='bottom', fontsize=9, color='black')
    ax.text(s_bar.get_x() + s_bar.get_width()/2, s_bar.get_height() + 1,
            str(intuitive_df["MSL"].iloc[i]), ha='center', va='bottom', fontsize=9, color='black')

# === Estilização ===
ax.set_ylabel("Number of Votes", fontsize=12)
ax.set_xlabel("Scenario", fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(intuitive_df["Scenario"], rotation=45, ha='right')
ax.set_ylim(0, max(intuitive_df[["JavaMOP", "MSL"]].max()) + 15)
ax.grid(axis='y', linestyle='--', alpha=0.6)

# ✅ Legenda centralizada dentro da área do gráfico
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0.95), ncol=2, frameon=True)

plt.tight_layout()
plt.show()
