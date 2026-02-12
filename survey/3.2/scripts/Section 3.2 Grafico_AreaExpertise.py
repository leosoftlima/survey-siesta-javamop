import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Dados organizados
expertise = {
    "Web Development": 73.5,
    "Data Science/Analytics": 23.5,
     "Mobile Development": 19.6,
    "DevOps/Cloud Computing": 15.7,   
    "Machine Learning/AI": 10.8,
    "Embedded Systems": 7.8,
    "Cybersecurity": 4.9,
    "Other": 1.2
}

# Ordenar do maior para o menor
sorted_expertise = dict(sorted(expertise.items(), key=lambda item: item[1], reverse=True))

labels = list(sorted_expertise.keys())
values = list(sorted_expertise.values())

# Cores: vermelho se >= 20%
colors = ['crimson' if v >= 19 else '#4C72B0' for v in values]

# Criar gráfico
plt.figure(figsize=(8, 5))
bars = plt.barh(labels, values, color=colors, edgecolor='lightgray')

# Adicionar texto nas barras
for bar, val in zip(bars, values):
    plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
             f"{val:.1f}%", va='center', fontsize=10)

# Estética
plt.xlabel("% of participants", fontsize=12)
plt.ylabel("Role of participants", fontsize=12)
#plt.title("Main area of expertise", fontsize=13)
plt.xlim(0, max(values) + 10)
plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.0f}%"))  # eixo com %
plt.gca().invert_yaxis()
plt.grid(axis='x', linestyle='--', alpha=0.4)
plt.tight_layout()

# Salvar se desejar
# plt.savefig("figure2_expertise.png", dpi=300)

plt.show()
