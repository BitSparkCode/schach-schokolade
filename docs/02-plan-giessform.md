# Plan: Giessform für ganze Schachfiguren

Ziel: 32 massive, ganze Figuren (16 dunkel, 16 weiss), glatte Oberfläche ohne sichtbare Rillen, Form wiederverwendbar, Formteile auf einem Bambu Lab gedruckt.

## 1. Grundentscheid

| Variante | Oberfläche | Lebensmittelkontakt | Entformen | Entscheid |
|---|---|---|---|---|
| A. Form direkt drucken (PLA Pure oder PETG Translucent) | Druckrillen sichtbar | Filament, Rillen schwer zu reinigen | Starr, Pferd verhakt | Nur als Schnelltest |
| B. Gedruckter Master, Silikonform in gedruckter Stützschale | So glatt wie der polierte Master | Lebensmittelechtes Platin-Silikon | Silikon gibt nach, Stützschale hält die Form | **Gewählt** |
| C. Silikonform ohne Stützschale | Glatt | Silikon | Silikon verformt sich, Figur wird schief | Verworfen |

Der Drucker baut in Variante B alles ausser der Kontaktfläche: Master, Stützschalen (gleichzeitig Formkasten für das Silikon), Trennplatten, Klammern, Trichterplatte.

Eine Besonderheit hilft: Rotationskörper (Bauer, Turm, Läufer, Dame, König) haben bei einer Trennebene durch die Mittelachse keine Hinterschnitte. Die zwei Formhälften lassen sich senkrecht zur Trennebene abheben. Nur der Springer und das Kreuz des Königs brauchen die Nachgiebigkeit des Silikons.

## 2. Aufbau eines Formblocks

```
           Trichterplatte (PETG Translucent, aufgesteckt)
   ┌───────────────────────────────────────────────┐
   │  ▽        ▽        ▽        ▽     Einguss = Fuss│
   ├───────────────────────────────────────────────┤  ← Giessebene, plan
   │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐               │
   │ │Fuss │ │Fuss │ │Fuss │ │Fuss │   Silikon      │
   │ │  │  │ │  │  │ │  │  │ │  │  │   Hälfte A + B │
   │ │ Kopf│ │ Kopf│ │ Kopf│ │ Kopf│                │
   │ └─────┘ └─────┘ └─────┘ └─────┘               │
   └───────────────────────────────────────────────┘
     Stützschale A + B (PETG), Passstifte, Klammern
```

| Teil | Material | Funktion |
|---|---|---|
| Silikonhälfte A und B | Platin-Silikon Shore 20A bis 30A, lebensmittelecht, transluzent | Kontaktfläche, dichtet die Trennebene, gibt beim Entformen nach |
| Stützschale A und B | PETG (beliebige Farbe), 3 mm Wand, Rippen | Formkasten beim Silikonguss und danach starre Stütze. Das Silikon bleibt dauerhaft in seiner Schale. |
| Silikonverankerung | Schwalbenschwanz-Nuten und Durchgangslöcher in der Schale | Silikon kann in der Schale weder verrutschen noch sich abheben |
| Passkegel im Silikon | Halbkugeln Ø 8 mm, 4 pro Block | Hälften rasten exakt ein |
| Passstifte | 4 Zylinderstifte Edelstahl Ø 5 × 20 mm, eingepresst in Schale A | Schalen sitzen auf 0.05 mm genau |
| Verschluss | 6 Neodym-Magnete Ø 10 × 3 mm in Taschen plus 2 gedruckte Exzenterklammern | Magnete zum schnellen Schliessen, Klammern für gleichmässigen Druck auf die Naht |
| Trichterplatte | PETG Translucent oder PLA Pure (lebensmittelecht), Edelstahl- oder Stahldüse | Ein Trichter pro Figur, auf die Passstifte gesteckt, fängt Überlauf |

Konturnahe Schalen: Die Innenseite der Stützschale folgt der Figur mit 6 bis 8 mm Abstand statt eines rechteckigen Kastens. Das spart etwa die Hälfte des Silikons und verkürzt die Kühlzeit, weil Silikon isoliert.

### Blockaufteilung

Druckbett Bambu Lab X1, P1 und A1: 256 × 256 mm. Ein Block mit 4 Kavitäten in einer Reihe ist etwa 190 mm lang.

| Block | Kavitäten |
|---|---|
| 1 | König, Dame, Läufer, Läufer |
| 2 | Springer, Springer, Turm, Turm |
| 3 | 4 Bauern |
| 4 | 4 Bauern |

Ein Satz aus 4 Blöcken ergibt pro Guss eine Farbe (16 Figuren). Mit zwei Sätzen laufen dunkel und weiss gleichzeitig.

## 3. Anguss: der Fuss ist der Einguss

- Gegossen wird kopfüber. Die Standfläche aller Figuren liegt in der oberen Giessebene.
- Der ganze Fussdurchmesser (20 bis 26 mm) ist der Einguss. Es gibt keinen Angusskanal und damit keine Angussmarke an einer sichtbaren Stelle.
- Gefüllt wird mit Spritzbeutel oder Dosierflasche (Düse Ø 5 bis 6 mm) durch die Trichterplatte, in einem dünnen Strahl an der Wand entlang.
- Nach dem Rütteln wird die Trichterplatte abgenommen und der Fuss mit einem Edelstahlspachtel bündig zur Giessebene abgezogen. Die Standfläche wird dadurch plan.
- Schokolade schwindet beim Kristallisieren leicht. Eine kleine Einsenkung am Fuss ist erwünscht (Figur steht stabil). Ist sie zu tief, nach 5 Minuten dünn nachfüllen und erneut abziehen.

Verworfen: steigender Guss von unten wie beim Spritzguss. Der Angusskanal würde eine Marke auf einer sichtbaren Fläche hinterlassen, und Schokolade erstarrt in engen Kanälen.

## 4. Entlüftung

Luft steigt in Giesslage nach oben zum Fuss. Eingeschlossen wird sie nur unter Flächen, die in Giesslage nach unten offen sind.

1. **Gestaltungsregel** (siehe docs/03-figuren.md): Unterseiten von Kragen, Köpfen und Kreuzarmen laufen aufrecht betrachtet mit mindestens 45° in den Schaft. Damit entlüften sich die Rotationsfiguren selbst.
2. **Entlüftungskanäle** dort, wo die Regel nicht reicht (Springer: Ohren, Maul; König: Kreuzarme): 1.0 × 1.0 mm Kanal in der Trennebene, vom höchsten Punkt der Luftfalle bis zur Giessebene. Die Kanäle sind als Rippen auf der gedruckten Trennplatte modelliert und damit reproduzierbar.
3. Die Kanäle liegen auf der Naht. Der dünne Schokoladenfaden bricht beim Entformen ab und wird zusammen mit der Naht geglättet.
4. **Vorgehen beim Giessen**: zuerst eine dünne Schicht Schokolade mit Pinsel in die offene Form streichen (Details, Kopf), dann schliessen und füllen, danach 1 bis 2 Minuten rütteln oder auf einer Vibrationsplatte entlüften.

## 5. Herstellung der Silikonform

1. **Master drucken**: Bambu Lab, 0.08 mm Schichthöhe, aufrecht, PLA. Ein Master pro Kavität, mit 2 mm Fussverlängerung bis zur Giessebene.
2. **Master glätten**: Füllgrundierung, Nassschliff 400, 800, 1500, 3000, danach glänzender Lack oder Epoxid-Beschichtung. Ziel: Spiegelglanz. Das Silikon bildet jede Rille und jeden Schleifkratzer ab.
3. **Hemmungstest**: Lack und Knete an einer Probe mit dem Silikon testen. Nur schwefelfreie Knete verwenden.
4. **Trennplatte drucken**: Sie enthält die exakte Halbform jedes Masters (aus CAD abgeleitet), dazu Passkegel und Entlüftungsrippen. Master einlegen, Spalt mit schwefelfreier Knete schliessen.
5. **Hälfte A giessen**: Stützschale A auf die Trennplatte stecken. Silikon mischen, möglichst vakuumentgasen, sonst dünn auf den Master pinseln und aus Höhe in einem dünnen Strahl in eine Ecke giessen. Aushärten lassen.
6. **Hälfte B giessen**: Umdrehen, Trennplatte entfernen, Master bleibt in Hälfte A. Trennmittel auf Silikon A, Stützschale B aufstecken, giessen.
7. **Öffnen, Master entnehmen, waschen**: Trennmittel mit Spülmittel und warmem Wasser vollständig entfernen. Nachhärtung, falls im Datenblatt vorgeschrieben.

## 6. Kühlen

- 10 Minuten bei Raumtemperatur stehen lassen, damit die Kristallisation beginnt.
- Danach Kühlschrank 8 bis 12 °C. Richtwert für massive Figuren: 45 bis 60 Minuten, König und Dame am längsten, weiss länger als dunkel. Im Prototyp messen.
- Kein Tiefkühler (Spannungsrisse, Kondenswasser).
- Formen stehend kühlen, Giessebene oben, damit nichts nachläuft.

## 7. Entformen

1. Fertig ist die Figur, wenn sie sich sichtbar von der transluzenten Silikonwand gelöst hat.
2. Klammern lösen, Stützschale A mit Silikon A senkrecht zur Trennebene abheben (Passstifte führen).
3. Figuren liegen in Hälfte B. Silikon B am Rand leicht nach aussen biegen, Figur am Fuss fassen und herauskippen. Nie am Kopf ziehen.
4. Springer: Silikon um die Ohren abschälen, nicht hebeln.
5. Mit Baumwollhandschuhen anfassen. Naht und Entlüftungsfäden mit Handschuh oder lauwarmem Spachtel glätten.
6. Figuren in geschlossener Dose auf Raumtemperatur kommen lassen, danach verpacken.

## 8. Phasen

| Phase | Inhalt | Ergebnis | Abnahme |
|---|---|---|---|
| 0 | Plan freigeben, offene Fragen klären, Material bestellen | Bestellliste | Moritz |
| 1 | Figuren parametrisch in CadQuery (Python), Renderings | `cad/figuren.py`, STL, Bilder | Aussehen, Grösse |
| 2 | Prototyp Einzelform Bauer: Master, Trennplatte, Schale, Silikon | Erste Figuren dunkel und weiss | Oberfläche ohne Rillen, Naht, Entformen, Kühlzeit |
| 3 | Prototyp Einzelform Springer (schwierigste Figur) | Springer dunkel und weiss | Entlüftung, Ohren bleiben ganz |
| 4 | Formblöcke 1 bis 4 | Ein vollständiger Formsatz | 16 Figuren pro Guss |
| 5 | Ablauf Gusstag festlegen | docs/04-ablauf-giessen.md mit gemessenen Zeiten | Ein Set dunkel und weiss |
| 6 | Verpackung (separate Session) | verpackung/ | Figuren passen in die Einlage |

## 9. Material (Schätzung für einen Formsatz)

| Material | Menge | Hinweis |
|---|---|---|
| Platin-Silikon lebensmittelecht, Shore 20A bis 30A, transluzent | 1.5 kg | Zulassung für Lebensmittel prüfen, inkl. Prototypen |
| Trennmittel für Silikon auf Silikon | 1 Dose | Danach vollständig abwaschen |
| PETG (Stützschalen, Trennplatten, Klammern) | 1.5 kg | Keine Lebensmittelzulassung nötig |
| PLA (Master) | 0.3 kg | Keine Lebensmittelzulassung nötig |
| PETG Translucent oder PLA Pure (Trichterplatten) | 1 Spule | Lebensmittelecht, Konformitätserklärung der Farbe anfordern |
| Edelstahl- oder gehärtete Stahldüse 0.4 mm | 1 | Falls nicht schon montiert |
| Zylinderstifte Edelstahl Ø 5 × 20 mm | 16 | 4 pro Block |
| Neodym-Magnete Ø 10 × 3 mm | 24 | 6 pro Block |
| Füllgrundierung, Schleifpapier 400 bis 3000, Glanzlack | je 1 | Hemmungstest mit Silikon |
| Schwefelfreie Knete, Einwegbecher, Waage, Spatel | | Für den Silikonguss |
| Vibrationsplatte oder Rüttler | optional | Entlüftung beim Schokoladenguss |
| Kuvertüre dunkel und weiss | je 1 kg pro Testtag | Ein Set braucht etwa 130 g pro Farbe plus Überlauf |

## 10. Offene Fragen

1. Welches Bambu Lab Modell und welche Düse? (Bettgrösse und Lebensmittelkontakt der Trichterplatte)
2. Sind die Figurengrössen in docs/03-figuren.md richtig, oder sollen die Figuren grösser oder kleiner werden?
3. Wie viele Sets sollen hergestellt werden? Davon hängt ab, ob ein oder zwei Formsätze nötig sind.
4. Vakuumkammer für das Silikon vorhanden? Ohne Vakuum geht es auch, mit Pinselschicht und dünnem Strahl.
5. Sollen die Master selbst geglättet werden, oder werden sie als Harzdruck (SLA) bei einem Dienstleister bestellt? Harzdruck ist glatter und spart Schleifarbeit, Lebensmittelkontakt spielt beim Master keine Rolle.
