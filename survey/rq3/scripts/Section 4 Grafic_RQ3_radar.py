import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === Função para gerar comandos LaTeX do radar ===
def gerar_comandos_latex(radar_data, dimensoes):
    comandos = ""
    for i, dim in enumerate(dimensoes):
        msl_percent = int(round(radar_data['MSL'][i]))
        javamop_percent = int(round(radar_data['JavaMOP'][i]))
        comandos += f"\\newcommand{{\\perc{dim}MSL}}{{{msl_percent}}}\n"
        comandos += f"\\newcommand{{\\perc{dim}JavaMOP}}{{{javamop_percent}}}\n"
    return comandos

# === Função para gerar comandos LaTeX do padrão de trade-off ===
def gerar_comandos_latex_tradeoff(consolidated):
    total = consolidated['pID'].nunique()
    grouped = consolidated.groupby('pID')

    tradeoff_count = 0
    for _, group in grouped:
        if len(group) == 0:
            continue

        pct_int = (group['Intuitiveness'] == "MSL").mean()
        pct_eff = (group['Efficiency'] == "MSL").mean()
        pct_rig = (group['Rigor'] == "JavaMOP").mean()

        if pct_int >= 0.6 and pct_eff >= 0.6 and pct_rig >= 0.6:
            tradeoff_count += 1

    percent = round((tradeoff_count / total) * 100, 1) if total > 0 else 0

    comandos = f"""% Trade-off pattern stats
\\newcommand{{\\tradeoffTotalParticipants}}{{{total}}}
\\newcommand{{\\tradeoffMatchingParticipants}}{{{tradeoff_count}}}
\\newcommand{{\\tradeoffMatchingPercent}}{{{percent}}}
"""
    return comandos

# === Leitura dos dados
rq1_data = pd.read_csv(r"C:\Users\leona\Downloads\expermentSurvey\RQ3\respostas_rq1intuitiveAgeNew.csv")
rq2_data = pd.read_csv(r"C:\Users\leona\Downloads\expermentSurvey\RQ3\respostas_RQ2_FasterNew.csv")
rq3_data = pd.read_csv(r"C:\Users\leona\Downloads\expermentSurvey\RQ3\respostas_RQ3_detailAndRigorNew.csv")

# === Processamento dos dados
rq1_responses = rq1_data.filter(regex=r'\d+\.1_intuitive').copy()
rq2_responses = rq2_data.filter(regex=r'\d+\.2_faster').copy()
rq3_responses = rq3_data.filter(regex=r'\d+\.3_detailed').copy()

# Consolidar os dados
consolidated = pd.DataFrame()

for scenario in range(1, 12):
    df_temp = pd.DataFrame({
        'pID': rq1_data['pID'],
        'Scenario': scenario,
        'Intuitiveness': rq1_responses[f'{scenario}.1_intuitive'],
        'Efficiency': rq2_responses[f'{scenario}.2_faster'],
        'Rigor': rq3_responses[f'{scenario}.3_detailed']
    })
    consolidated = pd.concat([consolidated, df_temp], ignore_index=True)

# === Calcular percentuais para o radar
dimensions = ['Intuitiveness', 'Efficiency', 'Rigor']
languages = ['MSL', 'JavaMOP']

radar_data = {
    lang: [
        (consolidated[dim] == lang).sum() / len(consolidated) * 100 for dim in dimensions
    ]
    for lang in languages
}

# === Gerar comandos LaTeX
comandos_latex = gerar_comandos_latex(radar_data, dimensions)
comandos_tradeoff = gerar_comandos_latex_tradeoff(consolidated)

print("===== Comandos LaTeX para Overleaf (Radar) =====")
print(comandos_latex)
print("===== Comandos LaTeX para Overleaf (Trade-off) =====")
print(comandos_tradeoff)

# === Gráfico radar
angles = np.linspace(0, 2 * np.pi, len(dimensions), endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
display_names = {"MSL": "SIESTA", "JavaMOP": "JavaMOP"}
for lang, values in radar_data.items():
    values += values[:1]
    ax.plot(angles, values, label=display_names[lang])
    ax.fill(angles, values, alpha=0.25)

axis_labels = ['                              Intuitive and Understandable', 'Faster and More Direct    ', 'Detail and Rigor            ']
ax.set_thetagrids(np.degrees(angles[:-1]), axis_labels, fontsize=13)
ax.set_title('')
ax.set_ylim(0, 80)
ax.tick_params(labelsize=14)
ax.grid(linewidth=0.9)
ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
plt.tight_layout()
plt.show()
