"""Baseline efficiency classifier. Results are diagnostic only; inspect target leakage before deployment."""
from pathlib import Path
import json, joblib, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, balanced_accuracy_score, classification_report, confusion_matrix
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_excel(ROOT/'data'/'Thales_Group_Manufacturing.xlsx')
features=['Operation_Mode','Temperature_C','Vibration_Hz','Power_Consumption_kW','Network_Latency_ms','Packet_Loss_%','Quality_Control_Defect_Rate_%','Production_Speed_units_per_hr','Predictive_Maintenance_Score','Error_Rate_%']
X,y=df[features],df['Efficiency_Status']
cat=['Operation_Mode']; num=[c for c in features if c not in cat]
prep=ColumnTransformer([('cat',OneHotEncoder(handle_unknown='ignore'),cat),('num',SimpleImputer(strategy='median'),num)])
model=Pipeline([('prep',prep),('classifier',RandomForestClassifier(n_estimators=200,max_depth=10,min_samples_leaf=3,class_weight='balanced_subsample',n_jobs=-1,random_state=42))])
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=42,stratify=y)
model.fit(Xtr,ytr); pred=model.predict(Xte)
metrics={'accuracy':accuracy_score(yte,pred),'balanced_accuracy':balanced_accuracy_score(yte,pred),'classification_report':classification_report(yte,pred,output_dict=True),'confusion_matrix':confusion_matrix(yte,pred,labels=['High','Medium','Low']).tolist(),'labels':['High','Medium','Low'],'warning':'Near-perfect results may indicate target construction/leakage. Do not treat as external validity.'}
(ROOT/'models').mkdir(exist_ok=True)
joblib.dump({'pipeline':model,'features':features},ROOT/'models'/'efficiency_classifier.joblib')
(ROOT/'reports'/'model_metrics.json').write_text(json.dumps(metrics,indent=2))
print(json.dumps({k:v for k,v in metrics.items() if k not in ['classification_report']},indent=2))
print(classification_report(yte,pred))
