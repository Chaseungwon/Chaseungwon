#!/usr/bin/env python3
"""
Script to generate images using Google's Nano Banana (Gemini) AI model
"""

import os
import base64
from pathlib import Path
import google.generativeai as genai

# Configure API key from environment
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("Please set GOOGLE_API_KEY environment variable")

genai.configure(api_key=API_KEY)

# Image prompts
PROMPTS = [
    "A serene mountain landscape with golden sunset, calm lake reflecting the colors, and pine trees",
    "A futuristic cyberpunk city with neon lights, flying cars, and holographic billboards at night"
]

def generate_images():
    """Generate images from prompts using Nano Banana model"""

    # Create output directory
    output_dir = Path("generated_images")
    output_dir.mkdir(exist_ok=True)

    model = genai.GenerativeModel("gemini-2.0-flash")

    for idx, prompt in enumerate(PROMPTS, 1):
        print(f"Generating image {idx}/{len(PROMPTS)}: {prompt[:50]}...")

        try:
            # Generate image using Gemini with image generation capability
            response = model.generate_content([
                "Generate an image: " + prompt
            ])

            # Extract and save the image
            if response.parts and hasattr(response.parts[0], 'inline_data'):
                image_data = response.parts[0].inline_data.data

                # Save image
                output_path = output_dir / f"image_{idx}.png"
                with open(output_path, "wb") as f:
                    f.write(base64.b64decode(image_data))

                print(f"✓ Image {idx} saved: {output_path}")
            else:
                print(f"✗ Failed to generate image {idx}")

        except Exception as e:
            print(f"Error generating image {idx}: {e}")

    print(f"\nDone! Images saved in '{output_dir}' directory")

if __name__ == "__main__":
    generate_images()
