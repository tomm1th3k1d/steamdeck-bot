# 🎮 Steam Deck Availability Bot

Bot gratuito che controlla ogni 30 minuti se la Steam Deck torna disponibile su Steam e ti avvisa su Telegram. Gira su GitHub Actions — nessun server necessario.

---

## ⚙️ Setup (5 minuti)

### 1. Crea il bot Telegram
1. Apri Telegram e cerca **@BotFather**
2. Scrivi `/newbot` e segui le istruzioni
3. Copia il **token** (es. `123456:ABC-DEF...`)

### 2. Ottieni il tuo Chat ID
1. Cerca **@userinfobot** su Telegram
2. Scrivi `/start` → ti risponde con il tuo **Chat ID**

### 3. Crea il repository su GitHub
1. Vai su [github.com](https://github.com) → **New repository**
2. Chiamalo `steamdeck-bot`, mettilo **privato** ✅
3. Carica i file: `check.py` e la cartella `.github/`

### 4. Aggiungi i Secrets
1. Nel repository → **Settings** → **Secrets and variables** → **Actions**
2. Clicca **New repository secret** e aggiungi:

| Nome | Valore |
|------|--------|
| `TELEGRAM_BOT_TOKEN` | il token di @BotFather |
| `TELEGRAM_CHAT_ID` | il tuo Chat ID |

### 5. Abilita GitHub Actions
1. Vai nel tab **Actions** del repository
2. Clicca **"I understand my workflows, go ahead and enable them"**
3. Clicca su **Steam Deck Availability Check** → **Run workflow** per testarlo subito!

---

## ✅ Come funziona

- GitHub esegue `check.py` ogni 30 minuti gratuitamente
- Se trova la Steam Deck disponibile → ti manda un messaggio Telegram
- Se è ancora esaurita → non fa nulla (niente spam)
- Puoi vedere i log nel tab **Actions** del repository

## 🆓 È davvero gratis?
Sì! GitHub Actions offre **2.000 minuti/mese** gratuiti per repository privati.
Ogni run dura ~30 secondi × 48 volte al giorno × 30 giorni = ~720 minuti/mese. Siamo abbondantemente sotto il limite.
