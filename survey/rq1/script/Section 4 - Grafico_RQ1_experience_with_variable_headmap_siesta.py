import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# =========================
# CONFIGURAÇÃO
# =========================
csv_path = r"../rq1/data/respostas_rq1intuitive.csv"

OUT_DIR = "out_rq1"
VARS_DIR = os.path.join(OUT_DIR, "vars")
FIGS_DIR = os.path.join(OUT_DIR, "figs")

HEATMAP_PNG = os.path.join(FIGS_DIR, "rq1_experience_heatmap_siesta.png")
HEATMAP_PDF = os.path.join(FIGS_DIR, "rq1_experience_heatmap_siesta.pdf")
LATEX_VARS_TEX = os.path.join(VARS_DIR, "rq1_experience_vars_siesta.tex")


# =========================
# UTILITÁRIOS
# =========================
def ensure_dirs():
    for d in [OUT_DIR, VARS_DIR, FIGS_DIR]:
        if not os.path.exists(d):
            os.makedirs(d)


def sanitize_exp_label(exp):
    mapping = {
        "Less than 1 year": "LessThanOneYear",
        "1 - 3 years": "OneToThreeYears",
        "4 - 6 years": "FourToSixYears",
        "7 - 10 years": "SevenToTenYears",
        "More than 10 years": "MoreThanTenYears"
    }
    return mapping.get(exp, exp.replace(" ", "").replace("-", ""))


def write_latex_vars(vars_dict, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for k, v in vars_dict.items():
            f.write("\\newcommand{\\%s}{%s}\n" % (k, v))


# =========================
# DADOS
# =========================
def compute_heatmap_data_siesta(df, exp_col):
    experience_levels = df[exp_col].dropna().unique().tolist()
    heatmap_data = pd.DataFrame(index=experience_levels, columns=range(1, 12))

    for exp in experience_levels:
        filtered = df[df[exp_col] == exp]
        for scenario in range(1, 12):
            col = "%d.1_intuitive" % scenario
            if col in filtered.columns:
                votes = filtered[col].dropna().astype(str).str.strip()
                total = len(votes)
                siesta_count = (votes == "MSL").sum()
                percent = (siesta_count / total) * 100 if total > 0 else 0
                heatmap_data.loc[exp, scenario] = round(percent, 1)

    experience_order = [
        "More than 10 years",
        "7 - 10 years",
        "4 - 6 years",
        "1 - 3 years",
        "Less than 1 year"
    ]


    ordered = [e for e in experience_order if e in heatmap_data.index]
    return heatmap_data.loc[ordered].astype(float)


def export_latex_variables_rq1_siesta(heatmap_df):
    vars_out = {}

    # Médias por experiência (SIESTA)
    for exp in heatmap_df.index:
        suffix = sanitize_exp_label(exp)
        avg = round(float(heatmap_df.loc[exp].mean()), 1)
        vars_out["percSIESTA" + suffix] = avg

    # Médias por cenário
    scenario_means = heatmap_df.mean(axis=0)

    max_scenario = int(scenario_means.idxmax())
    max_percent = round(float(scenario_means.max()), 1)

    min_scenario = int(scenario_means.idxmin())
    min_percent = round(float(scenario_means.min()), 1)

    closest_scenario = int((scenario_means - 50).abs().idxmin())
    closest_percent = round(float(scenario_means.loc[closest_scenario]), 1)

    vars_out["scenarioSIESTAMaxScenario"] = max_scenario
    vars_out["scenarioSIESTAMaxPercent"] = max_percent
    vars_out["scenarioSIESTAMinScenario"] = min_scenario
    vars_out["scenarioSIESTAMinPercent"] = min_percent
    vars_out["scenarioClosestScenario"] = closest_scenario
    vars_out["scenarioClosestPercent"] = closest_percent

    return vars_out


# =========================
# PLOT
# =========================
def plot_experience_heatmap_siesta(heatmap_df, save_png, save_pdf=None):
    sns.set_style("white")

    plt.figure(figsize=(11, 5), facecolor="white")

    ax = sns.heatmap(
        heatmap_df,
        annot=True,
        fmt=".1f",
        cmap="YlOrRd",
        cbar_kws={"label": "% SIESTA"},
        linewidths=0.5,
        linecolor="white"
    )

    ax.set_facecolor("white")
    ax.set_xlabel("Scenario", fontsize=12)
    ax.set_ylabel("Experience Level", fontsize=12)
    plt.xticks(rotation=0)
    plt.yticks(rotation=0)

    plt.tight_layout()

    plt.savefig(save_png, dpi=300, bbox_inches="tight", facecolor="white")
    if save_pdf is not None:
        plt.savefig(save_pdf, dpi=300, bbox_inches="tight", facecolor="white")

    plt.show()


# =========================
# MAIN
# =========================
def main():
    ensure_dirs()

    df = pd.read_csv(csv_path)

    exp_cols = [c for c in df.columns if "experience" in c.lower()]
    if not exp_cols:
        raise RuntimeError("Coluna de experiência não encontrada no CSV.")
    exp_col = exp_cols[0]

    heatmap_siesta = compute_heatmap_data_siesta(df, exp_col)

    plot_experience_heatmap_siesta(
        heatmap_siesta,
        HEATMAP_PNG,
        HEATMAP_PDF
    )

    latex_vars = export_latex_variables_rq1_siesta(heatmap_siesta)
    write_latex_vars(latex_vars, LATEX_VARS_TEX)

    print("[OK] Figura gerada:", HEATMAP_PNG)
    print("[OK] Variáveis LaTeX geradas:", LATEX_VARS_TEX)
    print("[OK] Variáveis:", latex_vars)


if __name__ == "__main__":
    main()
