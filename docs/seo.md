# SEO beim Relaunch

Ziel: Das Ranking soll erhalten bleiben und nach Möglichkeit steigen.
Google bewertet einzelne URLs. Wenn sich URLs ändern, müssen ihre Signale per
301-Weiterleitung auf die neuen URLs übertragen werden, und die Inhalte, die
heute ranken, müssen erhalten bleiben.

Was hier noch fehlt, ergänze ich nach der Bestandsaufnahme
(siehe `docs/inventar.md` und `docs/redirects.csv`).

---

## 1. Vorher: Ausgangslage sichern

Ohne diese Zahlen lässt sich später nicht sagen, ob der Relaunch geschadet
oder genützt hat.

| Was | Wo | Wer |
|---|---|---|
| Leistung, Zeitraum 16 Monate, Tab „Seiten“ und Tab „Suchanfragen“ als CSV | Search Console → Leistung → Exportieren | Dominik |
| Externe Links: Tab „Top-verlinkte Seiten“ | Search Console → Links → Exportieren | Dominik |
| Vollständiger Crawl: URL, Statuscode, Title, Description, H1, Canonical | Skript im Repo | Claude |
| 10–20 wichtigste Suchbegriffe mit aktueller Position | aus dem Export oben | gemeinsam |

Die Exporte gehören in den Ordner `privat/`. Sie werden nicht committet.

## 2. URLs: so wenig wie möglich ändern

- **Die beste Weiterleitung ist keine.** Gute bestehende URLs mit nur einer
  Pfadebene (z. B. `/kontakt/`) behalten wir genau so.
- Jede wegfallende URL bekommt eine **301-Weiterleitung auf die thematisch
  passende neue Seite**. Eine Pauschal-Weiterleitung auf die Startseite wertet
  Google wie eine fehlende Seite („Soft 404“).
- **Keine Ketten:** Jede alte URL zeigt in einem einzigen Schritt auf das
  endgültige Ziel.
- Inhalte, die ersatzlos wegfallen und keine passende Zielseite haben,
  bekommen den Status **410 („entfernt“)**.
- Sonderfälle, die wir mit abdecken: `?p=123` und `?page_id=…`, die
  `/wordpress/…`-Pfade, Feeds, Kategorie-, Schlagwort-, Autoren- und
  Datumsarchive, Anhangseiten und Seitenzahlen (`/page/2/`).
- **WordPress bleibt im Ordner `/wordpress/`.** Dadurch bleiben alle Bilder
  unter `/wordpress/wp-content/uploads/…` erreichbar. Das zählt für die
  Bildersuche und für Links von außen.
- **Sicherheitsregel:** Weiterleitungen für `/wordpress/…` werden nur für
  einzelne, ausdrücklich aufgeführte Adressen geschrieben. `wp-admin`,
  `wp-login.php`, `wp-content`, `wp-includes`, `wp-json`, `wp-cron.php` und
  `xmlrpc.php` dürfen nie von einer Weiterleitung erfasst werden.
- Die Weiterleitungen bleiben **dauerhaft** bestehen, mindestens aber ein Jahr.
- Umsetzung: Ich empfehle Regeln in der `.htaccess` im Wurzelverzeichnis, die
  vor dem WordPress-Block stehen. Das ist schnell und kommt ohne Plugin aus.
  Die Regeln werden aus `docs/redirects.csv` erzeugt. Die Alternative ist das
  Plugin „Redirection“: Es lässt sich ohne SFTP pflegen, ist aber langsamer und
  ein zusätzliches Plugin, das gewartet werden muss.

## 3. Inhalte erhalten und bündeln

- Unterseiten, die heute Besucher bringen, werden nicht gestrichen. Ihr Text
  wird ein Abschnitt der neuen Übersichtsseite und bekommt eine Sprungmarke
  (z. B. `…/#textkritik`).
- **Ein Thema, eine Seite.** Zwei Seiten sollen nicht um denselben Suchbegriff
  konkurrieren.
- Jede Seite hat genau eine H1, einen sprechenden Seitentitel mit höchstens
  60 Zeichen nach dem Muster „Thema | Autorenforum Berlin“ und eine
  Beschreibung mit höchstens 155 Zeichen.
- Bilder bekommen beschreibende Dateinamen und einen Alt-Text. Der Alt-Text
  ist zugleich Pflicht für die Barrierefreiheit.
- Interne Links: Die Startseite verlinkt jede Übersichtsseite. Linktexte sagen,
  wohin der Link führt („Termine der Leseabende“ statt „hier“).

## 4. Technik im neuen Theme (baue ich ein)

- Mobil zuerst, semantisches HTML, saubere Überschriften-Hierarchie und
  Landmarken. Google bewertet die Mobilversion, und Barrierefreiheit hilft
  hier doppelt.
- Schnelle Ladezeit (Core Web Vitals): kein jQuery und keine Slider. Die
  Schriften liegen selbst gehostet als WOFF2 vor, mit `font-display: swap` und
  nur den nötigen Schnitten. Bilder kommen in passenden Größen (`srcset`) und
  werden erst beim Scrollen geladen (Lazy Loading).
- **Strukturierte Daten (JSON-LD):**
  - `Organization`: Verein, Logo, Adresse, Profile
  - `WebSite`
  - `Event` für jeden Leseabend mit Datum, Ort und Status. Bei „entfällt“
    wird der Status `EventCancelled` ausgegeben. Damit hat der Termin die
    Chance, in der Google-Veranstaltungssuche zu erscheinen. Ob Google ihn
    tatsächlich anzeigt, entscheidet Google.
- Es gibt **genau eine** XML-Sitemap: entweder die von WordPress oder die des
  SEO-Plugins. Die `robots.txt` verweist auf sie und sperrt weder CSS noch JS.
- Canonical-Tags und eine einzige Hostvariante (https, mit oder ohne www, so
  wie bisher). Das prüfe ich beim Crawl.
- Seiten mit wenig Inhalt werden abgeschaltet oder auf `noindex` gesetzt:
  Anhangseiten, Autoren- und Datumsarchive, Schlagwortarchive, falls sie kaum
  genutzt werden.
- Die 404-Seite bietet eine Suche und Links zu den Übersichtsseiten.
- Der Feed `/feed/` bleibt erreichbar.

## 5. SEO-Plugin

- Ist schon eines aktiv (Yoast, Rank Math, All in One SEO …), behalten wir es,
  sofern es mit PHP 8.4 läuft. Dann bleiben die gespeicherten Titel und
  Beschreibungen erhalten.
- Ist keines aktiv, nehmen wir ein schlankes Plugin für Titel,
  Beschreibungen, Sitemap und Social-Media-Vorschau. Die Entscheidung treffen
  wir in Schritt 6 (Plugin-Check).

## 6. Am Umstellungstag und danach

- Die Weiterleitungen gehen **im selben Moment** live wie die neue Struktur,
  nicht später.
- Alle alten URLs werden automatisch geprüft: Jede muss mit 301 antworten und
  auf eine Seite mit Status 200 führen. Das Skript dafür folgt.
- Unter Einstellungen → Lesen muss „Suchmaschinen davon abhalten, diese
  Website zu indexieren“ **aus** sein. Dieser Haken ist der häufigste Fehler
  nach einem Relaunch.
- In der Search Console die Sitemap neu einreichen und für die wichtigsten
  Seiten über die URL-Prüfung „Indexierung beantragen“ anklicken.
- 4–8 Wochen beobachten: Search Console → Seiten (404 und
  Weiterleitungsfehler) sowie Leistung im Vergleich zur Ausgangslage.
  Schwankungen in den ersten 2–6 Wochen sind normal.
- Wo möglich, Partner bitten, Links von außen auf die neuen URLs umzustellen.
  Die eigenen Social-Media-Profile und Verzeichniseinträge passen wir selbst an.

## 7. Chancen, das Ranking zu verbessern

- Leseabende als strukturierte Termine (siehe oben). Regelmäßig neue Termine
  zeigen außerdem, dass die Seite aktiv ist.
- Klare Seiten zu den Begriffen, nach denen Interessierte tatsächlich suchen.
  Welche das sind, zeigt die Auswertung der Search-Console-Daten.
- Neuerscheinungen der Mitglieder mit Titel, Autorin bzw. Autor und Verlag.
  Das bringt Besucher über Suchen nach Buchtiteln und Namen.
- Bessere Ladezeit und Mobildarstellung als das alte Theme.
