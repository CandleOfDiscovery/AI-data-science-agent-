from typing import Any, Literal
from pydantic import BaseModel, Field

CleaningActionType = Literal['drop_duplicates','fill_missing_mean','fill_missing_median','fill_missing_mode','remove_outliers_iqr','remove_outliers_zscore','drop_column','rename_column','convert_type']

class CleaningAction(BaseModel):
    action: CleaningActionType
    column: str | None = None
    enabled: bool = True
    new_name: str | None = None
    dtype: str | None = None

class ProfileRequest(BaseModel):
    dataset_path: str

class ProfileResult(BaseModel):
    rows: int
    columns: int
    missing_values: int
    duplicate_rows: int
    numeric_columns: list[str]
    categorical_columns: list[str]
    missing_by_column: dict[str, int]
    null_percentages: dict[str, float]
    unique_counts: dict[str, int]
    outlier_counts: dict[str, int]
    descriptive_statistics: dict[str, Any]
    correlations: dict[str, Any]
    correlation_warnings: list[str] = Field(default_factory=list)

class PlanResult(BaseModel):
    summary: str
    quality_issues: list[str]
    cleaning_plan: list[CleaningAction]

class AnalysisRecord(BaseModel):
    id: str
    filename: str
    status: str
    profile: dict[str, Any] | None = None
    plan: dict[str, Any] | None = None
    charts: list[dict[str, str]] = []
    ml: dict[str, Any] | None = None
    report: dict[str, str] | None = None
    timeline: list[str] = []
