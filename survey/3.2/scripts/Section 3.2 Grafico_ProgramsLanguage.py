import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Dados atualizados
languages = [
    "Java", "Python", "JavaScript/TypeScript", "C#", "C/C++", "PHP", "Kotlin", "Go", "Dart",
     "Swift", "Others"
]
percentages = [
    61.8, 50.0, 42.2, 11.8, 10.8, 7.8, 6.9, 6.9, 3.9,
     2.9, 1.0
]

# Cores: top 3 em vermelho, o restante em azul
colors = ['crimson' if i < 3 else 'steelblue' for i in range(len(languages))]

# Plot
plt.figure(figsize=(8, 6))
bars = plt.barh(languages, percentages, color=colors)
plt.ylabel('Programming Language')
plt.xlabel('% of participants')
#plt.title('Programming languages regularly used')

# Adicionar os valores ao lado das barras
for bar, pct in zip(bars, percentages):
    plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
             f'{pct}%', va='center', fontsize=9)

plt.gca().invert_yaxis()
plt.grid(axis='x', linestyle='--', alpha=0.4)

# Formatar o eixo X com símbolo %
plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.0f}%'))
plt.xlim(0, 80)

plt.tight_layout()
plt.show()
