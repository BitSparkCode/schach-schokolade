# Plan: Giessform für ganze Schachfiguren

Ziel: 32 massive, ganze Figuren (16 dunkel, 16 weiss), glatte Oberfläche ohne sichtbare Rillen, Form wiederverwendbar, Form direkt auf einem Bambu Lab gedruckt. Ohne Silikon.

## 1. Grundentscheid

| Variante | Oberfläche | Lebensmittelkontakt | Entformen | Entscheid |
|---|---|---|---|---|
| A. Starre Form direkt aus lebensmittelechtem Filament, Kavitäten geschliffen | Glatt, sofern stehend gedruckt und nachgeschliffen. Im Bauern-Prototyp zu prüfen. | Filament (PLA Pure), Handwäsche warm | Starr, nur Figuren ohne Hinterschnitte | **Gewählt** (Wunsch Moritz: ohne Silikon) |
| B. Wie A, Kavitäten zusätzlich mit lebensmittelechtem Epoxid beschichtet | Hochglanz | Beschichtung, Zulassung für Fett nötig | Wie A | Rückfallebene 1, falls A Rillen zeigt |
| C. Gedruckter Master, Silikonform in Stützschale | So glatt wie der Master | Platin-Silikon | Silikon gibt nach | Rückfallebene 2 |

Eine starre Form funktioniert, weil Rotationskörper (Bauer, Turm, Läufer, Dame, König) bei einer Trennebene durch die Mittelachse keine Hinterschnitte haben. Die zwei Hälften lassen sich senkrecht zur Trennebene abheben. Springer, Königskreuz und Turmzinnen werden so gestaltet, dass auch sie keine Hinterschnitte haben (docs/03-figuren.md). Industrielle Formen aus Polycarbonat arbeiten genauso: zwei starre Hälften, temperierte Schokolade schwindet und löst sich.

## 2. Waschen und Hygiene

- Kakaobutter schmilzt bei etwa 34 °C. Warmes Wasser (40 bis 45 °C) mit Spülmittel löst die Schokolade auch aus feinen Rillen. Weiche Bürste, keine Scheuerschwämme (Kratzer bilden sich auf der Schokolade ab).
- PLA Pure: Handwäsche bis etwa 45 °C, Bambu nennt 60 °C als Grenze. Keine Spülmaschine, kein kochendes Wasser.
- Schokolade enthält kaum Wasser, Keime finden darin wenig Nährboden. Feuchtigkeit in Rillen ist das grössere Risiko: Formen offen und vollständig trocknen lassen, Restwasser lässt die Schokolade beim nächsten Guss stocken.
- Formen sind Verbrauchsteile: bei Kratzern, Verfärbung oder Geruch neu drucken. Eine Platte kostet wenig Filament.

## 3. Rillen vermeiden

Die Schokolade bildet jede Schicht und jeden Kratzer der Kavität ab. Drei Massnahmen zusammen:

1. **Druckausrichtung**: Formhälften stehend drucken, Figurenachse senkrecht, Kopf unten (Giesslage). Die Schichten laufen dann als feine waagrechte Ringe um die Figur, wie bei einem gedrechselten Stück. Liegend gedruckt würden die Rundungen als Treppenstufen abgebildet.
2. **Druckeinstellungen**: 0.08 mm Schichthöhe, variable Schichthöhe in Bambu Studio für flache Partien (Kopf, Kragenoberseiten), langsame Aussenwand, Naht (Seam) auf die Rückseite der Platte statt in die Kavität, 5 Wandlinien rund um die Kavität. Einstellungen für den P2S: docs/05-cad-und-druck.md.
3. **Nachbearbeitung der Kavität**: Nassschliff 400, 800, 1500, 3000, mit runden Schleifstäben und Schleifschwamm. Nur Wasser und Schleifpapier, keine Polierpaste und kein Lack (nicht lebensmittelecht). Das Material bleibt dasselbe, die Konformität gilt weiter. Danach waschen.

Gleiche Regel löst zwei Probleme: Wird in Giesslage gedruckt, sind die Kavitätendecken in Giesslage gleichzeitig Überhänge im Druck. Die 45°-Regel für die Entlüftung (Abschnitt 6) macht die Form ohne Stützmaterial druckbar. Stützmaterial in der Kavität ist verboten, es hinterlässt raue Stellen.

Abnahmekriterium im Prototyp: Auf Armlänge sind keine Ringe sichtbar, unter Streiflicht dürfen feine Ringe erkennbar sein. Wenn nicht erreicht: Rückfallebene B.

## 4. Aufbau: eine Buchform für alle 16 Figuren

Alle 16 Figuren einer Farbe werden in einem Guss gegossen (Wunsch Moritz). Die Form besteht aus 5 senkrechten Platten, die wie Buchseiten hintereinander stehen. Zwischen zwei Platten liegt je eine Trennebene mit einer Reihe von 4 Kavitäten. Die 3 Innenplatten tragen auf beiden Seiten Halbkavitäten. CAD: `cad/form.py`, Masse und Druck: docs/05-cad-und-druck.md.

```
        Trichterplatte mit 16 Trichtern, Schürze rundum
   ┌────────────────────────────────────────────────────┐
   └────────────────────────────────────────────────────┘
   │P1│ Reihe 1 │P2│ Reihe 2 │P3│ Reihe 3 │P4│ Reihe 4 │P5│
   │  │ K D L L │  │ S S T T │  │ B B B B │  │ B B B B │  │
   ◉──────────── 4 Gewindestangen M5 mit Flügelmuttern ────◉
```

| Reihe | Kavitäten |
|---|---|
| 1 | König, Dame, Läufer, Läufer |
| 2 | Springer, Springer, Turm, Turm |
| 3 | 4 Bauern |
| 4 | 4 Bauern |

| Teil | Material | Funktion |
|---|---|---|
| Platten 1 bis 5 | PLA Pure White | Kavitäten, 161 × 64 mm, 16 bis 28.5 mm dick, dazu 3 mm Noppen |
| 4 Gewindestangen M5 × 160, Edelstahl, mit Unterlagscheiben und Flügelmuttern | Edelstahl | Führen und Spannen in einem. Ersetzt Spannrahmen und Magnete. |
| Kegelnoppen Ø 8 × 3 mm, 45° Flanke, 2 pro Trennebene | PLA Pure White, mitgedruckt | Platten zentrieren sich beim Schliessen selbst, Naht ohne Stufe. Die ungeraden Platten (1, 3, 5) tragen die Noppen, die geraden (2, 4) die Aufnahmen. Links sitzt die Noppe 4 mm tiefer, rechts 4 mm höher, so passt jede Platte nur richtig herum. |
| Trichterplatte | PLA Pure White | Ein Trichter pro Figur, Schürze sitzt auf dem Plattenstapel |

Die Bohrungen für die Gewindestangen haben 0.4 mm Spiel, die genaue Lage geben die Kegelnoppen. Die Aufnahmen sind 0.1 mm weiter und 0.5 mm tiefer, damit zuerst die Trennflächen aufliegen. Geöffnet wird durch Abziehen der Platten entlang der Stangen, also senkrecht zur Trennebene.

**Dichte Naht**: Die Trennflächen werden stehend gedruckt und sind dadurch nicht ganz plan. Nach dem Druck jede Trennfläche mit Nassschliffpapier 400 und 800 plan schleifen (Läppen), bis sie vollflächig trägt. Die geraden Platten liegen dazu flach auf der Glasplatte. Bei den ungeraden Platten stehen die Noppen vor: Sie werden auf einem schmalen Glas- oder Fliesenstreifen geschliffen, 125 bis 130 mm breit (Probeform 55 bis 60 mm), die Noppen ragen seitlich vorbei. Geschliffen wird nur in Längsrichtung des Streifens. Dann zeichnet sich nur eine feine Linie ab, die nach dem Entformen mit dem Handschuh geglättet wird.

**Probeform**: `druck/01_probeform.3mf` mit Bauer und Springer in 2 Platten (91 × 35 × 48 mm). Damit werden Oberfläche, Naht, Entformen und Kühlzeit geprüft, bevor die Buchform gedruckt wird.

## 5. Anguss: der Fuss ist der Einguss

- Gegossen wird kopfüber. Die Standfläche aller Figuren liegt in der oberen Giessebene.
- Der ganze Fussdurchmesser (20 bis 26 mm) ist der Einguss. Kein Angusskanal, keine Angussmarke an sichtbarer Stelle.
- Füllen mit Spritzbeutel oder Dosierflasche (Düse Ø 5 bis 6 mm) durch die Trichterplatte, dünner Strahl an der Wand.
- Nach dem Rütteln Trichterplatte abnehmen, Fuss mit Edelstahlspachtel bündig abziehen. Die Standfläche wird plan.
- Eine kleine Einsenkung am Fuss durch das Schwinden ist erwünscht. Ist sie zu tief, nach 5 Minuten dünn nachfüllen.

Verworfen: steigender Guss von unten wie beim Spritzguss. Der Angusskanal hinterlässt eine Marke auf sichtbarer Fläche, und Schokolade erstarrt in engen Kanälen.

## 6. Entlüftung

Luft steigt in Giesslage nach oben zum Fuss. Eingeschlossen wird sie nur unter Flächen, die in Giesslage nach unten offen sind.

1. **Gestaltungsregel** (docs/03-figuren.md): Unterseiten von Kragen, Köpfen und Kreuzarmen laufen aufrecht betrachtet mit mindestens 45° in den Schaft. Die Rotationsfiguren entlüften sich selbst, und die Form ist ohne Stützmaterial druckbar.
2. **Entlüftungskanäle** nur wo die Regel nicht reicht. Die CAD-Prüfung (`cad/pruefen.py`) findet bei allen 6 Figuren keine Luftfalle, auch nicht bei Springer und Königskreuz. Die Form hat darum vorerst keine Kanäle. Zeigt der Prototyp Lufteinschlüsse, kommt an der Stelle ein Kanal 0.8 × 0.8 mm in die Trennfläche bis zur Giessebene.
3. Ein dünner Schokoladenfaden aus einem Kanal bricht beim Entformen ab und wird mit der Naht geglättet.
4. **Beim Giessen**: offene Platten zuerst dünn mit Schokolade einpinseln (Kopf, Details), dann schliessen und füllen, 1 bis 2 Minuten rütteln oder Vibrationsplatte.

## 7. Kühlen

- 10 Minuten Raumtemperatur, damit die Kristallisation beginnt.
- Dann Kühlschrank 8 bis 12 °C. Richtwert für massive Figuren: 30 bis 45 Minuten, König und Dame am längsten, weiss länger als dunkel. Im Prototyp messen.
- Kein Tiefkühler: Spannungsrisse, Kondenswasser, und PLA wird spröde.
- Formen stehend kühlen, Giessebene oben.

## 8. Entformen

Eine starre Form gibt nicht nach. Entformt wird darum nur, wenn die Schokolade sich gelöst hat, und immer senkrecht zur Trennebene.

1. Fertig ist die Figur, wenn sie beim leichten Klopfen auf die Form lose klingt oder sich an der Giessebene ein feiner Spalt zeigt. Ein feiner Spalt zwischen Figur und Kavität ist an der Giessebene von oben sichtbar.
2. Flügelmuttern lösen. Platten einzeln entlang der Stangen abziehen, von aussen nach innen. Nicht kippen und nicht hebeln: Kippen bricht Hals und Kreuz.
3. Die Platten mit den Daumen an den Stirnseiten auseinanderdrücken. Kein Werkzeug in der Trennfuge, das zerkratzt die Trennfläche.
4. Die Figur liegt in einer Platte. Platte umdrehen und über einem Tuch leicht klopfen, die Figur fällt heraus. Nicht am Kopf ziehen.
5. Klebt eine Figur: Form zurück in den Kühlschrank, 10 Minuten. Nie mit Gewalt.
6. Mit Baumwollhandschuhen anfassen. Naht und Entlüftungsfäden mit Handschuh oder lauwarmem Spachtel glätten.
7. Figuren in geschlossener Dose auf Raumtemperatur kommen lassen, dann verpacken.

## 9. Phasen

| Phase | Inhalt | Ergebnis | Abnahme |
|---|---|---|---|
| 0 | Plan freigeben, offene Fragen klären, Material bestellen | Bestellliste | Moritz |
| 1 | Figuren und Formhälften parametrisch in CadQuery (Python), Renderings | `cad/`, STL, Bilder | Aussehen, Grösse |
| 2 | Probeform Bauer und Springer: drucken, schleifen, giessen | Erste Bauern und Springer dunkel und weiss | Keine sichtbaren Rillen, Naht, Entformen, Kühlzeit. Sonst Rückfallebene B. |
| 3 | Buchform mit 5 Platten | Eine Form für alle 16 Figuren | 16 Figuren pro Guss |
| 4 | Ablauf Gusstag festlegen | docs/04-ablauf-giessen.md mit gemessenen Zeiten | Ein Set dunkel und weiss |
| 5 | Box aus dem 3D-Drucker (docs/06-box.md) | `druck/04` bis `06` | Figuren passen in die Einlage, Deckel schliesst |

## 10. Material (Schätzung für einen Formsatz)

| Material | Menge | Hinweis |
|---|---|---|
| Bambu PLA Pure White (Platten, Trichterplatte, Probeform) | etwa 0.85 kg | Konformitätserklärung für die gewählte Farbe anfordern, fetthaltige Lebensmittel müssen abgedeckt sein. Natur oder Weiss. |
| Gehärtete Stahldüse 0.4 mm | Serie beim P2S | Pflicht für die Teile mit Schokoladenkontakt |
| Gewindestangen M5 Edelstahl, Flügelmuttern, Unterlagscheiben | 4 × 160 mm, 4 × 60 mm, je 8 | Führen und Spannen |
| Bohrer 5 mm | 1 | Bohrungen für die Gewindestangen nacharbeiten |
| Nassschliffpapier 400 bis 3000, Schleifstäbe, Glasplatte, Glas- oder Fliesenstreifen 125 mm und 55 mm breit | je 1 | Kavitäten und Trennflächen |
| Edelstahlspachtel, Spritzbeutel, Thermometer | je 1 | |
| Vibrationsplatte oder Rüttler | optional | Entlüftung |
| Kuvertüre dunkel und weiss | je 1 kg pro Testtag | Ein Set braucht etwa 130 g pro Farbe plus Überlauf |

## 11. Offene Fragen

1. Geklärt: Bambu Lab P2S, Bauraum 256 × 256 × 256 mm, Seriendüse gehärteter Stahl 0.4 mm.
2. Sind die Figurengrössen in docs/03-figuren.md richtig?
3. Wie viele Sets sollen hergestellt werden? Davon hängt ab, ob ein oder zwei Formsätze nötig sind.
4. Geklärt: PLA Pure Black, Apricot und White. Bambu prüft alle fünf Inhaltsstoffe nach EU 10/2011, also jedes Pigment. Grenze laut Bambu 60 °C.
