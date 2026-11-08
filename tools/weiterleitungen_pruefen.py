#!/usr/bin/env python3
"""
Prüft die Weiterleitungsliste docs/redirects.csv.

1. Ohne --live: prüft nur die Liste selbst (offline).
   - Pflichtspalten, gültige Statuscodes (301 oder 410)
   - keine doppelten alten Adressen (Groß-/Kleinschreibung egal, wie in der .htaccess)
   - keine Ketten (ein Ziel ist selbst wieder eine alte Adresse)
   - keine Schleifen (Ziel gleich alte Adresse)
   - nie technische WordPress-Pfade (wp-admin, wp-login.php usw.)
   - neue Seiten haben höchstens eine Pfadebene (Dateien unter
     /wordpress/wp-content/uploads/ ausgenommen)

2. Mit --live BASIS: ruft jede alte Adresse auf (nur GET, folgt keiner
   Weiterleitung) und erwartet den Status aus der Liste und genau das Ziel
   auf der kanonischen Adresse (https://autorenforum-berlin.de). Danach ruft
   es jedes Ziel auf, erwartet Status 200 und prüft, ob die Sprungmarke
   (#…) auf der Zielseite als id vorhanden ist.
   --live darf mehrfach stehen, z. B. auch mit https://www.… und http://…,
   damit Ketten über Hostvarianten auffallen.
   Zeilen der Art "muster-definition" (Platzhalter wie <name>) werden live
   übersprungen; ihre Beispielzeilen werden geprüft.

Aufruf (aus dem Repo-Ordner):
    python3 tools/weiterleitungen_pruefen.py docs/redirects.csv
    python3 tools/weiterleitungen_pruefen.py docs/redirects.csv --live https://autorenforum-berlin.de
    python3 tools/weiterleitungen_pruefen.py docs/redirects.csv --live https://autorenforum-berlin.de \
        --live https://www.autorenforum-berlin.de --mit-parameter

Rückgabewert 0 = alles in Ordnung, 1 = Fehler gefunden.
Nur Python-Standardbibliothek.
"""

import argparse
import csv
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

PFLICHT = ["alt", "neu", "status", "regel", "typ"]
TECHNIK = re.compile(
    r"^/(wordpress/)?(wp-admin|wp-login\.php|xmlrpc\.php|wp-cron\.php|wp-json|"
    r"wp-includes|wp-content/(?!uploads/))", re.I)
DATEI = re.compile(r"^/wordpress/wp-content/uploads/")
UA = "Mozilla/5.0 (compatible; Autorenforum-Weiterleitungspruefung/1.0)"
KANONISCH = "https://autorenforum-berlin.de"


class _KeinAutoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = urllib.request.build_opener(_KeinAutoRedirect)


def kodieren(url):
    """Umlaute und Leerzeichen prozentkodieren, vorhandene %-Folgen erhalten."""
    return urllib.parse.quote(url, safe=":/?#[]@!$&'()*+,;=%~")


def abrufen(url, inhalt=False):
    req = urllib.request.Request(kodieren(url), headers={"User-Agent": UA})
    try:
        with OPENER.open(req, timeout=30) as r:
            text = r.read().decode("utf-8", "replace") if inhalt else ""
            return r.status, r.headers.get("Location", ""), text
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location", ""), ""
    except Exception as e:
        return 0, str(e), ""


def ohne_anker(pfad):
    return pfad.split("#", 1)[0]


def ist_muster(z):
    return z.get("umsetzung", "") == "muster-definition" or "<" in z["alt"] or "<" in z["neu"]


def liste_pruefen(zeilen):
    fehler, warnungen = [], []
    if not zeilen:
        return ["Die Liste ist leer."], []
    fehlt = [s for s in PFLICHT if s not in zeilen[0]]
    if fehlt:
        return [f"Pflichtspalten fehlen: {', '.join(fehlt)}"], []

    alte = {}
    for nr, z in enumerate(zeilen, start=2):  # Zeile 1 ist die Kopfzeile
        alt, neu, status = z["alt"].strip(), z["neu"].strip(), z["status"].strip()
        ort = f"Zeile {nr} ({alt})"
        if status not in ("301", "410"):
            fehler.append(f"{ort}: Status muss 301 oder 410 sein, ist '{status}'")
        if not alt.startswith("/"):
            fehler.append(f"{ort}: alte Adresse muss mit / beginnen")
        if TECHNIK.match(alt):
            fehler.append(f"{ort}: technischer WordPress-Pfad darf nie weitergeleitet werden")
        schluessel = alt.lower()
        if schluessel in alte:
            fehler.append(f"{ort}: doppelt (schon in Zeile {alte[schluessel]})")
        alte[schluessel] = nr
        if ist_muster(z):
            continue  # Platzhalter: nur Status, Anfang und Doppel prüfen
        if status == "301" and not neu:
            fehler.append(f"{ort}: 301 ohne Ziel")
        if status == "410" and neu:
            warnungen.append(f"{ort}: 410 mit Ziel – das Ziel wird ignoriert")
        if neu and not (neu.startswith("/") or neu.startswith("https://")):
            fehler.append(f"{ort}: Ziel muss mit / oder https:// beginnen")
        if neu and ohne_anker(neu).lower() == alt.lower():
            fehler.append(f"{ort}: Schleife (Ziel = alte Adresse)")
        if neu.startswith("/") and not DATEI.match(neu):
            tiefe = len([t for t in ohne_anker(neu).strip("/").split("/") if t])
            if tiefe > 1:
                fehler.append(f"{ort}: Ziel hat {tiefe} Pfadebenen, erlaubt ist eine")

    for nr, z in enumerate(zeilen, start=2):
        ziel = ohne_anker(z["neu"].strip()).lower()
        if ziel.startswith("/") and ziel in alte and not ist_muster(z):
            fehler.append(f"Zeile {nr} ({z['alt']}): Kette – das Ziel {ziel} ist selbst eine "
                          f"alte Adresse (Zeile {alte[ziel]})")
    return fehler, warnungen


def live_pruefen(zeilen, basen, kanonisch, pause, mit_parameter):
    fehler, ziele = [], {}
    kanonisch = kanonisch.rstrip("/")
    for basis in basen:
        basis = basis.rstrip("/")
        for z in zeilen:
            if ist_muster(z):
                continue
            alt, neu, status = z["alt"].strip(), z["neu"].strip(), z["status"].strip()
            varianten = [alt]
            if mit_parameter:  # angehängter Parameter darf nicht am Ziel hängen bleiben
                varianten.append(alt + ("&" if "?" in alt else "?") + "pruefung=1")
            for v in varianten:
                ist, ort, _ = abrufen(basis + v)
                time.sleep(pause)
                erwartet = urllib.parse.urljoin(kanonisch + "/", neu) if neu else ""
                if str(ist) != status:
                    fehler.append(f"{basis}{v}: Status {ist}, erwartet {status}")
                elif status == "301" and urllib.parse.unquote(ort) != urllib.parse.unquote(erwartet):
                    fehler.append(f"{basis}{v}: leitet auf {ort}, erwartet {erwartet}")
            if neu:
                ziele.setdefault(erwartet, alt)
    for ziel, alt in sorted(ziele.items()):
        seite, _, anker = ziel.partition("#")
        ist, ort, text = abrufen(seite, inhalt=bool(anker))
        time.sleep(pause)
        if ist != 200:
            fehler.append(f"Ziel {ziel} (von {alt}): Status {ist} {ort}")
        elif anker and not re.search(r'id=["\']' + re.escape(anker) + r'["\']', text):
            fehler.append(f"Ziel {ziel} (von {alt}): Sprungmarke #{anker} fehlt auf der Seite")
    return fehler, len(ziele)


def main():
    ap = argparse.ArgumentParser(description="Prüft docs/redirects.csv")
    ap.add_argument("csv", help="Pfad zur Liste, z. B. docs/redirects.csv")
    ap.add_argument("--live", metavar="BASIS", action="append",
                    help="z. B. https://autorenforum-berlin.de (mehrfach möglich)")
    ap.add_argument("--kanonisch", default=KANONISCH, help="erwartete Zieladresse (Schema und Host)")
    ap.add_argument("--mit-parameter", action="store_true",
                    help="jede Adresse zusätzlich mit ?pruefung=1 aufrufen")
    ap.add_argument("--pause", type=float, default=0.3, help="Sekunden zwischen Abrufen")
    args = ap.parse_args()

    with open(args.csv, newline="", encoding="utf-8") as f:
        zeilen = list(csv.DictReader(f))

    fehler, warnungen = liste_pruefen(zeilen)
    print(f"Liste: {len(zeilen)} Zeilen, {len(fehler)} Fehler, {len(warnungen)} Warnungen")
    for w in warnungen:
        print("  Warnung:", w)
    for e in fehler:
        print("  FEHLER:", e)

    if args.live and not fehler:
        live_fehler, anzahl_ziele = live_pruefen(zeilen, args.live, args.kanonisch,
                                                 args.pause, args.mit_parameter)
        print(f"Live: {anzahl_ziele} Ziele geprüft, {len(live_fehler)} Fehler")
        for e in live_fehler:
            print("  FEHLER:", e)
        fehler += live_fehler
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
