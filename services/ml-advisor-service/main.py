from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI(title='ML Advisor Service')
class MLRequest(BaseModel): profile:dict; target_column:str|None=None
@app.post('/recommend')
def recommend(req:MLRequest):
    p=req.profile; target=req.target_column
    if target and target in p.get('numeric_columns',[]): task='Regression'; models=['Random Forest','XGBoost','LightGBM','CatBoost','Linear Regression']
    elif target: task='Classification'; models=['Logistic Regression','Random Forest','XGBoost','CatBoost','SVM']
    else: task='Clustering'; models=['KMeans','DBSCAN','HDBSCAN']
    return {'detected_task':task,'recommended_models':[{'name':m,'strengths':['Strong baseline','Works well with tabular data'],'weaknesses':['Requires validation and tuning'],'expected_performance':'Good with appropriate preprocessing'} for m in models]}
