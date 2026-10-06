"""Scrape the public contribution calendar (no token) into data/contributions.json."""
import json
import os
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GH_USER", "mesrobyan77")
OUT = Path(__file__).resolve().parent.parent / "data" / "contributions.json"

html = requests.get(
    f"https://github.com/users/{USERNAME}/contributions",
    headers={"User-Agent": "Mozilla/5.0 (profile-art)"},
    timeout=30,
)
html.raise_for_status()
soup = BeautifulSoup(html.text, "html.parser")

tips = {t.get("for"): t.get_text(" ", strip=True) for t in soup.find_all("tool-tip")}
days = []
for td in soup.select("td.ContributionCalendar-day"):
    d = td.get("data-date")
    if not d:
        continue
    tip = tips.get(td.get("id"), "")
    m = re.match(r"(\d+)\s+contribution", tip)
    days.append({"date": d, "count": int(m.group(1)) if m else 0, "level": int(td.get("data-level", 0))})
days.sort(key=lambda x: x["date"])
if not days:
    raise SystemExit("No contribution cells found; GitHub markup may have changed.")

total = sum(x["count"] for x in days)
best = max(days, key=lambda x: x["count"])

longest = run = 0
for x in days:
    run = run + 1 if x["count"] > 0 else 0
    longest = max(longest, run)

# current streak: allow today to be empty if yesterday had activity
cur = 0
for x in reversed(days):
    if x["count"] > 0:
        cur += 1
    elif x is days[-1]:
        continue
    else:
        break

monthly = {}
for x in days:
    monthly[x["date"][:7]] = monthly.get(x["date"][:7], 0) + x["count"]

OUT.parent.mkdir(exist_ok=True)
OUT.write_text(
    json.dumps(
        {
            "username": USERNAME,
            "total": total,
            "current_streak": cur,
            "longest_streak": longest,
            "best_day": best,
            "monthly": monthly,
            "days": days,
        },
        indent=1,
    )
)
print(f"{USERNAME}: {total} contributions, streak {cur}, longest {longest}")
