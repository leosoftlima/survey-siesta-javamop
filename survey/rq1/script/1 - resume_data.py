import pandas as pd
import os

# === Funções de exclusão de participantes ===
def replace_experience(df):
    # Corrigir a coluna 'Professional experience as a software developer :' se existir
    target_column = "Professional experience as a software developer :"
    if target_column in df.columns:
       df[target_column] = df[target_column].replace("6 - 10 years", "7 - 10 years")

def get_participants_no_consent(df):
    """IDs de participantes que não deram consentimento"""
    consent_col = next((col for col in df.columns if "agree" in col.lower()), None)
    if not consent_col:
        return []
    return df[df[consent_col].str.strip().str.lower() == "no"].index.tolist()

def get_participants_all_same_answers(df):
    """IDs de participantes que responderam tudo A ou tudo B"""
    comparison_cols = [col for col in df.columns if "Comparison" in col]
    same_answer_ids = []
    for idx, row in df[comparison_cols].iterrows():
        values = row.fillna("").astype(str).str.strip().str.upper()
        filtered = values[values.isin(["A", "B"])]
        if len(filtered) == 44 and filtered.nunique() == 1:
            same_answer_ids.append(idx)
    return same_answer_ids

def get_excluded_indices(df):
    """Índices dos participantes excluídos"""
    no_consent = get_participants_no_consent(df)
    all_same = get_participants_all_same_answers(df)
    return sorted(set(no_consent + all_same))

# === Processamento principal ===

# Caminho do arquivo CSV
csv_path = r"../rq1/data/respostas.csv"
df = pd.read_csv(csv_path)

replace_experience(df)

# Normalizar nomes das colunas
df.columns = df.columns.str.replace('\n', ' ', regex=False).str.replace(r'\s+', ' ', regex=True).str.strip()

# Remover participantes inválidos
excluded_indices = get_excluded_indices(df)
df_valid = df.drop(index=excluded_indices).reset_index(drop=True)

# Perguntas e labels
question_pairs = [
    ('Is more intuitive and understandable', 'intuitive'),
    ('Allows for faster and more direct specification writing for the proposed scenario', 'faster'),
    ('Requires greater detail and rigor when writing specifications', 'detailed'),
    ('Offers simpler syntax', 'simpler')
]

# Mapeamento de A/B por cenário
ab_mapping = {
    1:  ('JavaMOP', 'MSL'),
    2:  ('MSL', 'JavaMOP'),
    3:  ('JavaMOP', 'MSL'),
    4:  ('JavaMOP', 'MSL'),
    5:  ('MSL', 'JavaMOP'),
    6:  ('JavaMOP', 'MSL'),
    7:  ('MSL', 'JavaMOP'),
    8:  ('JavaMOP', 'MSL'),
    9:  ('JavaMOP', 'MSL'),
    10: ('MSL', 'JavaMOP'),
    11: ('JavaMOP', 'MSL')
}

scenario_data = []

for i in range(1, 12):
    a_label, b_label = ab_mapping[i]
    for long_q, short_label in question_pairs:
        col = [c for c in df_valid.columns if f"{i}" in c.split(')')[0] and long_q in c]
        if col:
            col_name = col[0]
            counts = df_valid[col_name].value_counts()
            a_votes = counts.get('A', 0)
            b_votes = counts.get('B', 0)
            scenario_data.append({
                "Scenario": f"Scenario {i}",
                "Question": long_q,
                f"{a_label}": a_votes,
                f"{b_label}": b_votes
            })

# Criar DataFrame final
final_df = pd.DataFrame(scenario_data)

# Garantir que todas as colunas estejam presentes
for lang in ['JavaMOP', 'MSL']:
    if lang not in final_df.columns:
        final_df[lang] = 0

final_df = final_df[['Scenario', 'Question', 'JavaMOP', 'MSL']]

# Caminho de saída
output_path = r"../rq1/data/resumo_cenarios_1_a_11_newLeo.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

try:
    final_df.to_csv(output_path, index=False)
    print("✅ Arquivo CSV salvo com sucesso em:")
    print(output_path)
except Exception as e:
    print("❌ Erro ao salvar o arquivo:", e)
