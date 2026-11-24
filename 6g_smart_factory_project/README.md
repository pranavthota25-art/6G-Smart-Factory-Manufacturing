# Impact of 6G Network Performance on Manufacturing Efficiency in Smart Factories

An exploratory analytics project using the supplied Thales Group manufacturing workbook (100,000 observations, 14 columns). It includes an interactive Streamlit dashboard and a baseline efficiency classifier.

## Key dataset findings
- 100,000 rows; 14 columns; 50 machine IDs; operating modes: Active, Idle, Maintenance.
- Date range: 1 Jan 2025 to 10 Mar 2025. `Timestamp` is a time-of-day field; the dashboard combines it with `Date`.
- Efficiency labels: Low 77,825 (77.825%), Medium 19,189 (19.189%), High 2,986 (2.986%). Strong class imbalance.
- Mean latency 25.556 ms (range 1–50 ms); mean packet loss 2.493% (range 0–5%).
- Pearson correlations of latency with production speed, defect rate and error rate are -0.001, -0.004 and 0.000 respectively. Packet-loss correlations with those outcomes are -0.007, -0.005 and -0.002.
- Across latency quartiles, mean production speed is 275.9, 277.5, 274.2 and 276.1 units/hour: no monotonic degradation pattern.

## Important interpretation limitation
The supplied dataset does **not** show a meaningful marginal relationship between the network metrics and the production/quality outcomes. It therefore does not support a claim that higher latency or packet loss caused lower manufacturing efficiency. It may be synthetic or generated with independent variables. No validated network threshold or causal effect should be claimed from this workbook alone.

A baseline random-forest classifier reaches 99.99% accuracy on a stratified random holdout. This suspiciously high score should be treated as a target-construction/leakage warning, not as proof of deployable AI performance. Before production use, inspect how `Efficiency_Status` was generated, use time- or machine-grouped holdouts, and test on independent factory data.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
Open the local URL printed by Streamlit (usually http://localhost:8501).

## Deploy on Streamlit Community Cloud
1. Create a GitHub repository and upload this project folder (including `data/Thales_Group_Manufacturing.xlsx`).
2. Sign in to Streamlit Community Cloud with GitHub and choose **New app**.
3. Select the repository, branch `main`, and main file path `app.py`.
4. Deploy. Copy the generated `https://...streamlit.app` URL into the submission form.

## Publish on GitHub
Create an empty repository, then from this folder run:
```bash
git init
git add .
git commit -m "Build 6G smart factory analytics project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```
Replace the remote URL with the repository URL created under your own GitHub account. Do not submit the example URL.

## Project contents
- `app.py` — interactive Streamlit dashboard
- `src/train_model.py` — reproducible baseline classifier training
- `models/efficiency_classifier.joblib` — trained baseline pipeline
- `reports/model_metrics.json` — holdout metrics
- `reports/research_paper.md` — research paper draft
- `reports/executive_summary.md` — concise stakeholder brief
- `reports/video_scripts.md` — recording scripts for both required videos
- `data/` — supplied workbook

## Responsible use
This is an academic exploratory analysis, not a validated industrial control system. Do not use these results to set network SLAs, safety limits or maintenance actions without real operational validation.
