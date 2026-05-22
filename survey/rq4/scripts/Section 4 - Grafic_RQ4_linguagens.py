import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === 1. Carregar e preparar os dados ===
file_path = r"../rq4/data/respostas_RQ4_Sintaxe.csv"
df = pd.read_csv(file_path)

syntax_cols = [col for col in df.columns if col.endswith("_simpler")]
df['MSL_votes'] = (df[syntax_cols] == 'MSL').sum(axis=1)
df['JavaMOP_votes'] = (df[syntax_cols] == 'JavaMOP').sum(axis=1)

def agrupar_linguagens(langs):
    langs = str(langs).lower()
    grupos = []
    if 'java' in langs:
        grupos.append('Java')
    if 'python' in langs:
        grupos.append('Python')
    if 'javascript' in langs or 'typescript' in langs:
        grupos.append('JavaScript/TypeScript')
    return grupos if grupos else ['Other']

df['LangGroup'] = df['Which programming languages do you regularly use?'].apply(agrupar_linguagens)
df_exploded = df.explode('LangGroup')
df_filtrado = df_exploded[df_exploded['LangGroup'].isin(['Java', 'Python', 'JavaScript/TypeScript'])]

agrupado = df_filtrado.groupby('LangGroup').agg(
    msl_votes=('MSL_votes', 'sum'),
    javamop_votes=('JavaMOP_votes', 'sum'),
    participantes=('MSL_votes', 'count')
).reset_index()

agrupado['MSL'] = (agrupado['msl_votes'] / (agrupado['participantes'] * 11) * 100)
agrupado['JavaMOP'] = (agrupado['javamop_votes'] / (agrupado['participantes'] * 11) * 100)

# === 2. Gerar gráfico empilhado ===
labels = agrupado["LangGroup"]
msl_vals = agrupado["MSL"]
javamop_vals = agrupado["JavaMOP"]
x = np.arange(len(labels))
width = 0.6

fig, ax = plt.subplots(figsize=(8, 5))
color_javamop = '#7A7A7A'   # cinza mais elegante
color_siesta = '#4C78A8'    # azul acadêmico mais suave

ax.bar(x, javamop_vals, width, label='JavaMOP', color=color_javamop)
ax.bar(x, msl_vals, width, bottom=javamop_vals, label='SIESTA', color=color_siesta)

plt.tight_layout(rect=[0, 0, 1, 0.93])
# Adicionar rótulos com fonte maior
for i in range(len(x)):
    ax.text(x[i], javamop_vals[i] / 2, f'{javamop_vals[i]:.2f}%', ha='center', va='center', color='white', fontsize=10)
    ax.text(x[i], javamop_vals[i] + msl_vals[i] / 2, f'{msl_vals[i]:.2f}%', ha='center', va='center', color='white', fontsize=10)

ax.set_ylabel('% Participants')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylim(0, 100)

ax.legend(
    loc='upper left',
    bbox_to_anchor=(1.02, 1.0),
    frameon=True,
    edgecolor='lightgray'
)

plt.tight_layout(rect=[0, 0, 0.99, 1])
plt.show()

# === 3. Gerar comandos LaTeX com precisão ===
def gerar_comandos_latex_preciso(agrupado):
    comandos = ""
    for _, row in agrupado.iterrows():
        lang = row['LangGroup'].replace("/", "").replace(" ", "")
        comandos += f"\\newcommand{{\\mslPct{lang}}}{{{row['MSL']:.2f}}}\n"
        comandos += f"\\newcommand{{\\javamopPct{lang}}}{{{row['JavaMOP']:.2f}}}\n"
        comandos += f"\\newcommand{{\\mslVotes{lang}}}{{{int(row['msl_votes'])}}}\n"
        comandos += f"\\newcommand{{\\javamopVotes{lang}}}{{{int(row['javamop_votes'])}}}\n"
        comandos += f"\\newcommand{{\\numParticipants{lang}}}{{{int(row['participantes'])}}}\n"
    return comandos

# Exibir comandos LaTeX
print("===== Comandos LaTeX precisos para Overleaf =====")
print(gerar_comandos_latex_preciso(agrupado))
