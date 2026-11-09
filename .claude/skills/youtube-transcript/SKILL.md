---
name: youtube-transcript
description: Haalt de transcript van een YouTube-video op en vat die samen voor Filip (Fitlipgym). Gebruik dit als Filip een YouTube-link deelt en vraagt om de video te analyseren, samen te vatten, de transcript te lezen, of te zeggen wat hij ermee kan voor zijn zaak of content.
---

# YouTube transcript

Lees een YouTube-video via de ondertitels. Vat samen in Filips stijl.

## Stap 1. Transcript ophalen

Eenmalig installeren:

```bash
pip install youtube-transcript-api
```

Ophalen (pad relatief aan de root van de repo):

```bash
python .claude/skills/youtube-transcript/scripts/get_transcript.py "<link>" --out transcript.txt
```

Opties:

- `--lang nl,en` voorkeurstalen, standaard Nederlands en dan Engels
- `--no-times` zonder tijdstempels
- zonder `--out` komt de tekst op het scherm

Het script geeft een duidelijke foutmelding als het misloopt.

## Stap 2. Lukt het niet?

- **"YouTube blokkeert dit netwerk"** of **"Sign in to confirm you're not a bot"**: je draait in de cloud. YouTube blokkeert servers. Draai het op je eigen computer.
- **Geen ondertitels**: de video heeft er geen. Zeg dat eerlijk.
- Altijd mogelijk: vraag Filip de transcript te plakken. Op YouTube: onder de beschrijving op **"Transcript tonen"** klikken, alles kopiëren.

Verzin nooit inhoud. Zonder transcript geen samenvatting.

## Stap 3. Analyse schrijven

Lees de hele transcript. Schrijf in het Nederlands, ook als de video Engels is.

Format:

```
## [Titel video], [maker]

**In één zin:** waar gaat het over

**Kernpunten**
- max 5-7 bullets, elk met tijdstempel [m:ss]

**Wat kan Filip ermee**
- concreet voor Fitlipgym
- helpt het naar 8 vaste klanten?
- bespaart het tijd op marketing of content?
- past het niet, zeg dat gewoon

**Content-idee** (alleen als het echt past)
- 1 of 2 ideeën voor een post of reel
```

## Stijlregels

- Informeel, direct, B1-niveau, korte zinnen
- Veel witruimte, max 4-5 regels per blok
- Geen em-dashes. Gebruik komma, punt of spatie
- Geen AI-speak (essentieel, cruciaal) of formele woorden (echter, derhalve)
- Cijfers, prijzen of claims uit de video: vermeld dat ze van de maker komen, niet nagecheckt
- Haalbaar advies voor een solo-zaak
