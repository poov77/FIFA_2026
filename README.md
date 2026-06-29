```markdown
# 🏆 FIFA 2026 AI Predictor & Tactical Scouting Dashboard

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B?logo=streamlit)
![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-Machine_Learning-F7931E?logo=scikit-learn)
![Status](https://img.shields.io/badge/Status-Active-success)

A professional-grade sports analytics web application built with **Python** and **Streamlit**. This dashboard utilizes a custom Heuristic Scoring Model to forecast the outcomes of the 2026 FIFA World Cup based on squad market valuations, 4-year performance cycles, and FIFA coefficients. 

Additionally, it features a specialized **Tactical ROI Algorithm** designed specifically for **Indian Super League (ISL)** sporting directors to identify high-value, undervalued international squads for tactical study.

---

## ✨ Key Features

* **📊 Global Win Probability Matrix:** Calculates and ranks the mathematical win probability for all 48 participating teams using MinMax scaled heuristic weights.
* **⭐ Final Four Prediction Engine:** Identifies the four teams mathematically engineered to dominate the knockout brackets based on depth and pedigree.
* **🎯 Attacking Dynamics:** Interactive Plotly scatter matrices visualizing attacking efficiency vs. squad market value.
* **🐴 Dark Horse Identifier:** Flags dangerous underdogs (ranked outside the FIFA Top 10) generating exceptionally high statistical threat levels.
* **🇮🇳 ISL Scouting Network (ROI Tool):** A custom Return on Investment (ROI) algorithm that flags international federations achieving high tactical output (goals + defensive rigidity) despite low squad market values.

---

## 💻 Tech Stack

* **Language:** Python 3.8+
* **Frontend / UI:** Streamlit (Custom Glassmorphism CSS & Pro-Max UI)
* **Data Manipulation:** Pandas, NumPy
* **Machine Learning / Math:** Scikit-Learn (`MinMaxScaler`)
* **Data Visualization:** Plotly (`plotly.express`, `plotly.graph_objects`)

---

## 🚀 Installation & Setup

Follow these steps to run the dashboard on your local machine.

### 1. Clone the repository
```bash
git clone [https://github.com/YourUsername/FIFA-2026-AI-Predictor.git](https://github.com/YourUsername/FIFA-2026-AI-Predictor.git)
cd FIFA-2026-AI-Predictor

```

### 2. Install dependencies

Ensure you have Python installed, then run:

```bash
pip install streamlit pandas scikit-learn plotly

```

### 3. Add the Dataset

Ensure the required dataset file is present in the root directory. The file **must** be named exactly:
`FIFA World Cup Dataset.csv.xlsx - test.csv`

### 4. Run the Application

Launch the Streamlit server:

```bash
streamlit run app.py

```

*The dashboard will automatically open in your default web browser at `http://localhost:8501`.*

---

## 🧠 How the Model Works (Methodology)

Unlike traditional Machine Learning models (like Random Forests) that require historical target labels to train, this system uses a **Weighted Heuristic Approach** suited for fresh data structures.

1. **Feature Extraction:** Extracts the most predictive features (FIFA Points, Squad Value, Past Titles, Goals Scored/Conceded).
2. **Normalization:** Utilizes `sklearn.preprocessing.MinMaxScaler` to bring multi-billion Euro market values and thousands of FIFA points into a comparative `[0.0, 1.0]` scale.
3. **Weighted Composite Scoring:** Applies human-engineered logic weights (e.g., 50% FIFA points, 40% Market Value, 10% Pedigree) to generate a raw tactical score.
4. **Probability Conversion:** Normalizes the composite scores across all 48 teams to equal a 100% total win probability.

---

## 🤝 Let's Connect

Designed and developed by Poovarasan K

If you are a sports data analyst, UI/UX engineer, or involved in Indian football analytics, I'd love to connect!

* **LinkedIn:** https://www.linkedin.com/in/poovarasan007/

---

*Disclaimer: This project is for educational and analytical purposes. Predictions are based on mathematical models and historical data, not guaranteed outcomes.*

```
