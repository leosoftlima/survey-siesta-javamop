# Código completo para gerar o heatmap final (ordenado corretamente)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar o CSV
df = pd.read_csv(r"C:\Users\leona\Downloads\expermentSurvey\RQ2\respostas_RQ2_FasterNew.csv")


# Normalizar nomes de colunas
df.columns = df.columns.str.replace('\n', ' ', regex=False).str.replace(r'\s+', ' ', regex=True).str.strip()

# Expandir domínios compostos (ex: "Web Development, Mobile Development")
df_expanded = df.assign(
    **{'What is your main area of expertise?': df['What is your main area of expertise?'].str.split(', ')}
).explode('What is your main area of expertise?')

# Domínios técnicos relevantes para o gráfico
relevant_domains = [
    'Web Development', 'Mobile Development', 'Embedded Systems',
    'Data Science/Analytics', 'DevOps/Cloud Computing', 'Machine Learning/AI'
]

# Filtrar apenas os domínios relevantes
df_filtered = df_expanded[df_expanded['What is your main area of expertise?'].isin(relevant_domains)]

# Identificar colunas de cenário (terminam com "_faster")
faster_cols = [col for col in df.columns if col.endswith('_faster')]

# Converter para formato longo (long format)
df_votes = df_filtered.melt(
    id_vars=['What is your main area of expertise?'],
    value_vars=faster_cols,
    var_name='Scenario',
    value_name='Selected'
)

# Agrupar e contar votos por (domínio, cenário, ferramenta)
votes_by_domain = df_votes.groupby(
    ['What is your main area of expertise?', 'Scenario', 'Selected']
).size().unstack(fill_value=0)

# Calcular % de votos MSL
votes_by_domain['MSL_percent'] = (
    votes_by_domain['MSL'] / (votes_by_domain['JavaMOP'] + votes_by_domain['MSL'])
) * 100

# Resetar índice para preparar a tabela final
votes_by_domain = votes_by_domain.reset_index()

# Pivotar para formato matriz (cenários nas colunas, domínios nas linhas)
heatmap_data = votes_by_domain.pivot(
    index='What is your main area of expertise?',
    columns='Scenario',
    values='MSL_percent'
)

# Renomear colunas para "Scenario 1", "Scenario 2", ...
heatmap_data.columns = [f"Scenario {int(s.split('.')[0])}" for s in heatmap_data.columns]

# Ordenar cenários numericamente
ordered_scenarios = sorted(heatmap_data.columns, key=lambda x: int(x.split(' ')[1]))
heatmap_data = heatmap_data[ordered_scenarios]

# Plotar heatmap
plt.figure(figsize=(14, 6))
sns.heatmap(
    heatmap_data,
    annot=True,
    cmap='YlOrRd',
    cbar_kws={'label': '% MSL'},
    linewidths=0.5,
    fmt='.1f'
)
#plt.title('Perceived Efficiency (Faster) - MSL Preference by Technical Domain (Y) and Scenario (X)')
plt.ylabel('Technical Domain')
plt.xlabel('Scenarios')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()