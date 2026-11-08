#!/usr/bin/env python3
"""
Bestandsaufnahme einer öffentlichen WordPress-Website (nur lesend).

Das Skript meldet sich nirgends an und sendet ausschließlich GET- und
HEAD-Anfragen an öffentlich erreichbare Adressen. Zwischen zwei Anfragen
wartet es (Standard: 0,4 Sekunden), damit der Server nicht belastet wird.

Aufruf (aus dem Repo-Ordner):
    python3 tools/bestandsaufnahme.py https://autorenforum-berlin.de privat/bestand

Ergebnisse im Zielordner. Er gehört nach privat/, weil Seiten Kontaktdaten
enthalten können; privat/ wird nie committet.
    urls.csv            jede gefundene Adresse mit Status, Weiterleitungsziel,
                        Titel, Beschreibung, H1, Canonical, robots, Seitentyp
    sitemaps.csv        alle Adressen aus den XML-Sitemaps
    feed.csv            Einträge des RSS-Feeds
    rest/*.json         Antworten der öffentlichen REST-API
    plugins.json        aus dem HTML abgeleitete Plugins und Themes
    html/               Roh-HTML aller abgerufenen Seiten
    zusammenfassung.json

Nur Python-Standardbibliothek, keine Zusatzpakete nötig.
"""

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict, deque
from html.parser import HTMLParser

UA = "Mozilla/5.0 (compatible; Autorenforum-Bestandsaufnahme/1.0)"

# Dateiendungen, die keine HTML-Seiten sind.
DATEI = re.compile(
    r"\.(jpe?g|png|gif|webp|avif|svg|ico|bmp|tiff?|pdf|docx?|xlsx?|pptx?|odt|ods|rtf|"
    r"txt|zip|mp3|mp4|m4a|wav|ogg|mov|avi|css|js|woff2?|ttf|otf|eot|xml|ics)$",
    re.I,
)
BILD = re.compile(r"\.(jpe?g|png|gif|webp|avif|svg|ico|bmp|tiff?)$", re.I)

# Technische WordPress-Pfade: werden nie abgerufen.
TECHNIK = re.compile(
    r"^/(wordpress/)?(wp-admin|wp-login\.php|xmlrpc\.php|wp-cron\.php|wp-json|"
    r"wp-includes|wp-signup\.php|wp-activate\.php|wp-trackback\.php)(/|$)"
)
# Abfrage-Parameter, die nur Varianten derselben Seite erzeugen.
UNWICHTIGE_PARAMETER = re.compile(r"^(utm_.*|fbclid|gclid|share|nb|amp)$")
UEBERSPRINGEN_PARAMETER = {"replytocom", "doing_wp_cron", "s", "preview", "print"}

SITEMAP_NS = {
    "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
    "image": "http://www.google.com/schemas/sitemap-image/1.1",
}


class _KeinAutoRedirect(urllib.request.HTTPRedirectHandler):
    """Weiterleitungen nicht automatisch folgen: Wir wollen sie sehen."""

    def redirect_request(self, *args, **kwargs):
        return None


OPENER = urllib.request.build_opener(_KeinAutoRedirect)


def abrufen(url, methode="GET", versuche=2):
    """Gibt (Status, Header als dict mit kleinen Schlüsseln, Inhalt) zurück.
    Status 0 bedeutet Netzwerkfehler."""
    req = urllib.request.Request(
        url, method=methode,
        headers={"User-Agent": UA, "Accept-Language": "de-DE,de;q=0.9"},
    )
    for versuch in range(versuche):
        try:
            with OPENER.open(req, timeout=30) as r:
                kopf = {k.lower(): v for k, v in r.headers.items()}
                return r.status, kopf, (r.read() if methode == "GET" else b"")
        except urllib.error.HTTPError as e:  # 3xx, 4xx, 5xx
            kopf = {k.lower(): v for k, v in e.headers.items()}
            return e.code, kopf, (e.read() if methode == "GET" else b"")
        except Exception as e:  # Netzwerkfehler, Zeitüberschreitung
            if versuch + 1 == versuche:
                return 0, {"fehler": str(e)}, b""
            time.sleep(3)


class SeitenParser(HTMLParser):
    """Sammelt aus einer HTML-Seite alles, was für SEO und Struktur zählt."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.titel, self._im_titel = "", False
        self.meta = {}
        self.canonical = self.shortlink = self.rest_root = ""
        self.feeds = []
        self.h1, self._h1_tiefe, self._h1_text = [], 0, []
        self.hrefs, self.bilder = [], []
        self.body_class = self.lang = ""
        self.kommentare = []
        self._ohne_text = 0  # innerhalb von <script>/<style>
        self.woerter = 0

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = a.get("lang", "")
        elif tag == "title":
            self._im_titel = True
        elif tag == "meta":
            name = (a.get("name") or a.get("property") or "").lower()
            if name:
                self.meta[name] = a.get("content", "")
        elif tag == "link":
            rel, href = a.get("rel", "").lower(), a.get("href", "")
            if rel == "canonical":
                self.canonical = href
            elif rel == "shortlink":
                self.shortlink = href
            elif rel == "https://api.w.org/":
                self.rest_root = href
            elif rel == "alternate" and "rss" in a.get("type", ""):
                self.feeds.append(href)
        elif tag == "body":
            self.body_class = a.get("class", "")
        elif tag == "h1":
            self._h1_tiefe += 1
            self._h1_text = []
        elif tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])
        elif tag == "img":
            src = a.get("src") or a.get("data-src") or ""
            if src:
                self.bilder.append((src, "alt" in a and a["alt"].strip() != ""))
        elif tag in ("script", "style", "noscript", "template"):
            self._ohne_text += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self._im_titel = False
        elif tag == "h1" and self._h1_tiefe:
            self._h1_tiefe -= 1
            self.h1.append(" ".join("".join(self._h1_text).split()))
        elif tag in ("script", "style", "noscript", "template") and self._ohne_text:
            self._ohne_text -= 1

    def handle_data(self, data):
        if self._im_titel:
            self.titel += data
        if self._h1_tiefe:
            self._h1_text.append(data)
        if not self._ohne_text:
            self.woerter += len(data.split())

    def handle_comment(self, data):
        self.kommentare.append(" ".join(data.split())[:200])


def seitentyp(body_class):
    """Leitet den WordPress-Seitentyp aus den body-Klassen ab."""
    k = set(body_class.split())
    reihenfolge = [
        ("error404", "404"), ("home", "Startseite"), ("attachment", "Anhangseite"),
        ("single", "Beitrag"), ("page", "Seite"), ("category", "Kategoriearchiv"),
        ("tag", "Schlagwortarchiv"), ("author", "Autorenarchiv"),
        ("date", "Datumsarchiv"), ("search", "Suche"),
        ("post-type-archive", "Eintragstyp-Archiv"), ("tax", "Taxonomiearchiv"),
        ("blog", "Beitragsübersicht"), ("archive", "Archiv"),
    ]
    typ = next((name for key, name in reihenfolge if key in k), "")
    if typ and "paged" in k:
        typ += " (Folgeseite)"
    m = re.search(r"\b(?:page-id|postid|attachmentid|category|tag)-(\d+)\b", body_class)
    return typ, (m.group(1) if m else "")


class Bestand:
    def __init__(self, start, ziel, pause, max_urls):
        self.start = start.rstrip("/") + "/"
        teile = urllib.parse.urlsplit(self.start)
        self.host = teile.hostname
        self.hosts = {self.host, "www." + self.host}
        self.ziel, self.pause, self.max_urls = ziel, pause, max_urls
        self.robots = urllib.robotparser.RobotFileParser()
        self.bekannt = {}  # url -> {"quellen": set, "von": list}
        self.warteschlange = deque()
        self.zeilen = []
        self.plugins, self.themes, self.signaturen = Counter(), Counter(), Counter()
        self.extern = Counter()
        self.query_je_pfad = Counter()
        self.rest_root = ""
        os.makedirs(os.path.join(ziel, "rest"), exist_ok=True)
        os.makedirs(os.path.join(ziel, "html"), exist_ok=True)

    # ---------- Hilfen ----------
    def warten(self):
        time.sleep(self.pause)

    def speichern(self, name, daten):
        with open(os.path.join(self.ziel, name), "w", encoding="utf-8") as f:
            json.dump(daten, f, ensure_ascii=False, indent=1)

    def normalisieren(self, href, basis):
        """Absolute URL ohne Sprungmarke und ohne Tracking-Parameter."""
        href = (href or "").strip()
        if not href or href.startswith(("mailto:", "tel:", "javascript:", "data:", "#")):
            return None
        url = urllib.parse.urljoin(basis, href)
        t = urllib.parse.urlsplit(url)
        if t.scheme not in ("http", "https"):
            return None
        params = [(k, v) for k, v in urllib.parse.parse_qsl(t.query, keep_blank_values=True)
                  if not UNWICHTIGE_PARAMETER.match(k)]
        return urllib.parse.urlunsplit(
            (t.scheme, (t.netloc or "").lower(), t.path or "/", urllib.parse.urlencode(params), ""))

    def merken(self, url, quelle, von=None):
        if not url:
            return
        if url not in self.bekannt:
            self.bekannt[url] = {"quellen": set(), "von": []}
            self.warteschlange.append(url)
        eintrag = self.bekannt[url]
        eintrag["quellen"].add(quelle)
        if von and len(eintrag["von"]) < 3 and von not in eintrag["von"]:
            eintrag["von"].append(von)

    # ---------- 1. robots.txt, Sitemaps, Feed ----------
    def robots_lesen(self):
        status, _, inhalt = abrufen(self.start + "robots.txt")
        text = inhalt.decode("utf-8", "replace") if status == 200 else ""
        with open(os.path.join(self.ziel, "robots.txt"), "w", encoding="utf-8") as f:
            f.write(text)
        self.robots.parse(text.splitlines())
        return status, [z.split(":", 1)[1].strip() for z in text.splitlines()
                        if z.lower().startswith("sitemap:")]

    def sitemaps_lesen(self, kandidaten):
        offen, gesehen, eintraege, protokoll = deque(kandidaten), set(), [], []
        while offen:
            sm = offen.popleft()
            if sm in gesehen:
                continue
            gesehen.add(sm)
            status, kopf, inhalt = abrufen(sm)
            self.warten()
            protokoll.append({"sitemap": sm, "status": status, "ziel": kopf.get("location", "")})
            if status in (301, 302, 307, 308) and kopf.get("location"):
                offen.append(urllib.parse.urljoin(sm, kopf["location"]))
                continue
            if status != 200:
                continue
            try:
                wurzel = ET.fromstring(inhalt)
            except ET.ParseError:
                protokoll[-1]["fehler"] = "kein gültiges XML"
                continue
            art = wurzel.tag.rsplit("}", 1)[-1]
            if art == "sitemapindex":
                for loc in wurzel.iterfind("sm:sitemap/sm:loc", SITEMAP_NS):
                    offen.append(loc.text.strip())
            elif art == "urlset":
                for u in wurzel.iterfind("sm:url", SITEMAP_NS):
                    loc = u.findtext("sm:loc", "", SITEMAP_NS).strip()
                    bilder = [i.text.strip() for i in u.iterfind("image:image/image:loc", SITEMAP_NS)]
                    eintraege.append({
                        "url": loc, "lastmod": u.findtext("sm:lastmod", "", SITEMAP_NS).strip(),
                        "sitemap": sm, "bilder": len(bilder)})
                    self.merken(self.normalisieren(loc, sm), "sitemap")
        with open(os.path.join(self.ziel, "sitemaps.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, ["url", "lastmod", "sitemap", "bilder"])
            w.writeheader()
            w.writerows(eintraege)
        return protokoll, len(eintraege)

    def feed_lesen(self):
        status, _, inhalt = abrufen(self.start + "feed/")
        self.warten()
        eintraege = []
        if status == 200:
            try:
                kanal = ET.fromstring(inhalt).find("channel")
                for item in kanal.iterfind("item"):
                    link = (item.findtext("link") or "").strip()
                    eintraege.append({
                        "titel": (item.findtext("title") or "").strip(),
                        "url": link, "datum": (item.findtext("pubDate") or "").strip(),
                        "kategorien": "; ".join(c.text or "" for c in item.iterfind("category"))})
                    self.merken(self.normalisieren(link, self.start), "feed")
            except (ET.ParseError, AttributeError):
                pass
        with open(os.path.join(self.ziel, "feed.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, ["titel", "url", "datum", "kategorien"])
            w.writeheader()
            w.writerows(eintraege)
        return status, len(eintraege)

    # ---------- 2. Öffentliche REST-API ----------
    def rest_url(self, root, pfad, params):
        q = urllib.parse.urlencode(params)
        if "rest_route=" in root:  # einfache Permalinks: ?rest_route=/
            return root.rstrip("/") + "/" + pfad + "&" + q
        return root.rstrip("/") + "/" + pfad + "?" + q

    def rest_liste(self, root, pfad, felder):
        alle, seite = [], 1
        while True:
            status, kopf, inhalt = abrufen(self.rest_url(
                root, pfad, {"per_page": 100, "page": seite, "_fields": felder}))
            self.warten()
            if status != 200:
                return alle, status
            try:
                alle.extend(json.loads(inhalt))
            except ValueError:
                return alle, "kein JSON"
            if seite >= int(kopf.get("x-wp-totalpages", "1") or 1):
                return alle, 200
            seite += 1

    def rest_lesen(self, root):
        ergebnis = {"root": root}
        status, _, inhalt = abrufen(self.rest_url(
            root, "", {"_fields": "name,description,url,home,namespaces,timezone_string"}))
        self.warten()
        if status != 200:
            ergebnis["status"] = status
            return ergebnis
        index = json.loads(inhalt)
        self.speichern("rest/index.json", index)
        ergebnis.update({"namespaces": index.get("namespaces", []),
                         "home": index.get("home"), "siteurl": index.get("url")})

        status, _, inhalt = abrufen(self.rest_url(root, "wp/v2/types", {}))
        self.warten()
        typen = json.loads(inhalt) if status == 200 else {}
        ergebnis["typen"] = {k: v.get("rest_base") for k, v in typen.items()}

        intern = {"attachment", "nav_menu_item", "wp_block", "wp_template", "wp_template_part",
                  "wp_navigation", "wp_global_styles", "wp_font_family", "wp_font_face"}
        felder = {
            "pages": "id,date,modified,slug,status,link,title,parent,menu_order,template,content",
            "posts": "id,date,modified,slug,link,title,categories,tags,featured_media,excerpt",
        }
        for typ, basis in ergebnis["typen"].items():
            if typ in intern or not basis:
                continue
            daten, st = self.rest_liste(root, "wp/v2/" + basis,
                                        felder.get(basis, "id,date,modified,slug,link,title,type"))
            self.speichern(f"rest/{basis}.json", daten)
            ergebnis[basis] = {"anzahl": len(daten), "status": st}
            for d in daten:
                self.merken(self.normalisieren(d.get("link"), self.start), "rest:" + basis)

        for basis in ("categories", "tags"):
            daten, st = self.rest_liste(root, "wp/v2/" + basis,
                                        "id,name,slug,count,link,parent,description")
            self.speichern(f"rest/{basis}.json", daten)
            ergebnis[basis] = {"anzahl": len(daten), "status": st}
            for d in daten:
                self.merken(self.normalisieren(d.get("link"), self.start), "rest:" + basis)

        daten, st = self.rest_liste(
            root, "wp/v2/media", "id,date,slug,link,source_url,mime_type,media_type,post,alt_text")
        self.speichern("rest/media.json", daten)
        ergebnis["media"] = {"anzahl": len(daten), "status": st}
        for d in daten:  # Anhangseiten (nicht die Dateien selbst)
            self.merken(self.normalisieren(d.get("link"), self.start), "rest:media")

        # Kommentare nur zählen (Namen sind personenbezogen). Benutzer nie abrufen.
        status, kopf, _ = abrufen(self.rest_url(root, "wp/v2/comments", {"per_page": 1, "_fields": "id"}))
        self.warten()
        ergebnis["kommentare"] = kopf.get("x-wp-total", f"Status {status}")
        return ergebnis

    # ---------- 3. Crawl ----------
    def zeile(self, url, **werte):
        e = self.bekannt.get(url, {"quellen": set(), "von": []})
        z = {"url": url, "quelle": " ".join(sorted(e["quellen"])), "verlinkt_von": " | ".join(e["von"])}
        z.update(werte)
        self.zeilen.append(z)

    def html_auswerten(self, url, inhalt):
        text = inhalt.decode("utf-8", "replace")
        for m in re.finditer(r"/wp-content/plugins/([A-Za-z0-9_.-]+)/", text):
            self.plugins[m.group(1)] += 1
        for m in re.finditer(r"/wp-content/themes/([A-Za-z0-9_.-]+)/", text):
            self.themes[m.group(1)] += 1
        p = SeitenParser()
        try:
            p.feed(text)
        except Exception:
            pass
        for k in p.kommentare:  # z. B. Hinweise von Cache- oder SEO-Plugins
            if re.search(r"yoast|super cache|cache|seo|generated|optimized|plugin", k, re.I):
                self.signaturen[re.sub(r"\d[\d:. -]*\d", "#", k)[:120]] += 1
        if p.meta.get("generator"):
            self.signaturen["generator: " + p.meta["generator"]] += 1
        datei = hashlib.sha1(url.encode()).hexdigest()[:12] + ".html"
        with open(os.path.join(self.ziel, "html", datei), "w", encoding="utf-8") as f:
            f.write(f"<!-- {url} -->\n" + text)
        intern = 0
        for href in p.hrefs:
            ziel = self.normalisieren(href, url)
            if not ziel:
                continue
            host = urllib.parse.urlsplit(ziel).hostname
            if host in self.hosts:
                intern += 1
                self.merken(ziel, "link", von=url)
            else:
                self.extern[host] += 1
        for src, _ in p.bilder:
            ziel = self.normalisieren(src, url)
            if ziel and urllib.parse.urlsplit(ziel).hostname in self.hosts:
                self.merken(ziel, "bild", von=url)
        typ, wp_id = seitentyp(p.body_class)
        return {
            "seitentyp": typ, "wp_id": wp_id, "titel": " ".join(p.titel.split()),
            "beschreibung": p.meta.get("description", ""), "h1": " || ".join(p.h1),
            "canonical": p.canonical, "robots": p.meta.get("robots", ""),
            "shortlink": p.shortlink, "woerter": p.woerter, "bilder": len(p.bilder),
            "bilder_ohne_alt": sum(1 for _, alt in p.bilder if not alt),
            "interne_links": intern, "html_datei": datei, "lang": p.lang,
            "_rest_root": p.rest_root,
        }

    def crawlen(self, limit):
        abgerufen = 0
        while self.warteschlange and abgerufen < limit:
            url = self.warteschlange.popleft()
            t = urllib.parse.urlsplit(url)
            if t.hostname not in self.hosts:
                continue
            params = dict(urllib.parse.parse_qsl(t.query, keep_blank_values=True))
            if TECHNIK.match(t.path):
                self.zeile(url, status="", hinweis="technischer Pfad, nicht abgerufen")
                continue
            if not self.robots.can_fetch(UA, url):
                self.zeile(url, status="", hinweis="durch robots.txt gesperrt, nicht abgerufen")
                continue
            if UEBERSPRINGEN_PARAMETER & set(params):
                self.zeile(url, status="", hinweis="Variante (Parameter), nicht abgerufen")
                continue
            if t.query:
                self.query_je_pfad[t.path] += 1
                if self.query_je_pfad[t.path] > 30:
                    self.zeile(url, status="", hinweis="zu viele Parameter-Varianten, nicht abgerufen")
                    continue
            if t.scheme == "http":  # der Proxy erlaubt nur https; die https-Variante prüfen
                self.zeile(url, status="", hinweis="http-Link im Inhalt")
                self.merken(urllib.parse.urlunsplit(("https",) + tuple(t[1:])), "http-link", von=url)
                continue
            if DATEI.search(t.path):
                if BILD.search(t.path):
                    self.zeile(url, status="", typ="Bild", hinweis="Bild, nicht abgerufen")
                    continue
                status, kopf, _ = abrufen(url, "HEAD")
                abgerufen += 1
                self.warten()
                self.zeile(url, status=status, ziel=kopf.get("location", ""),
                           typ=kopf.get("content-type", "").split(";")[0], hinweis="Datei (HEAD)")
                continue

            status, kopf, inhalt = abrufen(url)
            abgerufen += 1
            self.warten()
            werte = {"status": status, "ziel": kopf.get("location", ""),
                     "typ": kopf.get("content-type", "").split(";")[0],
                     "x_robots": kopf.get("x-robots-tag", "")}
            if 300 <= status < 400 and werte["ziel"]:
                self.merken(self.normalisieren(werte["ziel"], url), "weiterleitung", von=url)
            elif status == 200 and "html" in werte["typ"]:
                werte.update(self.html_auswerten(url, inhalt))
                rest = werte.pop("_rest_root", "")
                if rest and not self.rest_root:
                    self.rest_root = urllib.parse.urljoin(url, rest)
            elif status == 0:
                werte["hinweis"] = kopf.get("fehler", "")
            self.zeile(url, **werte)
            if abgerufen % 50 == 0:
                print(f"  … {abgerufen} abgerufen, {len(self.warteschlange)} offen", flush=True)
        return abgerufen

    def schreiben(self):
        spalten = ["url", "quelle", "status", "ziel", "typ", "seitentyp", "wp_id", "titel",
                   "beschreibung", "h1", "canonical", "robots", "x_robots", "shortlink", "lang",
                   "woerter", "bilder", "bilder_ohne_alt", "interne_links", "verlinkt_von",
                   "html_datei", "hinweis"]
        self.zeilen.sort(key=lambda z: z["url"])
        with open(os.path.join(self.ziel, "urls.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, spalten, extrasaction="ignore")
            w.writeheader()
            w.writerows(self.zeilen)
        self.speichern("plugins.json", {
            "plugins": self.plugins.most_common(), "themes": self.themes.most_common(),
            "signaturen": self.signaturen.most_common(30),
            "externe_hosts": self.extern.most_common(60)})


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("start", help="z. B. https://autorenforum-berlin.de")
    ap.add_argument("ziel", help="Ausgabeordner, z. B. privat/bestand")
    ap.add_argument("--pause", type=float, default=0.4, help="Sekunden zwischen Anfragen")
    ap.add_argument("--max", type=int, default=3000, help="höchstens so viele Abrufe")
    args = ap.parse_args()

    b = Bestand(args.start, args.ziel, args.pause, args.max)
    zusammenfassung = {"start": b.start}

    print("1/4 robots.txt und Sitemaps …", flush=True)
    status, sitemap_zeilen = b.robots_lesen()
    zusammenfassung["robots_status"] = status
    kandidaten = sitemap_zeilen + [b.start + p for p in ("sitemap_index.xml", "wp-sitemap.xml", "sitemap.xml")]
    zusammenfassung["sitemaps"], zusammenfassung["sitemap_urls"] = b.sitemaps_lesen(kandidaten)
    zusammenfassung["feed_status"], zusammenfassung["feed_eintraege"] = b.feed_lesen()

    print("2/4 Startseite …", flush=True)
    b.merken(b.start, "start")
    if b.start in b.warteschlange:  # Startseite zuerst: sie verrät die Adresse der REST-API
        b.warteschlange.remove(b.start)
    b.warteschlange.appendleft(b.start)
    gestartet = b.crawlen(limit=1)
    root = b.rest_root or (b.start + "wp-json/")

    print("3/4 REST-API …", flush=True)
    zusammenfassung["rest"] = b.rest_lesen(root)

    print("4/4 Crawl …", flush=True)
    zusammenfassung["abgerufen"] = gestartet + b.crawlen(limit=args.max - gestartet)
    zusammenfassung["nicht_abgerufen_offen"] = len(b.warteschlange)
    b.schreiben()
    zusammenfassung["status"] = Counter(str(z.get("status", "")) for z in b.zeilen)
    zusammenfassung["seitentypen"] = Counter(z.get("seitentyp", "") for z in b.zeilen if z.get("seitentyp"))
    b.speichern("zusammenfassung.json", zusammenfassung)
    print(json.dumps({k: zusammenfassung[k] for k in ("abgerufen", "status", "seitentypen")},
                     ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(main())
