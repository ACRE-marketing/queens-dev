import os
from datetime import timedelta
import pandas as pd
from dateutil import tz
from src import pincusco, yimby, cityrealty
from src.common import dedupe_append, ensure_columns
from src.config import OUTPUT_XLSX, DAILY_SHEET, WEEKLY_SHEET, DAILY_WINDOW, WEEKLY_WINDOW

def _load_sheet(path, sheet):
    if not os.path.exists(path):
        return None
    try:
        return pd.read_excel(path, sheet_name=sheet, engine="openpyxl")
    except Exception:
        return None

def _save(path, daily_df, weekly_df):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with pd.ExcelWriter(path, engine="openpyxl", mode="w") as w:
        if daily_df is not None and not daily_df.empty:
            daily_df.to_excel(w, index=False, sheet_name=DAILY_SHEET)
        else:
            pd.DataFrame(columns=["date","title","neighborhood","action","source","link"]).to_excel(w, index=False, sheet_name=DAILY_SHEET)
        if weekly_df is not None and not weekly_df.empty:
            weekly_df.to_excel(w, index=False, sheet_name=WEEKLY_SHEET)
        else:
            pd.DataFrame(columns=["date","title","neighborhood","action","source","link"]).to_excel(w, index=False, sheet_name=WEEKLY_SHEET)

def _fresh_filter(df, window_td):
    if df is None or df.empty:
        return df
    df = df.copy()
    # coerce datetime
    df["date_parsed"] = pd.to_datetime(df["date"], errors="coerce", utc=True)
    cutoff = pd.Timestamp.utcnow() - pd.Timedelta(seconds=window_td.total_seconds())
    return df[df["date_parsed"] >= cutoff].drop(columns=["date_parsed"])

def crawl_all():
    rows = []
    for fn, name in [(pincusco.fetch_recent, "PincusCo"),
                     (yimby.fetch_recent, "YIMBY"),
                     (cityrealty.fetch_recent, "CityRealty")]:
        try:
            rows.extend(fn())
        except Exception as e:
            # still continue other sources
            print(f"[WARN] {name} failed: {e}")
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df = ensure_columns(df)
    # normalize date to ISO (string) already done; ensure no NaNs
    df["neighborhood"] = df["neighborhood"].fillna("Queens")
    return df

def main(mode="daily"):
    new_df = crawl_all()

    # Load existing
    daily_existing = _load_sheet(OUTPUT_XLSX, DAILY_SHEET)
    weekly_existing = _load_sheet(OUTPUT_XLSX, WEEKLY_SHEET)

    # Freshness windows
    daily_df = new_df.copy()
    weekly_df = new_df.copy()

    daily_df = _fresh_filter(daily_df, DAILY_WINDOW)
    weekly_df = _fresh_filter(weekly_df, WEEKLY_WINDOW)

    # Deduplicate against existing logs
    daily_all = dedupe_append(daily_df, daily_existing, ["title", "link"])
    weekly_all = dedupe_append(weekly_df, weekly_existing, ["title", "link"])

    _save(OUTPUT_XLSX, daily_all, weekly_all)
    print(f"Saved {len(daily_df)} daily rows and {len(weekly_df)} weekly rows (post-dedupe totals: daily={len(daily_all)}, weekly={len(weekly_all)}).")

if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "daily"
    main(mode)
