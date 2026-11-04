# Referenz

`autorenforum-entwurf-3.html` ist ein Pitch-Entwurf, den Dominik mit Claude
gebaut hat. Die Datei läuft für sich im Browser, ohne Server und ohne
Internetverbindung.

**Sie ist keine Design-Vorgabe.** Das endgültige Design kommt aus Figma. Die
Datei zeigt, welche Funktionen der Verein gesehen hat und welche er vielleicht
wiederhaben möchte:

- Das Programm steht an genau einer Stelle (Array `PROGRAMM` im Skript). Der
  nächste Termin und der Countdown werden daraus berechnet, mit der Zeitzone
  Europe/Berlin. Termine, die entfallen, zeigen einen Hinweis.
- Kalenderdatei (ICS) für den nächsten Termin, für einzelne Termine und für
  alle Termine zusammen.
- Auf- und zuklappbare Abschnitte (Akkordeon) zur Textkritik.
- Zurückhaltende Animationen: Die Überschrift erscheint Wort für Wort,
  „Hart zum Text, sanft zum Autor“ Buchstabe für Buchstabe, „Weichspüler“ wird
  beim Scrollen durchgestrichen. Bei `prefers-reduced-motion` sind sie aus.
- Vorlesen per `speechSynthesis`, eine zufällige Frage zum Mitnehmen, Plan
  drucken, Abendmodus, größere Schrift.
- Montags von 19:30 bis 23:00 erscheint ein Hinweis, dass der Leseabend gerade
  läuft.
- Vorführmodus mit simulierter Uhrzeit, aufrufbar über
  `?jetzt=JJJJ-MM-TTTHH:MM` oder `?heute=JJJJ-MM-TT`.

Eingebettete Schriften: EB Garamond und Schibsted Grotesk, beide unter der SIL
Open Font License 1.1. Die Schriften für das echte Theme werden nach dem
Figma-Design ausgewählt und selbst gehostet (siehe `docs/seo.md`).
