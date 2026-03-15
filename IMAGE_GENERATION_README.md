# Nano Banana Image Generation Script

Dit script genereert afbeeldingen met het **Nano Banana** (Gemini) AI model van Google.

## Setup

### 1. Installeer afhankelijkheden
```bash
pip install -r requirements.txt
```

### 2. Voeg Google API Key toe
Je hebt een Google API key nodig voor de Gemini API.

#### Hoe je een API key krijgt:
1. Ga naar [Google AI Studio](https://aistudio.google.com/apikey)
2. Klik op "Create API Key"
3. Copy je API key

#### Stel de environment variabele in:
```bash
# Linux/Mac
export GOOGLE_API_KEY="your-api-key-here"

# Windows (PowerShell)
$env:GOOGLE_API_KEY="your-api-key-here"
```

## Script gebruiken

### Afbeeldingen genereren:
```bash
python generate_images.py
```

### Afbeeldingen aanpassen:
Open `generate_images.py` en wijzig de `PROMPTS` list:

```python
PROMPTS = [
    "Your first prompt here",
    "Your second prompt here"
]
```

## Output
Gegenereerde afbeeldingen worden opgeslagen in de `generated_images/` map.

## Gemini API Documentatie
- [Google Gemini API Docs](https://ai.google.dev/gemini-api/docs)
- [Nano Banana Model Info](https://ai.google.dev/gemini-api/docs/nanobanana)
