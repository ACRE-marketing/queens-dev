import re
from datetime import datetime, timezone
from dateutil import parser
import pandas as pd

def utcnow():
    return datetime.now(timezone.utc)

def parse_date(dt_str):
    try:
        return parser.parse(dt_str)
    except Exception:
        return None

def is_queens(text, neighborhoods):
    s = (text or "").lower()
    return any(nb in s for nb in neighborhoods)

def infer_action(title, summary, action_dict):
    blob = f"{title or ''} {summary or ''}".lower()
    for label, kws in action_dict.items():
        if any(kw in blob for kw in kws):
            return label
    return "other"

def dedupe_append(df_new: pd.DataFrame, df_existing: pd.DataFrame, subset_cols):
    if df_existing is not None and not df_existing.empty:
        cat = pd.concat([df_existing, df_new], ignore_index=True)
        cat = cat.drop_duplicates(subset=subset_cols, keep="first")
        return cat
    return df_new

def ensure_columns(df: pd.DataFrame):
    # normalized column order
    cols = ["date", "title", "neighborhood", "action", "source", "link"]
    for c in cols:
        if c not in df.columns:
            df[c] = None
    return df[cols]
