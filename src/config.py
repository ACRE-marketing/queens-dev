from datetime import timedelta

# Borough filter
QUEENS_NEIGHBORHOODS = {
    "long island city", "lic", "astoria", "sunnyside", "woodside", "rego park",
    "forest hills", "elmhurst", "jackson heights", "flushing", "college point",
    "fresh meadows", "bayside", "douglaston", "little neck", "jamaica",
    "briarwood", "kew gardens", "ozone park", "rockaway", "howard beach",
    "ridgewood", "maspeth", "middle village", "glendale", "corona", "whitestone",
    "queens"
}

# Action keywords to tag items
ACTION_KEYWORDS = {
    "land": ["buy", "purchase", "acquire", "acquisition", "sell", "sale", "sold"],
    "permit": ["permit", "dob", "filing", "filed", "approved", "issued", "alt-1", "nb", "new building"],
    "groundbreaking": ["groundbreaking", "break ground", "construction start", "topped out", "top out", "foundation work"],
    "financing": ["loan", "construction loan", "mortgage", "refi", "financing"]
}

# Freshness windows
DAILY_WINDOW = timedelta(days=2)   # keep last 48h to be safe
WEEKLY_WINDOW = timedelta(days=7)

OUTPUT_XLSX = "data/output/queens_dev_news.xlsx"
DAILY_SHEET = "daily_log"
WEEKLY_SHEET = "weekly_rollup"
