#!/usr/bin/env python3
"""
AziNews Auto-Updater
Extrage 8 știri de pe Digi24 + 8 de pe mediafax.ro și actualizează index.html
"""
import json
import re
from datetime import datetime
from pathlib import Path

# Fișierele
HTML_FILE = Path(__file__).parent / "index.html"
TEMPLATE_FILE = Path(__file__).parent / "template.html"

def fetch_digi24_news():
    """Preia știri de pe Digi24 RSS"""
    news = []
    try:
        import urllib.request
        url = "https://www.digi24.ro/rss"
        with urllib.request.urlopen(url, timeout=15) as response:
            content = response.read().decode('utf-8')
        
        # Parse RSS items
        items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
        for item in items[:8]:
            title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
            if not title_match:
                title_match = re.search(r'<title>(.*?)</title>', item)
            
            link_match = re.search(r'<link>(.*?)</link>', item)
            desc_match = re.search(r'<description><!\[CDATA\[(.*?)\]\]></description>', item)
            if not desc_match:
                desc_match = re.search(r'<description>(.*?)</description>', item)
            
            img_match = re.search(r'<media:content[^>]*url="([^"]+)"', item)
            if not img_match:
                img_match = re.search(r'<enclosure[^>]*url="([^"]+)"', item)
            
            if title_match and link_match:
                title = title_match.group(1).strip()
                link = link_match.group(1).strip()
                desc = desc_match.group(1).strip() if desc_match else ""
                desc = re.sub(r'<[^>]+>', '', desc)[:200]  # Strip HTML
                img = img_match.group(1) if img_match else ""
                
                news.append({
                    "source": "Digi24",
                    "url": link,
                    "title": title,
                    "image": img,
                    "content": desc,
                    "time": "Acum"
                })
    except Exception as e:
        print(f"Eroare Digi24: {e}")
    return news

def fetch_mediafax_news():
    """Preia știri de pe Mediafax RSS"""
    news = []
    try:
        import urllib.request
        url = "https://www.mediafax.ro/rss"
        
        # User-Agent for mediafax
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8')
        
        items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
        for item in items[:8]:
            title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
            if not title_match:
                title_match = re.search(r'<title>(.*?)</title>', item)
            
            link_match = re.search(r'<link>(.*?)</link>', item)
            desc_match = re.search(r'<description><!\[CDATA\[(.*?)\]\]></description>', item)
            if not desc_match:
                desc_match = re.search(r'<description>(.*?)</description>', item)
            
            img_match = re.search(r'<media:content[^>]*url="([^"]+)"', item)
            if not img_match:
                img_match = re.search(r'<enclosure[^>]*url="([^"]+)"', item)
            
            if title_match and link_match:
                title = title_match.group(1).strip()
                link = link_match.group(1).strip()
                desc = desc_match.group(1).strip() if desc_match else ""
                desc = re.sub(r'<[^>]+>', '', desc)[:200]
                img = img_match.group(1) if img_match else ""
                
                news.append({
                    "source": "Mediafax",
                    "url": link,
                    "title": title,
                    "image": img,
                    "content": desc,
                    "time": "Acum"
                })
    except Exception as e:
        print(f"Eroare Mediafax: {e}")
    return news

def update_html(news_list):
    """Actualizează index.html cu noile știri"""
    if not HTML_FILE.exists():
        print("Nu am găsit index.html!")
        return False
    
    html_content = HTML_FILE.read_text(encoding='utf-8')
    
    # Creează array-ul JavaScript cu știrile
    news_js = "const news = [\n"
    for n in news_list:
        img = n.get('image', '') or ''
        # Escape pentru JS
        title = n['title'].replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
        content = n.get('content', '').replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
        news_js += f'''    {{ source: '{n["source"]}', url: '{n["url"]}', title: "{title}", image: '{img}', content: "{content}", time: '{n["time"]}' }},\n'''
    news_js += "];"
    
    # Înlocuiește vechiul array de știri
    pattern = r'const news = \[.*?\];'
    html_content = re.sub(pattern, news_js, html_content, flags=re.DOTALL)
    
    # Scrie fișierul
    HTML_FILE.write_text(html_content, encoding='utf-8')
    print(f"Actualizat cu {len(news_list)} știri!")
    return True

def git_push():
    """Face commit și push la GitHub"""
    import subprocess
    import os
    import urllib.request
    import json
    try:
        # Configure git to use gh for credentials
        subprocess.run(["git", "config", "--global", "credential.helper", "!gh auth git-credential"], check=False)
        
        # Add și commit
        subprocess.run(["git", "add", "index.html"], check=True)
        subprocess.run(["git", "commit", "-m", f"Auto-update: {datetime.now().strftime('%Y-%m-%d %H:%M')}"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Push la GitHub făcut!")
        
        # Purge Cloudflare cache
        print("Curăț cache Cloudflare...")
        cloudflare_purge("azinews.ro")
        
        return True
    except Exception as e:
        print(f"Eroare git: {e}")
        return False

def cloudflare_purge(domain):
    """Purge cache Cloudflare pentru un domeniu"""
    import urllib.request
    import json
    
    # Configurație - păstrată local
    cf_email = "garconai93@gmail.com"
    cf_api_key = "db01e87b90a3508e9253fab849ef182c1ae40"
    
    # Zone IDs
    zone_ids = {
        "azinews.ro": "159d3820fe1ca3c29737db911e7e38ed",
        "flacarafood.ro": "f557a7215089ff0040c4235271faf16e"
    }
    
    zone_id = zone_ids.get(domain)
    if not zone_id:
        print(f"Nu am găsit Zone ID pentru {domain}")
        return
    
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache"
    data = json.dumps({"purge_everything": True}).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('X-Auth-Email', cf_email)
    req.add_header('X-Auth-Key', cf_api_key)
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode())
            if result.get('success'):
                print(f"✓ Cache purjat pentru {domain}")
            else:
                print(f"Eroare Cloudflare: {result}")
    except Exception as e:
        print(f"Eroare la purge cache: {e}")

def main():
    print(f"AziNews Updater - {datetime.now()}")
    
    # Preia știrile
    print("Preiau știri de pe Digi24...")
    digi_news = fetch_digi24_news()
    print(f"  -> {len(digi_news)} știri Digi24")
    
    print("Preiau știri de pe Mediafax...")
    mediafax_news = fetch_mediafax_news()
    print(f"  -> {len(mediafax_news)} știri Mediafax")
    
    # Combină (8 + 8)
    all_news = (digi_news[:8] + mediafax_news[:8])[:16]
    
    if all_news:
        print(f"Total: {len(all_news)} știri")
        update_html(all_news)
        git_push()
    else:
        print("Nu am putut prelua știri!")

if __name__ == "__main__":
    main()
