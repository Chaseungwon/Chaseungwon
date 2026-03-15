# Nano Banana Image Generation with Google GenAI SDK

Generate images using Google's **Nano Banana** (Gemini) AI model with the new unified **Google GenAI SDK** (2025).

## Overview

This script demonstrates image generation using:
- **Model:** `gemini-3.1-flash-image-preview` (supports vision and image generation)
- **SDK:** Google GenAI (unified standard library for Gemini API)
- **Features:** Text-only prompts + Image+text vision capability

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `google-genai` - Google's unified GenAI SDK
- `Pillow` - Image processing library

### 2. Get Your API Key

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Click "Create API Key"
3. Copy your API key

### 3. Set Environment Variable

Set the `GEMINI_API_KEY` environment variable with your API key:

**Linux/Mac:**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your-api-key-here
```

## Usage

### Generate Images from Text Prompts

Run the script to generate images from text prompts only:

```bash
python generate_images.py
```

This generates 2 images:
1. Mountain landscape with sunset
2. Cyberpunk city at night

Images are saved to `generated_images/` directory.

### Generate Images with Vision (Image + Text Input)

To use image input with a text prompt:

1. Set an image path in the script:
```python
SAMPLE_IMAGE_PATH = "/path/to/your/image.png"
```

2. Uncomment the vision generation code at the bottom of the `main()` function:
```python
if SAMPLE_IMAGE_PATH and Path(SAMPLE_IMAGE_PATH).exists():
    generate_image_with_vision(SAMPLE_IMAGE_PATH, IMAGE_PROMPT)
```

3. Run the script:
```bash
python generate_images.py
```

### Customize Prompts

Edit the `TEXT_PROMPTS` list in `generate_images.py`:

```python
TEXT_PROMPTS = [
    "Your first prompt here",
    "Your second prompt here",
    "Add more as needed"
]
```

Or for vision mode, edit `IMAGE_PROMPT`:

```python
IMAGE_PROMPT = "Create a picture of this cat eating a nano-banana..."
```

## Output

Generated images are saved in the `generated_images/` directory as PNG files:
- `image_1.png` - First text prompt result
- `image_2.png` - Second text prompt result
- `generated_with_vision.png` - Vision mode result (if enabled)

## What's New in This Version

✨ **Updated to Google GenAI SDK (2025):**
- Uses `google-genai` package (unified standard library)
- New client initialization: `genai.Client(api_key=API_KEY)`
- New environment variable: `GEMINI_API_KEY` (instead of `GOOGLE_API_KEY`)
- Modern API: `client.models.generate_content()`
- Better error handling and image processing with `part.as_image()`

✨ **New Features:**
- Vision capability: Process images + text together
- Improved response handling
- Cleaner code structure with separate functions for text-only and vision modes

## Model Information

**gemini-3.1-flash-image-preview**
- Supports image generation
- Supports vision (image understanding + processing)
- Fast response times
- Suitable for creative and analytical tasks

## Troubleshooting

### Error: "Please set GEMINI_API_KEY environment variable"
Make sure you've set the `GEMINI_API_KEY` environment variable with a valid Google API key.

### Error: "Image not found"
When using vision mode, ensure the image path is correct and the file exists.

### Import Error: "No module named 'google'"
Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Documentation Links

- [Google GenAI SDK Documentation](https://googleapis.github.io/python-genai/)
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Google AI Studio](https://aistudio.google.com)
- [Migration Guide from Legacy SDK](https://ai.google.dev/gemini-api/docs/migrate)

## License

This script is provided as-is for educational and experimental purposes.
