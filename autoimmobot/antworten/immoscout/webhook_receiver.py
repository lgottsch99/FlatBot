
from flask import Flask, request, jsonify
import threading
import queue
import immoscout 
import os

app = Flask(__name__)
task_queue = queue.Queue()
LOG_FILE = "/Users/Watanudon/Documents/autoimmobot/listings_url.txt"

AUTH_TOKEN = "mein_geheimer_berlin_token"

def save_url_to_file(url):
    """Schreibt eine neue URL ans Ende der Datei."""
    with open(LOG_FILE, "a") as f:
        f.write(url + "\n")

def remove_url_from_file(url_to_remove):
    """Löscht die URL aus der Datei, sobald sie verarbeitet wurde."""
    if not os.path.exists(LOG_FILE):
        return
    
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
    
    with open(LOG_FILE, "w") as f:
        for line in lines:
            if line.strip() != url_to_remove:
                f.write(line)

def bot_worker():
    while True:
        url = task_queue.get()
        if url is None: 
            print(f"Bot did not receive any url.")
            break
        
        print(f"🚀 Starte Prozess für: {url}")
        try:
            immoscout.apply_to_listing(url)
            

            # URL erst nach Erfolg (oder versuchter Bewerbung) entfernen
            #remove_url_from_file(url)
            

            print(f"✅ Erledigt und aus Datei entfernt: {url}")
        except Exception as e:
            print(f"❌ Fehler bei {url}: {e}")
            # Optional: Hier entscheiden, ob die URL in der Datei bleiben soll (für Retry)

        task_queue.task_done()
        print("☕️ Bereit für das nächste Listing...")

# Worker-Thread starten
threading.Thread(target=bot_worker, daemon=True).start()

@app.route('/new-listing', methods=['POST'])
def webhook():
    auth_header = request.headers.get('Authorization')
    if AUTH_TOKEN and auth_header != f"Bearer {AUTH_TOKEN}":
        return jsonify({"status": "unauthorized"}), 401

    data = request.json
    print(data)
    listings = data.get('listings', [])

    if not listings:
        return jsonify({"status": "no listings found"}), 400

    for item in listings:
        listing_url = item.get('url')
        print(f"📥 URL empfangen & gespeichert: {listing_url}")

        # 1. In Textdatei speichern (Sicherheit)
        save_url_to_file(listing_url)
        
        if listing_url and "immobilienscout24.de" in listing_url:
            
            # 2. In die Warteschlange für den Bot
            task_queue.put(listing_url)

    return jsonify({"status": "received", "count": len(listings)}), 202

def load_pending_urls():
    """Lädt beim Start alle noch nicht verarbeiteten URLs in die Queue."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            for line in f:
                url = line.strip()
                if url:
                    print(f"🔄 Recovery: {url} wieder in die Queue geladen")
                    task_queue.put(url)

# Vor dem App-Start aufrufen:
load_pending_urls()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
