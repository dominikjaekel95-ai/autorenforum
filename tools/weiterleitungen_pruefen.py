#!/usr/bin/env python3
"""
Prüft die Weiterleitungsliste docs/redirects.csv.

1. Ohne --live: prüft nur die Liste selbst (offline).
   - Pflichtspalten, gültige Statuscodes (301 oder 410)
   - keine doppelten alten Adressen
   - keine Ketten (ein Ziel ist selbst wieder eine alte Adresse)
   - keine Schleifen (Ziel gleich alte Adresse)
   - nie technische WordPress-Pfade (wp-admin, wp-login.php usw.)
   - neue Seiten haben höchstens eine Pfadebene (Dateien unter
     /wordpress/wp-content/uploads/ ausgenommen)

2. Mit --live: ruft jede alte Adresse auf (nur GET, folgt keiner
   Weiterleitung) und erwartet den Status aus der Liste und das richtige
   Ziel. Danach ruft es jedes Ziel auf und erwartet Status 200.
   Zeilen mit Platzhaltern wie <name> oder <n> werden dabei übersprungen.

Aufruf (aus dem Repo-Ordner):
    python3 tools/weiterleitungen_pruefen.py docs/redirects.csv
    python3 tools/weiterleitungen_pruefen.py docs/redirects.csv --live https://autorenforum-berlin.de

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


class _KeinAutoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = urllib.request.build_opener(_KeinAutoRedirect)


def abrufen(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with OPENER.open(req, timeout=30) as r:
            return r.status, r.headers.get("Location", "")
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location", "")
    except Exception as e:
        return 0, str(e)


def ohne_anker(pfad):
    return pfad.split("#", 1)[0]


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
        if not alt.startswith("/"):
            fehler.append(f"{ort}: alte Adresse muss mit / beginnen")
        if TECHNIK.match(alt):
            fehler.append(f"{ort}: technischer WordPress-Pfad darf nie weitergeleitet werden")
        if status not in ("301", "410"):
            fehler.append(f"{ort}: Status muss 301 oder 410 sein, ist '{status}'")
        if status == "301" and not neu:
            fehler.append(f"{ort}: 301 ohne Ziel")
        if status == "410" and neu:
            warnungen.append(f"{ort}: 410 mit Ziel – das Ziel wird ignoriert")
        if neu and not (neu.startswith("/") or neu.startswith("https://")):
            fehler.append(f"{ort}: Ziel muss mit / oder https:// beginnen")
        if neu and ohne_anker(neu) == alt:
            fehler.append(f"{ort}: Schleife (Ziel = alte Adresse)")
        if neu.startswith("/") and not DATEI.match(neu):
            tiefe = len([t for t in ohne_anker(neu).strip("/").split("/") if t])
            if tiefe > 1:
                fehler.append(f"{ort}: Ziel hat {tiefe} Pfadebenen, erlaubt ist eine")
        schluessel = alt.lower() if alt.startswith("/wordpress/") else alt
        if schluessel in alte:
            fehler.append(f"{ort}: doppelt (schon in Zeile {alte[schluessel]})")
        alte[schluessel] = nr

    for nr, z in enumerate(zeilen, start=2):
        ziel = ohne_anker(z["neu"].strip())
        if ziel.startswith("/") and ziel in alte:
            fehler.append(f"Zeile {nr} ({z['alt']}): Kette – das Ziel {ziel} ist selbst eine "
                          f"alte Adresse (Zeile {alte[ziel]})")
    return fehler, warnungen


def live_pruefen(zeilen, basis, pause):
    fehler, ziele = [], {}
    basis = basis.rstrip("/")
    for z in zeilen:
        alt, neu, status = z["alt"].strip(), z["neu"].strip(), z["status"].strip()
        if "<" in alt:
            continue  # Musterzeile, kein konkreter Aufruf möglich
        ist, ort = abrufen(basis + alt)
        time.sleep(pause)
        erwartet = urllib.parse.urljoin(basis + "/", neu) if neu else ""
        if str(ist) != status:
            fehler.append(f"{alt}: Status {ist}, erwartet {status}")
        elif status == "301" and urllib.parse.unquote(ort) != urllib.parse.unquote(erwartet):
            fehler.append(f"{alt}: leitet auf {ort}, erwartet {erwartet}")
        if neu:
            ziele.setdefault(ohne_anker(erwartet), alt)
    for ziel, alt in sorted(ziele.items()):
        ist, ort = abrufen(ziel)
        time.sleep(pause)
        if ist != 200:
            fehler.append(f"Ziel {ziel} (von {alt}): Status {ist} {ort}")
    return fehler, len(ziele)


def main():
    ap = argparse.ArgumentParser(description="Prüft docs/redirects.csv")
    ap.add_argument("csv", help="Pfad zur Liste, z. B. docs/redirects.csv")
    ap.add_argument("--live", metavar="BASIS", help="z. B. https://autorenforum-berlin.de")
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
        live_fehler, anzahl_ziele = live_pruefen(zeilen, args.live, args.pause)
        print(f"Live: {anzahl_ziele} Ziele geprüft, {len(live_fehler)} Fehler")
        for e in live_fehler:
            print("  FEHLER:", e)
        fehler += live_fehler
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
