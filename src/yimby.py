import requests
from bs4 import BeautifulSoup
from .common import parse_date, is_queens, infer_action
from .config import QUEENS_NEIGHBORHOODS, ACTION_KEYWORDS

BASE = "https://newyorkyimby.com"

def fetch_recent():
    """
    Pull recent posts; YIMBY typically uses /category/queens or city/queens tags.
    We try homepage + queens category for coverage.
    """
    urls = [
        f"{BASE}/category/queens",
        BASE
    ]
    items = []
    seen = set()

    for url in urls:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        for card in soup.select("article"):
            a = card.select_one("h2 a, h3 a")
            if not a: 
                continue
            title = a.get_text(strip=True)
            link = a["href"]
            if link in seen:
                continue
            seen.add(link)

            date_el = card.select_one("time")
            date_str = date_el.get("datetime") if date_el and date_el.has_attr("datetime") else (date_el.get_text(strip=True) if date_el else "")
            dt = parse_date(date_str)

            excerpt = card.get_text(" ", strip=True)
            if not (is_queens(title, QUEENS_NEIGHBORHOODS) or is_queens(excerpt, QUEENS_NEIGHBORHOODS)):
                continue

            action = infer_action(title, excerpt, ACTION_KEYWORDS)
            items.append({
                "date": dt.isoformat() if dt else None,
                "title": title,
                "neighborhood": "Queens",
                "action": action,
                "source": "YIMBY",
                "link": link
            })
    return items
