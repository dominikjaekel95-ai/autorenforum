# Autorenforum Berlin e.V. – Website-Relaunch

Neues, schlankes WordPress-Block-Theme für autorenforum-berlin.de
(Ziel: PHP 8.4, Pflege im Block-Editor ohne Technikkenntnisse).

## Ordner

| Ordner      | Inhalt                                                        |
|-------------|---------------------------------------------------------------|
| `docs/`     | Bestandsaufnahme, neue Struktur, Weiterleitungen, Anleitungen |
| `theme/`    | Block-Theme (folgt nach Freigabe der Struktur)                |
| `privat/`   | Exporte, Backups, Zugangsdaten – **wird nie committet**       |

## Wichtig

- WordPress-Exporte (`*.xml`), Datenbank-Dumps, ZIP-Backups und Zugangsdaten
  gehören in `privat/`. Die `.gitignore` verhindert, dass sie ins Repo gelangen.
- Zugangsdaten für das Deployment werden ausschließlich als
  GitHub-Repository-Secrets hinterlegt.
