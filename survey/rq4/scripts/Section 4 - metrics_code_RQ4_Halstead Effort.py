import pandas as pd

# Caminhos para os arquivos CSV
path_msl = r"..\rq4\data\halstead_summarySIESTA.csv"
path_mop = r"..\rq4\data\halstead_summaryMOP.csv"

# Leitura dos arquivos
df_msl = pd.read_csv(path_msl)
df_mop = pd.read_csv(path_mop)

# Métricas desejadas
metrics = ["Length", "Vocabulary", "Volume", "Difficulty", "Effort"]

# Construção da tabela
rows = []
for metric in metrics:
    mean_mop = df_mop[metric].mean()
    std_mop = df_mop[metric].std()
    mean_msl = df_msl[metric].mean()
    std_msl = df_msl[metric].std()
    rows.append((metric, mean_mop, std_mop, mean_msl, std_msl))

# Geração do código LaTeX da tabela
latex_table = r"""\begin{table}[ht]
\centering
\caption{Comparative Halstead metrics for JavaMOP and \siesta{} specifications (mean and standard deviation).}
\label{tab:halstead-summary}
\begin{tabular}{lrrrr}
\toprule
\textbf{Metric} & \multicolumn{2}{c}{\textbf{JavaMOP}} & \multicolumn{2}{c}{\textbf{\siesta{}}} \\
\cmidrule(r){2-3} \cmidrule(r){4-5}
& Mean & Std & Mean & Std \\
\midrule
"""

for metric, mean_mop, std_mop, mean_msl, std_msl in rows:
    line = f"{metric:<10} & {mean_mop:.2f} & {std_mop:.2f} & {mean_msl:.2f} & {std_msl:.2f} \\\\"
    latex_table += line + "\n"

latex_table += r"""\bottomrule
\end{tabular}
\end{table}
"""

print("===== LaTeX Table =====")
print(latex_table)

# Comandos LaTeX para Overleaf
print("\n===== LaTeX Commands =====")
latex_commands = "% RQ4 - metrics\n"

command_names = {
    "Volume": ("volJavamop", "volMSL"),
    "Length": ("lenJavamop", "lenMSL"),
    "Effort": ("effortJavamop", "effortMSL"),
    "Difficulty": ("diffJavamop", "diffMSL"),
    "Vocabulary": ("vocabJavamop", "vocabMSL"),
}

def format_decimal(val):
    """Format number with thousands separator and 2 decimal places."""
    parts = f"{val:,.2f}".split(".")
    parts[0] = parts[0].replace(",", "\\,")
    return f"{parts[0]}.{parts[1]}"

for metric, mean_mop, _, mean_msl, _ in rows:
    if metric in command_names:
        cmd_mop, cmd_msl = command_names[metric]
        val_mop = format_decimal(mean_mop)
        val_msl = format_decimal(mean_msl)
        latex_commands += f"\\newcommand{{\\{cmd_mop}}}{{{val_mop}}}\n"
        latex_commands += f"\\newcommand{{\\{cmd_msl}}}{{{val_msl}}}\n"

print(latex_commands)
