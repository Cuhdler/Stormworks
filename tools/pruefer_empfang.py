"""Empfaenger fuer den Lua-Pruefer (lua/pruefer.lua, Fahrzeug 'Lua Pruefer'): nimmt die Pakete auf Port 8769 an und
schreibt jede Zeile nach logs/lua_pruefer_<Zeit>.txt (doppelt gesendete Pakete nur einmal).
Aufruf: python -u tools/pruefer_empfang.py   (beenden mit Strg+C, sobald 'A:alles_fertig' kam)
"""
import http.server
import os
import socket
import sys
import threading
import time
import urllib.parse

PORT = 8769
ORDNER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(ORDNER, exist_ok=True)
DATEI = os.path.join(ORDNER, time.strftime("lua_pruefer_%Y%m%d_%H%M%S.txt"))
lock = threading.Lock()
gesehen = set()
zeilen = [0]


class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query, keep_blank_values=True)
        s, d = q.get("s", ["?"])[0], q.get("d", [""])[0]
        with lock:
            if s not in gesehen:
                gesehen.add(s)
                teile = [t for t in d.split(";") if t]
                with open(DATEI, "a", encoding="utf-8") as f:
                    for t in teile:
                        f.write(t + "\n")
                zeilen[0] += len(teile)
                letzte = teile[-1] if teile else ""
                print("Paket %s: %d Zeilen (gesamt %d), letzte: %s" % (s, len(teile), zeilen[0], letzte), flush=True)
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", "2")
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, *a):
        pass


class Server6(http.server.ThreadingHTTPServer):
    address_family = socket.AF_INET6
    daemon_threads = True


class Server4(http.server.ThreadingHTTPServer):
    daemon_threads = True


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
        sys.exit("Port %d ist belegt" % PORT)
    print("Lua-Pruefer-Empfang laeuft auf Port %d, schreibt nach %s" % (PORT, DATEI), flush=True)
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
