from pathlib import Path
import pandas as pd

def read_dataset(path: str) -> pd.DataFrame:
    p = Path(path)
    if p.suffix.lower() == '.csv':
        return pd.read_csv(p)
    if p.suffix.lower() in {'.xlsx', '.xls'}:
        return pd.read_excel(p)
    raise ValueError('Unsupported file type')

def write_dataset(df: pd.DataFrame, path: str) -> str:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(p, index=False)
    return str(p)
