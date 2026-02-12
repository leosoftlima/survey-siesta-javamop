# Survey: Developer Perceptions of JavaMOP and SIESTA

This repository contains the **replication package** of a survey-based empirical study investigating how professional software developers perceive two runtime verification specification approaches: **JavaMOP** and **SIESTA**.

The study analyzes developer perceptions across multiple dimensions, including **intuitiveness**, **perceived efficiency** (faster and more direct), **rigor**, and **syntactic simplicity**, based on controlled comparative behavioral scenarios.

---

## 📄 Associated Paper

**Title:**  
*Understanding Developer Preferences in Specifications Runtime Verification*

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
- **RQ2** – How do developers perceive the *faster and more direct* writing of runtime specifications using JavaMOP and SIESTA across different experience levels and technical domains?
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

survey-siesta-javamop/
│
├── README.md
├── LICENSE
├── CITATION.cff
│
├── data/
│   ├── raw/
│   │   ├── survey_responses.csv
│   │   └── ...
│   ├── processed/
│   │   ├── rq1_processed.csv
│   │   ├── rq2_processed.csv
│   │   ├── rq3_processed.csv
│   │   ├── rq4_processed.csv
│   │   └── halstead_metrics.csv
│
├── scripts/
│   ├── rq1_analysis.py
│   ├── rq2_analysis.py
│   ├── rq3_analysis.py
│   ├── rq4_analysis.py
│   ├── halstead_analysis.py
│   └── utils.py
│
├── results/
│   ├── rq1/
│   │   ├── figures/
│   │   │   ├── rq1_overall.png
│   │   │   └── rq1_heatmap.png
│   │   └── tables/
│   │       └── rq1_stats.csv
│   │
│   ├── rq2/
│   │   ├── figures/
│   │   └── tables/
│   │
│   ├── rq3/
│   │   ├── figures/
│   │   └── tables/
│   │
│   ├── rq4/
│   │   ├── figures/
│   │   └── tables/
│   │
│   └── objective-metrics/
│       ├── figures/
│       └── tables/
│
└── paper-material/
    ├── scenarios.pdf
    ├── questionnaire.pdf
    └── statistical-tests-description.md
