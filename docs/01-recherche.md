# Recherche: Schokolade in 3D-gedruckten Formen

Stand: November 2026. Quellen am Ende.

## Hat das schon jemand gemacht?

Ja, in drei Varianten:

| Variante | Beispiel | Ergebnis |
|---|---|---|
| Direkt gedruckte, zweiteilige Form | Hobby-Modelle auf MyMiniFactory, Printables und Thingiverse, z. B. ein zweiteiliger König, "mit Malerband zusammenhalten, Schokolade unten eingiessen" | Funktioniert für Einzelstücke. Druckrillen sind auf der Schokolade sichtbar, Fixierung mit Klebeband verrutscht, Reinigung der Rillen ist kaum möglich. |
| Gedruckter Master, daraus Silikonform | Anleitungen und Generatoren (z. B. Meshcast) und viele Chocolatiers | Der heute empfohlene Weg für Lebensmittel. Nur zertifiziertes Silikon berührt die Schokolade, die Oberfläche ist so glatt wie der Master. |
| Industrielle 3D-Formen aus Polycarbonat | Zweiteilige Magnetformen für massive 3D-Figuren (z. B. Chocolate World) | Profi-Standard für massive Figuren. Zwei starre Hälften, Magnete als Fixierung, Einguss von unten. Zeigt, dass massive ganze Figuren in geschlossenen Formen funktionieren. Polycarbonat lässt sich auf einem Bambu Lab nicht in dieser Oberflächenqualität drucken. |

Schach-Silikonformen für Schokolade gibt es zu kaufen (Etsy), meist als flache Halbfiguren oder in Formen für Giessharz. Ein Set aus ganzen, massiven Figuren in zwei Schokoladensorten mit passender Verpackung haben wir nicht gefunden.

## Was funktioniert, was nicht

| Ansatz | Funktioniert | Funktioniert nicht |
|---|---|---|
| Schokolade direkt in PLA oder PETG | Einmalige Versuche, grobe Formen | Glatte Oberfläche: jede Druckschicht (0.08 bis 0.2 mm) wird 1:1 abgebildet. Wiederholte Nutzung: Fett und Rückstände bleiben in den Rillen. Spülmaschine: PLA verformt sich ab etwa 55 °C. |
| Direktdruck plus Beschichtung (lebensmittelechtes Epoxid) | Glättet die Rillen | Nutzt sich ab, muss überwacht und erneuert werden. Die Zulassung der Beschichtung muss für fetthaltige Lebensmittel gelten. |
| Starre zweiteilige gedruckte Form | Gedrungene Figuren ohne Hinterschnitte | Hinterschnitte (Hals unter dem Kopf, Krone, Pferdekopf) brechen beim Entformen ab oder verhaken sich. |
| Gedruckter Master plus Platin-Silikon | Glatte, glänzende Oberfläche, Hinterschnitte, ganze Figuren, reinigbar, Kühlschrank und Spülmaschine (je nach Silikon) | Silikon ist weich und verformt sich ohne Stütze. Lösung: gedruckte Stützschale. |
| Zinn-vernetzendes (kondensationsvernetzendes) Silikon | Billiger | Nicht für Lebensmittel zugelassen. |

Folgerung (Stand nach Entscheid von Moritz, ohne Silikon): Die Form wird direkt aus lebensmittelechtem Filament gedruckt. Die Probleme der Direktdruckformen werden einzeln gelöst: stehend gedruckt mit 0.08 mm und nass geschliffen gegen Rillen, Figuren ohne Hinterschnitte für die starre Form, Kegelnoppen und Gewindestangen statt Klebeband, warme Handwäsche (Kakaobutter schmilzt bei etwa 34 °C). Silikon und Epoxid-Beschichtung bleiben Rückfallebenen. Details in docs/02-plan-giessform.md.

## Lebensmittelechtes Filament

### Was "lebensmittelecht" bei Filament heisst

- Massgebend in der EU ist die Verordnung (EU) Nr. 10/2011 über Kunststoffe mit Lebensmittelkontakt, zusammen mit der Rahmenverordnung (EG) Nr. 1935/2004. Die Schweiz hat gleichwertige Regeln (Bedarfsgegenständeverordnung).
- Eine Konformitätserklärung gilt für ein bestimmtes Produkt, eine bestimmte Farbe und bestimmte Bedingungen (Lebensmittelart, Temperatur, Dauer). Schokolade ist ein fetthaltiges Lebensmittel, die Erklärung muss Fett abdecken.
- Die Erklärung gilt für das Rohmaterial. Was danach passiert (Düse, Druck, Oberfläche, Reinigung), deckt sie nicht ab.

### Was Bambu Lab anbietet

- **Bambu PLA Pure**: laut Bambu Lab sind alle fünf Inhaltsstoffe inklusive Pigmente nach EU 10/2011 konform, zusätzlich EN 71-3 (Spielzeug) und UL 2904 (Emissionen).
- **Food-Contact Testing**: Bambu Lab listet PLA Basic, PLA Matte und PETG Translucent als nach EU 10/2011 geprüft, mit gedruckten Proben in definierten Szenarien.
- Vor dem Kauf: Konformitätserklärung für die gewählte Farbe anfordern und prüfen, ob fetthaltige Lebensmittel abgedeckt sind.

### Worauf beim Drucken mit Lebensmittelkontakt zu achten ist

| Punkt | Massnahme |
|---|---|
| Düse | Messingdüsen enthalten oft Blei. Edelstahl- oder gehärtete Stahldüse verwenden. Prüfen, welche Düse auf unserem Bambu Lab montiert ist. |
| Materialweg | Vorher kein Fremdmaterial, gründlich spülen (Purge). Keine Silk-, Glitzer-, Holz- oder Carbon-Filamente im gleichen Druck. |
| Oberfläche | 100 % Infill, mindestens 4 Wände, Bügeln (Ironing) auf Deckflächen. Rillen bleiben trotzdem. |
| Temperatur | PLA nur bis etwa 50 °C (Handwäsche, lauwarm). PETG bis etwa 70 °C. |
| Wiederverwendung | Teile mit direktem Kontakt als Verbrauchsteile behandeln und bei Abnutzung ersetzen. |

### Wofür wir lebensmittelechtes Filament brauchen

- **Formplatten**: Kontaktfläche zur Schokolade. Bambu PLA Pure, alle fünf Inhaltsstoffe inklusive Pigmente nach EU 10/2011 geprüft (Bambu Store, Stand November 2026).
- **Trichterplatte**: PLA Pure.
- **Abstreifer** für den Standfuss: Edelstahl-Spachtel.
- **Gewindestangen, Flügelmuttern**: Edelstahl, ausserhalb der Kavität.

## Lebensmittelechtes Silikon (nur Rückfallebene)

- Nur **platinvernetzendes** (additionsvernetzendes) Silikon mit Lebensmittelzulassung (EU 1935/2004, LFGB oder FDA 21 CFR 177.2600).
- Beispiele: Smooth-On Smooth-Sil 940 (Shore 40A, vom Hersteller als lebensmittelecht für Schokolade ausgewiesen), Smooth-On Sorta-Clear 37 und 40, transluzente lebensmittelechte RTV-2 Silikone mit Shore 20A aus dem Fachhandel.
- Für unsere Figuren mit Hinterschnitten: **Shore 20A bis 30A**, transluzent (Luftblasen und Schokoladenreste sind sichtbar).
- Platin-Silikon wird durch Schwefel, Zinn-Silikon, Latex und manche Lacke und Grundierungen gehemmt (härtet nicht aus). Jeden Masterlack vorher an einer Probe testen.
- Trennmittel zwischen den beiden Silikonhälften ist nötig, sonst verkleben sie. Vor dem ersten Lebensmittelkontakt Form gründlich mit Spülmittel waschen; Nachhärtung, falls im Datenblatt vorgeschrieben.

## Worauf beim Entformen zu achten ist

| Risiko | Ursache | Gegenmassnahme |
|---|---|---|
| Figur klebt, Oberfläche matt, graue Schlieren | Schokolade nicht temperiert | Temperieren: dunkel 31 bis 32 °C, Milch 29 bis 30 °C, weiss 28 bis 29 °C Verarbeitungstemperatur. Temperierte Schokolade zieht sich beim Kristallisieren zusammen und löst sich von selbst. |
| Hals oder Kreuz bricht | Zu früh entformt, Kern noch weich; Zug an dünnen Teilen | Massive Figuren brauchen länger als Pralinen. Erst entformen, wenn die Figur sich in der Form löst. Silikon abschälen, nie die Figur herausziehen. Mindestdicken einhalten (siehe docs/03-figuren.md). |
| Weisse Schokolade bricht oder verformt sich | Weiss ist weicher und schmilzt früher | Länger kühlen, mit Baumwollhandschuhen anfassen, nur am Fuss halten. |
| Wasserflecken, Zuckerreif | Kondenswasser beim Herausnehmen aus dem Kühlschrank | Nicht im Tiefkühler. Kühlschrank 8 bis 12 °C, danach in geschlossener Dose auf Raumtemperatur kommen lassen. |
| Luftlöcher an Kopf, Kragen, Pferdeohren | Eingeschlossene Luft | Erst dünn einstreichen, dann füllen, rütteln oder vibrieren. Entlüftungskanäle in der Trennebene. Gestaltungsregel: keine nach unten offenen Taschen in Giesslage. |
| Naht sichtbar | Hälften nicht dicht geschlossen oder verschoben | Passkegel im Silikon, Stützschale mit Passstiften, Klammern mit gleichmässigem Druck. Feine Naht mit Baumwollhandschuh glätten. |
| Fingerabdrücke | Warme Hände | Baumwoll- oder Nitrilhandschuhe, Figur kühl halten. |

## Quellen

- Bambu Lab, Food-Contact Testing (EU 10/2011): https://bambulab.com/en/filament/collections/food-contact-testing
- Bambu Lab Blog, Introducing Bambu Lab PLA Pure (Juni 2026): https://blog.bambulab.com/introducing-bambu-lab-pla-pure-a-filament-made-for-printing-where-you-live/
- LyraMaker, Food-safe 3D prints: what actually matters: https://lyramaker.com/guides/food-safe-prints/
- Meshcast, Are 3D-printed molds food-safe?: https://meshcast.app/guides/food-safe-molds
- Prusa Knowledge Base, Lebensmittelechtes FDM Drucken: https://help.prusa3d.com/de/article/lebensmittelechtes-fdm-drucken_112313
- MyMiniFactory, Chess king chocolate mold (zweiteilige Direktdruckform): https://www.myminifactory.com/object/3d-print-chess-king-chocolate-mold-114937
- Smooth-On, Smooth-Sil 940 Technisches Merkblatt (lebensmittelechtes Platin-Silikon, u. a. für Schokolade)
