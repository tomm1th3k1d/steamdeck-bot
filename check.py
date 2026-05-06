#!/usr/bin/env python3
"""
Steam Deck Availability Checker
Viene eseguito da GitHub Actions ogni 30 minuti.
Manda una notifica Telegram solo se la Steam Deck è disponibile.
"""

import os
import sys
import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException
from datetime import datetime, timezone

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
AVAILABLE_KEYWORDS   = ["add to cart", "aggiungi al carrello"]
UNAVAILABLE_KEYWORDS = ["out of stock", "esaurito", "sold out", "notify me", "avvisami"]


def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        resp = requests.post(url, json={
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
        }, timeout=30)
        resp.raise_for_status()
        print("✅ Notifica Telegram inviata!")
    except Timeout:
        print("❌ Errore: Timeout durante l'invio della notifica Telegram.")
    except ConnectionError:
        print("❌ Errore: Problema di connessione con le API di Telegram.")
    except HTTPError as e:
        print(f"❌ Errore HTTP da Telegram: {e}")
    except RequestException as e:
        print(f"❌ Errore imprevisto nell'invio a Telegram: {e}")


def check():
    for prod in PRODUCTS:
        name = prod["name"]
        url = prod["url"]
        
        print(f"🔍 Controllo {name} in corso — {datetime.now(timezone.utc).strftime('%d/%m/%Y %H:%M')} UTC")

        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
        except Timeout:
            print(f"❌ Errore: Timeout nel contattare Steam per {name}.")
            sys.exit(1)
        except ConnectionError:
            print(f"❌ Errore: Problema di connessione con Steam per {name}.")
            sys.exit(1)
        except HTTPError as e:
            print(f"❌ Errore HTTP contattando Steam per {name}: {e}")
            sys.exit(1)
        except RequestException as e:
            print(f"❌ Errore generico contattando Steam per {name}: {e}")
            sys.exit(1)

        page = resp.text.lower()
        found = False

        for kw in AVAILABLE_KEYWORDS:
            if kw in page:
                print(f"🟢 {name} DISPONIBILE! Keyword trovata: '{kw}'")
                now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M")
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
            print(f"⚠️  {name}: Nessuna keyword trovata — la pagina potrebbe essere cambiata (oppure è una pagina React)!")
            if name != "Steam Controller":
                now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M")
                send_telegram(
                    f"⚠️ <b>Attenzione! Anomalie per {name}</b>\n\n"
                    f"🕐 Rilevato il: {now} UTC\n\n"
                    f"Nessuna keyword (disponibile o esaurito) trovata. La pagina Steam potrebbe essere cambiata, controlla manualmente!\n\n"
                    f"👉 <a href=\"{url}\">Apri Steam</a>"
                )
            
        print("-" * 40)


if __name__ == "__main__":
    check()
