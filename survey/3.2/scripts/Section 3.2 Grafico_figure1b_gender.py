import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# Dados de gênero
gender_labels = ["Male", "Female", "Non-binary", "Prefer not to say"]
gender_values = [82.4, 13.7, 1.0, 2.9]

# Cor padrão
bar_color = "#4682B4"

# Criar gráfico
fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(gender_labels, gender_values, color=bar_color, edgecolor="lightgray")

# Título e eixo Y
#ax.set_title("Gender distribution among participants", fontsize=13)
ax.set_ylabel("% Participants", fontsize=11)
ax.set_ylim(0, 90)
ax.yaxis.set_major_formatter(PercentFormatter())  # Eixo Y com símbolo de %

# Eixo X sem rotação
plt.xticks(rotation=0, fontsize=10)
ax.yaxis.grid(True, linestyle='--', linewidth=0.6, color='lightgray')
ax.set_axisbelow(True)

# Adicionar valores sobre as barras
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height}%', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points",
                ha='center', va='bottom', fontsize=9)

plt.tight_layout()
# plt.savefig("C:/Users/leona/Downloads/expermentSurvey/figure1b_gender.png", dpi=300)
plt.show()
