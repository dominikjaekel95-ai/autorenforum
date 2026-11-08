# Neue Struktur: Vorschlag zur Freigabe

Stand: 08.11.2026. Diese Fassung ist nach einer unabhängigen Prüfung aus drei
Blickwinkeln überarbeitet: SEO, Technik und Vollständigkeit.

Grundlagen:
- `docs/anforderungen.md`: Vorgaben des Vereins
- `docs/keywords.md`: Suchbegriffe, Titel und Beschreibungen
- `docs/inventar.md`: Bestand der Live-Seite
- `docs/seo.md`: Regeln für die Weiterleitungen

**Noch nicht freigegeben.** Die Entscheidungen in Abschnitt 4 trifft Dominik.
Erst danach geht es mit dem Theme weiter.

## Auf einen Blick

- **9 Seiten statt heute 23:**
  - 6 im Menü
  - 2 im Footer
  - `/wettbewerbe/` als Archiv ohne Menüpunkt
- **Jede Adresse hat höchstens eine Pfadebene** (`/name/`). Ausnahme sind die
  Dateien unter `/wordpress/wp-content/uploads/`; sie bleiben, wo sie sind.
- **Adressen:** 7 heutige Adressen bleiben unverändert, 2 kommen neu hinzu.
- **Weiterleitungen:** Jede wegfallende Adresse leitet per 301 direkt auf ihr
  neues Ziel, ohne Ketten.
  - Die vollständige Liste steht in `docs/redirects.csv` (552 Zeilen).
  - `tools/weiterleitungen_pruefen.py` meldet 0 Fehler.
  - Jede gecrawlte Adresse ist abgedeckt.

## 1. Seiten und Menü

Die Reihenfolge des Menüs hat der Verein vorgegeben. Untermenüs gibt es nicht.

| Menü | URL | Adresse | H1 | Inhalt und Abschnitte | Patterns | Hauptbegriff |
|---|---|---|---|---|---|---|
| Aktuelles | `/` | bleibt | „Berlins älteste wöchentliche Lesebühne“, ganz oben | direkt darunter der nächste Montagabend (automatisch aus den Terminen: Datum, Moderation, 20 Uhr, Anmeldung zum Lesen ab 19:30); nächste Veranstaltung; Beiträge der letzten zwei Monate (gibt es keine, steht dort ein Hinweis mit Link auf die Veröffentlichungen); kurze Vorstellung; Wegweiser zu allen Unterseiten | Nächster Leseabend, Neuerscheinungen | Autoren Berlin, Lesebühne Berlin |
| Werkstattbühne | `/offener-leseabend/` | bleibt (E3) | „Werkstattbühne“, Untertitel „Lesung und Diskussion von unveröffentlichten Texten“ | `#ablauf`, `#selbst-lesen`, `#haeufige-fragen`; kurzer Hinweis zum Ort mit Link auf `/termine/#anfahrt`; Links auf `/textkritik/` („Wie wir Textkritik üben“) und `/termine/` | Nächster Leseabend | Feedback zu eigenen Texten |
| Inspiration für Textkritik (Name: E4) | `/textkritik/` | **neu** | nach E4 | `#methode`, `#fragen` (die Fragen stehen heute auf `/offener-leseabend/` und dann nur noch hier), `#heisser-stuhl` | Textkritik-Methode | Textkritik für Schreibende |
| Termine | `/termine/` | bleibt | „Termine der Werkstattbühne“ | Untertitel als Text mit Link auf die Werkstattbühne; sichtbar: montags, 20 Uhr, Anmeldung zum Lesen ab 19:30; `#naechster-termin`, `#moderationsplan` (Quartal), `#weitere-termine` (Lesungen wie die Nikolauslesung), `#kalender` (.ics), `#anfahrt` | Moderationsplan, Nächster Leseabend, Anfahrt | Werkstattbühne Termine, Schwartzsche Villa |
| Über uns | `/verein/` | bleibt | „Über das Autorenforum Berlin“ | `#ziele`, `#geschichte`, `#lesungen`, `#wettbewerbe` (kurz, mit Link auf `/wettbewerbe/`), `#organisation` (mit Kontoverbindung), `#kontakt` | – | Autorenverein Berlin |
| Veröffentlichungen der Mitglieder | `/veroeffentlichungen/` | **neu** (E2) | „Veröffentlichungen der Mitglieder“ | Einleitung, Suchfeld (sucht nur in den Veröffentlichungen), Liste aller Neuerscheinungen | Neuerscheinungen der Mitglieder | Bücher Berliner Autorinnen und Autoren |
| – (kein Menüpunkt) | `/wettbewerbe/` | bleibt (E5a) | „Wettbewerbe des Autorenforums Berlin“ | Einleitung; je Jahrgang ein Abschnitt `#wettbewerb-2024` … `#wettbewerb-2012` mit Anthologie, Verlag, ISBN und Preisträgern; Links auf die Wettbewerbs-Beiträge | – | Literaturwettbewerb Berlin |

**Footer:**
- Impressum (`/impressum/`, bleibt)
- Datenschutz (`/datenschutzerklaerung/`, bleibt; der Text muss für die neue
  Seite überarbeitet werden)
- Links zu den Social-Media-Profilen (E6)

**Beiträge** (Neuerscheinungen, Neuigkeiten): künftig `/titel/` (E1).

**Termine** bekommen keine eigenen Seiten. Sie erscheinen auf `/termine/`, auf
der Startseite und in der Kalenderdatei. Die Event-Daten für Google (JSON-LD)
stehen nur auf `/termine/`, damit sie nicht doppelt ausgegeben werden. Den
Eintragstyp dafür schlage ich in Schritt 5 vor.

Zur Überschrift auf `/termine/`: Der Verein wünscht dort „Werkstattbühne“ mit
Untertitel. Die H1 „Termine der Werkstattbühne“ erfüllt das, ohne mit der
Werkstattbühnen-Seite um denselben Begriff zu konkurrieren.

## 2. Überschriften der Sprungmarken

Google wertet eine Weiterleitung ohne den Teil nach `#`. Die Zielseite trägt
das Thema der alten Seite also nur, wenn der Abschnitt eine passende
Überschrift hat. Deshalb sind die Überschriften festgelegt. Die Sprungmarken
werden in Patterns und Vorlagen eingebaut, und das Prüfskript kontrolliert sie
auf der Live-Seite.

| Ziel | Überschrift (H2) |
|---|---|
| `/verein/#geschichte` | Geschichte des Autorenforums Berlin |
| `/verein/#organisation` | Organisation und Kontoverbindung |
| `/verein/#kontakt` | Kontakt |
| `/verein/#lesungen` | Lesungen und Nikolauslesung |
| `/termine/#anfahrt` | Anfahrt zur Schwartzschen Villa |
| `/textkritik/#heisser-stuhl` | Der heiße Stuhl |
| `/wettbewerbe/#wettbewerb-JJJJ` | Wettbewerb JJJJ, mit dem Titel der Anthologie |

## 3. Was mit den alten Inhalten passiert

Die Texte wandern vollständig als Abschnitt auf die neue Seite. Die alte
Adresse leitet direkt dorthin, mit Sprungmarke.

| Alt | Neu | Warum |
|---|---|---|
| `/der-heisse-stuhl/` | `/textkritik/#heisser-stuhl` | Sonderform der Textkritik für Mitglieder |
| `/geschichte/`, `/organisation/` | `/verein/#geschichte`, `/verein/#organisation` | Vorgabe in `keywords.md` |
| `/kontakt/` | `/verein/#kontakt` | Vorgabe in `keywords.md` (E5b); Kontaktdaten stehen außerdem im Impressum |
| `/anfahrt/` | `/termine/#anfahrt` | Laut `keywords.md` trägt `/termine/` den Ort („Schwartzsche Villa“). |
| `/archiv/` | `/veroeffentlichungen/` | Das Archiv ist eine Liste der Neuerscheinungen. |
| `/nikolauslesung/` | `/verein/#lesungen` | Kein eigener Menüpunkt; in der Saison steht die Lesung zusätzlich unter Termine. |
| 9 Jahrgangs- und Elternseiten der Wettbewerbe | `/wettbewerbe/#wettbewerb-JJJJ` | Texte vollständig übernehmen, je Jahrgang eine Sprungmarke |
| Beitrag „Jeden Montag: offener Leseabend“ (2016) | `/offener-leseabend/` | dünner Beitrag zum selben Thema; er würde mit der Seite konkurrieren |
| 3 Wettbewerbs-Beiträge (2017, 2021) | bleiben | werden aus `/wettbewerbe/` verlinkt |

## 4. Entscheidungen für Dominik

**E1 – Adressen der Beiträge** (heute `/2016/01/02/titel/`, vier Ebenen)

- **A:** Die Adressen bleiben. Das ist ohne Risiko und entspricht `keywords.md`.
  Es widerspricht aber der Vorgabe „maximal ein Pfad“.
- **B (empfohlen, endgültig nach dem Search-Console-Abgleich):** Beiträge auf
  `/titel/`. Die Umstellung braucht eine Musterregel und zwei Ausnahmen davor.
  - Dafür:
    - Die Vorgabe wird erfüllt.
    - Google erfasst die Seite nach dem Relaunch ohnehin neu.
    - Das Datum 2016 steht heute auch bei viel älteren Büchern.
  - Risiken:
    - 2–6 Wochen Schwankung bei den Beiträgen.
    - Weil alles gleichzeitig wechselt, lassen sich Schwankungen keiner
      Ursache zuordnen.
    - Die Beiträge sind kurz (Cover, Kurztext). Ob Google jeden neu aufnimmt,
      ist nicht sicher.
    - Beiträge teilen sich die oberste Ebene mit alten, weitergeleiteten
      Adressen. Ein künftiger Beitrag „Nikolauslesung“ landete sonst auf der
      Weiterleitung. Das Begleit-Plugin reserviert diese Namen deshalb (es
      hängt „-2“ an).
- **B später:** zuerst Relaunch mit A, die Umstellung 2–3 Monate danach. Die
  Ursachen lassen sich dann trennen, aber es braucht eine zweite Umstellung.
- Ich empfehle B, wenn der Search-Console-Export zeigt, dass die Beiträge nur
  einen kleinen Teil der Klicks bringen. Bringen sie den Großteil, empfehle ich
  „B später“.
- Bei B bekommen die beiden Beiträge mit einer Zahl als Slug sprechende
  Adressen:
  - `/2016/03/03/447/` → `/wolfgang-rill-gebaeck-fuer-das-volk-und-das-kind/`
  - `/2017/03/01/657/` → `/doris-anselm-und-in-dem-moment-holt-meine-liebe/`
- Bei A entfallen alle Zeilen mit `gilt_bei = E1=B`. Die Anhangseiten unter
  Beiträgen übernimmt dann WordPress selbst.

**E2 – Übersicht der Veröffentlichungen**

- **Neue Seite `/veroeffentlichungen/` (empfohlen):** Das ist eine Ebene, und
  die Einleitung wird im normalen Editor gepflegt. Das Suchfeld nutzt die
  WordPress-Suche mit Kategoriefilter; die funktioniert schon heute ohne
  Plugin. Das Kategoriearchiv und `/archiv/` leiten auf die neue Seite.
- **Kategoriearchiv beibehalten** (`keywords.md`): Das sind zwei Ebenen, und
  die Einleitung lässt sich nur über die Kategoriebeschreibung pflegen.

**E3 – Adresse der Werkstattbühne**

- **`/offener-leseabend/` beibehalten (empfohlen):** Der Name ist noch nicht
  abgestimmt („Werkstattbühne“ oder „Werkstattabend“), und die Adresse passt
  zu den heutigen Suchen.
- **`/werkstattbuehne/`:** Ein späterer Wechsel kostet eine neue Regel, vier
  geänderte Ziele, vier Regeln für Anhangseiten und neue Flyer- und
  Listeneinträge. Wenn der Wechsel kommt, dann am besten vor dem Relaunch und
  vor dem Flyerdruck.

**E4 – Name und Adresse der Textkritik-Seite**

- Den Namen entscheidet der Verein: „Inspiration für Textkritik“
  (Vereinsplan) oder „Anregungen zur Textkritik“ (`keywords.md`).
- Als Adresse empfehle ich `/textkritik/`: kurz, flyertauglich und unabhängig
  vom Titel. Die Alternative ist `/anregungen-zur-textkritik/`.

**E5a – Wettbewerbe**

- **`/wettbewerbe/` als Archivseite ohne Menüpunkt (empfohlen):** Die Adresse
  bleibt, die Texte der Jahrgänge bleiben vollständig, und „Über uns“ bleibt
  übersichtlich. Der Verein hat nur den Menüpunkt gestrichen.
- **Alles nach `/verein/#wettbewerbe`:** eine Seite weniger, aber „Über uns“
  wird lang. Dann ändern sich 12 Zeilen der Liste.

**E5b – Kontakt**

- **Auf `/verein/#kontakt` weiterleiten (empfohlen, Vorgabe in
  `keywords.md`).** Das Beispiel in `docs/seo.md` ist angepasst.
- **`/kontakt/` als eigene Footer-Seite behalten.**

**E6 – Social Media** (Vorgabe „automatische Verlinkung“)

- **(a) Profil-Links im Footer und in den Organisationsdaten für Google
  (empfohlen):** ohne Skripte von Dritten.
- **(b) Teilen-Knöpfe:** als einfache Links ohne Tracking möglich.
- **(c) Neue Beiträge automatisch posten:** Dafür braucht es ein weiteres
  Plugin oder einen Dienst mit Zugriff auf die Konten. Davon rate ich vorerst
  ab.
- Frage: Welche Profile gibt es (Facebook, Instagram, Meetup …)?

**E7 – Ablauf unter Aktuelles**

- **(a) Feste Regel im Theme (empfohlen):** Die Startseite zeigt Beiträge der
  letzten zwei Monate und Veranstaltungen bis zu ihrem Datum. Niemand muss ein
  Datum eintragen. PublishPress Future kann dann entfallen, wenn es sonst
  nicht genutzt wird.
- **(b) Ablaufdatum je Beitrag mit PublishPress Future:** Das Plugin bleibt,
  und wir prüfen es auf PHP 8.4.
- In beiden Fällen bleiben die Beiträge veröffentlicht. Es entsteht also kein
  404.

## 5. Archive, Anhänge, Kategorien, Yoast

- **Anhangseiten:** Alle 311 werden abgeschaltet und leiten auf die Datei.
  147 übernimmt WordPress selbst, 164 brauchen eine eigene Regel, weil ihre
  Elternadresse wegfällt.
- **Kategorien:**
  - Es bleiben „Veröffentlichungen der Mitglieder“ und „Aktuelles“.
  - Die drei Wettbewerbs-Kategorien werden aufgelöst. Ihre Beiträge kommen zu
    „Aktuelles“ und werden aus `/wettbewerbe/` verlinkt.
  - `/category/aktuelles/` leitet auf die Startseite. Die heißt genau
    „Aktuelles“.
- **Yoast nach dem Relaunch:** Kategorien und Medienseiten aus den
  Suchergebnissen nehmen, Autoren- und Datumsarchive abschalten. Die Sitemap
  enthält danach nur noch Seiten und Beiträge.
- **Theme:** Die Vorlagen geben keine Links auf Kategorie-, Autoren- oder
  Datumsarchive aus, weil diese Adressen weiterleiten.
- **Beiträge unter Aktuelles:** Sie bleiben nach zwei Monaten erreichbar,
  über die Sitemap und, bei Wettbewerben, über `/wettbewerbe/`.
- **Startseite:** Sie wird nicht mehr paginiert. Die alten Folgeseiten
  `/page/2/` usw. leiten auf die Veröffentlichungen.
- **Feeds:** `/feed/` bleibt. Kategorie-, Autoren-, Datumsfeeds und
  `/comments/feed/` leiten auf `/feed/`.
- **Kommentare:** Es gibt keine. Wir schalten sie ganz ab. Das vereinfacht
  auch die Datenschutzerklärung.

## 6. Die Weiterleitungsliste `docs/redirects.csv`

| Spalte | Bedeutung |
|---|---|
| `alt`, `neu`, `status` | alte Adresse, Ziel, 301 (oder 410) |
| `regel` | R1 Seiten und Kurzlinks, R2 `/wordpress/`, R3 Beiträge, R4 Anhänge, R5 Archive, R6 Muster |
| `umsetzung` | `einzeln` = eigene Regel in der `.htaccess`; `muster` = von einer Musterregel abgedeckt, die Zeile dient zum Testen; `muster-definition` = die Musterregel selbst, mit Platzhaltern wie `<titel>`; `wordpress` = WordPress leitet selbst weiter |
| `reihenfolge` | Rang in der `.htaccess`: 10 Kurzlinks (Abfrage), 20 feste Adressen, 25 Ausnahmen vor dem Beitragsmuster, 30–31 Beitragsmuster, 40–46 Archiv- und Folgeseitenmuster, 90 WordPress |
| `gilt_bei` | Entscheidung, von der die Zeile abhängt (z. B. `E1=B`); leer = immer |

| Umsetzung | Zeilen |
|---|---|
| einzeln | 247 |
| muster (Testzeilen) | 149 |
| muster-definition | 9 |
| wordpress | 147 |

Bewusst nicht in der Liste:
- Dateien unter `/wordpress/wp-content/uploads/` (bleiben unverändert)
- `/feed/` und die Sitemaps
- technische WordPress-Pfade
- die vier toten Links auf alte `.htm`-Seiten: Sie liefern schon heute 404,
  wir korrigieren sie im Inhalt

Das eingebaute Raten von WordPress ist nur ein Notbehelf. Es sucht Beiträge
und Seiten, deren Slug mit dem letzten Pfadteil beginnt, und lässt Anhänge
aus. Nach dem Start werten wir deshalb die 404-Berichte der Search Console aus
und tragen fehlende Adressen fest ein.

**Noch offen:** der Abgleich mit dem Search-Console-Export. Damit prüfe ich,
dass jede Adresse mit Klicks oder externen Links ein passendes Ziel hat.

## 7. Vorschau auf die Umsetzung (Schritt 8)

- **Lage:** Der Block steht ganz oben in der `.htaccess` der Wurzel, vor
  `# BEGIN WPSuperCache` und vor dem WordPress-Block. Beim Umschalten wird der
  gesamte Cache geleert, erst danach folgt die Live-Prüfung.
- **Ziele absolut** (`https://autorenforum-berlin.de/…`): Alte `http://`- und
  `www.`-Links kommen so in einem Schritt an. Prüfung mit
  `--live https://www.autorenforum-berlin.de` und, von einem Rechner mit
  freiem Netz, mit `http://`.
- **Flags:**
  - Abfrage-Regeln über `RewriteCond %{QUERY_STRING} ^(p|page_id)=ID$`.
  - Alle Regeln mit `[R=301,L,QSD]`, damit kein alter Query-String am Ziel
    hängt.
  - `[NE]` nur bei Zielen mit `#`.
  - `[NC]` bei allen festen Regeln.
  - Der abschließende Schrägstrich ist optional.
- **Muster:** Sie sind mit `^…$` verankert. Datums-, Autoren- und
  `/page/`-Muster greifen nur ohne Query-String, sonst bricht das Blättern in
  den Suchergebnissen.
- **Kodierung:** Zwei alte Anhang-Adressen enthalten zerlegte Umlaute (NFD).
  mod_rewrite vergleicht den dekodierten Pfad, deshalb schreiben wir die
  Regel mit den UTF-8-Bytes. Diese Ziele bekommen kein `[NE]`, damit Apache die
  Umlaute kodiert.
- **`/wordpress/.htaccess`:** Enthält diese Datei irgendeine Rewrite-Anweisung,
  gelten für Adressen unter `/wordpress/` nur ihre Regeln, nicht die der
  Wurzel. Die R2-Regeln kommen dann relativ in diese Datei, vor deren
  WordPress-Block. Das kläre ich in der Testumgebung.
- **Nach dem Permalink-Wechsel (E1 = B):**
  - Die Datenoptimierung von Yoast laufen lassen.
  - Im Export prüfen, ob Beiträge eigene Canonical-Felder haben.
  - Danach crawlen: Jedes Canonical zeigt auf die eigene neue Adresse, keines
    auf eine alte Adresse oder mit `#`.
- **Inhalte korrigieren:** in der Testumgebung per Suchen und Ersetzen, dort
  auch prüfen:
  - 73 `http://`-Links
  - `/wordpress/`-Links
  - vier tote `.htm`-Links
  - Links auf zusammengelegte Seiten
