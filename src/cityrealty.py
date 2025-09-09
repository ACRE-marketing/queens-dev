import requests
from bs4 import BeautifulSoup
from .common import parse_date, is_queens, infer_action
from .config import QUEENS_NEIGHBORHOODS, ACTION_KEYWORDS

BASE = "https://www.cityrealty.com"

def fetch_recent():
    """
    CityRealty news feed; we scan the news hub & filter to Queens.
    """
    url = f"{BASE}/nyc/market-insight"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")

    items = []
    for card in soup.select("article, .article-card, .post-item"):
        a = card.select_one("a")
        if not a or not a.get("href"): 
            continue
        link = a["href"]
        if link.startswith("/"):
            link = BASE + link
        title = a.get_text(strip=True)
        meta = card.get_text(" ", strip=True)

        # Date
        time_el = card.find("time")
        date_str = time_el.get("datetime") if time_el and time_el.has_attr("datetime") else (time_el.get_text(strip=True) if time_el else "")
        dt = parse_date(date_str)

        # Queens filter
        if not (is_queens(title, QUEENS_NEIGHBORHOODS) or is_queens(meta, QUEENS_NEIGHBORHOODS)):
            continue

        action = infer_action(title, meta, ACTION_KEYWORDS)
        items.append({
            "date": dt.isoformat() if dt else None,
            "title": title,
            "neighborhood": "Queens",
            "action": action,
            "source": "CityRealty",
            "link": link
        })
    return items
