import requests
from bs4 import BeautifulSoup
from .common import parse_date, is_queens, infer_action
from .config import QUEENS_NEIGHBORHOODS, ACTION_KEYWORDS

BASE = "https://www.pincusco.com"  # site root

def fetch_recent():
    """
    Light, robust listing scrape of recent posts.
    NOTE: If PincusCo changes markup/paywalls, adjust selectors below accordingly.
    """
    url = f"{BASE}/category/real-estate-news/"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")

    items = []
    for card in soup.select("article"):
        a = card.select_one("h2 a")
        if not a:
            continue
        title = a.get_text(strip=True)
        link = a["href"]
        date_el = card.select_one("time")
        date_str = date_el.get("datetime") if date_el else (date_el.get_text(strip=True) if date_el else "")
        dt = parse_date(date_str)

        # neighborhood guess from title
        neighborhood = None
        if is_queens(title, QUEENS_NEIGHBORHOODS):
            neighborhood = "Queens"
        # Try excerpt
        excerpt = card.select_one(".entry-summary, .post-excerpt")
        summary = excerpt.get_text(" ", strip=True) if excerpt else ""

        # Secondary Queens check
        if not neighborhood and is_queens(summary, QUEENS_NEIGHBORHOODS):
            neighborhood = "Queens"

        if neighborhood:
            action = infer_action(title, summary, ACTION_KEYWORDS)
            items.append({
                "date": dt.isoformat() if dt else None,
                "title": title,
                "neighborhood": neighborhood,
                "action": action,
                "source": "PincusCo",
                "link": link
            })
    return items
