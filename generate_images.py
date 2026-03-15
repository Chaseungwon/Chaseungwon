#!/usr/bin/env python3
"""
Script to generate images using Google's Nano Banana (Gemini) AI model
Uses the new unified Google GenAI SDK (as of 2025)
"""

import os
import sys
from pathlib import Path
from google import genai
from PIL import Image

# Configure API key from environment
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Please set GEMINI_API_KEY environment variable")

client = genai.Client(api_key=API_KEY)

# Text-only image generation prompts
TEXT_PROMPTS = [
    """Professional fitness gym advertisement banner for FitLipGym.
    Design shows a modern, energetic gym environment with fit people exercising.
    Prominent text overlay: "FitLipGym BEURTENSKAART ACTIE"
    Include promotional details: "10 of 15 BEURTENSKAARTEN - €100 KORTING"
    Add urgency text: "GELDIG TOT 30 APRIL" and "SLECHTS 5 KAARTEN BESCHIKBAAR"
    Use vibrant colors: bright energetic blues, oranges, and whites.
    Modern, clean design suitable for social media and print advertising.""",

    """Modern fitness gym promotional poster for FitLipGym.
    Show dynamic action shot: people training with dumbbells, doing cardio, and strength training.
    Bold headline: "START JE FITNESS JOURNEY"
    Add offer details as text elements: "BEURTENSKAART ACTIE - €100 KORTING"
    Include limited time text: "GELDIG TOT 30 APRIL 2025"
    Add scarcity message: "⚠️ SLECHTS 5 KAARTEN OVER"
    Options shown: "10 BEURT - 15 BEURT KAARTEN"
    Professional gym aesthetic with modern typography and energetic atmosphere."""
]

# Example for image + text mode (optional)
IMAGE_PROMPT = "Create a picture of this cat eating a nano-banana in a fancy restaurant under the Gemini constellation"
SAMPLE_IMAGE_PATH = None  # Set to "/path/to/image.png" if you have an image


def generate_text_only_images():
    """Generate images from text prompts only"""

    print("\n🎨 Generating images from text prompts...\n")
    output_dir = Path("generated_images")
    output_dir.mkdir(exist_ok=True)

    model = "gemini-3.1-flash-image-preview"

    for idx, prompt in enumerate(TEXT_PROMPTS, 1):
        print(f"[{idx}/{len(TEXT_PROMPTS)}] {prompt[:60]}...")

        try:
            response = client.models.generate_content(
                model=model,
                contents=[prompt],
            )

            # Extract and save the image
            for part in response.parts:
                if part.inline_data is not None:
                    image = part.as_image()
                    output_path = output_dir / f"image_{idx}.png"
                    image.save(output_path)
                    print(f"    ✓ Saved: {output_path}\n")
                elif part.text is not None:
                    print(f"    Response: {part.text}\n")

        except Exception as e:
            print(f"    ✗ Error: {e}\n")


def generate_image_with_vision(image_path: str, prompt: str):
    """Generate images using vision (image + text prompt)"""

    print("\n🎨 Generating image with vision input...\n")
    output_dir = Path("generated_images")
    output_dir.mkdir(exist_ok=True)

    # Verify image exists
    if not Path(image_path).exists():
        print(f"✗ Image not found: {image_path}")
        return

    # Load the image
    try:
        input_image = Image.open(image_path)
        print(f"📷 Loaded image: {image_path}")
    except Exception as e:
        print(f"✗ Error loading image: {e}")
        return

    model = "gemini-3.1-flash-image-preview"

    try:
        response = client.models.generate_content(
            model=model,
            contents=[prompt, input_image],
        )

        # Extract and save the generated image
        for part in response.parts:
            if part.inline_data is not None:
                image = part.as_image()
                output_path = output_dir / "generated_with_vision.png"
                image.save(output_path)
                print(f"✓ Generated image saved: {output_path}")
            elif part.text is not None:
                print(f"Response: {part.text}")

    except Exception as e:
        print(f"✗ Error generating image: {e}")


def main():
    """Main function to generate images"""

    print("=" * 60)
    print("Nano Banana Image Generation with Google GenAI SDK")
    print("=" * 60)

    # Generate text-only images (default behavior)
    generate_text_only_images()

    # Uncomment below to generate with image input if you have a sample image
    # if SAMPLE_IMAGE_PATH and Path(SAMPLE_IMAGE_PATH).exists():
    #     generate_image_with_vision(SAMPLE_IMAGE_PATH, IMAGE_PROMPT)

    print("=" * 60)
    print("✨ All done! Check 'generated_images/' directory.")
    print("=" * 60)


if __name__ == "__main__":
    main()
