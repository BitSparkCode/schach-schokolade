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

1. Die Figuren werden als Modelle (Master) in CAD entworfen und auf dem Bambu Lab gedruckt, danach geschliffen und lackiert, bis keine Druckrillen mehr sichtbar sind.
2. Um die Master wird lebensmittelechtes Platin-Silikon gegossen. Nur das Silikon berührt die Schokolade.
3. Gedruckte Stützschalen halten die zweiteiligen Silikonformen, Passkegel und Klammern verhindern jedes Verrutschen.
4. Gegossen wird kopfüber durch den Standfuss, der Fuss ist der Anguss. Entlüftungskanäle liegen in der Trennebene.
5. Nach dem Auskühlen werden Stützschale und Silikon abgenommen, die Figur bleibt ganz.

## Repository-Struktur (geplant)

```
cad/        parametrische Modelle (CadQuery, Python)
stl/        Druckdateien für Bambu Studio
docs/       Pläne, Recherche, Ablauf
verpackung/ Falzmuster, Einlage, Deckeldruck
```
