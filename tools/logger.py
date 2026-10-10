"""Fahrtenschreiber fuer die Figet Marena (Schiffs-Chip ab v2.4): nimmt die Zeilen entgegen, die die Helm-Anzeige
(shud.lua) per async.httpGet an localhost schickt, entpackt sie und schreibt sie als CSV nach
stormworks_schiff/logs/fahrt_<Datum>_<Zeit>.csv.

Eine Rohzeile = Tick, Ausgang 1-32 des Schiffs-Skripts, Bool 1-12 als Bits (wie im Chip gepackt; siehe schiff.lua; 12 = Wellen-Schaltsperre ab v2.7).
Aufruf: python logger.py [port]   (Standard 8766 = Chip-Eigenschaft 'Log Port'); laeuft bis Strg+C.
Port 8767 = Flossen-Chip (lua/flossen.lua): Zeilen schon lesbar, nach logs/flossen_<Datum>_<Zeit>.csv.
Lauscht nur auf dem eigenen PC (127.0.0.1 und ::1), nicht im Netz.
"""
import http.server
import os
import socket
import sys
import threading
import time
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGDIR = os.path.join(ROOT, "logs")
PORT = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 8766

MOTOREN = ["L1", "L2", "R1", "R2"]
ZUSTAND = ["OK", "HEISS", "AUSFALL", "TEMP", "LEER", "KUPPELT", "---"]
SPALTEN = (["tick", "tempo_kn", "tempo_kmh", "kurs", "hebel_pct", "gang", "uebersetzung", "automatik", "ruder_pct",
            "e_motor_pct", "motoren_an", "rueckwaerts_l", "rueckwaerts_r", "getriebe_a", "getriebe_b", "getriebe_c"] +
           ["%s_%s" % (m, k) for m in MOTOREN for k in
            ("rps", "temp", "zustand", "gas_pct", "mix", "q", "luft_pct", "treib_drossel", "kupplung", "anlasser")] +
           ["wellen_sperre", "e_motor_aus_batterie"])   # v3.5: Zahl 20 = E-Motor-Gas (vorher Bugstrahl), Bool 13
ROH = 1 + 32 + 1
FLOSSEN = PORT == 8767
FLOSSEN_SPALTEN = ["tick", "tempo_ms", "nick", "roll", "nickrate", "rollrate", "steigen", "verstaerkung",
                   "vorn_l", "vorn_r", "hinten_l", "hinten_r", "mitte_l", "mitte_r", "vorn_mitte_l", "vorn_mitte_r",
                   "heck_wasser"]          # ab Flossen v1.5 (17 Werte; heck_wasser = Liquid Meter, 0 = keiner)


def zahl(t):
    return float(t.replace(" ", "+"))          # '+' im Exponenten kommt aus der URL als Leerzeichen an


def entpacke(roh):
    """Rohzeile (Text) -> Liste der Spaltenwerte (Text), None wenn kaputt."""
    f = roh.split(",")
    if FLOSSEN:
        return [x.replace(" ", "+") for x in f] if len(f) == len(FLOSSEN_SPALTEN) else None
    if len(f) != ROH:
        return None
    try:
        tick, n, bits = int(zahl(f[0])), [0.0] + [zahl(x) for x in f[1:33]], int(zahl(f[33]))
    except ValueError:
        return None
    bit = lambda i: (bits >> (i - 1)) & 1
    v = int(round(n[15]))
    w = [tick, "%.2f" % (n[17] * 1.944), "%.1f" % (n[17] * 3.6), "%.0f" % n[18], "%.0f" % (n[16] * 100),
         (v // 100) % 100 if v > 0 else 0, "%.2f" % ((v // 10000) / 10) if v > 0 else 0, (v // 10) % 10 if v > 0 else 0,
         "%.0f" % (n[19] * 100), "%.0f" % (n[20] * 100), bit(1), bit(6), bit(7), bit(9), bit(10), bit(11)]
    for e in range(1, 5):
        a, b, q = int(round(n[19 + 2 * e])), int(round(n[20 + 2 * e])), int(round(n[28 + e]))
        z = b // 1000000
        w += ["%.1f" % ((a // 1000) / 10), a % 1000, ZUSTAND[z] if 0 <= z < len(ZUSTAND) else z, (b % 1000000) // 1000,
              "%.2f" % ((b % 1000) / 100 - 2), "%.1f" % ((q // 1000) / 10), q % 1000,
              "%.4g" % n[3 * e - 1], "%.2f" % n[3 * e], bit(1 + e)]
    w.append(bit(12))
    w.append(bit(13))
    return [str(x) for x in w]


if __name__ == "__main__":
    os.makedirs(LOGDIR, exist_ok=True)
    datei = os.path.join(LOGDIR, time.strftime(("flossen" if FLOSSEN else "fahrt") + "_%Y%m%d_%H%M%S.csv"))
    f = open(datei, "w", encoding="utf-8", buffering=1)
    f.write(",".join(["pc_zeit"] + (FLOSSEN_SPALTEN if FLOSSEN else SPALTEN)) + "\n")
    lock = threading.Lock()
    zaehler = {"pakete": 0, "zeilen": 0, "fehler": 0}

    class Empfang(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            jetzt = "%.3f" % time.time()
            with lock:
                zaehler["pakete"] += 1
                for roh in q.get("d", [""])[0].split(";"):
                    if not roh:
                        continue
                    w = entpacke(roh)
                    if w is None:
                        zaehler["fehler"] += 1
                        continue
                    f.write(jetzt + "," + ",".join(w) + "\n")
                    zaehler["zeilen"] += 1
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", "2")
            self.end_headers()
            self.wfile.write(b"ok")

        def log_message(self, *args):
            pass

    class Server6(http.server.ThreadingHTTPServer):
        address_family = socket.AF_INET6

    def starte(server_klasse, adresse):
        try:
            s = server_klasse((adresse, PORT), Empfang)
        except OSError as e:
            print("  (%s nicht moeglich: %s)" % (adresse, e))
            return None
        threading.Thread(target=s.serve_forever, daemon=True).start()
        return s

    laeuft = [s for s in (starte(http.server.ThreadingHTTPServer, "127.0.0.1"), starte(Server6, "::1")) if s]
    if not laeuft:
        sys.exit("Port %d ist belegt - laeuft der Fahrtenschreiber schon?" % PORT)
    print("Fahrtenschreiber laeuft auf Port %d, schreibt nach %s" % (PORT, datei))
    print("Im Spiel: Schiff spawnen, der Helm zeigt unten 'LOG OK ...'. Beenden mit Strg+C.")
    try:
        letzte = -1
        while True:
            time.sleep(5)
            with lock:
                z = dict(zaehler)
            if z["zeilen"] != letzte:
                print("%s  %d Pakete, %d Zeilen (%.0f s Fahrt)%s" % (time.strftime("%H:%M:%S"), z["pakete"], z["zeilen"], z["zeilen"] / 60,
                                                                    ", %d kaputte Zeilen" % z["fehler"] if z["fehler"] else ""))
                letzte = z["zeilen"]
    except KeyboardInterrupt:
        print("beendet, Datei:", datei)
