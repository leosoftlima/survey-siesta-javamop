import pandas as pd
from scipy.stats import binomtest

# === Caminho local do CSV de RQ3 (rigor) ===
csv_path = r"../rq3/data/respostas_RQ3_detailAndRigor.csv"

# === 1) Ler dados ===
rq3 = pd.read_csv(csv_path)

# Colunas que terminam em ".3_detailed" (11 cenários)
rigor_cols = [c for c in rq3.columns if ".3_detailed" in c]

# Formato longo
rigor_long = rq3.melt(
    id_vars=[
        "pID",
        "Which programming languages do you regularly use?",
        "What is your main area of expertise?"
    ],
    value_vars=rigor_cols,
    var_name="Scenario",
    value_name="ChosenRigor"
).dropna()

rigor_long.rename(columns={
    "Which programming languages do you regularly use?": "DevLang"
}, inplace=True)

# Linguagens-alvo
target_langs = ["Java", "Python", "JavaScript/TypeScript"]

# === 2) Executar teste binomial (H0: p = 0.5) ===
latex_cmds = []
for lang in target_langs:
    subset = rigor_long[rigor_long["DevLang"] == lang]
    total = len(subset)
    javamop_count = (subset["ChosenRigor"] == "JavaMOP").sum()
    res = binomtest(javamop_count, total, p=0.5, alternative="two-sided")

    pval = round(res.pvalue, 4)
    sig  = "True" if res.pvalue < 0.05 else "False"

    lang_clean = lang.replace("/", "").replace(" ", "")

    latex_cmds.append(f"\\newcommand{{\\pvalRigorJavaMOP{lang_clean}}}{{{pval if pval > 0 else '<0.0001'}}}")
    latex_cmds.append(f"\\newcommand{{\\sigRigorJavaMOP{lang_clean}}}{{{sig}}}")

# === 3) Imprimir comandos LaTeX ===
print("===== Comandos LaTeX (teste binomial) =====")
print("\n".join(latex_cmds))
