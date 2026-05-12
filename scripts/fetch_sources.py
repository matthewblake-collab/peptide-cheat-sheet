#!/usr/bin/env python3
"""Fetch source pages for each mapped product into scripts/raw/<id>.<src>.txt as stripped text.
Dev tool only — raw/ is gitignored. Re-run anytime to refresh."""
import json, os, re, sys, time, urllib.request, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(HERE, "raw")
os.makedirs(RAW, exist_ok=True)
MAP = json.load(open(os.path.join(ROOT, "data", "products.map.json")))

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

def strip(t):
    t = re.sub(r'<script[^>]*>.*?</script>', ' ', t, flags=re.S|re.I)
    t = re.sub(r'<style[^>]*>.*?</style>', ' ', t, flags=re.S|re.I)
    t = re.sub(r'<svg[^>]*>.*?</svg>', ' ', t, flags=re.S|re.I)
    t = re.sub(r'<noscript[^>]*>.*?</noscript>', ' ', t, flags=re.S|re.I)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = html.unescape(t)
    t = re.sub(r'[ \t ]+', ' ', t)
    t = re.sub(r'\n\s*\n+', '\n', t)
    return t.strip()

def fetch(url):
    for attempt in range(2):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            if attempt == 0:
                time.sleep(2); continue
            return f"__FETCH_ERROR__ {e}"

jobs = []
for r in MAP:
    if r.get("peptidedb_slug"):
        jobs.append((r["id"], "peptidedb", f"https://peptide-db.com/peptides/{r['peptidedb_slug']}"))
    if r.get("pdp_slug"):
        jobs.append((r["id"], "pdp", f"https://www.peptidedosingprotocols.com/protocol/{r['pdp_slug']}"))

print(f"{len(jobs)} pages to fetch")
log = []
for n, (pid, src, url) in enumerate(jobs, 1):
    out = os.path.join(RAW, f"{pid}.{src}.txt")
    raw = fetch(url)
    if raw.startswith("__FETCH_ERROR__"):
        log.append(f"ERR  {pid} {src} {url} :: {raw}")
        open(out, "w").write(raw + "\n" + url)
    else:
        txt = strip(raw)
        # peptide-db pages have a long nav header; trim everything before "Home Peptides" / "Home Protocols" marker if present
        m = re.search(r'(Mechanism of Action|Dosing Protocol|Overview|Research Indications)', txt)
        body = txt
        full = f"SOURCE_URL: {url}\nLENGTH: {len(txt)}\n\n{txt}"
        open(out, "w").write(full)
        flag = "thin" if len(txt) < 800 else "ok"
        log.append(f"{flag:4} {pid} {src} len={len(txt)}")
    print(f"[{n}/{len(jobs)}] {log[-1]}")
    time.sleep(0.7)

open(os.path.join(HERE, "fetch.log"), "w").write("\n".join(log))
errs = [l for l in log if l.startswith("ERR") or l.startswith("thin")]
print(f"\nDone. {len(jobs)} fetched. {len(errs)} need attention:")
print("\n".join(errs) if errs else "  none")
