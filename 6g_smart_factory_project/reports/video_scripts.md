# Recording scripts for submission videos

## Video 1 — Project explanation (target 4–6 minutes)

**Opening (0:00–0:30)**
"Hello, my name is Pranav. My project is titled Impact of 6G Network Performance on Manufacturing Efficiency in Smart Factories. The objective is to explore whether network latency and packet loss are associated with manufacturing efficiency, production speed and quality outcomes."

**Problem and dataset (0:30–1:20)**
"Smart factories depend on timely communication between machines, sensors and AI systems. I used the supplied Thales Group Manufacturing Excel dataset, which contains 100,000 observations and 14 variables, including machine operating conditions, network latency, packet loss, production speed, defect rate, error rate and an efficiency class. The data covers January to March 2025 and includes 50 machine IDs and Active, Idle and Maintenance modes."

**Methodology (1:20–2:20)**
"I first checked the data structure and efficiency-class distribution. Then I profiled latency and packet loss, compared network metrics with speed and quality outcomes, examined operating modes, and calculated correlations. I also trained a baseline Random Forest classifier and created a Streamlit dashboard with date, mode, efficiency, latency and packet-loss filters."

**Dashboard walkthrough (2:20–4:10)**
[Share screen: open deployed Streamlit app.] "The overview displays record count, mean latency, mean packet loss and average production speed. The network section shows latency and packet-loss distributions and daily trends. The efficiency section compares classes by operation mode and plots latency against production speed. The quality panel explores packet loss against error and defect rates. The final sections show latency bands, operating-mode summaries and a correlation matrix. Users can filter the records and download the filtered data as CSV."

**Findings and honest interpretation (4:10–5:20)**
"The dataset has 77.825 percent Low, 19.189 percent Medium and 2.986 percent High efficiency records. Mean latency is about 25.56 milliseconds and mean packet loss is about 2.49 percent. In this dataset, latency and packet loss have correlations very close to zero with production speed, defect rate and error rate. Therefore, I cannot claim that network degradation caused lower efficiency or set a validated 6G tolerance threshold. The baseline classifier's very high score also needs a target-leakage audit and independent validation."

**Closing (5:20–5:45)**
"My recommendation is to collect synchronized factory and network telemetry and conduct controlled experiments before making network investment or operational decisions. Thank you."

## Video 2 — Internship experience & feedback (target 2–3 minutes)

"Hello, my name is Pranav. During my internship experience, I worked on a manufacturing analytics project focused on the relationship between network performance and smart-factory efficiency. This project helped me understand how to approach an industry-oriented problem, inspect a large dataset, clean and prepare data, perform exploratory analysis, interpret correlations, build a machine-learning baseline and develop an interactive Streamlit dashboard.

One of my key learnings was that data analysis is not just about producing high model scores or attractive charts. It is equally important to question whether the data supports the hypothesis. In this project, latency and packet loss showed almost no relationship with the measured production and quality outcomes. I have highlighted that limitation instead of making unsupported claims. I also learned that an unusually high model score can indicate target leakage and must be validated carefully.

The project improved my skills in Python, pandas, data visualization, scikit-learn, Streamlit, research documentation and communicating technical findings. I appreciated the opportunity to work on a practical manufacturing use case. My feedback is that more access to real-time industrial telemetry, domain-expert discussions and opportunities to validate models with plant data would make the learning experience even stronger. Overall, this internship helped me connect analytical concepts with a real business and technology problem. Thank you."

**Recording note:** Record these in your own voice and show the actual project screen for the explanation video. Do not claim an internship activity, supervisor feedback or company endorsement that did not happen. Adjust the internship reflection to match your real experience.
