# Peptide Cheat Sheet

Interactive, searchable peptide reference — static site, no build step.

## Files
- `index.html` — the whole app (HTML + CSS + JS). Fetches `data/peptides.json` at runtime.
- `data/peptides.json` — all product data. **Edit this and `git push` to update the live site.**
- `data/products.map.json` — dev seed: product → id / category / source slugs.
- `scripts/fetch_sources.py` — dev tool that scraped peptide-db.com + peptidedosingprotocols.com into `scripts/raw/` (gitignored).
- `netlify.toml` — publish config (root dir, no build).

## Run locally
`fetch()` won't work from a `file://` URL — serve over HTTP:
```
python3 -m http.server 8000
# open http://localhost:8000
```

## Update workflow
1. Edit `data/peptides.json` (add/edit a product object).
2. `git add data/peptides.json && git commit -m "update peptides" && git push`
3. Netlify auto-deploys from `main`.

## Data record shape
```json
{
  "id": "bpc-157",
  "name": "BPC-157",
  "aka": ["Body Protection Compound-157", "Pentadecapeptide"],
  "category": "Healing & Recovery",
  "summary": "...",
  "mechanism": "...",
  "dosing": "...",
  "cycle": "...",
  "sideEffects": "...",
  "synergies": ["tb-500", "ghk-cu"],
  "comparisons": "...",
  "sources": ["https://peptide-db.com/peptides/bpc-157", "https://www.peptidedosingprotocols.com/protocol/bpc-157"]
}
```

## Disclaimer
Educational / research reference only. Not medical advice. Many compounds listed are not approved for human use. Data aggregated from peptide-db.com and peptidedosingprotocols.com. Consult a licensed physician before using any of these.
