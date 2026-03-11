#!/usr/bin/env python3
"""
AziNews X Poster - Extrage știri și le formatează pentru X/Twitter
"""
import re
import sys

NEWS_FILE = "/home/elitedesk/.openclaw/workspace/AziNews-HTML/index.html"

def extract_news():
    """Extrage știrile din fișierul HTML"""
    try:
        with open(NEWS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return None
    
    # Găsește secțiunea de știri
    news_match = re.search(r'const news = \[(.*?)\]', content, re.DOTALL)
    if not news_match:
        return None
    
    news_str = news_match.group(1)
    
    # Extrage titlurile și sursele
    news_items = []
    item_matches = re.finditer(r"\{([^}]+)\}", news_str)
    
    for item_match in item_matches:
        item = item_match.group(1)
        # title poate avea ghilimele duble sau simple
        title_match = re.search(r'''title: ["']([^"']+)["']''', item)
        source_match = re.search(r"source: '([^']+)'", item)
        url_match = re.search(r"url: '([^']+)'", item)
        
        if title_match and source_match and url_match:
            news_items.append({
                'title': title_match.group(1),
                'source': source_match.group(1),
                'url': url_match.group(1)
            })
    
    return news_items

def format_for_x(news_item, max_length=280):
    """Formatează știrea pentru X"""
    title = news_item['title']
    source = news_item['source']
    url = news_item['url']
    
    # Scurtează titlul dacă e prea lung
    if len(title) > 180:
        title = title[:177] + "..."
    
    post = f"{title}\n\n📰 Sursa: {source}\n🔗 {url}\n\n🌐 azinews.ro"
    
    # Verifică lungimea
    if len(post) > max_length:
        # Reduce și mai mult
        while len(post) > max_length and len(title) > 100:
            title = title[:-10] + "..."
            post = f"{title}\n\n📰 Sursa: {source}\n🔗 {url}\n\n🌐 azinews.ro"
    
    return post

def main():
    news_items = extract_news()
    
    if not news_items:
        print("❌ Nu s-au găsit știri!")
        sys.exit(1)
    
    print(f"✅ Găsite {len(news_items)} știri")
    
    # Alege prima (cea mai recentă)
    news_item = news_items[0]
    
    post = format_for_x(news_item)
    
    print("=" * 50)
    print("🦞 AZINEWS X POST DRAFT")
    print("=" * 50)
    print()
    print(post)
    print()
    print("=" * 50)
    print(f"Caractere: {len(post)}/{280}")
    print("=" * 50)
    
    # Salvează într-un fișier pentru posting
    with open("/home/elitedesk/.openclaw/workspace/AziNews-HTML/x_post.txt", "w", encoding='utf-8') as f:
        f.write(post)
    
    print("\n✅ Draft salvat în x_post.txt")

if __name__ == "__main__":
    main()
