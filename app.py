import json
import os
import re
import sys

import requests
from dotenv import load_dotenv
from openai import OpenAI

MAX_CHARS = 12000


def fetch_text(url):
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    r.raise_for_status()
    text = re.sub(r"<[^>]+>", " ", r.text)
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        raise ValueError("No text found on page.")
    return text[:MAX_CHARS]


def analyze(text):
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("Set OPENAI_API_KEY in .env")

    client = OpenAI(api_key=key)
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": (
                    "Analyze this document for investors. Return JSON with keys: "
                    "summary, risks, opportunities, sentiment, event_type.\n\n"
                    + text
                ),
            }
        ],
    )
    return json.loads(resp.choices[0].message.content)


def main():
    load_dotenv()
    url = input("URL: ").strip()
    if not url:
        sys.exit("Empty URL")

    print("Fetching...")
    text = fetch_text(url)
    print("Analyzing...")
    result = analyze(text)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
