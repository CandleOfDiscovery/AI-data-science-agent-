from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
from shared.utils.data import read_dataset
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, seaborn as sns

app=FastAPI(title='Visualization Service')
class VizRequest(BaseModel): dataset_path:str; analysis_id:str; output_dir:str='/app/storage/reports'
def save(fig,path): Path(path).parent.mkdir(parents=True,exist_ok=True); fig.tight_layout(); fig.savefig(path,dpi=150); plt.close(fig); return path
@app.post('/visualize')
def visualize(req:VizRequest):
    df=read_dataset(req.dataset_path); out=Path(req.output_dir)/req.analysis_id/'charts'; charts=[]
    nums=df.select_dtypes('number').columns[:5]
    for c in nums:
        fig,ax=plt.subplots(figsize=(6,4)); sns.histplot(df[c].dropna(), ax=ax); charts.append({'title':f'{c} histogram','url':save(fig,out/f'{c}_hist.png')})
        fig,ax=plt.subplots(figsize=(6,4)); sns.boxplot(x=df[c], ax=ax); charts.append({'title':f'{c} boxplot','url':save(fig,out/f'{c}_box.png')})
    for c in df.select_dtypes(exclude='number').columns[:5]:
        fig,ax=plt.subplots(figsize=(6,4)); df[c].value_counts().head(15).plot(kind='bar',ax=ax); charts.append({'title':f'{c} bar chart','url':save(fig,out/f'{c}_bar.png')})
    if len(nums)>1:
        fig,ax=plt.subplots(figsize=(7,5)); sns.heatmap(df[nums].corr(), cmap='mako', ax=ax); charts.append({'title':'Correlation heatmap','url':save(fig,out/'correlation_heatmap.png')})
    fig,ax=plt.subplots(figsize=(7,4)); df.isna().mean().sort_values(ascending=False).head(30).plot(kind='bar',ax=ax); charts.append({'title':'Missing value chart','url':save(fig,out/'missing_values.png')})
    return {'charts':charts}
