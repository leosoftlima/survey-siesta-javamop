import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from scipy.stats import chi2_contingency

# Template LaTeX para variáveis
latex_macro_template = """
\\newcommand{{\\percMSLLessThanOne}}{{{perc_less_than_1:.1f}}}
\\newcommand{{\\percJavaMOPOneToThree}}{{{perc_javamop_1_3:.1f}}}
\\newcommand{{\\percMSLFourToSix}}{{{perc_msl_4_6:.1f}}}
\\newcommand{{\\percMSLSixToTen}}{{{perc_msl_6_10:.1f}}}
\\newcommand{{\\percMSLMoreThanTenYears}}{{{perc_msl_10_more:.1f}}}
\\newcommand{{\\chisquareStat}}{{{chi2_stat:.2f}}}
\\newcommand{{\\pvalueChi}}{{$\\num{{{p_val:.1e}}}$}}
"""

# --- Funções principais --- #
def load_experience_data(filepath):
    df = pd.read_csv(filepath)
    exp_col = [col for col in df.columns if "experience" in col.lower()][0]
    return df, exp_col

def count_votes_by_experience(df, exp_col):
    experience_groups = [
        "Less than 1 year",
        "1 - 3 years",
        "4 - 6 years",
        "7 - 10 years",
        "More than 10 years"
    ]
    vote_counts = {group: {"JavaMOP": 0, "MSL": 0} for group in experience_groups}

    for _, row in df.iterrows():
        group = row[exp_col]
        if group not in experience_groups:
            continue
        for scenario in range(1, 12):
            col = f"{scenario}.1_intuitive"
            if col in df.columns and pd.notna(row[col]):
                answer = row[col].strip()
                if answer in ["JavaMOP", "MSL"]:
                    vote_counts[group][answer] += 1

    df_votes = pd.DataFrame(vote_counts).T
    df_votes["Total"] = df_votes["JavaMOP"] + df_votes["MSL"]
    df_votes["% JavaMOP"] = df_votes["JavaMOP"] / df_votes["Total"] * 100
    df_votes["% MSL"] = df_votes["MSL"] / df_votes["Total"] * 100
    return df_votes

def extract_latex_macros(df_votes):
    chi2_stat, p_val, _, _ = chi2_contingency(df_votes[["JavaMOP", "MSL"]])
    return latex_macro_template.format(
        perc_less_than_1=df_votes.loc["Less than 1 year"]["% MSL"],
        perc_javamop_1_3=df_votes.loc["1 - 3 years"]["% JavaMOP"],
        perc_msl_4_6=df_votes.loc["4 - 6 years"]["% MSL"],
        perc_msl_6_10=df_votes.loc["7 - 10 years"]["% MSL"],
        perc_msl_10_more=df_votes.loc["More than 10 years"]["% MSL"],
        chi2_stat=chi2_stat,
        p_val=p_val
    )

def save_latex_file(latex_code: str, output_path: str):
    with open(output_path, "w") as f:
        f.write("% Variáveis para gráfico por experiência profissional\n")
        f.write(latex_code.strip())

def plot_experience_chart(df_votes):
    ordered_experience = [
        "Less than 1 year",
        "1 - 3 years",
        "4 - 6 years",
        "7 - 10 years",
        "More than 10 years"
    ]
    df = df_votes.loc[[g for g in ordered_experience if g in df_votes.index]]

    labels = df.index.tolist()
    x = range(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))
    bars1 = ax.bar([i - width/2 for i in x], df["% MSL"], width, label='SIESTA', color='#1f77b4')
    bars2 = ax.bar([i + width/2 for i in x], df["% JavaMOP"], width, label='JavaMOP', color='#B8B8B8')

    ax.set_ylabel('% of participants', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=0)
    ax.set_ylim(0, 90)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.0f}%'))
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0.98), ncol=2, frameon=True)

    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}%', xy=(bar.get_x() + bar.get_width()/2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.show()

# --- Execução final: Edite os caminhos abaixo --- #
csv_path = r"../rq1/data/respostas_rq1intuitive.csv"
output_path = r"../rq1/data/experience_macros.tex"

df_exp, exp_col = load_experience_data(csv_path)
votes_df = count_votes_by_experience(df_exp, exp_col)
latex_code = extract_latex_macros(votes_df)
save_latex_file(latex_code, output_path)
plot_experience_chart(votes_df)

print("✅ Arquivo .tex salvo e gráfico gerado com sucesso.")

