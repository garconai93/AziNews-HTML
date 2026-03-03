#!/usr/bin/env python3
"""
AziNews Horoscop Generator
Generează horoscop zilnic diferit pentru fiecare zodie
"""
import random
from datetime import datetime
from pathlib import Path

# Mesaje pentru fiecare zodie (vor fi amestecate zilnic)
HOROSCOPE_MESSAGES = {
    "Berbec": [
        "Zi perfectă pentru inițiative noi",
        "Energie maximă, profită de ea",
        "Momente favoabile în relații",
        "Success în proiectele personale",
        "Opportunități profesionale"
    ],
    "Taur": [
        "Stabilitate financiară",
        "Zi de relaxare și reflecție",
        "Conexiuni emoționale puternice",
        "Progrese în carieră",
        "Harmonie în familie"
    ],
    "Gemeni": [
        "Zi dinamică și interesantă",
        "Comunicare excelentă",
        "Inspirație creativă",
        "Noi cunoștințe valoroase",
        "Flexibilitate și adaptabilitate"
    ],
    "Rac": [
        "Timp prețios cu familia",
        "Intuiție puternică",
        "Emoții profunde",
        "Protecție și siguranță",
        "Sentimente reciproce"
    ],
    "Leu": [
        "Strălucești în orice situație",
        "Atenție din partea celorlalți",
        "Creativitate debordantă",
        "Leadership natural",
        "Succes în afaceri"
    ],
    "Fecioară": [
        "Sănătate și bunăstare",
        "Atenție la detalii",
        "Organizare impecabilă",
        "Analiză profundă",
        "Perfecțiune în lucruri"
    ],
    "Balanță": [
        "Echilibru în toate",
        "Relații armonioase",
        "Justiție și fair-play",
        "Frumusețe și artă",
        "Diplomație excelentă"
    ],
    "Scorpion": [
        "Putere și determinare",
        "Transformări pozitive",
        "Mister și charisma",
        "Intensitate emoțională",
        "Descoperiri importante"
    ],
    "Săgetător": [
        "Aventură și explorare",
        "Optimism exploziv",
        "Călătorii benefice",
        "Filozofie de viață",
        "Libertate personală"
    ],
    "Capricorn": [
        "Responsabilitate și disciplină",
        "Obiective clare",
        "Ambitionează sus",
        "Disciplină de fier",
        "Succes garantat"
    ],
    "Vărsător": [
        "Inovație și originalitate",
        "Gândire unică",
        "Schimbări benefice",
        "Comunitate și prietenie",
        "Viitor luminos"
    ],
    "Pești": [
        "Creativitate artistică",
        "Intuiție spirituală",
        "Visatori romantici",
        "Compasiune profundă",
        "Lume interioară bogată"
    ]
}

def get_daily_horoscope():
    """Generează horoscop zilnic bazat pe ziua lunii"""
    today = datetime.now()
    day_of_month = today.day
    month = today.month
    
    # Seed pentru random bazat pe ziua lunii
    seed = day_of_month * 100 + month
    random.seed(seed)
    
    horoscope = []
    signs = list(HOROSCOPE_MESSAGES.keys())
    random.shuffle(signs)
    
    for i, sign in enumerate(signs):
        messages = HOROSCOPE_MESSAGES[sign]
        # Alege un mesaj diferit în fiecare zi
        msg_index = (day_of_month + i) % len(messages)
        horoscope.append({
            "sign": sign,
            "msg": messages[msg_index]
        })
    
    # Resetează random seed-ul
    random.seed()
    
    return horoscope

def update_html(horoscope):
    """Actualizează index.html cu horoscopul zilnic"""
    HTML_FILE = Path(__file__).parent / "index.html"
    html_content = HTML_FILE.read_text(encoding='utf-8')
    
    # Creează array-ul JavaScript
    js_array = "const horoscope = [\n"
    for h in horoscope:
        js_array += f'            {{ sign: "{h["sign"]}", msg: "{h["msg"]}" }},\n'
    js_array += "        ];"
    
    # Înlocuiește vechiul horoscop
    import re
    pattern = r'const horoscope = \[.*?\];'
    html_content = re.sub(pattern, js_array, html_content, flags=re.DOTALL)
    
    HTML_FILE.write_text(html_content, encoding='utf-8')
    print(f"Horoscop actualizat pentru {datetime.now().strftime('%d-%m-%Y')}")

def main():
    print(f"Horoscop Generator - {datetime.now()}")
    horoscope = get_daily_horoscope()
    
    print("\nHoroscop zilnic:")
    for h in horoscope:
        print(f"  {h['sign']}: {h['msg']}")
    
    update_html(horoscope)
    print("\nGata!")

if __name__ == "__main__":
    main()
