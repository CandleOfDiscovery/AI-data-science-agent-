from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
app=FastAPI(title='Report Service')
class ReportRequest(BaseModel): analysis_id:str; profile:dict; plan:dict; charts:list[dict]=[]; ml:dict; output_dir:str='/app/storage/reports'
@app.post('/report')
def report(req:ReportRequest):
    d=Path(req.output_dir)/req.analysis_id; d.mkdir(parents=True,exist_ok=True)
    html=d/'report.html'; pdf=d/'report.pdf'
    body=f"""<html><body><h1>AI Data Science Agent Report</h1><h2>Executive Summary</h2><p>{req.plan.get('summary','')}</p><h2>Dataset Overview</h2><p>{req.profile.get('rows')} rows, {req.profile.get('columns')} columns</p><h2>Quality Findings</h2><ul>{''.join(f'<li>{x}</li>' for x in req.plan.get('quality_issues',[]))}</ul><h2>Cleaning Actions</h2><ul>{''.join(f'<li>{a}</li>' for a in req.plan.get('cleaning_plan',[]))}</ul><h2>ML Recommendations</h2><p>{req.ml.get('detected_task')}</p></body></html>"""
    html.write_text(body)
    styles=getSampleStyleSheet(); doc=SimpleDocTemplate(str(pdf)); story=[Paragraph('AI Data Science Agent Report',styles['Title']),Spacer(1,12),Paragraph(req.plan.get('summary',''),styles['BodyText'])]; doc.build(story)
    return {'html_path':str(html),'pdf_path':str(pdf)}
