#!/usr/bin/env python3
"""Scrie all_news.json (formatul vechi, ultimele 300 de știri) din data/latest.json.

Scripturile mai vechi (post_x.py) citeau all_news.json. Arhiva completă e acum în data/archive/.
"""
import json
import os

OUT = "all_news.json"
KEYS = ("source", "url", "title", "image", "time", "date", "content", "fetched_at")


def main():
    with open(os.path.join("data", "latest.json"), encoding="utf-8") as f:
        items = json.load(f).get("items", [])
    old = [{k: n.get(k, "") for k in KEYS} for n in items[:300]]
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(old, f, ensure_ascii=False)
    print(f"all_news.json: {len(old)} știri")


if __name__ == "__main__":
    main()
