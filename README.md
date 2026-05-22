# Replication Package — Understanding Developer Preferences in Runtime Verification Specifications

This repository contains the full replication package, datasets, statistical analyses, scripts, and visualization artifacts used in the empirical study investigating how professional software developers perceive two runtime verification specification approaches: JavaMOP and SIESTA.

The study analyzes developer perceptions across multiple dimensions, including intuitiveness, understandability, writing faster and more direct, rigor, and syntactic simplicity, using controlled comparative behavioral scenarios.

---

![Status](https://img.shields.io/badge/status-under_review-orange)
![Language](https://img.shields.io/badge/python-3.10-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Replication Package](https://img.shields.io/badge/artifact-available-brightgreen)

---

## 📄 Associated Paper

**Title:**  
*Understanding Developer Preferences in Runtime Verification Specifications*

**Status:**  
Under preparation / submission

---

## 👥 Authors

- **Leonardo Lima**
- **Breno Miranda**
- **Leopoldo Teixeira**

---

## 📚 Background

Runtime Verification (RV) techniques allow software systems to be monitored during program execution to ensure that behavioral properties are respected.

This study compares two runtime specification approaches:

- **JavaMOP**: a formal runtime verification framework based on monitoring-oriented programming and declarative behavioral specifications.
- **SIESTA**: a lightweight annotation-based specification approach designed to reduce syntactic overhead and improve accessibility for developers.

The goal of this study is to better understand how developers perceive different runtime specification styles in terms of usability, clarity, writing effort, rigor, and syntactic complexity.

---

## 🎯 Research Questions

This study addresses the following research questions:

- **RQ1** – How do developers perceive the intuitiveness and understandability of runtime specifications written using JavaMOP and SIESTA across different professional backgrounds?

- **RQ2** – How do developers perceive faster and more direct runtime specifications writing using JavaMOP and SIESTA across different experience levels and domains?

- **RQ3** – How does the frequency of selecting JavaMOP or SIESTA as the more rigorous option vary across specification dimensions and developer language backgrounds?

- **RQ4** – How does the syntactic simplicity of specifications influence developer preference between JavaMOP and SIESTA?

---

## 📊 Study Overview

### Participants

- 102 professional software developers

### Method

- Online survey with comparative questions

### Scenarios

- 11 behavioral runtime monitoring scenarios

### Experimental Design

- Alternatives randomized (A/B) to mitigate positional bias
- Multiple demographic dimensions collected:
  - Professional experience
  - Technical domain
  - Primary programming language
  - Familiarity with runtime verification tools and specification languages

### Evaluated Dimensions

- Intuitiveness and understandability
- Faster and more direct specification writing
- Required rigor
- Syntactic simplicity

---

## 🧪 Statistical Analysis

The study combines descriptive and inferential statistical analyses, including:

- Descriptive statistics
- One-tailed binomial tests
- Two-tailed binomial tests
- Chi-squared tests of independence
- Visual analysis using:
  - Bar charts
  - Heatmaps
  - Radar charts
  - Boxenplots

A significance level of 5% (`α = 0.05`) was adopted throughout the analyses.

---

## 📈 Objective Specification Complexity Analysis

To complement subjective perceptions, the repository includes objective syntactic complexity measurements for all evaluated specifications.

The following Halstead metrics were computed:

- Length
- Vocabulary
- Volume
- Difficulty
- Effort

These metrics were used to investigate whether developer preferences correlate with measurable syntactic complexity differences.

---

## 📁 Repository Structure

```text
survey/
│
├── 3.2/
│   ├── data/
│   │   └── Survey responses and LaTeX macro files used in the participant demographics analysis
│   │
│   ├── images/
│   │   └── Figures generated for age, gender, experience, expertise, programming languages, and runtime verification familiarity
│   │
│   └── scripts/
│       └── Scripts for extracting demographic data, generating figures, and producing LaTeX macros for Section 3.2
│
├── RQ1/
│   ├── data/
│   │   └── Processed survey responses used to analyze intuitiveness and understandability perceptions across behavioral scenarios and professional experience levels
│   │
│   ├── images/
│   │   └── Bar charts, heatmaps, and visualizations generated for the intuitiveness and understandability analysis
│   │
│   └── scripts/
│       └── Scripts for data extraction, binomial tests, Chi-squared tests, heatmap generation, and visualization pipelines related to RQ1
│
├── RQ2/
│   ├── data/
│   │   └── Processed survey responses used to analyze perceptions of faster and more direct runtime specification writing
│   │
│   ├── images/
│   │   └── Heatmaps and visualizations generated for experience-level and technical-domain analyses
│   │
│   └── scripts/
│       └── Scripts for data extraction, heatmap generation, statistical analysis, and visualization pipelines related to RQ2
│
├── RQ3/
│   ├── data/
│   │   └── Processed survey responses used to analyze perceived rigor and compare it with intuitiveness and faster/direct writing dimensions
│   │
│   ├── images/
│   │   └── Radar charts generated for the rigor analysis across specification dimensions and developer language backgrounds
│   │
│   └── scripts/
│       └── Scripts for extracting RQ3 data, generating radar charts, and computing binomial test variables
│
├── RQ4/
│   ├── data/
│   │   └── Processed survey responses and Halstead metric outputs
│   │
│   ├── images/
│   │   └── Figures generated for the syntactic simplicity analysis
│   │
│   ├── javamop11/
│   │   └── JavaMOP specifications used in the 11 evaluated scenarios
│   │
│   ├── siesta11/
│   │   └── SIESTA specifications used in the 11 evaluated scenarios
│   │
│   └── scripts/
│       └── Scripts for data extraction, statistical analysis, Halstead metrics, and figure generation
│
└── README.md
