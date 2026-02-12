import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Dados
labels = ['Yes', 'No', 'Heard about it']
values = [35.3, 31.4, 33.3]
colors = ['#4682B4', '#A9A9A9', '#D2B48C']

# Formato do eixo Y com %
def percent_formatter(x, _):
    return f'{x:.0f}%'

# Criar gráfico
plt.figure(figsize=(6, 4))
bars = plt.bar(labels, values, color=colors, edgecolor='lightgray')

# Adicionar valores sobre as barras
for bar, val in zip(bars, values):
    plt.text(bar.get_x() + bar.get_width() / 2, val + 1, f'{val}%', 
             ha='center', va='bottom', fontsize=10)

# Estilo dos eixos
plt.ylabel('% Participants', fontsize=12)
plt.ylim(0, 40)
plt.title('Familiarity with runtime verification tools', fontsize=13)

# Linhas tracejadas horizontais com mais contraste
plt.grid(axis='y', linestyle='--', linewidth=0.6, color='lightgray')
plt.gca().yaxis.set_major_formatter(FuncFormatter(percent_formatter))

plt.tight_layout()
# Salvar se necessário
# plt.savefig("C:/Users/leona/Downloads/expermentSurvey/familiarity_bar_chart.png", dpi=300)
plt.show()
