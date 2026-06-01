import json
import urllib.error
import urllib.request
from dataclasses import dataclass

import google.generativeai as genai


@dataclass
class LLMConfig:
    provider: str = "gemini"
    api_key: str = ""
    model: str = "gemini-2.5-flash"
    base_url: str = ""


class BaseLLMClient:
    def generate_text(self, prompt: str, temperature: float = 0.2) -> str:
        raise NotImplementedError

    def generate_json(self, prompt: str, temperature: float = 0.2) -> dict:
        text = self.generate_text(prompt, temperature=temperature)
        return json.loads(_strip_json_fences(text))


class GeminiLLMClient(BaseLLMClient):
    def __init__(self, config: LLMConfig):
        if not config.api_key:
            raise ValueError("Gemini API key is required")
        self.config = config
        genai.configure(api_key=config.api_key)
        self.model = genai.GenerativeModel(config.model or "gemini-2.5-flash")

    def generate_text(self, prompt: str, temperature: float = 0.2) -> str:
        response = self.model.generate_content(
            prompt,
            generation_config={"temperature": temperature},
        )
        return (response.text or "").strip()

    def generate_json(self, prompt: str, temperature: float = 0.2) -> dict:
        response = self.model.generate_content(
            prompt,
            generation_config={
                "response_mime_type": "application/json",
                "temperature": temperature,
            },
        )
        return json.loads(response.text)


class OpenAICompatibleLLMClient(BaseLLMClient):
    def __init__(self, config: LLMConfig):
        if not config.model:
            raise ValueError("LLM model is required")
        self.config = config
        self.base_url = (config.base_url or "https://api.openai.com/v1").rstrip("/")

    def generate_text(self, prompt: str, temperature: float = 0.2) -> str:
        payload = {
            "model": self.config.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
        }
        return self._chat(payload)

    def generate_json(self, prompt: str, temperature: float = 0.2) -> dict:
        payload = {
            "model": self.config.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "response_format": {"type": "json_object"},
        }
        try:
            return json.loads(self._chat(payload))
        except Exception:
            payload.pop("response_format", None)
            return json.loads(_strip_json_fences(self._chat(payload)))

    def _chat(self, payload: dict) -> str:
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=data,
            headers=self._headers(),
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"LLM provider returned HTTP {e.code}: {detail}") from e

        choices = body.get("choices") or []
        if not choices:
            raise RuntimeError(f"LLM provider returned no choices: {body}")
        message = choices[0].get("message") or {}
        content = message.get("content")
        if isinstance(content, list):
            content = "".join(part.get("text", "") for part in content if isinstance(part, dict))
        return str(content or "").strip()

    def _headers(self):
        headers = {"Content-Type": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        return headers


def create_llm_client(config: LLMConfig) -> BaseLLMClient:
    provider = (config.provider or "gemini").lower()
    if provider == "gemini":
        return GeminiLLMClient(config)
    if provider in {"openai", "openai-compatible", "openai_compatible"}:
        return OpenAICompatibleLLMClient(config)
    raise ValueError(f"Unsupported LLM provider: {config.provider}")


def _strip_json_fences(text: str) -> str:
    value = (text or "").strip()
    if value.startswith("```"):
        value = value.strip("`").strip()
        if value.lower().startswith("json"):
            value = value[4:].strip()
    return value
