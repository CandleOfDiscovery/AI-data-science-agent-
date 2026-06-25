import os, json, requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title='Planner Service')
SYSTEM = 'You are a senior data scientist. You never manipulate data. You only analyze profiling results and generate structured recommendations. Return valid JSON only. Do not include markdown.'
class PlanRequest(BaseModel): profile: dict
class OpenRouterClient:
    def __init__(self):
        self.key=os.getenv('OPENROUTER_API_KEY',''); self.model=os.getenv('OPENROUTER_MODEL','nvidia/nemotron-3-ultra-550b-a55b:free')
    def plan(self, profile):
        if not self.key: return fallback(profile)
        r=requests.post('https://openrouter.ai/api/v1/chat/completions',headers={'Authorization':f'Bearer {self.key}','Content-Type':'application/json'},json={'model':self.model,'messages':[{'role':'system','content':SYSTEM},{'role':'user','content':json.dumps(profile)}],'response_format':{'type':'json_object'}},timeout=60)
        r.raise_for_status(); return json.loads(r.json()['choices'][0]['message']['content'])
def fallback(p):
    actions=[]; issues=[]
    if p.get('duplicate_rows',0): actions.append({'action':'drop_duplicates','enabled':True}); issues.append('Duplicate rows detected')
    for c,n in p.get('missing_by_column',{}).items():
        if n: actions.append({'action':'fill_missing_median' if c in p.get('numeric_columns',[]) else 'fill_missing_mode','column':c,'enabled':True}); issues.append(f'Missing values in {c}')
    for c,n in p.get('outlier_counts',{}).items():
        if n: actions.append({'action':'remove_outliers_iqr','column':c,'enabled':False}); issues.append(f'Potential outliers in {c}')
    return {'summary':'Deterministic fallback plan generated from profiling results.','quality_issues':issues,'cleaning_plan':actions}
@app.post('/plan')
def plan(req: PlanRequest): return OpenRouterClient().plan(req.profile)
