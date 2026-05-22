import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar o CSV
df = pd.read_csv(r"../rq2/data/respostas_RQ2_Faster.csv")
# Normalizar nomes das colunas
df.columns = df.columns.str.replace('\n', ' ', regex=False).str.replace(r'\s+', ' ', regex=True).str.strip()

# Expandir domínios técnicos compostos (ex: "DevOps/Cloud, Back-end")
df_expanded = df.assign(
    **{'What is your main area of expertise?': df['What is your main area of expertise?'].str.split(', ')}
).explode('What is your main area of expertise?')

# Domínios técnicos considerados relevantes
relevant_domains = [
    'Web Development', 'Mobile Development', 'Embedded Systems',
    'Data Science/Analytics', 'DevOps/Cloud Computing', 'Machine Learning/AI'
]

# Filtrar apenas os domínios relevantes
df_filtered = df_expanded[df_expanded['What is your main area of expertise?'].isin(relevant_domains)]

# Identificar colunas de cenário (terminam com "_faster")
faster_cols = [col for col in df.columns if col.endswith('_faster')]

# Converter para formato longo
df_votes = df_filtered.melt(
    id_vars=['What is your main area of expertise?'],
    value_vars=faster_cols,
    var_name='Scenario',
    value_name='Selected'
)

# Agrupar e contar votos por (domínio, cenário, ferramenta)
vote_counts = df_votes.groupby(
    ['What is your main area of expertise?', 'Scenario', 'Selected']
).size().unstack(fill_value=0)

# Calcular % de votos JavaMOP
vote_counts['JavaMOP_percent'] = (
    vote_counts['JavaMOP'] / (vote_counts['JavaMOP'] + vote_counts['MSL'])
) * 100

# Resetar índice para organizar como DataFrame tabular
vote_counts = vote_counts.reset_index()

# Criar tabela pivot para heatmap
heatmap_data = vote_counts.pivot(
    index='What is your main area of expertise?',
    columns='Scenario',
    values='JavaMOP_percent'
)

# Renomear colunas de cenário para "Scenario 1", "Scenario 2", ...
heatmap_data.columns = [f"Scenario {int(s.split('.')[0])}" for s in heatmap_data.columns]

# Ordenar colunas numericamente
heatmap_data = heatmap_data[sorted(heatmap_data.columns, key=lambda x: int(x.split()[1]))]

# Plotar o heatmap
plt.figure(figsize=(14, 6))
sns.heatmap(
    heatmap_data,
    annot=True,
    cmap='YlGnBu',
    cbar_kws={'label': '% JavaMOP'},
    linewidths=0.5,
    fmt='.1f'
)
#plt.title('Perceived Efficiency (Faster) - JavaMOP Preference by Technical Domain (Y) and Scenario (X)')
plt.ylabel('Technical Domain')
plt.xlabel('Scenarios')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()