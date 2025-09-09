# Queens Dev News (PincusCo + YIMBY + CityRealty)

Daily + weekly scraper that appends Queens-only development news to a single Excel:
- `data/output/queens_dev_news.xlsx`
  - Sheet `daily_log` = last 48h (deduped)
  - Sheet `weekly_rollup` = last 7 days (deduped)

## How to use

1) Create this repo and copy all files.
2) In the repo settings → Actions → General:
   - Set "Workflow permissions" to **Read and write permissions** (needed to push the Excel).
3) Go to "Actions" tab, run the workflow manually once (Workflow dispatch) to create the Excel.
4) The workflow will also run on schedule:
   - Daily around 08:00 New York (cron `0 12 * * *` UTC)
   - Weekly Monday 08:05 New York (cron `5 12 * * 1` UTC)

## Notes
- If any site changes HTML or adds paywalls/anti-bot, tweak selectors in `src/*.py`.
- This project respects light scraping; consider adding per-source RSS or public APIs if available.
