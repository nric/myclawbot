# LTX-2 Lustige Video-Prompts
# Für Enric - lustige Beispiele zum Testen

## 🎬 Kategorie: Süße & Lustige Roboter

1. **Der tanzende Roboter-Barista**
   "Ein kleiner silberner Roboter mit großen LED-Augen tanzt fröhlich hinter einer futuristischen Kaffeemaschine, dampfender Kaffee schwebt in Zeitlupe, warmes goldenes Licht, 4k, cinematic"

2. **Roboter-Welpe**
   "Ein niedlicher Roboter im Welpen-Design wackelt mit seinem metallischen Schwanz und macht einen Luftsprung, Sonnenuntergang im Hintergrund, flauschige Wolken, Pixar-Stil"

3. **Der aufgeregte Roboter beim Frühstück**
   "Ein Retro-Roboter aus den 50ern flippt aus vor Freude über einen riesigen Stapel Pfannkuchen, Butter tropft in Zeitlupe, Dampf steigt auf, kitschige Küche"

## 🎬 Kategorie: Absurde Alltagsszenen

4. **Katze im Büro**
   "Eine ernsthaft aussehende Katze in Anzug und Krawatte tippt auf einer futuristischen holografischen Tastatur, andere Katzenkollegen im Hintergrund, Neon-Beleuchtung, Cyberpunk-Büro"

5. **Das Alien beim Einkaufen**
   "Ein kleines grünes Alien mit riesigen Augen steht verwirrt vor einem riesigen Regal mit bunten Erdbeermarmeladen, Supermarkt-Beleuchtung, Fish-eye-Linse"

6. **Pinguin-DJ**
   "Ein cooler Pinguin mit Sonnenbrille legt an einem futuristischen DJ-Pult auf, Laserlichter, Nebelmaschine, tanzende Meerestiere im Hintergrund"

## 🎬 Kategorie: Magische Momente

7. **Der fliegende Goldfisch**
   "Ein glitzernder Goldfisch schwimmt elegant durch die Luft in einem sonnendurchfluteten Wohnzimmer, Staubpartikel tanzen im Licht, magische Atmosphäre, Studio Ghibli Stil"

8. **Sprechblumen**
   "Bunte Blumen in einem verzauberten Garten bewegen ihre Blütenblätter wie Münder und scheinen miteinander zu singen, sanfter Wind, Schmetterlinge, Traumlandschaft"

9. **Der verträumte Mond**
   "Ein freundlicher, animierter Mond mit Gesicht gähnt und streckt sich am Nachthimmel, Sterne zwinkern, eine Katze auf einem Dach schaut zu, Märchenstimmung"

## 🎬 Kategorie: Sci-Fi Comedy

10. **Das UFO beim Picknick**
    "Ein kleines UFO schwebt neugierig über einem Sommerpicknick, entführt heimlich eine Erdbeertorte, Schafe gucken verdutzt, ländliche Idylle trifft Sci-Fi"

11. **Roboter-Zahnarzt-Panik**
    "Ein ängstlicher Roboter zittert vor einem riesigen Zahnbohrer, während ein freundlicher menschlicher Zahnarzt ihn beruhigen will, komische Rollenumkehr, helle Praxis"

12. **Der Zeit-Reisende Eichhörnchen**
    "Ein Eichhörnchen in Miniatur-Steampunk-Rüstung aktiviert eine Zeitmaschine aus Nüssen und Stöckchen, blaue Energieblitze, verwirrte Vögel fliegen davon"

## 🎬 Kategorie: Visual Effects Demo

13. **Explodierende Früchte in Zeitlupe**
    "Eine Wassermelone explodiert in ultra-zeitlupe zu saftigen Partikeln, rot leuchtendes Fruchtfleisch fliegt durch die Luft, schwarzer Hintergrund, professionelle Beleuchtung"

14. **Magische Transformation**
    "Ein alter Rosthaufen verwandelt sich langsam in einen schimmernden Kristall-Schmetterling, Partikeleffekte, mystisches Glühen, dunkler Hintergrund"

15. **Tanzende Farbe**
    "Zwei Farbtropfen (blau und gold) prallen zusammen und tanzen in Schwerelosigkeit, bilden symmetrische Muster, schwarzer Hintergrund, hypnotisch"

## 🎬 Kategorie: Film-Parodien

16. **Der Matrix-Hamster**
    "Ein Hamster in schwarzem Trenchcoat weicht in Bullet-Time Matrix-Stil einem fallenden Käsestück aus, grüne Matrix-Code-Regen im Hintergrund, Sonnenbrille"

17. **Hitchcock mit Enten**
    "Dramatische Vogelperspektive auf einen Park voller friedlicher Enten, plötzlich dreht eine Ente den Kopf und schaut bedrohlich in die Kamera, Thriller-Atmosphäre"

18. **Jurassic Park mit Hühnern**
    "Ein riesiges Huhn bricht durch einen Zaun in einem Hühnerstall, kleine Hühner rennen panisch weg, Wasserspritzer, dramatische Musik (stilisiert), Abenteuer"

## ⚙️ Technische Parameter für Tests

### Konservativ (schnell, weniger VRAM):
- Resolution: 512x320 oder 704x384
- Frames: 17 (ca. 0.7 Sekunden)
- Steps: 20
- CFG: 1.0 (distilled model)

### Mittel (gute Qualität):
- Resolution: 704x384 oder 960x544
- Frames: 25 (1 Sekunde)
- Steps: 30

### Hoch (beste Qualität, mehr Zeit):
- Resolution: 1280x720
- Frames: 49 (2 Sekunden)
- Steps: 40
- Mit Stage 2 Upsampling

## 📝 Prompt Engineering Tipps für LTX-2

1. **Bewegung beschreiben**: Nutze aktive Verben im Präsens ("tanzt", "springt", "explodiert")
2. **Zeitliche Abfolge**: Nutze Zeit-Wörter ("dann", "plötzlich", "langsam")
3. **Kamera-Bewegung**: Spezifiziere ("Kamera zoomt rein", "Tracking Shot", "Statisch")
4. **Licht**: Beschreibe Lichtquellen ("warmes Golden Hour", " Neon-Röhren", "Dämmerung")
5. **Audio** (optional): LTX-2 kann auch Audio generieren! Füge Sound-Beschreibungen hinzu.

## 🎥 Beispiel-Workflow für ComfyUI

1. Lade das Template: `video_ltx2_t2v_distilled.json`
2. Ändere den Prompt im Node 177 (oder dem Haupt-Input-Node)
3. Passe Auflösung und Frames an
4. Klicke "Queue Prompt"
5. Warte auf das Ergebnis!

Viel Spaß beim Testen! 🎬
