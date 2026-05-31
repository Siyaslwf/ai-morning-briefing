"""
Shared OpenRouter client with multi-model fallback.

Free OpenRouter models are rate-limited at the provider level — when one is
saturated, retrying the same model is hopeless. This helper rotates through a
list of free models and only retries with backoff after exhausting the list.
"""

import json
import os
import re
import time
from typing import Iterable

from dotenv import load_dotenv
from openai import OpenAI, APIError, APIConnectionError, RateLimitError

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Ordered by recent probe results: fastest reliable free model first.
DEFAULT_MODELS = [
    "nvidia/nemotron-3-super-120b-a12b:free",
    "openai/gpt-oss-120b:free",
    "openai/gpt-oss-20b:free",
    "deepseek/deepseek-v4-flash:free",
]


class LLMError(RuntimeError):
    pass


def _client() -> OpenAI:
    if not OPENROUTER_API_KEY:
        raise LLMError("OPENROUTER_API_KEY not set")
    return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)


def _strip_json(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```", 2)[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()
    if raw.endswith("```"):
        raw = raw[: raw.rfind("```")].strip()
    # Drop trailing commas before } or ] — common model JSON mistake
    return re.sub(r",\s*([}\])])", r"\1", raw)


def chat_json(
    system: str,
    user: str,
    *,
    models: Iterable[str] | None = None,
    temperature: float = 0.3,
    max_retries: int = 2,
) -> dict:
    """
    Call OpenRouter with a fallback chain of free models. Returns parsed JSON.

    Strategy:
      1. Try each model in order; skip immediately on 404/429/connection error.
      2. If a model returns content but JSON fails to parse, try the next model.
      3. After exhausting the list, sleep and retry the whole list up to max_retries.
    """
    models = list(models or DEFAULT_MODELS)
    client = _client()
    last_error: str | None = None

    for attempt in range(max_retries + 1):
        for model in models:
            try:
                t0 = time.time()
                resp = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                    temperature=temperature,
                )
                raw = (resp.choices[0].message.content or "").strip()
                if not raw:
                    last_error = f"{model}: empty response"
                    print(f"[llm] {last_error}")
                    continue
                cleaned = _strip_json(raw)
                parsed = json.loads(cleaned)
                print(f"[llm] {model} OK ({time.time()-t0:.1f}s)")
                return parsed
            except (RateLimitError, APIConnectionError) as exc:
                last_error = f"{model}: {type(exc).__name__}: {str(exc)[:160]}"
                print(f"[llm] skip {last_error}")
                continue
            except APIError as exc:
                # 404 (model gone), 402 (no balance), 5xx
                last_error = f"{model}: APIError: {str(exc)[:160]}"
                print(f"[llm] skip {last_error}")
                continue
            except json.JSONDecodeError as exc:
                last_error = f"{model}: bad JSON: {exc} | preview={raw[:120]!r}"
                print(f"[llm] {last_error}")
                continue
            except Exception as exc:
                last_error = f"{model}: {type(exc).__name__}: {str(exc)[:160]}"
                print(f"[llm] skip {last_error}")
                continue

        if attempt < max_retries:
            wait = 20 * (attempt + 1)
            print(f"[llm] all models failed (attempt {attempt+1}/{max_retries+1}) — sleeping {wait}s")
            time.sleep(wait)

    raise LLMError(
        f"All {len(models)} free models failed after {max_retries+1} pass(es). "
        f"Last error: {last_error}"
    )


if __name__ == "__main__":
    out = chat_json(
        system="Return strict JSON only. No prose.",
        user='Return {"hello":"world","n":42}.',
    )
    print(out)
