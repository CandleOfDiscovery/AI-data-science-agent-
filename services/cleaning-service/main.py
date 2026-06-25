from fastapi import FastAPI
from pydantic import BaseModel
from shared.schemas.models import CleaningAction
from shared.utils.data import read_dataset, write_dataset

app=FastAPI(title='Cleaning Service')
class CleanRequest(BaseModel): dataset_path:str; output_path:str; actions:list[CleaningAction]
@app.post('/clean')
def clean(req:CleanRequest):
    df=read_dataset(req.dataset_path); lineage=['Original Dataset']
    for a in [x for x in req.actions if x.enabled]:
        c=a.column
        if a.action=='drop_duplicates': before=len(df); df=df.drop_duplicates(); lineage.append(f'Removed {before-len(df)} duplicates')
        elif a.action=='fill_missing_mean' and c: df[c]=df[c].fillna(df[c].mean()); lineage.append(f'Filled {c} with mean')
        elif a.action=='fill_missing_median' and c: df[c]=df[c].fillna(df[c].median()); lineage.append(f'Filled {c} with median')
        elif a.action=='fill_missing_mode' and c: df[c]=df[c].fillna(df[c].mode(dropna=True).iloc[0] if not df[c].mode(dropna=True).empty else 'Unknown'); lineage.append(f'Filled {c} with mode')
        elif a.action=='remove_outliers_iqr' and c: q1,q3=df[c].quantile([.25,.75]); i=q3-q1; before=len(df); df=df[(df[c]>=q1-1.5*i)&(df[c]<=q3+1.5*i)]; lineage.append(f'Removed {before-len(df)} outliers from {c}')
        elif a.action=='drop_column' and c: df=df.drop(columns=[c]); lineage.append(f'Dropped {c}')
        elif a.action=='rename_column' and c and a.new_name: df=df.rename(columns={c:a.new_name}); lineage.append(f'Renamed {c} to {a.new_name}')
        elif a.action=='convert_type' and c and a.dtype: df[c]=df[c].astype(a.dtype); lineage.append(f'Converted {c} to {a.dtype}')
    return {'clean_path':write_dataset(df, req.output_path),'lineage':lineage,'rows':len(df),'columns':len(df.columns)}
