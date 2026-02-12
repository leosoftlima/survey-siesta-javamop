import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Dados
labels = [
    "More than 10 years",
    "7–10 years",
    "4–6 years",
    "1–3 years",
    "Less than 1 year"
]
percentages = [40.2, 27.5, 11.8, 10.8, 9.8]
colors = ['steelblue'] * len(labels)  # Cor única para todas as barras

# Função para adicionar símbolo de porcentagem no eixo Y
def percent_formatter(x, _):
    return f'{x:.0f}%'

# Criar gráfico
plt.figure(figsize=(6, 4))
bars = plt.bar(labels, percentages, color=colors, edgecolor='lightgray')

# Texto nas barras
for bar, pct in zip(bars, percentages):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, f'{pct}%',
             ha='center', va='bottom', fontsize=10)

# Ajustes visuais
plt.ylabel("% Participants", fontsize=12)
plt.xticks(rotation=35, ha='right', rotation_mode='anchor', fontsize=10)
plt.ylim(0, 55)
#plt.title("Years of professional experience", fontsize=13)
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.gca().yaxis.set_major_formatter(FuncFormatter(percent_formatter))
plt.tight_layout()

# Salvar (descomente se quiser salvar)
# plt.savefig("C:/Users/leona/Downloads/expermentSurvey/figure1c_experience.png", dpi=300)

plt.show()
