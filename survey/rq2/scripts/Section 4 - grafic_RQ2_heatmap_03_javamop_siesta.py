import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar o CSV
csv_path = r"../rq2/data/respostas_RQ2_Faster.csv"
df_rq2 = pd.read_csv(csv_path)

df_rq2 = pd.read_csv(csv_path)

# Função para expandir domínios técnicos compostos
def expand_domains(df, column):
    df_expanded = df.assign(**{column: df[column].str.split(', ')}).explode(column)
    return df_expanded

# Expandir domínios técnicos
df_domains = expand_domains(df_rq2, 'What is your main area of expertise?')

# Filtrar domínios e grupos relevantes
relevant_domains = [
    'Web Development', 'Mobile Development', 'Embedded Systems',
    'Data Science/Analytics', 'DevOps/Cloud Computing', 'Machine Learning/AI'
]

# Definir ordem desejada para grupos de experiência
experience_groups_order = [
    'More than 10 years',
    '7 - 10 years',
    '4 - 6 years',
    '1 - 3 years',
    'Less than 1 year'
]

# Transformar para formato longo
df_votes = df_domains.melt(
    id_vars=['What is your main area of expertise?', 'Professional experience as a software developer :'],
    value_vars=[col for col in df_rq2.columns if col.endswith('_faster')],
    var_name='Scenario',
    value_name='Selected'
)

# Filtrar respostas
df_votes_filtered = df_votes[
    (df_votes['What is your main area of expertise?'].isin(relevant_domains)) &
    (df_votes['Professional experience as a software developer :'].isin(experience_groups_order))
]

# Agrupar votos por grupo de experiência, domínio técnico e linguagem
votes_summary = df_votes_filtered.groupby(
    ['Professional experience as a software developer :', 'What is your main area of expertise?', 'Selected']
).size().unstack(fill_value=0)

# Calcular % JavaMOP e MSL por grupo e domínio
votes_summary['Total'] = votes_summary['JavaMOP'] + votes_summary['MSL']
votes_summary['JavaMOP_percent'] = (votes_summary['JavaMOP'] / votes_summary['Total']) * 100
votes_summary['MSL_percent'] = (votes_summary['MSL'] / votes_summary['Total']) * 100

# Pivot com eixos invertidos
heatmap_data_javamop = votes_summary.reset_index().pivot(
    index='What is your main area of expertise?',
    columns='Professional experience as a software developer :',
    values='JavaMOP_percent'
).reindex(columns=experience_groups_order)

heatmap_data_msl = votes_summary.reset_index().pivot(
    index='What is your main area of expertise?',
    columns='Professional experience as a software developer :',
    values='MSL_percent'
).reindex(columns=experience_groups_order)

# Criar máscara para células sem dados (Total == 0)
mask_javamop = votes_summary.reset_index().pivot(
    index='What is your main area of expertise?',
    columns='Professional experience as a software developer :',
    values='Total'
).reindex(columns=experience_groups_order).isna()

# Plot JavaMOP
plt.figure(figsize=(12, 6))
sns.heatmap(heatmap_data_javamop, annot=True, cmap='YlGnBu', cbar_kws={'label': '% JavaMOP'}, linewidths=0.5, fmt='.1f', mask=mask_javamop)
#plt.title('Perceived Efficiency (Faster) - JavaMOP Preference by Technical Domain (Y) and Experience Group (X)')
plt.xlabel('Experience Group')
plt.ylabel('Technical Domain')
plt.xticks(rotation=0)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()

# Plot MSL
plt.figure(figsize=(12, 6))
sns.heatmap(heatmap_data_msl, annot=True, cmap='YlOrRd', cbar_kws={'label': '% SIESTA'}, linewidths=0.5, fmt='.1f', mask=mask_javamop)
#plt.title('Perceived Efficiency (Faster) - MSL Preference by Technical Domain (Y) and Experience Group (X)')
plt.xlabel('Experience Group')
plt.ylabel('Technical Domain')
plt.xticks(rotation=0)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()