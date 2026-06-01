"""
=============================================================
  DIAGNOSTIC SCRIPT — Run this ONCE
  It fetches real HTML and shows actual class names
  So we can write CORRECT selectors
=============================================================
  Run: python diagnose.py
  Cost: Only 2 API credits total
=============================================================
"""

import requests
import re
from bs4 import BeautifulSoup

# ── Fill these in ──────────────────────────
SCRAPER_API_KEY = "your_scraperapi_key_here"
# ──────────────────────────────────────────

def fetch(url):
    api_url = (
        f"http://api.scraperapi.com"
        f"?api_key={SCRAPER_API_KEY}"
        f"&url={requests.utils.quote(url, safe='')}"
        f"&render=true"
        f"&country_code=in"
    )
    print(f"Fetching: {url[:60]}...")
    r = requests.get(api_url, timeout=90)
    print(f"Status: {r.status_code}, Size: {len(r.text)} chars")
    return r.text if r.status_code == 200 else None

def analyze(html, site):
    soup = BeautifulSoup(html, "html.parser")

    print(f"\n{'='*60}")
    print(f"  {site} — HTML Analysis")
    print(f"{'='*60}")

    # Save full HTML
    fname = f"{site.lower()}_live.html"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Full HTML saved to: {fname}")

    # Find all unique class names
    all_classes = []
    for tag in soup.find_all(True):
        classes = tag.get("class", [])
        all_classes.extend(classes)

    unique = list(set(all_classes))
    print(f"\n📋 Total unique CSS classes found: {len(unique)}")

    # Find price-related classes (contain ₹ or numbers)
    print(f"\n💰 Tags containing ₹ (price candidates):")
    for tag in soup.find_all(string=re.compile(r"₹|\bRS\b", re.I))[:15]:
        parent = tag.parent
        print(f"   Tag: <{parent.name}> | Class: {parent.get('class')} | Text: {tag.strip()[:50]}")

    # Find discount-related classes
    print(f"\n📉 Tags containing % off (discount candidates):")
    for tag in soup.find_all(string=re.compile(r"\d+%\s*off", re.I))[:15]:
        parent = tag.parent
        print(f"   Tag: <{parent.name}> | Class: {parent.get('class')} | Text: {tag.strip()[:50]}")

    # Find product name candidates
    print(f"\n📱 Anchor tags with product links:")
    if site == "Flipkart":
        links = soup.find_all("a", href=re.compile(r"/p/itm"))[:10]
    else:
        links = soup.find_all("a", href=re.compile(r"/dp/"))[:10]

    for a in links:
        print(f"   Class: {a.get('class')} | Text: {a.get_text(strip=True)[:60]}")

    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    print("=" * 60)
    print("  DIAGNOSTIC — Finding Real CSS Classes")
    print("  This uses only 2 API credits")
    print("=" * 60)

    if "your_" in SCRAPER_API_KEY:
        print("❌ Please fill in your SCRAPER_API_KEY first!")
        exit(1)

    # Flipkart
    fk_html = fetch("https://www.flipkart.com/search?q=smartphones&sort=discount")
    if fk_html:
        analyze(fk_html, "Flipkart")

    # Amazon
    amz_html = fetch("https://www.amazon.in/s?k=smartphones&s=discount-rank")
    if amz_html:
        analyze(amz_html, "Amazon")

    print("\n✅ DONE! Share the output above with Claude.")
    print("   Claude will write EXACT correct selectors from this.")
