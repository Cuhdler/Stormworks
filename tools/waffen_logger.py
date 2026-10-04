"""Waffen-Schreiber v2 der Figet Marena (PC-Seite): nimmt die Pakete der Waffen-Skripte entgegen (der Schreiber steckt
seit Lage v2.8 / Bild v2.9 / Flak v1.8 in den Skripten selbst, siehe Kopf von lua/lage.lua) und schreibt nach
stormworks_schiff/logs/waffen_<Datum>_<Zeit>/:
- je Datenstrom eine CSV (<q><Kennbuchstabe>.csv, Spalten aus tools/schreiber_spalten.py, leer = 0)
- empfang.csv: jedes Paket mit Ankunftszeit (ms seit Start), Messstelle, Paketnummer, verworfene Zeilen, Zeilen,
  Zeichen, erster/letzter Tick - daran sieht man Luecken (fehlende Paketnummern), Spieltempo (Ticks je Sekunde) und
  ob Pakete zu lang waren
Anfrage: /w?q=<Messstelle>&s=<Paketnummer>&x=<verworfene Zeilen>&d=<Zeile>;<Zeile>;...  Zeile: [Buchstabe]Tick,Wert,...
Aufruf: python waffen_logger.py [port]   (Standard 8768 = Chip-Eigenschaft 'Schreiber Port'); laeuft bis Strg+C.
Lauscht nur auf dem eigenen PC (127.0.0.1 und ::1), nicht im Netz.
"""
import http.server
import os
import socket
import sys
import threading
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from schreiber_spalten import spalten  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 8768
ORDNER = os.path.join(ROOT, "logs", "waffen_" + time.strftime("%Y%m%d_%H%M%S"))
T0 = time.time()
lock = threading.Lock()
dateien, zeilen = {}, {}
pakete, fehlt, verworfen, naechste = {}, {}, {}, {}
empfang = None


def datei(strom, n):
    """CSV eines Datenstroms (beim ersten Mal mit Kopf: Spalten aus schreiber_spalten, sonst v1..vn)."""
    if strom not in dateien:
        sp = spalten(strom)
        if not sp or len(sp) != n:
            sp = ["v%d" % i for i in range(1, n + 1)]
        f = open(os.path.join(ORDNER, strom + ".csv"), "w", encoding="utf-8", newline="\n")
        f.write("tick," + ",".join(sp) + "\n")
        dateien[strom], zeilen[strom] = f, 0
    return dateien[strom]


def schreibe(q, s, x, w, d):
    global empfang
    q = "".join(c for c in q if c.isalnum())[:8] or "x"
    with lock:
        os.makedirs(ORDNER, exist_ok=True)
        if empfang is None:
            empfang = open(os.path.join(ORDNER, "empfang.csv"), "w", encoding="utf-8", newline="\n")
            empfang.write("ms,q,paket,verworfen,antwort_ticks,zeilen,zeichen,tick_von,tick_bis\n")
        ticks, n = [], 0
        for z in d.split(";"):
            if not z:
                continue
            i = 0
            while i < len(z) and z[i].isalpha():
                i += 1
            teile = z[i:].split(",")
            if not teile[0].lstrip("-").isdigit():
                continue
            f = datei(q + z[:i], len(teile) - 1)
            f.write(z[i:] + "\n")
            zeilen[q + z[:i]] += 1
            ticks.append(int(teile[0]))
            n += 1
        pakete[q] = pakete.get(q, 0) + 1
        verworfen[q] = verworfen.get(q, 0) + x
        if s > naechste.get(q, 1):
            fehlt[q] = fehlt.get(q, 0) + s - naechste.get(q, 1)
        naechste[q] = max(naechste.get(q, 0), s + 1)
        empfang.write("%d,%s,%d,%d,%d,%d,%d,%s,%s\n" % ((time.time() - T0) * 1000, q, s, x, w, n, len(d),
                                                    min(ticks) if ticks else "", max(ticks) if ticks else ""))
        for f in list(dateien.values()) + [empfang]:
            f.flush()


class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        a = urllib.parse.parse_qs(u.query, keep_blank_values=True)
        if u.path == "/w" and "q" in a and "d" in a:
            zahl = lambda k: int(a[k][0]) if k in a and a[k][0].lstrip("-").isdigit() else 0
            schreibe(a["q"][0], zahl("s"), zahl("x"), zahl("w"), a["d"][0])
        try:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", "2")
            self.end_headers()
            self.wfile.write(b"ok")
        except OSError:
            pass                    # das Spiel wartet seit v2 nicht mehr auf die Antwort und schliesst manchmal vorher

    def log_message(self, *a):
        pass


class Server6(http.server.ThreadingHTTPServer):
    address_family = socket.AF_INET6
    daemon_threads = True
    request_queue_size = 64         # Python-Standard 5: mehr gleichzeitige Verbindungen wurden abgewiesen


class Server4(http.server.ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = 64


def starte(klasse, adresse):
    try:
        s = klasse((adresse, PORT), H)
    except OSError as e:
        print("  (%s nicht moeglich: %s)" % (adresse, e))
        return None
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


def main():
    if not [s for s in (starte(Server4, "127.0.0.1"), starte(Server6, "::1")) if s]:
        sys.exit("Port %d ist belegt - laeuft der Waffen-Schreiber schon?" % PORT)
    print("Waffen-Schreiber v2 laeuft auf Port %d, schreibt nach %s" % (PORT, ORDNER))
    print("Im Spiel: Schiff spawnen (Chip-Eigenschaft 'Schreiber Port' %d). Beenden mit Strg+C." % PORT)
    try:
        while True:
            time.sleep(5)
            with lock:
                stand = ", ".join("%s %d/%d%s" % (q, pakete[q], pakete[q] + fehlt.get(q, 0),
                                                  " -%d" % verworfen[q] if verworfen.get(q) else "")
                                  for q in sorted(pakete))
            print(time.strftime("%H:%M:%S"), ("Pakete da/gesendet: " + stand) if stand else "noch nichts angekommen")
    except KeyboardInterrupt:
        pass
    finally:
        with lock:
            for f in list(dateien.values()) + ([empfang] if empfang else []):
                f.close()


if __name__ == "__main__":
    main()
