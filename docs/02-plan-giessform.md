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
- PLA Pure: Handwäsche bis etwa 45 °C. PETG Translucent: bis etwa 60 °C. Keine Spülmaschine, kein kochendes Wasser.
- Schokolade enthält kaum Wasser, Keime finden darin wenig Nährboden. Feuchtigkeit in Rillen ist das grössere Risiko: Formen offen und vollständig trocknen lassen, Restwasser lässt die Schokolade beim nächsten Guss stocken.
- Formen sind Verbrauchsteile: bei Kratzern, Verfärbung oder Geruch neu drucken. Ein Block kostet wenig Filament.

## 3. Rillen vermeiden

Die Schokolade bildet jede Schicht und jeden Kratzer der Kavität ab. Drei Massnahmen zusammen:

1. **Druckausrichtung**: Formhälften stehend drucken, Figurenachse senkrecht, Kopf unten (Giesslage). Die Schichten laufen dann als feine waagrechte Ringe um die Figur, wie bei einem gedrechselten Stück. Liegend gedruckt würden die Rundungen als Treppenstufen abgebildet.
2. **Druckeinstellungen**: 0.08 mm Schichthöhe, variable Schichthöhe in Bambu Studio für flache Partien (Kopf, Kragenoberseiten), langsame Aussenwand, Naht (Seam) auf die Rückseite der Hälfte statt in die Kavität, 100 % Infill rund um die Kavität.
3. **Nachbearbeitung der Kavität**: Nassschliff 400, 800, 1500, 3000, mit runden Schleifstäben und Schleifschwamm. Nur Wasser und Schleifpapier, keine Polierpaste und kein Lack (nicht lebensmittelecht). Das Material bleibt dasselbe, die Konformität gilt weiter. Danach waschen.

Gleiche Regel löst zwei Probleme: Wird in Giesslage gedruckt, sind die Kavitätendecken in Giesslage gleichzeitig Überhänge im Druck. Die 45°-Regel für die Entlüftung (Abschnitt 6) macht die Form ohne Stützmaterial druckbar. Stützmaterial in der Kavität ist verboten, es hinterlässt raue Stellen.

Abnahmekriterium im Prototyp: Auf Armlänge sind keine Ringe sichtbar, unter Streiflicht dürfen feine Ringe erkennbar sein. Wenn nicht erreicht: Rückfallebene B.

## 4. Aufbau eines Formblocks

```
            Trichterplatte (PLA Pure, aufgesteckt)
   ┌───────────────────────────────────────────────┐
   │  ▽        ▽        ▽        ▽     Einguss = Fuss│
   ├───────────────────────────────────────────────┤  ← Giessebene, plan
   │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐               │
   │ │Fuss │ │Fuss │ │Fuss │ │Fuss │  Hälfte A + B  │
   │ │  │  │ │  │  │ │  │  │ │  │  │  PLA Pure      │
   │ │ Kopf│ │ Kopf│ │ Kopf│ │ Kopf│                │
   │ └─────┘ └─────┘ └─────┘ └─────┘               │
   └───────────────────────────────────────────────┘
         Passkegel, Passstifte, Spannrahmen
```

| Teil | Material | Funktion |
|---|---|---|
| Formhälfte A und B | PLA Pure (lebensmittelecht), Edelstahl- oder gehärtete Stahldüse | Kavität, konturnahe Wand 3 mm plus Rippen |
| Passkegel | In die Hälften gedruckt, Kegel auf A, Bohrung auf B, 4 pro Block | Grobe Führung beim Schliessen |
| Passstifte | 2 Zylinderstifte Edelstahl Ø 4 × 16 mm, in Hälfte A eingepresst | Hälften sitzen auf etwa 0.05 mm genau, Naht ohne Versatz |
| Magnete | 6 Neodym Ø 10 × 3 mm, beim Druck eingelegt (Druckpause) und überdruckt | Schnelles Schliessen. Kein Kontakt zur Schokolade. |
| Spannrahmen | PETG, U-Rahmen mit 2 Keilen oder 2 Rändelschrauben | Gleichmässiger Druck auf die ganze Trennebene, Form steht stabil |
| Trichterplatte | PLA Pure | Ein Trichter pro Figur, auf die Passstifte gesteckt, fängt Überlauf |

**Dichte Naht**: Die Trennflächen werden stehend gedruckt und sind dadurch nicht ganz plan. Nach dem Druck jede Trennfläche auf einer Glasplatte mit Nassschliffpapier 400 und 800 plan schleifen (Läppen), bis sie vollflächig trägt. Dann zeichnet sich nur eine feine Linie ab, die nach dem Entformen mit dem Handschuh geglättet wird.

**Konturnahe Wand**: 3 mm Wand um die Kavität statt eines vollen Blocks. Dünnes PLA leitet die Kälte besser als Silikon, die Kühlzeit wird kürzer.

### Blockaufteilung

Druckbett Bambu Lab X1, P1 und A1: 256 × 256 mm. Ein Block mit 4 Kavitäten in einer Reihe ist etwa 170 mm lang. Stehend gedruckt sind die Hälften 70 mm hoch (König plus Fussverlängerung).

| Block | Kavitäten |
|---|---|
| 1 | König, Dame, Läufer, Läufer |
| 2 | Springer, Springer, Turm, Turm |
| 3 | 4 Bauern |
| 4 | 4 Bauern |

Ein Satz aus 4 Blöcken ergibt pro Guss eine Farbe (16 Figuren). Mit zwei Sätzen laufen dunkel und weiss gleichzeitig.

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
2. **Entlüftungskanäle** wo die Regel nicht reicht (Springer: Ohren, Maul; König: Kreuzarme): 0.8 × 0.8 mm Kanal in der Trennfläche, vom höchsten Punkt der Luftfalle bis zur Giessebene. Direkt im CAD modelliert.
3. Der dünne Schokoladenfaden im Kanal bricht beim Entformen ab und wird mit der Naht geglättet.
4. **Beim Giessen**: offene Hälften zuerst dünn mit Schokolade einpinseln (Kopf, Details), dann schliessen und füllen, 1 bis 2 Minuten rütteln oder Vibrationsplatte.

## 7. Kühlen

- 10 Minuten Raumtemperatur, damit die Kristallisation beginnt.
- Dann Kühlschrank 8 bis 12 °C. Richtwert für massive Figuren: 30 bis 45 Minuten, König und Dame am längsten, weiss länger als dunkel. Im Prototyp messen.
- Kein Tiefkühler: Spannungsrisse, Kondenswasser, und PLA wird spröde.
- Formen stehend kühlen, Giessebene oben.

## 8. Entformen

Eine starre Form gibt nicht nach. Entformt wird darum nur, wenn die Schokolade sich gelöst hat, und immer senkrecht zur Trennebene.

1. Fertig ist die Figur, wenn sie beim leichten Klopfen auf die Form lose klingt oder sich an der Giessebene ein feiner Spalt zeigt. PETG Translucent statt PLA Pure für eine Hälfte macht das Lösen sichtbar (Option im Prototyp).
2. Spannrahmen abnehmen. Hälfte A senkrecht abheben, die Passstifte führen. Nicht kippen und nicht hebeln: Kippen bricht Hals und Kreuz.
3. Abhebehilfe: zwei Nasen an den Blockenden, an denen die Hälften mit den Daumen auseinandergedrückt werden. Kein Werkzeug in der Trennfuge, das zerkratzt die Trennfläche.
4. Figur liegt in Hälfte B. Hälfte B umdrehen und über einem Tuch leicht klopfen, die Figur fällt heraus. Nicht am Kopf ziehen.
5. Klebt eine Figur: Form zurück in den Kühlschrank, 10 Minuten. Nie mit Gewalt.
6. Mit Baumwollhandschuhen anfassen. Naht und Entlüftungsfäden mit Handschuh oder lauwarmem Spachtel glätten.
7. Figuren in geschlossener Dose auf Raumtemperatur kommen lassen, dann verpacken.

## 9. Phasen

| Phase | Inhalt | Ergebnis | Abnahme |
|---|---|---|---|
| 0 | Plan freigeben, offene Fragen klären, Material bestellen | Bestellliste | Moritz |
| 1 | Figuren und Formhälften parametrisch in CadQuery (Python), Renderings | `cad/`, STL, Bilder | Aussehen, Grösse |
| 2 | Prototyp Einzelform Bauer: drucken, schleifen, giessen | Erste Bauern dunkel und weiss | Keine sichtbaren Rillen, Naht, Entformen, Kühlzeit. Sonst Rückfallebene B. |
| 3 | Prototyp Einzelform Springer (schwierigste Figur) | Springer dunkel und weiss | Entlüftung, Ohren bleiben ganz, kein Verhaken |
| 4 | Formblöcke 1 bis 4 | Ein vollständiger Formsatz | 16 Figuren pro Guss |
| 5 | Ablauf Gusstag festlegen | docs/04-ablauf-giessen.md mit gemessenen Zeiten | Ein Set dunkel und weiss |
| 6 | Verpackung (separate Session) | verpackung/ | Figuren passen in die Einlage |

## 10. Material (Schätzung für einen Formsatz)

| Material | Menge | Hinweis |
|---|---|---|
| Bambu PLA Pure (Formhälften, Trichterplatte) | 1 kg plus 0.5 kg für Prototypen | Konformitätserklärung für die gewählte Farbe anfordern, fetthaltige Lebensmittel müssen abgedeckt sein. Natur oder Weiss. |
| Bambu PETG Translucent | 0.25 kg | Option für eine durchsichtige Hälfte im Prototyp |
| PETG beliebig (Spannrahmen, Keile) | 0.5 kg | Kein Lebensmittelkontakt |
| Edelstahl- oder gehärtete Stahldüse 0.4 mm | 1 | Pflicht für die Teile mit Schokoladenkontakt |
| Zylinderstifte Edelstahl Ø 4 × 16 mm | 8 | 2 pro Block |
| Neodym-Magnete Ø 10 × 3 mm | 24 | 6 pro Block, überdruckt |
| Nassschliffpapier 400 bis 3000, Schleifstäbe, Glasplatte | je 1 | Kavitäten und Trennflächen |
| Edelstahlspachtel, Spritzbeutel, Thermometer | je 1 | |
| Vibrationsplatte oder Rüttler | optional | Entlüftung |
| Kuvertüre dunkel und weiss | je 1 kg pro Testtag | Ein Set braucht etwa 130 g pro Farbe plus Überlauf |

## 11. Offene Fragen

1. Welches Bambu Lab Modell und welche Düse? (Bettgrösse, Düse für Lebensmittelkontakt)
2. Sind die Figurengrössen in docs/03-figuren.md richtig?
3. Wie viele Sets sollen hergestellt werden? Davon hängt ab, ob ein oder zwei Formsätze nötig sind.
4. Welche Farbe PLA Pure ist mit Konformitätserklärung für Fett erhältlich?
