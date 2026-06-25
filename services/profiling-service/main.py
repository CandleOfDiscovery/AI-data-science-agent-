from fastapi import FastAPI
from shared.schemas.models import ProfileRequest
from shared.utils.data import read_dataset
import numpy as np

app = FastAPI(title='Profiling Service')

@app.post('/profile')
def profile(req: ProfileRequest):
    df = read_dataset(req.dataset_path)
    num = df.select_dtypes(include=np.number).columns.tolist()
    cat = [c for c in df.columns if c not in num]
    outliers = {}
    for c in num:
        q1, q3 = df[c].quantile([0.25, 0.75]); iqr = q3 - q1
        outliers[c] = int(((df[c] < q1 - 1.5*iqr) | (df[c] > q3 + 1.5*iqr)).sum()) if iqr else 0
    corr = df[num].corr(numeric_only=True).fillna(0).round(3).to_dict() if len(num) > 1 else {}
    warnings = [f'{a} and {b} are highly correlated ({corr[a][b]:.2f})' for a in corr for b in corr[a] if a < b and abs(corr[a][b]) >= .85]
    return {
        'rows': len(df), 'columns': len(df.columns), 'missing_values': int(df.isna().sum().sum()),
        'duplicate_rows': int(df.duplicated().sum()), 'numeric_columns': num, 'categorical_columns': cat,
        'missing_by_column': {k:int(v) for k,v in df.isna().sum().items()},
        'null_percentages': {k: round(float(v)*100,2) for k,v in df.isna().mean().items()},
        'unique_counts': {k:int(v) for k,v in df.nunique(dropna=True).items()}, 'outlier_counts': outliers,
        'descriptive_statistics': df.describe(include='all').replace({np.nan: None}).to_dict(),
        'correlations': corr, 'correlation_warnings': warnings}
