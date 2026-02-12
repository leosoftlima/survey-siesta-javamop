import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Caminho para o CSV fornecido
csv_path = r"C:\Users\leona\Downloads\RQ2-20251210T142707Z-1-001\RQ2\respostas_RQ2_FasterNew.csv"
df = pd.read_csv(csv_path)

# Remover a etapa de expandir domínios técnicos
# Filtrar colunas com .2_faster
scenario_cols = [col for col in df.columns if col.endswith('.2_faster')]

# Definir grupos de experiência em ordem desejada
ordered_experience_groups = [
    'More than 10 years',
    '7 - 10 years',
    '4 - 6 years',
    '1 - 3 years',
    'Less than 1 year'
]

# Transformar para formato longo
df_votes = df.melt(
    id_vars=['Professional experience as a software developer :'],
    value_vars=scenario_cols,
    var_name='Scenario',
    value_name='Selected'
)

# Renomear colunas
df_votes = df_votes.rename(columns={
    'Professional experience as a software developer :': 'Experience Group'
})

# Remover valores ausentes
df_votes = df_votes.dropna(subset=['Selected', 'Scenario', 'Experience Group'])

# Inicializar tabela de contagem
vote_counts = []

# Contar votos corretamente (sem expandir domínios)
for (group, scenario), group_data in df_votes.groupby(['Experience Group', 'Scenario']):
    total = len(group_data)
    java_count = (group_data['Selected'] == 'JavaMOP').sum()
    msl_count = (group_data['Selected'] == 'MSL').sum()
    vote_counts.append({
        'Experience Group': group,
        'Scenario': scenario,
        'JavaMOP': java_count,
        'MSL': msl_count,
        'Total': java_count + msl_count
    })

votes_df = pd.DataFrame(vote_counts)

# Extrair número do cenário e preparar label
votes_df['Scenario Number'] = votes_df['Scenario'].str.extract(r'(\d+)').astype(int)
votes_df['Scenario Label'] = 'Scenario ' + votes_df['Scenario Number'].astype(str)

# Calcular percentual JavaMOP
votes_df['JavaMOP_percent'] = (votes_df['JavaMOP'] / votes_df['Total']) * 100

# Pivotar dados
heatmap_data = votes_df.pivot(index='Experience Group', columns='Scenario Label', values='JavaMOP_percent')

# Ordenar eixos
heatmap_data = heatmap_data.reindex(index=ordered_experience_groups)
heatmap_data = heatmap_data[sorted(heatmap_data.columns, key=lambda x: int(x.split()[-1]))]

# Plotar heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(
    heatmap_data,
    annot=True,
    fmt=".1f",
    annot_kws={"size": 10},
    cmap="YlGnBu",
    cbar_kws={'label': '% JavaMOP'},
    linewidths=0.5
)
#plt.title("Perceived Efficiency (Faster) - JavaMOP Preference by Scenario and Experience Group")
plt.xlabel("Scenarios")
plt.ylabel("Professional Experience Group")
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()