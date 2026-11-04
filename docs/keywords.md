# Suchbegriffe für die neue Seite

Diese Datei ergänzt `docs/seo.md`. `seo.md` beschreibt, wie das Ranking beim
Relaunch erhalten bleibt. Diese Datei beschreibt, für welche Suchbegriffe wir
die Seiten bauen.

Stand: 04.11.2026. Grundlage sind Stichproben der Suchergebnisse (mit einem
Suchwerkzeug, nicht direkt bei Google) und der Bestand der Live-Seite
(`docs/bestand-live.md`). Suchvolumen fehlen hier mit Absicht, weil niemand sie
gemessen hat. Für kleine lokale Begriffe zeigen Tools wie Semrush oft gar keine
oder nur grobe Werte. Die verlässlichste Quelle ist der Search-Console-Export
(siehe `docs/seo.md`, Abschnitt 1). Sobald er da ist, prüfen wir diese Liste
gegen die echten Suchanfragen.

## Wer sucht?

1. **Schreibende**, die einen Ort zum Vorlesen und ehrliche Rückmeldung suchen.
   Sie sind die wichtigste Zielgruppe, denn aus ihnen werden Lesende und
   Mitglieder.
2. **Publikum**, das in Berlin eine Lesung oder Lesebühne besuchen will.
3. **Leserinnen und Leser**, die ein Buch oder eine Autorin oder einen Autor
   aus dem Verein suchen.
4. **Presse, Partner, Förderer**, die nach dem Verein selbst suchen.

## Startseite

**Zielbegriff: „offene Lesebühne Berlin“.** Dazu kommen „Textkritik“ und der
Vereinsname.

Warum dieser Begriff:

- „Lesebühne Berlin“ beschreibt das Angebot, die Ergebnisse dazu bestehen aber
  fast nur aus Listen, Ticketportalen und Presseartikeln (visitBerlin,
  berlin.de, rausgegangen, tip Berlin, top10berlin, Tagesspiegel, taz). Meist
  geht es dort um Unterhaltungsshows. Eine kleine Vereinsseite überholt diese
  Seiten kaum. In diese Ergebnisse kommt der Verein nur, wenn er selbst in den
  Listen steht (siehe unten).
- „offen“ trifft den Kern des Leseabends: Alle dürfen eigene Texte lesen. Für
  diese Kombination gibt es in Berlin wenig Konkurrenz, und die Absicht der
  Suchenden passt.
- „Textkritik“ ist das zweite Merkmal, das den Verein unterscheidet („Hart zum
  Text, sanft zum Autor“). Danach wird auch außerhalb Berlins gesucht.
- „Autorenforum Berlin“ steht schon im Namen. Damit passt der Titel auch
  teilweise zu Suchen wie „Autoren Berlin“.

So setzen wir es um:

- **Seitentitel** (52 Zeichen): `Autorenforum Berlin: offene Lesebühne mit Textkritik`
- **Meta-Description** (149 Zeichen): `Montags lesen Autorinnen und Autoren
  unveröffentlichte Texte und bekommen ehrliche Textkritik. Offene Lesebühne in
  Berlin: zuhören oder selbst lesen.`
- **H1:** Ein poetischer Satz als Überschrift ist erlaubt. Dann gehören
  „offene Lesebühne“, „Berlin“ und „Textkritik“ als echter Text in die ersten
  zwei Sätze darunter, nicht in ein Bild.
- Die nächsten Termine stehen als Text auf der Startseite, mit Event-Daten
  (siehe `docs/seo.md`, Abschnitt 4).
- **Sofort möglich, schon vor dem Relaunch:** Die Startseite heißt heute
  „Autorenforum Berlin e.V. -“. Der Strich am Ende entsteht, weil der
  Untertitel der Website leer ist. Dominik kann den Titel in Yoast SEO unter
  Einstellungen → Inhaltstypen → Startseite setzen, zusammen mit der
  Meta-Description. Falls die Startseite eine statische Seite ist, führt dort
  ein Link zu dieser Seite; die Felder stehen dann in deren Yoast-Box unter
  „Suchdarstellung“. Die Instanz ändert an der Live-Seite nichts.

## Zuordnung: ein Hauptbegriff pro Seite

Auch wenn die Seite stark gekürzt wird: Jede Suchabsicht braucht eine eigene
URL, die zu ihr passt. Was nur noch ein Abschnitt ist, bekommt eine
Sprungmarke. Die heutige URL bleibt, oder sie leitet per 301 auf die passende
neue Seite weiter.

| Seite oder Abschnitt | Hauptbegriff | Nebenbegriffe | Heutige URL | Hinweis |
|---|---|---|---|---|
| Startseite | offene Lesebühne Berlin | Lesebühne Berlin, Leseabend Berlin, Textkritik, Autorenforum Berlin | `/` | siehe oben |
| Leseabend: selbst lesen | eigene Texte vorlesen Berlin | Autorengruppe Berlin, Schreibgruppe Berlin, Feedback für eigene Texte, Werkstattbühne | `/offener-leseabend/` | Ablauf, Anmeldung, Regeln. Fragen und Antworten passen hier gut („Darf ich das erste Mal lesen?“, „Wie lang darf mein Text sein?“). |
| Textkritik | Textkritik | Textkritik in der Gruppe, Feedback Schreibgruppe, heißer Stuhl | `/der-heisse-stuhl/` | Die Methode genau erklären. Das ist der Teil, den andere nicht haben. |
| Termine | Lesung Berlin Montag | Lesungen Berlin, Lesung mit Ortsteil (z. B. Steglitz) | `/termine/` | Die Event-Daten sind hier wichtiger als der Text. |
| Veröffentlichungen | Buchtitel und Namen der Mitglieder | Neuerscheinung, Autorin aus Berlin | `/category/veroeffentlichungen_der_mitglieder/` und die Beitrags-URLs | Die Beiträge bringen Besucher über Buchtitel und Namen. Die einzelnen Beitrags-URLs behalten, auch wenn die Übersicht neu wird. |
| Wettbewerbe | Literaturwettbewerb Berlin, Schreibwettbewerb mit Jahreszahl | Kurzgeschichtenwettbewerb | `/wettbewerbe/` und die Jahresseiten | Aktiv bewerben nur, solange ein Wettbewerb läuft. Alte Jahrgänge bleiben als Archiv. |
| Nikolauslesung | Nikolauslesung Berlin | Weihnachtslesung Berlin | `/nikolauslesung/` | saisonal, ab Anfang November aktuell halten |
| Verein und Geschichte | Autorenforum Berlin | Autorenverein Berlin, Literaturverein Berlin (beide noch nicht geprüft) | `/verein/`, `/geschichte/` | für Markensuche und Presse |

## Vereinsname

Bei den Stichproben zu „Autorenforum Berlin Leseabend“ standen rausgegangen
und visitBerlin mit Terminen des Vereins oben, die eigene Seite nicht. Das war
nicht Google selbst. Bitte einmal im privaten Fenster bei Google suchen und in
der Search Console prüfen, auf welcher Position die Seite bei „Autorenforum
Berlin“ steht. Steht sie nicht auf Platz 1, hat das Vorrang: Die
`Organization`-Daten (siehe `docs/seo.md`), überall derselbe Name und Links aus
den Einträgen unten helfen dabei.

## In die Listen kommen

Bei „Lesebühne Berlin“ entscheiden Listen und Kalender. Jeder Eintrag bringt
Besucher und einen Link. Er soll auf `/offener-leseabend/` oder `/termine/`
zeigen, nicht nur auf die Startseite.

- **visitBerlin** führt schon einzelne Veranstaltungen des Vereins. Die
  Leseabende dort regelmäßig eintragen.
- **rausgegangen** führt den „Leseabend Werkstattbühne“ schon. Die Einträge
  aktuell halten.
- **top10berlin** (Schlagwort Lesebühne), **tip Berlin** und **berlinecho**
  (Übersicht über Berliner Lesebühnen vom Juni 2026): fragen, ob die offene
  Lesebühne aufgenommen wird.
- **the-berliner.com** hat eine Übersicht über Schreibgruppen in Berlin. Sie ist
  auf Englisch. Sie lohnt sich nur, wenn auch Gäste kommen sollen, die kaum
  Deutsch verstehen.
- Noch zu prüfen: der Kalender von literaturport.de und die Kalender der
  Bezirke.

## Messen

- **Search Console:** Ausgangslage vor dem Relaunch sichern, danach monatlich
  vergleichen (Klicks, Impressionen, Position).
- **Begriffe zum Beobachten:** Autorenforum Berlin, offene Lesebühne Berlin,
  Lesebühne Berlin, eigene Texte vorlesen Berlin, Autorengruppe Berlin,
  Schreibgruppe Berlin, Textkritik, Nikolauslesung Berlin und die Buchtitel der
  letzten Neuerscheinungen.
- **Semrush:** gut für die großen Begriffe (Lesebühne Berlin, Lesung Berlin,
  Schreibgruppe Berlin, Textkritik) und um zu sehen, für welche Begriffe
  rausgegangen, tip Berlin oder top10berlin mit ihren Lesebühnen-Seiten ranken.
  Bei den kleinen Begriffen ist ein leeres Ergebnis normal. Es heißt nicht,
  dass niemand danach sucht.
