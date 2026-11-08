# Neue Struktur: Vorschlag zur Freigabe

Stand: 08.11.2026. Grundlagen:
- `docs/anforderungen.md`: Vorgaben des Vereins, unter anderem Menü und Inhalte
- `docs/keywords.md`: Suchbegriffe, Titel und Beschreibungen
- `docs/inventar.md`: Bestand der Live-Seite
- `docs/seo.md`: Regeln für die Weiterleitungen

**Diese Struktur ist noch nicht freigegeben.** Die Entscheidungen in
Abschnitt 3 trifft Dominik. Erst danach geht es mit dem Theme weiter.

## Auf einen Blick

- 8 Seiten statt 22: Startseite, 5 Unterseiten, Impressum und Datenschutz.
- Jede Adresse hat höchstens eine Pfadebene (`/name/`). Ausnahme sind die
  Dateien unter `/wordpress/wp-content/uploads/`; sie bleiben, wo sie sind.
- 6 heutige Adressen bleiben unverändert, 2 kommen neu hinzu.
- Jede wegfallende Adresse leitet per 301 direkt auf ihr neues Ziel, ohne
  Ketten. Die vollständige Liste steht in `docs/redirects.csv` (529 Zeilen).
  Geprüft wird sie mit `tools/weiterleitungen_pruefen.py`.

## 1. Seiten und Menü

Die Reihenfolge des Menüs hat der Verein vorgegeben. Untermenüs gibt es nicht.

| Menü | URL | Adresse | Abschnitte (Sprungmarken) | Patterns | Hauptbegriff |
|---|---|---|---|---|---|
| Aktuelles | `/` | bleibt | nächster Montagabend (automatisch, ganz oben), nächste Veranstaltung, Beiträge der letzten zwei Monate, kurze Vorstellung mit H1, Wegweiser zu den Unterseiten | Nächster Leseabend, Neuerscheinungen | Autoren Berlin, Lesebühne Berlin |
| Werkstattbühne | `/offener-leseabend/` | bleibt (siehe E3) | `#ablauf`, `#selbst-lesen`, `#anfahrt`, `#fragen` | Nächster Leseabend, Anfahrt | Feedback zu eigenen Texten |
| Inspiration für Textkritik (Name siehe E4) | `/textkritik/` | **neu** | `#methode`, `#fragen`, `#heisser-stuhl` | Textkritik-Methode | Textkritik für Schreibende |
| Termine | `/termine/` | bleibt | Überschrift „Werkstattbühne“, `#naechster-termin`, `#moderationsplan`, `#kalender` (.ics) | Moderationsplan, Nächster Leseabend | Werkstattbühne Termine |
| Über uns | `/verein/` | bleibt | `#ziele`, `#geschichte`, `#lesungen`, `#wettbewerbe`, `#organisation` (mit Kontoverbindung), `#kontakt` | – | Autorenverein Berlin |
| Veröffentlichungen der Mitglieder | `/veroeffentlichungen/` | **neu** (siehe E2) | Einleitung, Suchfeld, Liste aller Neuerscheinungen | Neuerscheinungen der Mitglieder | Bücher Berliner Autorinnen und Autoren |

**Footer:** Impressum (`/impressum/`, bleibt) und Datenschutz
(`/datenschutzerklaerung/`, bleibt; der Text muss für die neue Seite
überarbeitet werden).

**Beiträge** (Neuerscheinungen, Neuigkeiten): künftig `/titel/` (siehe E1).

**Termine der Werkstattbühne** bekommen keine eigenen Seiten. Sie erscheinen
auf `/termine/`, auf der Startseite und in der Kalenderdatei. Den Eintragstyp
dafür schlage ich in Schritt 5 vor.

## 2. Was mit den alten Seiten passiert

Die Texte wandern als Abschnitt auf die neue Seite. Die alte Adresse leitet
direkt dorthin, mit Sprungmarke.

| Alte Seite | Neues Ziel | Warum dort |
|---|---|---|
| `/der-heisse-stuhl/` | `/textkritik/#heisser-stuhl` | Sonderform der Textkritik für Mitglieder |
| `/geschichte/` | `/verein/#geschichte` | Vorgabe in `keywords.md` |
| `/organisation/` | `/verein/#organisation` | Vorgabe in `keywords.md` |
| `/kontakt/` | `/verein/#kontakt` | Vorgabe in `keywords.md`; Kontaktdaten stehen außerdem im Impressum |
| `/anfahrt/` | `/offener-leseabend/#anfahrt` | Wer die Anfahrt sucht, will zur Werkstattbühne |
| `/archiv/` | `/veroeffentlichungen/` | Das Archiv ist eine Liste der Neuerscheinungen |
| `/nikolauslesung/` | `/verein/#lesungen` | Kein eigener Menüpunkt mehr. Der Termin erscheint in seiner Saison unter Aktuelles und Termine. |
| `/wettbewerbe/` und die 9 Jahrgangs- und Elternseiten | `/verein/#wettbewerbe` | Kein Menüpunkt mehr. Die Jahrgänge bleiben als kurze Chronik erhalten. |

## 3. Entscheidungen für Dominik

**E1 – Adressen der Beiträge.** Heute haben sie die Form
`/2016/01/02/titel/` mit vier Ebenen.

- **A:** Die Adressen bleiben. Das ist ohne Risiko und entspricht der Empfehlung
  in `keywords.md`. Es widerspricht aber der Vorgabe „maximal ein Pfad“.
- **B (empfohlen):** Die Beiträge bekommen die Form `/titel/`. Die alten
  Adressen leiten per Musterregel weiter (93 Zeilen der Gruppe R3).

Für B spricht:
- Der Relaunch ist der günstigste Zeitpunkt, weil Google die Seite danach
  ohnehin neu erfasst.
- Eine einzige Regel deckt alle Beiträge ab.
- Das Datum 2016 steht heute auch bei viel älteren Büchern und führt in die
  Irre.
- Es gibt keine Kollision mit Seiten- oder Anhangnamen.

Gegen B spricht: Die Beiträge können 2–6 Wochen in den Suchergebnissen
schwanken.

Bei B brauchen zwei Beiträge einen neuen Slug, weil WordPress reine Zahlen
dann nicht erlaubt:
- `/2016/03/03/447/` → `/wolfgang-rill-gebaeck-fuer-das-volk-und-das-kind/`
- `/2017/03/01/657/` → `/doris-anselm-und-in-dem-moment-holt-meine-liebe/`

Bei A fallen die R3-Zeilen weg. Außerdem übernimmt WordPress dann die 117
Anhangseiten unter Beiträgen selbst (statt R4 einzeln).

**E2 – Übersicht der Veröffentlichungen.**

- **Neue Seite `/veroeffentlichungen/` (empfohlen):** Das ist eine Ebene, und
  die Einleitung lässt sich im normalen Seiten-Editor bearbeiten. Das
  Suchfeld sucht nur in dieser Kategorie. Das Kategoriearchiv und `/archiv/`
  leiten auf die neue Seite.
- **Kategoriearchiv `/category/veroeffentlichungen_der_mitglieder/`
  beibehalten** (so steht es in `keywords.md`): Das sind zwei Ebenen, und die
  Einleitung lässt sich nur über die Kategoriebeschreibung pflegen.

**E3 – Adresse der Werkstattbühne.**

- **`/offener-leseabend/` beibehalten (empfohlen):** Der neue Name ist noch
  nicht abgestimmt („Werkstattbühne“ oder „Werkstattabend“). Die alte Adresse
  passt zu den heutigen Suchen. Die Seite bekommt nur einen neuen Titel.
- **`/werkstattbuehne/`:** Ein Wechsel ist später mit einer einzigen
  Weiterleitung möglich, sobald der Name feststeht.

**E4 – Name und Adresse der Textkritik-Seite.**

- Der Verein nennt den Menüpunkt „Inspiration für Textkritik“,
  `keywords.md` schlägt „Anregungen zur Textkritik“ vor. Den Namen entscheidet
  der Verein.
- Als Adresse empfehle ich `/textkritik/`. Sie ist kurz, passt auf Flyer und
  bleibt richtig, egal wie der Titel endet.
- Die Alternative laut `keywords.md` ist `/anregungen-zur-textkritik/`.

**E5 – Wohin die übrigen Inhalte kommen.** Die Ziele in Abschnitt 2 sind mein
Vorschlag, vor allem für Nikolauslesung, Wettbewerbe, Der heiße Stuhl und
Anfahrt. Wenn du ein anderes Ziel willst, ändere ich nur die betroffenen
Zeilen in der Liste.

## 4. Archive, Anhänge, Kategorien

- **Anhangseiten:** Alle 311 werden abgeschaltet (Yoast oder WordPress:
  Medienseiten deaktivieren) und leiten auf die Datei weiter.
  - 147 übernimmt WordPress selbst (Gruppe „R4 Anhang (WordPress)“).
  - 164 brauchen eine eigene Regel, weil ihre Elternadresse wegfällt (Gruppe
    „R4 Anhang (einzeln)“).
- **Kategorien aufräumen:** Es bleiben „Veröffentlichungen der Mitglieder“ und
  „Aktuelles“. Die drei Wettbewerbs-Kategorien werden aufgelöst. Ihre drei
  Beiträge kommen zu „Aktuelles“. Die alten Kategoriearchive leiten weiter
  (R5); `/category/aktuelles/` geht auf die Startseite, die genau „Aktuelles“
  ist.
- **Autoren- und Datumsarchive:** in Yoast abschalten und auf die Übersicht der
  Veröffentlichungen weiterleiten (R5, R6). Die Login-Namen der beiden Konten
  stehen nur in `privat/`, nicht im Repo.
- **Folgeseiten der alten Startseite** (`/page/2/` usw.): leiten auf die
  Übersicht der Veröffentlichungen.
- **Feed** `/feed/` bleibt. Kategorie- und Autorenfeeds leiten auf `/feed/`.
- **Kommentare:** Es gibt keine. Im neuen Setup schalten wir sie ganz ab. Das
  vereinfacht auch die Datenschutzerklärung.

## 5. Die Weiterleitungsliste `docs/redirects.csv`

Spalten: `alt`, `neu`, `status` (301 oder 410), `regel`, `typ`, `hinweis`.

| Regel | Zeilen | Inhalt |
|---|---|---|
| R1 Seite | 35 | 17 wegfallende Seiten, ihre `?page_id=`-Kurzlinks, `/datenschutz/` |
| R2 /wordpress/ | 24 | alte Pfade unter `/wordpress/`, Groß- und Kleinschreibung egal |
| R3 Beitrag (Muster) | 93 | `/JJJJ/MM/TT/titel/` → `/titel/` (nur bei E1 = B) |
| R4 Anhang (einzeln) | 164 | Anhangseiten, deren Elternadresse wegfällt → Datei |
| R4 Anhang (WordPress) | 147 | Anhangseiten, die WordPress selbst weiterleitet → Datei |
| R5 Archiv | 58 | Kategorien, Kategorie-Folgeseiten, 49 Datumsarchive |
| R6 Muster | 8 | Platzhalterzeilen (`<name>`, `<n>`) für Autoren-, Datums-, Feed- und Folgeadressen |

Bewusst nicht in der Liste:
- Dateien unter `/wordpress/wp-content/uploads/` (bleiben unverändert)
- `/feed/`, die Sitemaps (Yoast)
- technische WordPress-Pfade
- die vier toten Links auf alte `.htm`-Seiten: Sie liefern schon heute 404,
  wir korrigieren sie im Inhalt

Für Adressen, die niemand kennt, bleibt die eingebaute Vermutung von WordPress
als Sicherheitsnetz: Sie leitet unbekannte alte Adressen auf einen ähnlich
heißenden Inhalt.

**Noch offen:** Sobald der Search-Console-Export da ist, gleiche ich die Liste
mit den Seiten ab, die Klicks oder externe Links haben. So bleibt keine Adresse
mit Besuchern ohne Ziel.

## 6. Vorschau auf die Umsetzung (Schritt 8)

- Die Regeln kommen in die `.htaccess` im Wurzelverzeichnis, vor den
  WordPress-Block. Für Ziele mit Sprungmarke gilt `[NE]`, ein abschließender
  Schrägstrich ist optional, `/wordpress/…` wird ohne Rücksicht auf Groß- und
  Kleinschreibung erkannt (`[NC]`).
- **Zu prüfen:** Hat der Ordner `/wordpress/` eine eigene `.htaccess` mit
  `RewriteEngine On`? Dann gelten die Regeln der Wurzel dort nicht, und die
  R2-Regeln gehören in diese Datei. Das kläre ich in der lokalen
  Testumgebung und beschreibe es in `docs/umstellung.md`.
- **Inhalte korrigieren:** Diese Schritte erledigen wir in der Testumgebung
  per Suchen und Ersetzen und prüfen sie dort:
  - 73 `http://`-Links auf `https://` umstellen
  - `/wordpress/…`-Links auf die neuen Adressen setzen
  - die toten `.htm`-Links entfernen
  - interne Links auf zusammengelegte Seiten aktualisieren
