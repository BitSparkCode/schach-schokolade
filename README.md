# Max' Schach Schokolade

Ein vollständiges Schachspiel aus Schokolade: 16 Figuren aus dunkler und 16 Figuren aus weisser Schokolade, als ganze, freistehende Figuren gegossen. Die Formen und Hilfsteile entstehen auf einem Bambu Lab Drucker, die Verpackung zeigt auf dem Deckel das Schachbrett.

## Stand

Planungsphase. Gebaut wird erst nach Freigabe des Plans.

## Dokumente

| Dokument | Inhalt |
|---|---|
| [docs/01-recherche.md](docs/01-recherche.md) | Was andere gemacht haben, was funktioniert und was nicht, lebensmittelechtes Filament, Entformen |
| [docs/02-plan-giessform.md](docs/02-plan-giessform.md) | Plan für die Giessform: Aufbau, Anguss, Entlüftung, Fixierung, Kühlen, Entformen, Phasen |
| [docs/03-figuren.md](docs/03-figuren.md) | Figurenset: Masse, Gestaltungsregeln, Gewicht |
| [docs/04-ablauf-giessen.md](docs/04-ablauf-giessen.md) | Ablauf eines Gusstags für dunkle und weisse Schokolade |
| [docs/ideen.md](docs/ideen.md) | Ideen und offene Fragen |
| [verpackung/](verpackung/) | Verpackung mit Falzmuster, erhöhter Einlage und Schachbrett-Deckel (eigene Session) |

## Kurzfassung des Plans

1. Die Giessform wird direkt auf dem Bambu Lab gedruckt, aus lebensmittelechtem PLA Pure mit Edelstahl- oder Stahldüse. Kein Silikon.
2. Gegen Rillen: Formhälften stehend mit 0.08 mm gedruckt, Kavitäten nass geschliffen bis Körnung 3000.
3. Die Figuren haben keine Hinterschnitte, damit sich die starren Hälften senkrecht abheben lassen.
4. Gegossen wird kopfüber durch den Standfuss, der Fuss ist der Einguss. Entlüftung über 45°-Schrägen und Kanäle in der Trennebene.
5. Passstifte, Magnete und ein Spannrahmen verhindern jedes Verrutschen.
6. Waschen von Hand mit warmem Wasser bis 45 °C, Kakaobutter schmilzt bei etwa 34 °C.

## Repository-Struktur (geplant)

```
cad/        parametrische Modelle (CadQuery, Python)
stl/        Druckdateien für Bambu Studio
docs/       Pläne, Recherche, Ablauf
verpackung/ Falzmuster, Einlage, Deckeldruck
```
