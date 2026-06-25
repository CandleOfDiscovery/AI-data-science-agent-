import os, uuid, shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import httpx

app=FastAPI(title='AI Data Science Agent API Gateway')
app.add_middleware(CORSMiddleware, allow_origins=os.getenv('CORS_ORIGINS','http://localhost:3000').split(','), allow_methods=['*'], allow_headers=['*'])
UPLOAD=Path('/app/storage/uploads'); REPORT=Path('/app/storage/reports'); UPLOAD.mkdir(parents=True,exist_ok=True); REPORT.mkdir(parents=True,exist_ok=True)
ANALYSES={}
SERV={'profile':'http://profiling-service:8000/profile','plan':'http://planner-service:8000/plan','clean':'http://cleaning-service:8000/clean','viz':'http://visualization-service:8000/visualize','ml':'http://ml-advisor-service:8000/recommend','report':'http://report-service:8000/report'}
@app.post('/upload')
async def upload(file:UploadFile=File(...)):
    ext=Path(file.filename).suffix.lower()
    if ext not in {'.csv','.xlsx'}: raise HTTPException(400,'Only CSV and XLSX files are supported')
    aid=str(uuid.uuid4()); safe=f'{aid}{ext}'; dest=UPLOAD/safe
    with dest.open('wb') as f: shutil.copyfileobj(file.file,f)
    ANALYSES[aid]={'id':aid,'filename':file.filename,'dataset_path':str(dest),'status':'uploaded','timeline':['Uploading']}
    return ANALYSES[aid]
@app.post('/analyze')
async def analyze(payload:dict):
    aid=payload.get('analysis_id'); rec=ANALYSES.get(aid)
    if not rec: raise HTTPException(404,'Analysis not found')
    async with httpx.AsyncClient(timeout=120) as c:
        rec['timeline']+=['Profiling']; profile=(await c.post(SERV['profile'],json={'dataset_path':rec['dataset_path']})).json()
        rec['timeline']+=['Planning']; plan=(await c.post(SERV['plan'],json={'profile':profile})).json()
        rec['timeline']+=['Cleaning']; clean_path=str(UPLOAD/f'{aid}_clean.csv'); clean=(await c.post(SERV['clean'],json={'dataset_path':rec['dataset_path'],'output_path':clean_path,'actions':plan.get('cleaning_plan',[])})).json()
        rec['timeline']+=['Visualizing']; charts=(await c.post(SERV['viz'],json={'dataset_path':clean_path,'analysis_id':aid})).json()['charts']
        rec['timeline']+=['Generating Report']; ml=(await c.post(SERV['ml'],json={'profile':profile,'target_column':payload.get('target_column')})).json()
        rep=(await c.post(SERV['report'],json={'analysis_id':aid,'profile':profile,'plan':plan,'charts':charts,'ml':ml})).json()
    rec.update(status='complete',profile=profile,plan=plan,cleaning=clean,charts=charts,ml=ml,report=rep); rec['timeline'].append('Complete'); return rec
@app.get('/analysis/{aid}')
def get_analysis(aid:str):
    if aid not in ANALYSES: raise HTTPException(404,'Analysis not found')
    return ANALYSES[aid]
@app.get('/report/{aid}')
def get_report(aid:str):
    path=ANALYSES.get(aid,{}).get('report',{}).get('html_path')
    if not path: raise HTTPException(404,'Report not found')
    return FileResponse(path, media_type='text/html')
@app.get('/download/{aid}')
def download(aid:str):
    path=ANALYSES.get(aid,{}).get('cleaning',{}).get('clean_path')
    if not path: raise HTTPException(404,'Clean dataset not found')
    return FileResponse(path, filename='clean_dataset.csv')
