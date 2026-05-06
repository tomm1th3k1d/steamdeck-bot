#!/usr/bin/env python3
"""
Steam Deck Availability Checker
Viene eseguito da GitHub Actions ogni 30 minuti.
Manda una notifica Telegram solo se la Steam Deck è disponibile.
"""

import os
import sys
import requests
from datetime import datetime

# ── Letti dai GitHub Secrets ──────────────────────────────────────
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID   = os.environ["TELEGRAM_CHAT_ID"]
# ─────────────────────────────────────────────────────────────────

PRODUCTS = [
    {
        "name": "Steam Deck",
        "url": "https://store.steampowered.com/steamdeck",
        "msg": (
            "🎮 <b>Steam Deck è tornata disponibile!</b>\n\n"
            "🕐 Rilevato il: {time} UTC\n\n"
            "👉 <a href=\"{url}\">Acquista subito su Steam</a>"
        )
    },
    {
        "name": "Steam Controller",
        "url": "https://store.steampowered.com/hardware/steamcontroller",
        "msg": (
            "🕹️ <b>Steam Controller è tornato disponibile!</b>\n\n"
            "🕐 Rilevato il: {time} UTC\n\n"
            "👉 <a href=\"{url}\">Acquista subito su Steam</a>"
        )
    }
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8",
}

# Parole chiave che indicano disponibilità
AVAILABLE_KEYWORDS   = ["add to cart", "aggiungi al carrello", "buy now", "acquista ora"]
UNAVAILABLE_KEYWORDS = ["out of stock", "esaurito", "sold out", "notify me", "avvisami"]


def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    resp = requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    }, timeout=10)
    resp.raise_for_status()
    print("✅ Notifica Telegram inviata!")


def check():
    for prod in PRODUCTS:
        name = prod["name"]
        url = prod["url"]
        
        print(f"🔍 Controllo {name} in corso — {datetime.utcnow().strftime('%d/%m/%Y %H:%M')} UTC")

        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
        except Exception as e:
            print(f"❌ Errore nel contattare Steam per {name}: {e}")
            sys.exit(1)

        page = resp.text.lower()
        found = False

        for kw in AVAILABLE_KEYWORDS:
            if kw in page:
                print(f"🟢 {name} DISPONIBILE! Keyword trovata: '{kw}'")
                now = datetime.utcnow().strftime("%d/%m/%Y %H:%M")
                send_telegram(prod["msg"].format(time=now, url=url))
                found = True
                break

        if found:
            print("-" * 40)
            continue

        for kw in UNAVAILABLE_KEYWORDS:
            if kw in page:
                print(f"🔴 {name} ancora esaurito. Keyword trovata: '{kw}'")
                found = True
                break
        
        if not found:
            print(f"⚠️  {name}: Nessuna keyword trovata — controlla manualmente la pagina Steam.")
            
        print("-" * 40)


if __name__ == "__main__":
    check()
