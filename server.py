"""
Brainiall Speech AI - MCP Server

MCP server providing AI-powered pronunciation assessment,
speech-to-text, and text-to-speech capabilities via Brainiall APIs.

Get your free API key at https://app.brainiall.com
"""

import os
import sys
from typing import Annotated, Optional

import httpx
from fastmcp import FastMCP

API_BASE = "https://api.brainiall.com"
API_KEY = os.environ.get("BRAINIALL_API_KEY", "")

if not API_KEY:
    print(
        "ERROR: BRAINIALL_API_KEY environment variable is required.\n"
        "Get your free API key at https://app.brainiall.com",
        file=sys.stderr,
    )
    sys.exit(1)

mcp = FastMCP(
    "brainiall-speech-ai",
    instructions=(
        "AI-powered speech tools: pronunciation assessment, "
        "speech-to-text, and text-to-speech by Brainiall."
    ),
)

_headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


def _client() -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url=API_BASE,
        headers=_headers,
        timeout=60.0,
    )


@mcp.tool()
async def assess_pronunciation(
    text: Annotated[str, "The reference text the user should have read aloud"],
    audio_base64: Annotated[str, "Base64-encoded audio of the user reading the text (WAV or MP3)"],
    language: Annotated[str, "Language code, e.g. 'en-US', 'pt-BR', 'es-ES'"] = "en-US",
) -> dict:
    """Assess how accurately a speaker pronounced the given text.

    Returns an overall pronunciation score (0-100), per-word scores,
    and phoneme-level feedback including accuracy, fluency, and completeness.
    """
    async with _client() as client:
        response = await client.post(
            "/v1/pronunciation/assess",
            json={
                "text": text,
                "audio_base64": audio_base64,
                "language": language,
            },
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def transcribe_speech(
    audio_base64: Annotated[str, "Base64-encoded audio to transcribe (WAV, MP3, WEBM, OGG)"],
    language: Annotated[Optional[str], "Optional language hint, e.g. 'en', 'pt'. Auto-detected if omitted."] = None,
) -> dict:
    """Transcribe speech audio into text.

    Supports multiple languages with automatic language detection.
    Returns the transcription text and detected language.
    """
    payload: dict = {"audio_base64": audio_base64}
    if language:
        payload["language"] = language

    async with _client() as client:
        response = await client.post("/v1/stt/transcribe", json=payload)
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def synthesize_speech(
    text: Annotated[str, "The text to convert to speech"],
    voice: Annotated[str, "Voice ID to use (see list_voices for available options)"] = "alloy",
    speed: Annotated[float, "Speaking speed multiplier (0.5 to 2.0)"] = 1.0,
) -> dict:
    """Convert text to natural-sounding speech audio.

    Returns base64-encoded audio in MP3 format.
    Use list_voices to see available voice options.
    """
    async with _client() as client:
        response = await client.post(
            "/v1/tts/synthesize",
            json={
                "text": text,
                "voice": voice,
                "speed": speed,
            },
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_voices() -> dict:
    """List all available text-to-speech voices.

    Returns voice IDs, names, supported languages, and sample previews.
    """
    async with _client() as client:
        response = await client.get(
            "/v1/tts/voices",
            headers={"Authorization": f"Bearer {API_KEY}"},
        )
        response.raise_for_status()
        return response.json()
