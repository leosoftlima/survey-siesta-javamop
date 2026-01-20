# Survey: Developer Perceptions of JavaMOP and SIESTA

This repository contains the **replication package** of a survey-based empirical study investigating how professional software developers perceive two runtime verification specification approaches: **JavaMOP** and **SIESTA**.

The study analyzes developer perceptions across multiple dimensions, including **intuitiveness**, **perceived efficiency** (faster and more direct), **rigor**, and **syntactic simplicity**, based on controlled comparative behavioral scenarios.

---

## 📄 Associated Paper

**Title:**  
*Understanding Developer Preferences in Specifications Runtime Verification*

**Status:**  
Under preparation / submission  
*(This repository is currently private and will be made public upon acceptance or during the camera-ready phase.)*

---

## 👥 Authors

- **Leonardo Lima**
- **Leopoldo Teixeira**
- **Breno Miranda**
- **Marcelo D’Amorim**

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

```text
survey-siesta-javamop/
│
├── README.md
├── paper/
│   ├── main.pdf
│   └── figures/
├── data/
│   ├── raw/
│   ├── cleaned/
│   └── metadata/
├── scripts/
│   ├── rq1/
│   ├── rq2/
│   ├── rq3/
│   ├── rq4/
│   └── utils/
├── results/
│   ├── figures/
│   ├── tables/
│   └── latex_vars/
├── questionnaire/
│   ├── survey_instrument.pdf
│   └── scenarios/
├── ethics/
│   └── consent_statement.txt
├── LICENSE
└── CITATION.cff
