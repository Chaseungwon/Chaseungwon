#!/usr/bin/env python3
"""
Script to generate AI avatar videos using HeyGen API.
Generates Dutch-language promotional videos.

Usage:
    python heygen_video.py grasmaaien
    python heygen_video.py waterdrink

Environment variables:
    HEYGEN_API_KEY   (required)
    HEYGEN_AVATAR_ID (optional, default: Angela-inblackskirt-20220820)
    HEYGEN_VOICE_ID  (optional, default: nl-NL-ColetteNeural)
"""

import os
import sys
import time
import configparser
from pathlib import Path

import requests

BASE_URL = "https://api.heygen.com"
PROMPTS_FILE = Path(__file__).parent / "heygen_prompts.txt"
VALID_TYPES = ["grasmaaien", "waterdrink"]

DEFAULT_AVATAR_ID = "Angela-inblackskirt-20220820"
DEFAULT_VOICE_ID = "nl-NL-ColetteNeural"


def load_prompt(video_type: str) -> tuple[str, str]:
    config = configparser.ConfigParser()
    config.read(PROMPTS_FILE)
    if video_type not in config:
        raise ValueError(f"Video type '{video_type}' niet gevonden in {PROMPTS_FILE}")
    section = config[video_type]
    return section["title"], section["script"]


def create_video(api_key: str, script_text: str, title: str) -> str:
    avatar_id = os.getenv("HEYGEN_AVATAR_ID", DEFAULT_AVATAR_ID)
    voice_id = os.getenv("HEYGEN_VOICE_ID", DEFAULT_VOICE_ID)

    payload = {
        "video_inputs": [
            {
                "character": {
                    "type": "avatar",
                    "avatar_id": avatar_id,
                    "avatar_style": "normal",
                },
                "voice": {
                    "type": "text",
                    "input_text": script_text,
                    "voice_id": voice_id,
                },
                "background": {
                    "type": "color",
                    "value": "#ffffff",
                },
            }
        ],
        "dimension": {"width": 1280, "height": 720},
        "title": title,
    }

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }

    print(f"Video aanmaken: {title}")
    response = requests.post(f"{BASE_URL}/v2/video/generate", json=payload, headers=headers)

    if response.status_code != 200:
        print(f"Fout bij aanmaken video: HTTP {response.status_code}")
        print(response.text)
        sys.exit(1)

    data = response.json()
    video_id = data.get("data", {}).get("video_id")
    if not video_id:
        print(f"Geen video_id ontvangen: {data}")
        sys.exit(1)

    print(f"Video aangemaakt. ID: {video_id}")
    return video_id


def poll_video_status(api_key: str, video_id: str, max_wait: int = 300, interval: int = 10) -> str:
    headers = {"x-api-key": api_key}
    elapsed = 0

    print(f"Wachten op video voltooiing (max {max_wait}s)...")

    while elapsed < max_wait:
        response = requests.get(
            f"{BASE_URL}/v1/video_status.get",
            params={"video_id": video_id},
            headers=headers,
        )

        if response.status_code != 200:
            print(f"Fout bij ophalen status: HTTP {response.status_code}")
            print(response.text)
            sys.exit(1)

        data = response.json().get("data", {})
        status = data.get("status")
        print(f"  Status: {status} ({elapsed}s)")

        if status == "completed":
            video_url = data.get("video_url")
            if not video_url:
                print(f"Video klaar maar geen URL ontvangen: {data}")
                sys.exit(1)
            return video_url

        if status == "failed":
            error = data.get("error", "Onbekende fout")
            print(f"Video generatie mislukt: {error}")
            sys.exit(1)

        time.sleep(interval)
        elapsed += interval

    print(f"Timeout na {max_wait}s. Controleer handmatig met video_id: {video_id}")
    sys.exit(1)


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in VALID_TYPES:
        print(f"Gebruik: python heygen_video.py [{' | '.join(VALID_TYPES)}]")
        sys.exit(1)

    video_type = sys.argv[1]

    api_key = os.getenv("HEYGEN_API_KEY")
    if not api_key:
        raise ValueError("Omgevingsvariabele HEYGEN_API_KEY is niet ingesteld.")

    title, script = load_prompt(video_type)
    print(f"Script geladen: {title}")
    print(f"Tekst: {script[:80]}...")

    video_id = create_video(api_key, script, title)
    video_url = poll_video_status(api_key, video_id)

    print(f"\nVideo klaar!")
    print(f"URL: {video_url}")


if __name__ == "__main__":
    main()
