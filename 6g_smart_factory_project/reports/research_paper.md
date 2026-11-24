# Impact of 6G Network Performance on Manufacturing Efficiency in Smart Factories

## Abstract
This project examines whether network latency and packet loss are associated with manufacturing efficiency, production speed and quality outcomes in a supplied smart-factory dataset. The workbook contains 100,000 observations and 14 fields covering 50 machine identifiers and three operating modes from 1 January to 10 March 2025. Exploratory analysis finds mean latency of 25.556 ms and mean packet loss of 2.493%. However, Pearson correlations between latency and production speed, defect rate and error rate are -0.001, -0.004 and 0.000; corresponding packet-loss correlations are -0.007, -0.005 and -0.002. Latency quartiles also show no monotonic production-speed decline. A random-forest classifier achieves 99.99% accuracy on a random holdout, but this near-perfect result raises concerns about target construction or information leakage. The available evidence therefore does not establish that network degradation reduces manufacturing efficiency. The project provides a reproducible dashboard and recommends controlled network experiments and independent factory validation before operational conclusions are drawn.

**Keywords:** 6G, smart factory, Industry 4.0, latency, packet loss, manufacturing analytics, efficiency classification.

## 1. Introduction
Smart factories connect machines, sensors, controllers and AI services through communication networks. Low latency and reliable data exchange are important design goals for time-sensitive automation. A network-centric investigation can help distinguish communication issues from mechanical or process issues. The present analysis tests whether the supplied dataset contains measurable associations between network performance and production outcomes. The title refers to 6G-enabled manufacturing as the intended application context; the workbook itself does not establish that observations were collected over a deployed 6G network.

## 2. Problem statement and objectives
The study asks whether latency and packet loss are associated with (i) efficiency class, (ii) production speed, (iii) error rate and (iv) quality-control defect rate, and whether these patterns differ by operation mode. It also builds a baseline classifier for the supplied `Efficiency_Status` label and an interactive dashboard for exploration.

## 3. Dataset and variables
The Excel workbook contains 100,000 rows and 14 columns: Date, Timestamp, Machine_ID, Operation_Mode, Temperature_C, Vibration_Hz, Power_Consumption_kW, Network_Latency_ms, Packet_Loss_%, Quality_Control_Defect_Rate_%, Production_Speed_units_per_hr, Predictive_Maintenance_Score, Error_Rate_% and Efficiency_Status. There are 50 distinct machine IDs and three operation modes: Active, Idle and Maintenance. The date range is 1 January 2025 through 10 March 2025. The `Timestamp` field is a time-of-day value and is combined with Date for time-series display. The dataset contains no explicit network-slice identifier, radio conditions, retransmission count, jitter, throughput, control-loop deadline misses or experimental treatment indicator.

## 4. Methodology
The analysis uses descriptive statistics, histograms, Pearson correlation, latency and packet-loss quartile comparisons, and grouping by operating mode. The Streamlit application provides date, operation-mode, efficiency-class, latency and packet-loss filters. A random-forest classifier is trained using a stratified 80/20 random train-test split with a fixed random seed. Categorical operation mode is one-hot encoded; numeric missing values are median-imputed. The model is included as a baseline diagnostic only. A random row split is not a robust test of generalization across time or machines.

## 5. Results
### 5.1 Efficiency-label distribution
Low efficiency accounts for 77,825 records (77.825%), Medium for 19,189 (19.189%) and High for 2,986 (2.986%). This is a substantial class imbalance; accuracy alone is insufficient to assess a model.

### 5.2 Network profile
Mean network latency is 25.556 ms (standard deviation 14.121; minimum 1; maximum 50). The median is 25.536 ms. Mean packet loss is 2.493% (standard deviation 1.443; minimum 0; maximum 5), with median 2.488%.

### 5.3 Network metrics and manufacturing outcomes
Pearson correlation between latency and production speed is -0.001; latency and defect rate is -0.004; latency and error rate is 0.000. Packet-loss correlations with production speed, defect rate and error rate are -0.007, -0.005 and -0.002. These values are effectively zero in this dataset. Dividing latency into quartiles gives mean production speeds of 275.892, 277.454, 274.188 and 276.131 units/hour from lowest to highest latency quartile. This does not show a monotonic decline. The share of High labels ranges only from 2.8% to 3.1% across latency quartiles. Packet-loss quartiles likewise show no clear deterioration in speed, defects or errors.

### 5.4 Operating modes
The three modes have similar average network measurements: Active mean latency 25.539 ms and packet loss 2.493%; Idle 25.640 ms and 2.501%; Maintenance 25.502 ms and 2.480%. Average production speed is 276.199 units/hour in Active, 274.126 in Idle and 277.544 in Maintenance. These descriptive differences do not establish network sensitivity because mode, machine state and production activity are not controlled experimentally.

### 5.5 Baseline classification
The random-forest model achieved 99.99% accuracy and approximately 99.94% balanced accuracy on a stratified random 20% holdout. It misclassified only two records in the 20,000-row test set. Such an unusually high result, particularly alongside negligible pairwise network correlations, requires investigation. The efficiency label may be directly derived from other recorded process fields, or the random split may allow near-duplicate/time-adjacent records into both partitions. The score must not be represented as proven real-world predictive performance. A grouped split by machine and chronological validation are required, along with an audit of label-generation rules.

## 6. Discussion
The original hypothesis—that degraded network performance may reduce manufacturing efficiency—is technically plausible, but the supplied workbook does not demonstrate it. The near-zero associations suggest that network metrics may have been generated independently of the measured production outcomes, or that relevant dynamics are not captured by the available variables. Aggregate latency and packet-loss percentages may also be insufficient to describe real-time control performance; jitter, burst loss, retransmissions, deadline misses, slice congestion, traffic priority and control-loop timing would provide more diagnostic value.

## 7. Recommendations
1. Obtain validated plant data with network telemetry synchronized to machine and production timestamps.
2. Record latency percentiles (p50, p95, p99), jitter, burst packet loss, retransmissions, throughput and deadline misses—not only averages.
3. Run controlled tests by varying latency and packet loss while holding machine, product, workload and operating mode constant.
4. Define outcomes such as cycle-time deviation, missed control deadlines, scrap, rework, downtime and throughput.
5. Compare network slices and QoS policies using randomized or carefully matched trials.
6. Validate models using time-based splits and machine-held-out tests; audit the efficiency-label definition and remove target leakage.
7. Treat any latency or packet-loss threshold as provisional until validated for the specific process and control-loop requirements.

## 8. Limitations
The workbook's provenance and data-generation process are not documented. It does not identify a verified 6G deployment or network slicing configuration. Observational correlations cannot establish causality. The efficiency classes are highly imbalanced. The random holdout may overstate model performance due to temporal or machine-level dependence and potential label leakage. No external validation dataset is supplied.

## 9. Conclusion
This project delivers an interactive analytics workflow for exploring network and manufacturing metrics. Its central finding is a limitation of the supplied evidence: latency and packet loss show almost no marginal association with speed, defects or errors. Accordingly, the analysis cannot quantify a causal 6G efficiency impact or claim validated tolerance thresholds. The most valuable next step is to collect synchronized, experimentally varied network and production measurements and validate the findings across machines and factories.

## Appendix: reproducibility
Install dependencies using `pip install -r requirements.txt`; run `streamlit run app.py` to open the dashboard; run `python src/train_model.py` to reproduce the baseline classifier and metrics. The workbook used for this report is in `data/Thales_Group_Manufacturing.xlsx`.
