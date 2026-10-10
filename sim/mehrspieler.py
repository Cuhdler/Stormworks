"""Mehrspieler-Modus des Simulators: Host und Mitspieler (Gast) als zwei getrennte Rechner.

MODELL - VERMUTET [V], NICHT IM SPIEL BESTAETIGT (darum alles einstellbar):
1. Jeder Rechner hat seine eigenen Lua-Skripte mit eigenem Zustand; Lua-Variablen werden nie abgeglichen
   (Entwickler-Aussage Geometa #22188 [W]).
2. Die Fuehler-Werte (Physik) rechnet der Host und schickt sie; beim Gast sind sie gleich, ausser dort, wo
   gast_fuehler etwas anderes sagt (z. B. Radar sieht beim Gast nichts: "fehlt", oder nur manche Ziele: Funktion).
3. Die Werte an den Chip-Anschluessen (Ein- und Ausgaenge der Microcontroller) schickt der Host nur alle
   'abgleich_ticks' Ticks ("Zwischenstand"); in diesem Tick ersetzen sie beim Gast die eigenen Werte. Dazwischen
   rechnen die Chips des Gasts selbst weiter. Video wird nicht abgeglichen (jeder Rechner zeichnet selbst).
   Innere Werte der Logik-Bausteine (Speicher, Zaehler ...) werden in diesem Modell nicht abgeglichen.

Beispiel:
    mp = Mehrspieler("Figet Marena", chips=["Figet Marena Licht"], abgleich_ticks=120,
                     gast_fuehler={("microprocessor", (0, 8, -55)): "fehlt"})
    mp.tick(600, szenario)          # szenario(host_fahrzeug, tick) setzt die Fuehler beim Host
    mp.host.teil(...).lese(...), mp.gast.teil(...).lese(...)
"""
from chip import SimFehler, leer, als_signal
from fahrzeug import Fahrzeug, FahrzeugDaten


class Mehrspieler:
    def __init__(self, daten, chips=None, abgleich_ticks=120, gast_fuehler=None, **opt):
        daten = daten if isinstance(daten, FahrzeugDaten) else FahrzeugDaten.lesen(daten)
        self.host = Fahrzeug(daten, chips, **opt)
        self.gast = Fahrzeug(daten, chips, **opt)
        self.n = int(abgleich_ticks or 0)
        self.regeln = self._regeln(gast_fuehler or {})
        self.tick_nr, self.abgleiche = 0, 0

    def _regeln(self, spec):
        """gast_fuehler -> {Anschluss-Nr: Regel}. Schluessel: Art d, (d, Position), (d, Position, Label) oder ein
        Chip-Name (fuer nicht simulierte Chips). Regel: "gleich", "fehlt" oder Funktion(wert, tick) -> wert."""
        d = self.host.daten
        out = {}
        for key, regel in spec.items():
            if not (regel in ("gleich", "fehlt") or callable(regel)):
                raise SimFehler("Regel fuer %r: 'gleich', 'fehlt' oder eine Funktion, nicht %r" % (key, regel))
            if isinstance(key, str):
                teile = [t for t in d.teile if t.d == key or (t.chipdef is not None and t.name == key)]
                label = None
            else:
                teile = [t for t in d.teile if t.d == key[0] and t.vp == tuple(key[1])]
                label = key[2] if len(key) > 2 else None
            treffer = [a for t in teile for a in d.anschluesse_von(t.nr) if not a.eingang
                       and (label is None or a.label == label)]
            if not treffer:
                raise SimFehler("gast_fuehler %r: kein passender Ausgang im Fahrzeug" % (key,))
            for a in treffer:
                out[a.nr] = regel
        return out

    def tick(self, n=1, szenario=None, szenario_gast=None):
        """n Ticks. szenario(host, tick) setzt die Fuehler beim Host; szenario_gast(gast, tick) darf danach beim Gast
        einzelne Werte ueberschreiben (z. B. eigene Radar-Ziele)."""
        for _ in range(n):
            t = self.tick_nr
            if szenario is not None:
                szenario(self.host, t)
            an = self.host.daten.anschluesse
            for nr, v in self.host.gesetzt.items():
                regel = self.regeln.get(nr, "gleich")
                if regel == "fehlt":
                    v = leer(an[nr].typ)
                elif regel != "gleich":
                    v = als_signal(an[nr].typ, regel(v, t), self.gast.f32)
                self.gast.wert[nr] = v
                self.gast.gesetzt[nr] = v
            if szenario_gast is not None:
                szenario_gast(self.gast, t)
            self.host.ein_tick()
            if self.n and t % self.n == 0:
                self.gast.ein_tick(fremd=self.host)
                self._abgleich()
            else:
                self.gast.ein_tick()
            self.tick_nr += 1
        return self

    def _abgleich(self):
        """Chip-Ausgaenge des Hosts ersetzen die des Gasts (Video ausgenommen)."""
        an = self.host.daten.anschluesse
        for t, ch in self.gast.laufend.items():
            hc = self.host.laufend[t]
            for kn, a in self.gast.chip_aus[t]:
                if an[a].typ != 6:
                    ch.werte[kn] = hc.werte[kn]
                    self.gast.wert[a] = hc.werte[kn]
        self.abgleiche += 1
