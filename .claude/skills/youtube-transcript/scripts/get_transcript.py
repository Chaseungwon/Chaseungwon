#!/usr/bin/env python3
"""Haal de transcript van een YouTube-video op.

Gebruik:
    python get_transcript.py <youtube-link of video-id> [--lang nl,en] [--out bestand.txt] [--no-times]

Werkt op je eigen computer. In cloud-omgevingen blokkeert YouTube dit vaak.
"""
import argparse
import re
import sys

ID_PATTERNS = [
    r"(?:v=|/v/)([A-Za-z0-9_-]{11})",
    r"youtu\.be/([A-Za-z0-9_-]{11})",
    r"/(?:shorts|embed|live)/([A-Za-z0-9_-]{11})",
]


def video_id(value: str) -> str:
    value = value.strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", value):
        return value
    for pattern in ID_PATTERNS:
        match = re.search(pattern, value)
        if match:
            return match.group(1)
    raise ValueError(f"Geen YouTube video-id gevonden in: {value}")


def timestamp(seconds: float) -> str:
    s = int(seconds)
    h, rest = divmod(s, 3600)
    m, s = divmod(rest, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def fetch(vid: str, languages: list[str]):
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        sys.exit("Pakket ontbreekt. Installeer met: pip install youtube-transcript-api")

    api = YouTubeTranscriptApi()
    transcripts = api.list(vid)
    try:
        chosen = transcripts.find_transcript(languages)
    except Exception:
        # Geen van de gevraagde talen: neem de eerste die er is.
        chosen = next(iter(transcripts))
    return chosen.language_code, chosen.is_generated, chosen.fetch()


def main() -> None:
    parser = argparse.ArgumentParser(description="YouTube transcript ophalen")
    parser.add_argument("video", help="YouTube-link of video-id")
    parser.add_argument("--lang", default="nl,en", help="Voorkeurstalen, komma-gescheiden (standaard: nl,en)")
    parser.add_argument("--out", help="Schrijf naar dit bestand in plaats van naar het scherm")
    parser.add_argument("--no-times", action="store_true", help="Zonder tijdstempels")
    args = parser.parse_args()

    try:
        vid = video_id(args.video)
    except ValueError as err:
        sys.exit(str(err))

    try:
        lang, generated, snippets = fetch(vid, [l.strip() for l in args.lang.split(",") if l.strip()])
    except SystemExit:
        raise
    except Exception as err:
        name = type(err).__name__
        hints = {
            "TranscriptsDisabled": "Deze video heeft geen ondertitels.",
            "NoTranscriptFound": "Geen ondertitels gevonden.",
            "VideoUnavailable": "Video niet beschikbaar (privé, verwijderd of fout id).",
            "RequestBlocked": "YouTube blokkeert dit netwerk. Probeer op je eigen computer of plak de transcript.",
            "IpBlocked": "YouTube blokkeert dit netwerk. Probeer op je eigen computer of plak de transcript.",
        }
        message = str(err)
        if name not in hints and ("/sorry/" in message or "not a bot" in message or "ProxyError" in name):
            name = "RequestBlocked"
        sys.exit(f"Ophalen mislukt ({name}). {hints.get(name, message[:300])}")

    lines = [
        s.text.replace("\n", " ") if args.no_times else f"[{timestamp(s.start)}] {s.text.replace(chr(10), ' ')}"
        for s in snippets
    ]
    header = (
        f"# Transcript {vid}\n"
        f"# Bron: https://www.youtube.com/watch?v={vid}\n"
        f"# Taal: {lang} ({'automatisch gegenereerd' if generated else 'handmatig'})\n\n"
    )
    text = header + "\n".join(lines) + "\n"

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Opgeslagen: {args.out} ({len(lines)} regels)")
    else:
        print(text)


if __name__ == "__main__":
    main()
