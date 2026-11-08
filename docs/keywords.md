# Suchbegriffe für die neue Seite

Diese Datei ergänzt `docs/seo.md`. `seo.md` beschreibt, wie das Ranking beim
Relaunch erhalten bleibt. Diese Datei beschreibt, für welche Suchbegriffe wir
die Seiten bauen.

Stand: 08.11.2026. **Vorschlag, die Entscheidung treffen Dominik und der
Verein.** Grundlage sind Stichproben der Suchergebnisse (mit einem
Suchwerkzeug, nicht direkt bei Google), der Bestand der Live-Seite
(`docs/bestand-live.md`) und die Planung des Vereins für die neue Struktur.
Suchvolumen stehen nur da, wo Dominik sie aus Semrush geliefert hat. Für kleine
lokale Begriffe sind diese Werte grob.
Die verlässlichste Quelle ist der Search-Console-Export (siehe `docs/seo.md`,
Abschnitt 1).

## Neue Struktur laut Verein

- **Aktuelles** als Startseite, mit dem nächsten Montagabend ganz oben
  (Details in `docs/anforderungen.md`)
- **Werkstattbühne**: neuer Name für den Leseabend, Untertitel „Lesung und
  Diskussion von unveröffentlichten Texten“. Im Menü nennt der Verein den
  Punkt auch „Werkstattabend“; der Name ist noch abzustimmen.
- **Anregungen zur Textkritik**: eigene Seite. Die Fragen stehen heute mit auf
  `/offener-leseabend/`.
- **Termine**: das Quartal mit Moderation. Sichtbar sein sollen Montag, Beginn
  20 Uhr und Anmeldung zum Lesen ab 19:30 Uhr.
- **Über uns**, mit Kontaktadresse und Kontoverbindung
- **Veröffentlichungen der Mitglieder**, mit Suchfeld
- Impressum und Datenschutz nur im Footer

Ohne eigene Seite in der neuen Struktur: Wettbewerbe mit den Jahresseiten,
Nikolauslesung, Der heiße Stuhl, Geschichte, Organisation, Kontakt, Anfahrt,
Archiv. Ihre Adressen brauchen Weiterleitungen (siehe `docs/seo.md`,
Abschnitt 2).

## Grundsätze

- Die Texte des Vereins bleiben weitgehend, wie sie sind. Die Suchbegriffe
  tragen der Seitentitel, die Meta-Description und der Text der Startseite,
  den wir selbst schreiben.
- Ein Hauptbegriff gehört auf genau eine Seite. Sonst konkurrieren die Seiten
  um denselben Begriff.
- Seitentitel 55 bis 60 Zeichen, Meta-Description bis 155 Zeichen.
- In Titeln und auf der Startseite steht „Autorinnen und Autoren“. Die
  Doppelform enthält das Suchwort „Autoren“ sicher. Ob Google „Autor*innen“
  genauso liest, ist nicht gesichert. In den übrigen Texten bleibt der Stern.

## Startseite `/`

**Hauptbegriff: „Autoren Berlin“, Nebenbegriff: „Lesebühne Berlin“.**
Semrush (08.11.2026): „autoren berlin“ 30 Suchen im Monat, „lesebühne berlin“
10. Für „Lesebühne Berlin“ rankt die Seite derzeit nicht.

- Google braucht die Wortfolge nicht exakt. Stehen „Lesebühne“, „Autoren“ und
  „Berlin“ im Titel und im Text, kann die Seite für beide Begriffe ranken.
- Die Texte des Vereins enthalten „Lesebühne“ nicht und „Autoren“ nur als
  „Autor*innen“. Den Text der Startseite schreiben wir selbst. Deshalb gehören
  beide Begriffe dorthin und nicht auf eine Unterseite.
- Die Startseite steht für den ganzen Verein. „Autoren Berlin“ passt zu
  Schreibenden, die andere Autorinnen und Autoren suchen, und zu Lesenden, die
  Berliner Autorinnen und Autoren und ihre Bücher suchen. Der Begriff steckt
  außerdem im Vereinsnamen und in der Domain.
- Einschränkung: Bei „Lesebühne Berlin“ suchen viele nach Shows mit fertigen,
  oft lustigen Texten (die Ergebnisse dort: visitBerlin, berlin.de,
  rausgegangen, tip Berlin, top10berlin, Tagesspiegel, taz). Die Werkstattbühne
  ist das Gegenteil: keine fertigen Texte, kein Applaus. „Lesebühne für
  Autorinnen und Autoren“ im Titel sortiert vor.

So setzen wir es um:

- **Seitentitel** (57 Zeichen): `Autorenforum Berlin: Lesebühne für Autorinnen und Autoren`
- Alternative ohne „Lesebühne“ (55 Zeichen): `Autorenforum Berlin – Verein für Autorinnen und Autoren`.
  Sie ist die bessere Wahl, falls „autorenverein berlin“ nennenswert gesucht
  wird.
- **Meta-Description** (146 Zeichen), aus vorhandenen Sätzen des Vereins:
  `Berlins älteste wöchentliche Lesebühne: Kein Applaus. Konstruktive Kritik.
  Bessere Texte. Immer montags, immer 20 Uhr, in der Schwartzschen Villa.`
- **H1:** „Berlins älteste wöchentliche Lesebühne“ (aus dem Meetup-Text des
  Vereins), darunter „Kein Applaus. Konstruktive Kritik. Bessere Texte.“ (aus
  der heutigen Meta-Description). „Autorinnen und Autoren“ steht im ersten
  Satz des Textes.
- **Interne Links:** Die Startseite verlinkt die Werkstattbühne, die Termine,
  die Anregungen zur Textkritik und die Veröffentlichungen, mit Linktexten, die
  sagen, wohin sie führen.
- Die nächsten Termine stehen als Text auf der Startseite, mit Event-Daten
  (siehe `docs/seo.md`, Abschnitt 4).
- **Vorher prüfen:** In der Search Console unter Leistung → Suchanfragen nach
  „autoren“ und nach „lesebühne“ filtern. Begriffe, für die die Seite schon
  Impressionen hat, müssen den Relaunch überstehen.
- **Sofort möglich, schon vor dem Relaunch:** Die Startseite heißt heute
  „Autorenforum Berlin e.V. -“, weil der Untertitel der Website leer ist.
  Dominik kann Titel und Meta-Description in Yoast SEO unter Einstellungen →
  Inhaltstypen → Startseite setzen. Die Instanz ändert an der Live-Seite
  nichts.

## Unterseiten

### Werkstattbühne

- **Hauptbegriff:** „Feedback zu eigenen Texten“, dazu „unveröffentlichte
  Texte“ und der Name „Werkstattbühne“. Der Text des Vereins handelt genau
  davon. „Lesebühne“ steht hier nicht, weil die Startseite den Begriff trägt.
- **Adresse:** `/offener-leseabend/` bleibt. Will der Verein den neuen Namen in
  der Adresse, dann `/werkstattbuehne/` mit 301 von der alten Adresse.
- **Seitentitel** (60 Zeichen): `Werkstattbühne Berlin: Feedback zu unveröffentlichten Texten`
- **Meta-Description** (145 Zeichen): `Lies deinen unveröffentlichten Text vor
  und hol dir Rückmeldung von 30 bis 60 Schreibenden und
  Literaturinteressierten. Jeden Montag in Steglitz.`

### Anregungen zur Textkritik

- **Hauptbegriff:** „Textkritik für Schreibende“, dazu „Fragen an einen
  literarischen Text“. „Textkritik“ allein meint bei Google vor allem die
  Editionswissenschaft (alte Handschriften, Bibeltexte).
- **Adresse:** neu, zum Beispiel `/anregungen-zur-textkritik/`. Die
  Werkstattbühne verlinkt sie.
- **Seitentitel** (56 Zeichen): `Textkritik für Schreibende: Fragen an literarische Texte`
- **Meta-Description** (146 Zeichen): `Fragen an einen literarischen Text:
  Anregungen zur Textkritik aus der Werkstattbühne des Autorenforums Berlin,
  für Schreibende und Schreibgruppen.`

### Termine

- **Hauptbegriffe:** „Werkstattbühne Termine“, „Lesung Berlin-Steglitz“,
  „Schwartzsche Villa“. Wichtiger als der Text sind die Event-Daten.
- **Adresse:** `/termine/` bleibt.
- **Seitentitel** (58 Zeichen): `Werkstattbühne Termine: montags 20 Uhr, Schwartzsche Villa`
- **Meta-Description** (139 Zeichen): `Alle Termine der Werkstattbühne mit
  Moderation: montags um 20 Uhr in der Schwartzschen Villa in Steglitz.
  Anmeldung zum Lesen ab 19:30 Uhr.`

### Über uns

- **Hauptbegriff:** „Autorenverein Berlin“.
- **Adresse:** `/verein/` bleibt. `/geschichte/`, `/organisation/` und
  `/kontakt/` leiten dorthin weiter.
- **Seitentitel** (59 Zeichen): `Autorenverein in Berlin: Über das Autorenforum Berlin e. V.`
- **Meta-Description** (147 Zeichen): `Das Autorenforum Berlin e. V. fördert
  seit über 40 Jahren unbekannte Autorinnen und Autoren: mit der
  Werkstattbühne, mit Lesungen und Wettbewerben.`
- Gründungsjahr ist 1984 (40-jähriges Jubiläum 2024). Die heutige
  Meta-Description mit „seit 1987“ ist falsch.

### Veröffentlichungen der Mitglieder

- **Hauptbegriffe:** „Bücher Berliner Autorinnen und Autoren“ sowie Namen und
  Buchtitel. Die Beiträge zu den Neuerscheinungen stützen zugleich „Autoren
  Berlin“ auf der Startseite.
- **Adresse:** `/category/veroeffentlichungen_der_mitglieder/` und die
  Beitrags-URLs bleiben.
- **Seitentitel** (56 Zeichen): `Neuerscheinungen: Bücher Berliner Autorinnen und Autoren`
- **Meta-Description** (132 Zeichen): `Neuerscheinungen von Mitgliedern des
  Autorenforums Berlin: Romane, Erzählungen, Gedichte und mehr, durchsuchbar
  nach Titel und Name.`
- Für die einzelnen Beiträge genügt die Titelvorlage von Yoast.

### Impressum und Datenschutz

Keine Optimierung nötig. Ein kurzer Titel wie „Impressum | Autorenforum Berlin
e. V.“ reicht.

## Vereinsname

Bei den Stichproben zu „Autorenforum Berlin Leseabend“ standen rausgegangen
und visitBerlin mit Terminen des Vereins oben, die eigene Seite nicht. Das war
nicht Google selbst. Bitte einmal im privaten Fenster bei Google suchen und in
der Search Console prüfen, auf welcher Position die Seite bei „Autorenforum
Berlin“ steht. Steht sie nicht auf Platz 1, hat das Vorrang: Die
`Organization`-Daten (siehe `docs/seo.md`), überall derselbe Name („Autorenforum
Berlin e. V.“) und Links aus den Einträgen unten helfen dabei.

## In die Listen kommen

Bei „Lesebühne Berlin“ entscheiden Listen und Kalender, und auch bei „Autoren
Berlin“ gibt es Listenartikel. Jeder Eintrag bringt Besucher und einen Link.
Er soll auf die passende Unterseite zeigen, meist auf die Werkstattbühne oder
die Termine.

- **visitBerlin** führt schon einzelne Veranstaltungen des Vereins. Die Abende
  dort regelmäßig eintragen.
- **rausgegangen** führt den „Leseabend Werkstattbühne“ schon. Die Einträge
  aktuell halten und auf den neuen Namen umstellen.
- **top10berlin** (Schlagwort Lesebühne), **tip Berlin** und **berlinecho**
  (Übersicht über Berliner Lesebühnen vom Juni 2026): fragen, ob die
  Werkstattbühne aufgenommen wird.
- **berlinecho** hat außerdem eine Übersicht über Berliner Autoren und
  Schriftsteller (Juni 2026). Ein Hinweis auf den Verein passt dort zu
  „Autoren Berlin“.
- **the-berliner.com** hat eine Übersicht über Schreibgruppen in Berlin. Sie ist
  auf Englisch und lohnt sich nur, wenn auch Gäste kommen sollen, die kaum
  Deutsch verstehen.
- Noch zu prüfen: der Kalender von literaturport.de, die Kalender des Bezirks
  Steglitz-Zehlendorf und der Schwartzschen Villa.

## Messen

- **Search Console:** Ausgangslage vor dem Relaunch sichern, danach monatlich
  vergleichen (Klicks, Impressionen, Position).
- **Begriffe zum Beobachten:** Autoren Berlin, Lesebühne Berlin, Autorenforum
  Berlin, Werkstattbühne, Feedback zu eigenen Texten, Textkritik für
  Schreibende, Autorenverein Berlin, Lesung Steglitz, Schwartzsche Villa und
  die Buchtitel der letzten Neuerscheinungen.
- **Semrush:** gut für die großen Begriffe (Autoren Berlin, Lesebühne Berlin,
  Lesung Berlin) und um zu sehen, wofür rausgegangen, tip Berlin oder
  top10berlin ranken. Bei den kleinen Begriffen ist ein leeres Ergebnis normal.
  Es heißt nicht, dass niemand danach sucht.
