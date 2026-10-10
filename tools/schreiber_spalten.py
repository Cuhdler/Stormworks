"""Spalten des Waffen-Schreibers v2 (Schreiber steckt in den Skripten selbst, siehe Kopf von lua/lage.lua) und Lesen
eines Logs. Je Datenstrom (Messstelle q + Kennbuchstabe der Zeile) eine Liste der Spalten nach 'tick'; leer = 0.

Messstellen: r1..r6 Mast-Radare, la Lagezentrale (laD jeden Tick: was mit den Ortungen geschah), ba Bildschirm
(Zielwahl), fLr/fRr Flak-Radar (fLrT/fRrT alle 8 Ticks: alle Spuren), fLf/fRf Flak-Feuerleitung, kBr/kBf und kAr/kAf
Turm-Radar und Feuerleitung der Kanonen vorn (BC, AC - dieselben Skripte wie die Flak).
Einheiten: Winkel in Umdrehungen (U, 1 = 360 Grad), Wege m, Tempo m/s, Zeiten in Ticks (60 = 1 s), wenn nicht anders.

Lesen:  from schreiber_spalten import lade;  z = lade(ordner, "fLr")  -> Liste von dicts (tick, Spalten -> float)
"""
import csv
import os


def _je(prefix, n, felder):
    return ["%s%d_%s" % (prefix, k, f) for k in range(1, n + 1) for f in felder]


SPALTEN = {
    # KI Landkreuzer (landkreuzer/lua/ki_status.lua): Zustand (0 aus .. 10 Laser?), Ort, Kurs Grad, Tempo ist/soll m/s,
    # Fahr-/Lenkbefehl roh (-1..1), Laser vorn L/M/R, Seite L/R, unten, hinten (m, 0 = nichts), Batterie 0..1,
    # Wegpunkt / Zahl, Nick/Roll Grad (+ Bug hoch / rechts tief), KI an, Waffen frei, Schutzzone, Sitz, nach Hause,
    # Rad-Richtung umgelernt L/R
    "ki": ["zustand", "x", "z", "hoehe", "kurs", "v", "v_soll", "fahr", "lenk", "laser_vl", "laser_vm", "laser_vr",
           "laser_li", "laser_re", "laser_un", "laser_hi", "batterie", "wp", "wp_zahl", "nick", "roll", "ki_an",
           "waffen_frei", "schutzzone", "sitz", "heim", "umgelernt_l", "umgelernt_r"],
    # Mast-Radar: haelt (Lock), Winkel ab Strahl (1 = ab Sockel, 2 = ab Strahl, leer = unbekannt), Lock-Richtung
    # (von der Lage), Gimbal-Befehl, Schirm-Modell (wohin er gerade zeigt), Stimmen Strahl/Sockel, Ortungen da / neu
    # (Bits je Platz 1-7), Ausgabe an die Lage (Seite, Hoehe, Entfernung), neue Ortungen roh (Entfernung, Seite, Hoehe)
    "r": ["haelt", "ab_strahl", "lock_seite", "lock_hoehe", "befehl_seite", "befehl_hoehe", "schirm_seite",
          "schirm_hoehe", "stimmen_strahl", "stimmen_sockel", "da_bits", "neu_bits", "aus_seite", "aus_hoehe",
          "aus_entf"] + _je("o", 7, ["entf", "seite", "hoehe"]),
    # Lage je Tick: Ergebnis der Ortung von Radar 1-6 (k = Platz k nachgefuehrt, 30+k = dabei falsches Tempo verworfen
    # (Lage v2.9), -k = haltendes Radar: Ortung nicht im engen Fangbereich, 10+j = Kandidat j, 99 = neuer Kandidat,
    # -8 = an einem gemerkten stehenden Ort (Lage v3.1), -9 = zu nah / zu weit, 0 = keine Ortung)
    "laD": ["radar%d" % i for i in range(1, 7)],
    # Lage alle 4 Ticks: Schiff (Welt x/z, Hoehe, Kurs U, Nick, Roll, Tempo Ost/Nord/Hoch), Bedrohung, Kandidaten;
    # Platz 1-5 (Kennung, Ort relativ zum Schiff Ost/Nord, Hoehe ueber dem Meer, Tempo, Ticks ohne Ortung, Messdauer s,
    # Art: 1 Luft + 2 bewegt + 4 dicht bestaetigt (ab Lage v2.9) + 8 nachweislich stehend (ab v3.1) + 16 Land (ab v3.2)
    # + 32 zu schnell fuer ein Schiff (ab v3.3)),
    # Kandidat 1-6 (Ort,
    # Ticks ohne Ortung, Art), Zahl der gemerkten stehenden Orte (ab v3.1)
    "la": ["x", "z", "hoehe", "kurs", "nick", "roll", "v_ost", "v_nord", "v_hoch", "bedrohung", "kandidaten"]
          + _je("p", 5, ["id", "ost", "nord", "hoehe", "v_ost", "v_nord", "v_hoch", "alter", "mess", "art"])
          + _je("k", 6, ["ost", "nord", "hoehe", "alter", "art"]) + ["stehend_gemerkt"],
    # Bildschirm: gewaehlte Waffe (0 keine, 1 BC, 2 AC, 3 Flak L, 4 Flak R), gewaehlt und Sitz besetzt, Master Arm,
    # Leertaste, Sitz, Radar-Zoom m, Flak L/R Zustand (0 wartet, 1 sucht, 2 Ziel, 3 feuert, 4 zu flach) und Entfernung,
    # Ziel-Platz und Kennung je Waffe, Zaehler 'sucht/zu flach' der Flaks, erreichbar fuer Flak L/R (Bits je Platz),
    # passt je Waffe (Bits je Platz), Feuer frei (Bits je Waffe), Kennungen der Plaetze, Sperre je Platz fuer L/R (Ticks)
    "ba": ["wahl", "gewaehlt", "master_arm", "leertaste", "sitz", "zoom", "fL_zust", "fL_entf", "fR_zust", "fR_entf",
           "platz_bc", "platz_ac", "platz_fl", "platz_fr", "id_bc", "id_ac", "id_fl", "id_fr", "zaehl_fl", "zaehl_fr",
           "erreicht_fl", "erreicht_fr", "passt_bc", "passt_ac", "passt_fl", "passt_fr", "feuer_frei"]
          + ["id_p%d" % k for k in range(1, 6)] + _je("p", 5, ["sperre_fl", "sperre_fr"]),
    # Flak-Radar: Vorgabe da, Feuer frei, Zielnummer, Vorgabe Ost/Nord/Hoch (relativ zum Turm-Radar), Turm U, Kurs U,
    # Nick, Roll, Radar-Drehung U, 'ab Strahl'-Schaetzung (0..1), Spuren; Ziel Ost/Nord/Hoch (relativ), Tempo, Messdauer s,
    # Ticks ohne Meldung, Hoehe ueber dem Meer; bester Abstand einer Spur zur Vorgabe, Abstand der gehaltenen Spur,
    # Loslass-Zaehler, Ziel-Nummer (zaehlt bei jedem Wechsel), Gimbal Seite/Hoehe, Zustand (0 sucht, 1 sucht Vorgabe,
    # 2 Ziel), eigenes Tempo Ost/Nord/Hoch, Ortungen roh (Platz 1-6: Entfernung, Seite, Hoehe)
    "fr": ["vorgabe", "frei", "zielnr", "v_ost", "v_nord", "v_hoch", "turm", "kurs", "nick", "roll", "radar_dreh",
           "ab_strahl", "spuren", "z_ost", "z_nord", "z_hoch", "z_vost", "z_vnord", "z_vhoch", "z_mess", "z_alter",
           "z_hoehe", "best_abst", "halt_abst", "loslass", "ziel_id", "gimbal_seite", "gimbal_hoehe", "zustand",
           "eig_vost", "eig_vnord", "eig_vhoch"] + _je("o", 6, ["entf", "seite", "hoehe"]),
    # Flak-Radar alle 8 Ticks: Spur 1-16 (Ost, Nord, Hoch relativ, Ticks ohne Meldung, Messdauer s)
    "frT": _je("s", 16, ["ost", "nord", "hoch", "alter", "mess"]),
    # Dachkamera (KAMERA v1.1): Phase (1-4 Messfahrt, 9 im Betrieb), Waffe, Ziel-Platz, Ziel Ost/Nord/Hoehe, Entfernung,
    # Richtung rel. Bug U, Hoehe gegen Deck U, Befehl Drehung/Neigung (Tempo-Eingaenge), Bildwinkel rad, Rueckmeldung
    # Neigung/Drehung des Kopfs U (relativ zum Spawnen), Laser-Entfernung, Laser-Treffer x/y/z, Eichung (Kipp-Seite,
    # Tempo je Befehl U/s, Drehung 0 ab Bug U, Drehrichtung, Versuche), Laser-Richtung rel. Bug U, Kurs U
    "ka": ["phase", "waffe", "ziel", "ost", "nord", "hoehe", "entf", "richtung", "hoehenwinkel", "befehl_drehung",
           "befehl_neigung", "fov", "rueck_neigung", "rueck_drehung", "laser_entf", "laser_x", "laser_y", "laser_z",
           "kipp_seite", "tempo_je", "drehung_0", "drehung_vz", "versuche", "laser_richtung", "kurs",
           # ab v2.0: Blick X/Y (U), Blick gegen die Mitte (Grad), korrigiert gerade, Korrektur der gewaehlten Waffe
           # seitlich/Hoehe (rad), Hotkey-6-Ticks, gelernte Blick-Mitte X/Y (Grad)
           "blick_x", "blick_y", "blick_dx", "blick_dy", "korrigiert", "korr_seite", "korr_hoehe", "hotkey6",
           "blick_mitte_x", "blick_mitte_y", "korrektur_an"],
    # Schutz (SCHUTZ v1.0): Auto-Chaff an, Ortung Radar Detector, Salve, Salven gesamt, Salven dieser Ortung, Ticks ohne
    # Ortung, Pumpen an, Master Arm, Zielkorrektur an
    "mr": ["t_bb", "t_sb"],
    "sc": ["auto_chaff", "ortung", "salve", "salven", "salven_ortung", "ohne_ortung", "pumpen", "master_arm", "korrektur"],
    # Seeradar (SEERADAR v1.0, Radar 6 + Monitor 3x3): Strahl ab Bug (U), Gimbal-Befehl, frische Ortungen, neue
    # Kontakte, Kontakte See/Land/Luft, Reichweite m, Kurs U, Schirm hat den Befehl eingeholt
    "sr": ["strahl", "befehl", "ortungen", "neue", "see", "land", "luft", "reichweite", "kurs", "eingeholt"],
    # Seeradar ab v1.2 jede Sekunde: die ersten 8 Kontakte (Ost/Nord relativ zum Schiff m, Hoehe ueber dem Meer m,
    # Art 1 See, 2 Land, 3 Luft)
    "srK": _je("k", 8, ["ost", "nord", "hoehe", "art"]),
    # Jet-Steuerung (JET STEUERUNG v1.0, alle 4 Ticks): Befehle Quer, Nick, Gas, Seite, Zoom, Triebwerk, Licht, Magnete,
    # Kamera (1 vorn, 2 unten), Booster; Flugdaten Hoehe m, Tempo m/s, Kurs U, Nick Grad, Querlage Grad, Sprit %,
    # Steigen m/s, Notprogramm, kein Signal, Funk-Signal, Entfernung km, Knueppel X/Y roh
    "js": ["quer", "nick", "gas", "seite", "zoom", "triebwerk", "licht", "magnete", "kamera", "booster", "hoehe", "tempo",
           "kurs", "nick_ist", "querlage", "sprit", "steigen", "notprogramm", "kein_signal", "signal", "entf_km",
           "knueppel_x", "knueppel_y"],
    # Autopilot (AUTOPILOT v1.0, alle 4 Ticks): an, Modus (0 Kurs, 1 Route), Kurs Grad, Soll-Kurs, Ausweichen Grad,
    # Kursfehler, Drehrate Grad/s, Ruder (Achse 1), Tempo kn, Soll kn, Ziel kn (bei Hindernis kleiner), Soll-Hebel,
    # Hebel (mitgerechnet), Hebel-Befehl (Achse 2), Welt x/y, Wegpunkte, Entfernung/Peilung zum naechsten, Sitz A/D, W/S,
    # Motoren an, Hindernis, Hindernis-Entfernung (vorwaerts), Laser-Feld (1-9), Laser-Entfernung, Treffer-Hoehe ueber
    # dem Meer, Nick U
    "ap": ["an", "modus", "kurs", "soll_kurs", "ausweichen", "fehler", "drehrate", "ruder", "tempo_kn", "soll_kn",
           "ziel_kn", "hebel_soll", "hebel", "hebel_befehl", "x", "y", "wegpunkte", "wp_entf", "wp_peilung", "sitz_ad",
           "sitz_ws", "motoren", "hindernis", "hind_entf", "laser_feld", "laser_entf", "laser_hoehe", "nick",
           # ab v1.1: Anti-Kollision an, Griff besetzt, Blick X/Y (U), Kreuz x/y (Pixel), Zoom-Stufe (1-7)
           "anti_koll", "griff", "blick_x", "blick_y", "kreuz_x", "kreuz_y", "zoom_stufe",
           # ab v1.2: Griff-Achsen roh (A/D, W/S, Pfeil links/rechts, Pfeil hoch/runter), Griff Hotkey 3/4
           "griff_ad", "griff_ws", "griff_pfeil_lr", "griff_pfeil_hr", "griff_hk3", "griff_hk4"],
    # Flak-Feuerleitung: Ziel da, Feuer frei, Zustand (0 aus, 1 sucht, 2 Ziel, 3 feuert, 4 zu flach), Feuer (ab v2.0:
    # 1 linkes Rohr, 2 rechtes), Turm-
    # Befehl, Rohrwinkel U, tiefster erlaubter U, Richtung Grad ab Bug, Entfernung, Messdauer, Ticks ohne Meldung,
    # Turm U, Seitenfehler U, Zuender s, Schuesse, Turm-Integral, Kamera U, Einzelschuss-Ticks (ab Flak v1.9); ab v2.3
    # Battle Cannon: Lader (v2.5: Zustand links + 3 x rechts, je 0 zu, 1 offen, 2 wartet auf 'Loaded'; bis v2.4: laedt
    # 0 keins, 1 links, 2 rechts), geladen (1 links + 2 rechts; ab v2.5 + 4/8 Zufuehrung L/R hat Granate + 16 Melder da),
    # Weiche umgekehrt (gelernt); ab v2.5 Nachlauf Ticks, gemessene Ladezeit Ticks (Schuss bis 'Loaded'), Weiche auf (1/2);
    # ab v2.6 Kamera-Bildwinkel rad (Auto-Zoom)
    "ff": ["ziel", "frei", "zustand", "feuer", "turm_befehl", "rohr", "rohr_min", "richtung", "entf", "mess", "alter",
           "turm", "seitenfehler", "zuender", "schuesse", "integral", "kamera", "einzel", "lader", "geladen",
           "weiche_umgekehrt", "nachlauf", "ladezeit", "weiche_auf", "kamera_fov"],
}


def spalten(strom):
    """Spaltenliste (ohne tick) fuer einen Datenstrom wie 'r3', 'laD', 'fLrT', 'fRf'."""
    if strom in SPALTEN:
        return SPALTEN[strom]
    if strom[:1] == "r" and strom[1:].isdigit():
        return SPALTEN["r"]
    if strom[:1] in ("f", "k") and len(strom) >= 3:
        # Flak (fL/fR) und Kanonen vorn (kB/kA, gleiche Skripte): r Radar, rT Spuren, f Feuerleitung
        return SPALTEN.get("f" + strom[2:])
    return None


def lade(ordner, strom):
    """Datenstrom eines Logs lesen -> Liste von dicts (tick + Spalten, leer = 0.0), nach Tick sortiert."""
    p = os.path.join(ordner, strom + ".csv")
    out = []
    with open(p, encoding="utf-8") as f:
        r = csv.reader(f)
        kopf = next(r)
        for z in r:
            if len(z) != len(kopf):
                continue
            d = {}
            for k, v in zip(kopf, z):
                try:
                    d[k] = float(v) if v else 0.0
                except ValueError:
                    d[k] = float("nan")
            out.append(d)
    out.sort(key=lambda d: d["tick"])
    return out
