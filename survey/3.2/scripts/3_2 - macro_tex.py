import pandas as pd
from collections import Counter

# --- Funções auxiliares --- #


def get_participant_ids(df):
    """Gera lista de IDs no formato P1, P2, ..., PN"""
    return [f"P{i+1}" for i in range(len(df))]

def get_participants_no_consent(df):
    """Retorna IDs de participantes que não deram consentimento"""
    consent_col = next((col for col in df.columns if "agree" in col.lower()), None)
    if not consent_col:
        return []
    
    no_consent = df[df[consent_col].str.strip().str.lower() == "no"].index
    return [f"P{i+1}" for i in no_consent]


def get_participants_all_same_answers(df):
    comparison_cols = [col for col in df.columns if "Comparison" in col]
    same_answer_ids = []

    for idx, row in df[comparison_cols].iterrows():
        values = row.fillna("").astype(str).str.strip().str.upper()
        filtered = values[values.isin(["A", "B"])]
        if len(filtered) == 44 and filtered.nunique() == 1:
            same_answer_ids.append(f"P{idx+1}")
    
    return same_answer_ids

def compute_consent_metrics(df, excluded):
    total = len(df)
    consent_col = next((col for col in df.columns if "agree" in col.lower()), None)
    if not consent_col:
        return 0.0, 0.0
    
    # Total que não deu consentimento
    no_consent = df[df[consent_col].str.strip().str.lower() == "no"]
    num_no_consent = no_consent.shape[0]

    # Quantos disseram "Yes"
    num_agreed = total - num_no_consent

    # Cálculo percentual
    consent_agreed = round((num_agreed / total) * 100, 1)              # Apenas os que disseram "Yes"
    consent_agreed_all = round(((total - len(excluded)) / total) * 100, 1)  # Todos que não foram excluídos

    return consent_agreed, consent_agreed_all


def get_excluded_participants(df):
    """Retorna lista final de participantes excluídos"""
    no_consent = get_participants_no_consent(df)
    all_same = get_participants_all_same_answers(df)
    excluded = sorted(set(no_consent + all_same))
    return excluded


# Participantes válidos
def get_valid_participants(df, excluded):
    return [i for i in df.index if f"P{i+1}" not in excluded]

# Cálculo normalizado
def count_normalized(series, total):
    return (series.value_counts(normalize=True) * 100).round(1).to_dict()

def split_and_count(series, total):
    all_items = series.dropna().astype(str).str.split(', ').explode()
    return (all_items.value_counts() / total * 100).round(1).to_dict()

def replace_experience(df):
    # Corrigir a coluna 'Professional experience as a software developer :' se existir
    target_column = "Professional experience as a software developer :"
    if target_column in df.columns:
       df[target_column] = df[target_column].replace("6 - 10 years", "7 - 10 years")

def get_latex_commands(demo_stats):
    heard_key = "I've heard about it, but I've never used it."
    heard_value = demo_stats['familiarity'].get(heard_key, 0)
    lines = [
        "% Total participants",
        "\\newcommand{\\totalparticipants}{" + str(demo_stats['total']) + "}",
        "\\newcommand{\\excludedparticipants}{" + str(demo_stats['excluded']) + "}",
        "\\newcommand{\\validparticipants}{" + str(demo_stats['valid']) + "}",
        "\\newcommand{\\totalscenarios}{11}",
        "\\newcommand{\\totalintuitivevotes}{880}",
        "\\newcommand{\\totalintuitivevotesSelection}{858}",
        "",
        "% 3.2 Consent percentage",
        f"\\newcommand{{\\consentAgreed}}{{{demo_stats['consent_agreed']}}}",
        f"\\newcommand{{\\consentAgreedAll}}{{{demo_stats['consent_agreed_all']}}}",

        "",
        "% 3.2 Age group percentages",
        f"\\newcommand{{\\ageGroupUnderEighteen}}{{{demo_stats['age'].get('Under 18', 0)}}}",
        f"\\newcommand{{\\ageGroupEighteenToTwentyFour}}{{{demo_stats['age'].get('18–24', 0)}}}",
        f"\\newcommand{{\\ageGroupTwentyFiveToThirtyFour}}{{{demo_stats['age'].get('25–34', 0)}}}",
        f"\\newcommand{{\\ageGroupThirtyFiveToFortyFour}}{{{demo_stats['age'].get('35–44', 0)}}}",
        f"\\newcommand{{\\ageGroupFortyFiveToFiftyFour}}{{{demo_stats['age'].get('45–54', 0)}}}",
        f"\\newcommand{{\\ageGroupFiftyFiveToSixtyFour}}{{{demo_stats['age'].get('55–64', 0)}}}",
        f"\\newcommand{{\\ageGroupSixtyFivePlus}}{{{demo_stats['age'].get('65+', 0)}}}",
        "",
        "% 3.2 Gender distribution percentages",
        f"\\newcommand{{\\genderMale}}{{{demo_stats['gender'].get('Male', 0)}}}",
        f"\\newcommand{{\\genderFemale}}{{{demo_stats['gender'].get('Female', 0)}}}",
        f"\\newcommand{{\\genderNonBinary}}{{{demo_stats['gender'].get('Non-binary', 0)}}}",
        f"\\newcommand{{\\genderPreferNotSay}}{{{demo_stats['gender'].get('Prefer not to say', 0)}}}",
        "",
        "% 3.2 Professional experience percentages",
        f"\\newcommand{{\\experienceMoreThanTen}}{{{demo_stats['experience'].get('More than 10 years', 0)}}}",
        f"\\newcommand{{\\experienceSixToTen}}{{{demo_stats['experience'].get('7 - 10 years', 0)}}}",
        f"\\newcommand{{\\experienceFourToSix}}{{{demo_stats['experience'].get('4 - 6 years', 0)}}}",
        f"\\newcommand{{\\experienceOneToThree}}{{{demo_stats['experience'].get('1 - 3 years', 0)}}}",
        f"\\newcommand{{\\experienceLessThanOne}}{{{demo_stats['experience'].get('Less than 1 year', 0)}}}",
        "",
        "% 3.3 Area of expertise percentages",
        f"\\newcommand{{\\expertiseWebDev}}{{{demo_stats['expertise'].get('Web Development', 0)}}}",
        f"\\newcommand{{\\expertiseDataScience}}{{{demo_stats['expertise'].get('Data Science/Analytics', 0)}}}",
        f"\\newcommand{{\\expertiseDevOps}}{{{demo_stats['expertise'].get('DevOps/Cloud Computing', 0)}}}",
        f"\\newcommand{{\\expertiseMobileDev}}{{{demo_stats['expertise'].get('Mobile Development', 0)}}}",
         f"\\newcommand{{\\expertiseMachineLearning}}{{{demo_stats['expertise'].get('Machine Learning/AI', 0)}}}",
        "",
        "% 3.3 Programming languages percentages",
        f"\\newcommand{{\\langJava}}{{{demo_stats['languages'].get('Java', 0)}}}",
        f"\\newcommand{{\\langPython}}{{{demo_stats['languages'].get('Python', 0)}}}",
        f"\\newcommand{{\\langJavaScript}}{{{demo_stats['languages'].get('JavaScript/TypeScript', 0)}}}",
        "",
        "% 3.3 Familiarity with runtime verification tools",
        f"\\newcommand{{\\familiarityYes}}{{{demo_stats['familiarity'].get('Yes', 0)}}}",
        f"\\newcommand{{\\familiarityNo}}{{{demo_stats['familiarity'].get('No', 0)}}}",
        f"\\newcommand{{\\familiarityHeard}}{{{heard_value}}}",
    ]
    return "\n".join(lines)

# --- PROCESSAMENTO PRINCIPAL --- #

csv_path = r"../3.2/data/respostas.csv"
df = pd.read_csv(csv_path)

replace_experience(df)
excluded = get_excluded_participants(df)
valid_indices = get_valid_participants(df, excluded)
valid_df = df.loc[valid_indices].copy()

demo_stats = {
    'total': len(df),
    'excluded': len(excluded),
    'valid': len(valid_df),
}

# Consentimento (dois cálculos)
demo_stats['consent_agreed'], demo_stats['consent_agreed_all'] = compute_consent_metrics(df, excluded)


# Demográficos
age_col = [col for col in df.columns if "age group" in col.lower()]
gender_col = [col for col in df.columns if "gender" in col.lower()]
exp_col = [col for col in df.columns if "experience" in col.lower()]

demo_stats['age'] = count_normalized(valid_df[age_col[0]], len(valid_df)) if age_col else {}
demo_stats['gender'] = count_normalized(valid_df[gender_col[0]], len(valid_df)) if gender_col else {}
demo_stats['experience'] = count_normalized(valid_df[exp_col[0]], len(valid_df)) if exp_col else {}

# Expertise e Linguagens 
expertise_col = [col for col in df.columns if "expertise" in col.lower()]
language_col = [col for col in df.columns if "programming languages" in col.lower()]
expertise_valid = valid_df[expertise_col[0]] if expertise_col else pd.Series()
lang_valid = valid_df[language_col[0]] if language_col else pd.Series()

demo_stats['expertise'] = split_and_count(expertise_valid, len(valid_df))
demo_stats['languages'] = split_and_count(lang_valid, len(valid_df))

# Familiaridade
familiarity_col = [col for col in df.columns if "runtime verification tools" in col.lower()]
if familiarity_col:
    fam_series = valid_df[familiarity_col[0]].dropna().astype(str).str.strip()
    demo_stats['familiarity'] = (fam_series.value_counts(normalize=True) * 100).round(1).to_dict()
else:
    demo_stats['familiarity'] = {}

# Exportar LaTeX
latex_output = get_latex_commands(demo_stats)
output_path = r"../3.2/data/survey_metrics_macros.tex"
with open(output_path, "w") as f:
    f.write(latex_output.strip())

print(f"✅ Arquivo LaTeX gerado em: {output_path}")
