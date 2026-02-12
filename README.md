# Survey: Developer Perceptions of JavaMOP and SIESTA

This repository contains the **replication package** of a survey-based empirical study investigating how professional software developers perceive two runtime verification specification approaches: **JavaMOP** and **SIESTA**.

The study analyzes developer perceptions across multiple dimensions, including **intuitiveness**, **perceived efficiency** (faster and more direct), **rigor**, and **syntactic simplicity**, based on controlled comparative behavioral scenarios.

---

## 📄 Associated Paper

**Title:**  
*Understanding Developer Preferences in Runtime Verification Specifications*

**Status:**  
Under preparation / submission  

---

## 👥 Authors

- **Leonardo Lima**
- **Leopoldo Teixeira**
- **Breno Miranda**

---

## 🎯 Research Questions

This study addresses the following research questions:

- **RQ1** – How do developers perceive the *intuitiveness and understandability* of runtime specifications written using JavaMOP and SIESTA?
- **RQ2** – How do developers perceive the *writing efficiency* of runtime specifications using JavaMOP and SIESTA across different experience levels and technical domains?
- **RQ3** – How does the frequency of selecting JavaMOP or SIESTA as the *more rigorous* option vary across specification dimensions and developer language backgrounds?
- **RQ4** – How does *syntactic simplicity* influence developer preference between JavaMOP and SIESTA?

---

## 📊 Study Overview

- **Participants:** Professional software developers  
- **Method:** Online survey with comparative questions  
- **Scenarios:** 11 behavioral runtime monitoring scenarios  

**Experimental Design:**
- Alternatives randomized (A/B) to mitigate positional bias
- Multiple demographic dimensions collected (experience, domain, primary programming language)

**Analysis Techniques:**
- Descriptive statistics
- One-tailed and two-tailed binomial tests
- Chi-squared tests of independence
- Visual analysis using bar charts, heatmaps, radar charts, and boxenplots
- Objective syntactic complexity analysis using **Halstead metrics**

---

## 📁 Repository Structure

```
survey/
│
├── resumo_cenarios_1_a_11.csv
├── respostas_dadostratados.csv
├── survey_metrics_macros.tex
│
├── RQ1/
│   ├── respostas_rq1intuitiveAgeNew.csv
│   ├── Section 4 - RQ1 - binominal test.py
│   ├── Section 4 - RQ1 - Chisquared test.py
│   ├── imagens/
│   └── scripts/
│
├── RQ2/
│   ├── respostas_RQ2_FasterNew.csv
│   ├── Section 4 - extrair_data_RQ2.py
│   ├── Section 4 - grafic_RQ2_heatmap_01_MSL.py
│   └── images/
│
├── RQ3/
│   ├── respostas_RQ3_detailAndRigorNew.csv
│   ├── Section 4 variaveis_RQ3_binominal.py
│   ├── Section 4 Grafic_RQ3_radar.py
│   └── radar_languages.png
│
├── RQ4/
│   ├── respostas_RQ4_SintaxeNew.csv
│   ├── Section 4 - Grafic_RQ4_linguagens.py
│   ├── Section 4 - metrics_code_RQ4.py
│   ├── mop11/
│   ├── code11/
│   └── ck_metrics/
│
├── code/
│   └── (Java specification examples)
│
├── scripts/
│   └── (Section 3.2 demographic scripts)
│
├── backup/
│   └── (original survey backups)
│
└── paper/
    └── related references
```

