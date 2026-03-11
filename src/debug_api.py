"""Small utility to verify a Gemini API key at runtime."""

from __future__ import annotations

import argparse

from google import genai


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Test a Gemini API key.")
    parser.add_argument("--api-key", required=True, help="Gemini API key to test.")
    parser.add_argument("--model-name", default="gemini-2.0-flash", help="Gemini model name.")
    return parser.parse_args()


def test_api(api_key: str, model_name: str) -> int:
    api_key = api_key.strip()
    if not api_key:
        print("ERROR: --api-key is required.")
        return 1

    print(f"Testing model: {model_name}")
    print(f"API key prefix: {api_key[:4]}...")

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model_name,
            contents="Reply with the single word: OK",
        )
        print("API call succeeded.")
        print(f"Response: {response.text}")
        return 0
    except Exception as exc:  # pragma: no cover - network/API dependent
        print("API call failed.")
        print(f"Error type: {type(exc).__name__}")
        print(f"Error message: {exc}")
        return 1


if __name__ == "__main__":
    arguments = parse_args()
    raise SystemExit(test_api(arguments.api_key, arguments.model_name))
