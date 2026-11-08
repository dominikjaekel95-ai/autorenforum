# Bestandsaufnahme der Live-Seite

Stand: 08.11.2026. Erhoben mit `tools/bestandsaufnahme.py`. Das Skript liest
nur: XML-Sitemaps, RSS-Feed, öffentliche REST-API und alle internen Links
(515 Abrufe). Die Rohdaten liegen in `privat/bestand/` und werden nicht
committet, weil die Seiten Kontakt- und Kontodaten enthalten.

Plugins und Theme sind von außen abgeleitet. Bitte im WP-Admin bestätigen
(siehe Abschnitt 8).

## 1. Eckdaten

| | |
|---|---|
| Adresse | `https://autorenforum-berlin.de/`. `www.` leitet per 301 hierher. |
| WordPress | liegt in `/wordpress/`. Die Website-Adresse ist die Domain-Wurzel. |
| Theme | Ordner `autorenforum`: eine angepasste Kopie von Arras 1.6.2, kein Child-Theme |
| Startseite | Beitragsliste „Aktuelles“. Folgeseiten `/page/2/` usw. existieren, sind aber nicht verlinkt. |
| Permalinks | Beiträge `/JJJJ/MM/TT/titel/` (vier Ebenen), Seiten `/titel/` |
| Sprache | `de-DE` auf allen Seiten |
| Sitemap | Yoast: `/sitemap_index.xml` mit 5 Teil-Sitemaps (Beiträge, Seiten, Anhänge, Kategorien, Autoren), zusammen 292 Einträge. `/sitemap.xml` und `/wp-sitemap.xml` leiten dorthin. |
| Feed | `/feed/` mit den 10 neuesten Beiträgen |
| robots.txt | sperrt nur `/wordpress/wp-admin/` und verweist auf die Sitemap |
| Uploads | `/wordpress/wp-content/uploads/JJJJ/MM/…` |

## 2. Öffentliche Adressen nach Seitentyp

| Seitentyp | Anzahl | in Sitemap | indexierbar | Bemerkung |
|---|---|---|---|---|
| Startseite | 1 | ja | ja | keine H1 |
| Seiten | 22 | 22 | ja | 3 davon zweistufig |
| Beiträge | 93 | 93 | ja | 89 in „Veröffentlichungen der Mitglieder“ |
| Kategoriearchive | 5 + 4 Folgeseiten | 5 | ja | |
| Autorenarchive | 2 + 4 Folgeseiten | 2 | ja | zeigen die Login-Namen der Redaktionskonten |
| Datumsarchive | 48 + 1 Folgeseite | nein | nein (`noindex`) | |
| Anhangseiten | 311 | 168 | ja | eine eigene HTML-Seite je Bild oder PDF |
| PDF-Dateien | 13 | – | – | 11 Wettbewerbsplakate 2017, 2 weitere |

Auch Adressen mit `?p=123` funktionieren: WordPress leitet sie per 301 auf
den Permalink weiter.

## 3. Navigation

**Hauptmenü** (Einträge in eckigen Klammern haben keinen eigenen Link):

- Aktuelles → `/` (als `http://` verlinkt)
- Termine Leseabend → `/termine/`
- [Veranstaltungsformate]
  - Leseabend → `/offener-leseabend/`
  - Wettbewerbe → `/wettbewerbe/`
    - Wettbewerb 2012, 2014, 2015 → `/wettbewerb-2012/` usw.
    - Wettbewerb 2017 → `/wettbewerbe/wettbewerb-2017/` (zweistufig)
    - Wettbewerb 2019 → `/wettbewerb-2019/wettbewerb-2019/` (zweistufig)
    - Wettbewerb 2021, 2024 → `/wettbewerb-2021/`, `/wettbewerb-2024/`
  - Nikolauslesung → `/nikolauslesung/`
- Veröffentlichungen der Mitglieder → `/category/veroeffentlichungen_der_mitglieder/`
- [über uns]
  - Verein | Ziele → `/verein/`
  - Geschichte des Autorenforums Berlin → `/geschichte/`
  - Der heiße Stuhl → `/der-heisse-stuhl/`
  - Organisation und Kontodaten → `/organisation/`

**Fußzeile und Seitenleiste** (auf jeder Seite): Links auf `/wordpress/Kontakt/`,
`/wordpress/Impressum/`, `/wordpress/Anfahrt/` und
`/wordpress/datenschutzerklaerung/`, dazu Facebook. Die `/wordpress/`-Adressen
funktionieren nur, weil WordPress sie errät und per 301 auf `/kontakt/` usw.
weiterleitet. Das Gleiche gilt für `/wordpress/offener-leseabend/` und
`/wordpress/termine/`, die in Inhalten verlinkt sind, sowie für `/datenschutz/`
(leitet auf `/datenschutzerklaerung/`). `/wordpress/` selbst liefert 404.

## 4. Seiten (22)

„Wörter“ zählt nur den Inhalt, ohne Menü und Fußzeile.

| URL | Titel | Wörter | geändert | im Menü | Inhalt |
|---|---|---|---|---|---|
| `/offener-leseabend/` | Leseabend | 562 | 2024-05 | ja | Ablauf des offenen Leseabends, „Wie üben wir Textkritik?“ (zweite H1) |
| `/termine/` | Termine Leseabend | 65 | 2026-10 | ja | Moderationsplan des Quartals (Datum, Moderation, „entfällt“) |
| `/der-heisse-stuhl/` | Der heiße Stuhl | 79 | 2024-05 | ja | Sonderformat für Mitglieder: Besprechung längerer Prosatexte |
| `/verein/` | Verein \| Ziele | 117 | 2024-05 | ja | Selbstverständnis, Ziele |
| `/geschichte/` | Geschichte des Autorenforums Berlin | 125 | 2024-05 | ja | Vereinsgeschichte |
| `/organisation/` | Organisation und Kontodaten | 61 | 2025-01 | ja | Organisation, Bankverbindung |
| `/nikolauslesung/` | Nikolauslesung | 35 | 2016-01 | ja | jährliche Lesung um den Nikolaustag |
| `/wettbewerbe/` | Wettbewerbe | 34 | 2016-01 | ja | Einleitung, Verweis auf die Jahrgänge |
| `/wettbewerb-2012/` | Wettbewerb 2012 | 161 | 2024-05 | ja | Jahrgang, Anthologie |
| `/wettbewerb-2014/` | Wettbewerb 2014 | 202 | 2024-05 | ja | Jahrgang |
| `/wettbewerb-2015/` | Wettbewerb 2015 | 110 | 2024-08 | ja | Jahrgang |
| `/wettbewerbe/wettbewerb-2017/` | Wettbewerb 2017 | 70 | 2025-04 | ja | Jahrgang |
| `/wettbewerb-2019/` | Wettbewerbe | 0 | 2021-11 | nein | leere Elternseite |
| `/wettbewerb-2019/wettbewerb-2019/` | Wettbewerb 2019 | 114 | 2024-10 | ja | Jahrgang |
| `/wettbewerb-2019/wettbewerbe-2019/` | Wettbewerbe 2019 | 0 | 2024-05 | nein | leer |
| `/wettbewerb-2021/` | Wettbewerb 2021 | 140 | 2024-08 | ja | Jahrgang |
| `/wettbewerb-2024/` | Wettbewerb 2024 | 74 | 2025-05 | ja | Jahrgang |
| `/anfahrt/` | Anfahrt | 32 | 2018-05 | Fußzeile | Schwartzsche Villa, ÖPNV |
| `/kontakt/` | Kontakt | 13 | 2025-01 | Fußzeile | nur eine Mailadresse |
| `/impressum/` | Impressum | 138 | 2025-01 | Fußzeile | |
| `/datenschutzerklaerung/` | Datenschutzerklärung | 327 | 2018-05 | Fußzeile | Stand 2018, muss für die neue Seite überarbeitet werden |
| `/archiv/` | Archiv | 831 | 2016-03 | nein | automatisch erzeugte Monatsliste aller Beiträge |

## 5. Beiträge (93) und Kategorien (5)

- **Veröffentlichungen der Mitglieder:** 89 Beiträge, Archiv
  `/category/veroeffentlichungen_der_mitglieder/` mit 4 Folgeseiten. Inhalt:
  Neuerscheinungen mit Cover, Kurztext und Links zu Verlag oder Händler.
- **Aktuelles:** 1 Beitrag (Einladung zum Leseabend), `/category/aktuelles/`
- **Wettbewerb 2017:** 1 Beitrag, `/category/wettbewerb-2017/`
- **Wettbewerb 2019:** 0 Beiträge, `/category/wettbewerb-2019/`
- **Wettbewerb 2021:** 2 Beiträge, `/category/wettbewerb-2019/wettbewerb-2021/`
  (als Unterkategorie von 2019 angelegt)
- **Jahre:** 2016: 33 (Massenimport älterer Titel), 2017: 3, 2018: 3, 2019: 9,
  2020: 4, 2021: 10, 2022: 6, 2023: 7, 2024: 9, 2025: 6, 2026: 3
- Kein Beitrag hat eine eigene Meta-Beschreibung (siehe Abschnitt 7). Ein
  Beitrag hat die Zahl als Slug (`/2016/03/03/447/`).
- Es gibt keine Schlagwörter und keine Slug-Gleichheit zwischen Beiträgen und
  Seiten. Eine Umstellung der Beiträge auf `/titel/` wäre ohne Kollision
  möglich.

## 6. Medien

- 311 Dateien in der Mediathek: 271 JPEG, 26 PNG, 1 WebP, 13 PDF
- 168 sind einem Beitrag oder einer Seite zugeordnet. Die meisten davon
  gehören zu Beiträgen, 14 zu `/organisation/`, 14 zu `/wettbewerb-2012/` und
  11 zu `/wettbewerb-2014/`. Die übrigen 143 sind keinem Inhalt zugeordnet.
- **Jede Datei hat eine eigene Anhangseite.** Die Adresse ist `/dateiname/` oder
  `/JJJJ/MM/TT/beitrag/dateiname/`. 168 davon stehen in der Sitemap. Diese
  Seiten haben keinen eigenen Inhalt, und viele tragen denselben Titel
  (z. B. „Plakat Wettbew 2017“ 11-mal).
- **Alt-Texte:** In der Mediathek fehlen sie bei 309 von 311 Dateien. In den
  Seiten fehlt bei 603 von 1.804 Bildeinbindungen das `alt`-Attribut.

## 7. SEO- und Technikbefunde

| Befund | Folge | Behebung |
|---|---|---|
| Startseite hat den Titel „Autorenforum Berlin e.V. -“ und keine H1 | schwacher Titel für die wichtigste Seite | sofort in Yoast (siehe `docs/keywords.md`), im neuen Theme mit H1 |
| Keine Seite hat eine eigene Meta-Beschreibung. Alle 22 Seiten und die Startseite tragen denselben Text (295 Zeichen, Google kürzt ihn), alle 93 Beiträge denselben mit 116 Zeichen, alle Kategorien denselben mit 75 Zeichen. | Suchergebnisse sehen überall gleich aus | eigene Beschreibung je Seite (Vorschläge in `docs/keywords.md`), für Beiträge eine Yoast-Vorlage mit Auszug |
| Die Beschreibung nennt „seit 1987“, gegründet wurde der Verein 1984 | falsche Angabe in jedem Suchergebnis | mit den neuen Beschreibungen korrigieren |
| Startseite braucht ohne Cache 3,8 Sekunden (laut HTML-Kommentar) | langsam, wenn der Cache leer ist | schlankes Block-Theme, Cache behalten |
| 311 Anhangseiten öffentlich, 168 davon in der Sitemap | viele dünne, doppelte Seiten im Index | Anhangseiten abschalten, per 301 auf die Datei |
| 73 `http://`-Links im Inhalt, meist Bilder | gemischte Inhalte, unnötige Weiterleitungen | beim Umzug per Suchen und Ersetzen auf `https://` |
| 4 kaputte interne Links auf alte `.htm`-Seiten aus der Zeit vor WordPress (in 2 Beiträgen und 1 Seite) | 404 für Besucher | Links im Inhalt korrigieren oder entfernen |
| `/wordpress/…`-Links in Fußzeile und Inhalt, teils mit Großbuchstaben | funktionieren nur durch WordPress-Raten | feste Weiterleitungen, Links im Inhalt korrigieren |
| Autorenarchive indexierbar | zeigen Login-Namen, doppeln die Beitragslisten | abschalten, per 301 weiterleiten |
| Datumsarchive (49) | schon `noindex` | abschalten, per 301 weiterleiten |
| Seitenstruktur zweistufig (Wettbewerbe 2017, 2019), leere Seiten | widerspricht „maximal eine Ebene“ | zusammenlegen |
| `/offener-leseabend/` hat zwei H1 | unklare Hauptüberschrift | im neuen Theme: eine H1 |
| Alt-Texte fehlen fast überall | Barrierefreiheit, Bildersuche | bei der Übernahme ergänzen |
| Kategorie „Wettbewerb 2021“ hängt unter 2019 | verwirrende URL | Kategorien aufräumen |
| `robots.txt` enthält zwei Gruppen für alle Crawler | unschädlich | im neuen Setup vereinfachen |

Unauffällig sind: Canonicals (bis auf 2 Anhangseiten mit Umlaut-Kodierung),
Sprache, Statuscodes (keine Ketten, keine Serverfehler).

In der Seitenleiste stehen zwei leere Widgets („Welcome to Arras!“, „Tag
Cloud“).

## 8. Plugins und Theme (bitte bestätigen)

| Plugin | erkannt über | Zweck |
|---|---|---|
| Yoast SEO | HTML-Kommentar, REST-API | Titel, Beschreibungen, Sitemaps |
| WP Super Cache | HTML-Kommentar, REST-API | Seiten-Cache |
| Wordfence Security mit Login Security | REST-API | Firewall, Login-Schutz |
| PublishPress Future | REST-API | Beiträge zeitgesteuert ablaufen lassen |
| WP Lightbox 2 | Dateipfade im HTML | Bilder vergrößert anzeigen |

Plugins ohne Ausgabe auf der Website (z. B. Backup oder Spamschutz) sind von
außen nicht zu sehen. Die vollständige Liste kommt aus WP-Admin → Werkzeuge →
Website-Zustand → Bericht. Versionsnummern stehen bewusst nicht im Repo, weil
es öffentlich ist.

## 9. Externe Links

Facebook (auf jeder Seite), Amazon (44 Links in Beiträgen) sowie Verlags- und
Autorenseiten. Ein Link führt über eine Newsletter-Trackingadresse eines
Verlags. Ihn ersetzen wir bei der Übernahme durch die direkte Adresse.

## 10. Abgleich mit `docs/bestand-live.md`

Die zweite Erhebung (im Browser, 45 Seiten bis Tiefe 2) stimmt in Zahlen,
Menü, Fußzeile, Hostvarianten und Plugins mit diesem Crawl überein. Sie hat
zusätzlich gefunden: `/datenschutz/` und die kleingeschriebenen
`/wordpress/kontakt/` und `/wordpress/impressum/` (alle per WordPress-Raten
weitergeleitet), die leeren Widgets, die Ladezeit ohne Cache und das falsche
Gründungsjahr. Dieser Crawl hat zusätzlich alle 311 Anhangseiten, 49
Datumsarchive, die Autorenarchive und drei weitere tote `.htm`-Links in
Beiträgen erfasst. Eine Abweichung gibt es bei `/verein/`: Hier liegt im
gespeicherten HTML nur eine H1, die Browser-Erhebung zählt zwei.

## 11. Was von außen nicht sichtbar ist

- Entwürfe, private Seiten, Benutzer, Einstellungen, Plugin-Versionen:
  kommen aus dem WordPress-Export und dem Website-Zustand.
- Klicks, Impressionen und Suchbegriffe: kommen aus dem Search-Console-Export
  (siehe `docs/seo.md`, Abschnitt 1).
