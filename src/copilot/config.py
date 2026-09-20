"""Central config, loaded once from environment variables / .env."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=False)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DIR = DATA_DIR / "docs"
EVAL_DIR = DATA_DIR / "eval"

def _env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()

def _env_bool(name: str, default: bool) -> bool:
    val = os.environ.get(name)
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "yes", "on"}

@dataclass(frozen=True)
class ProviderConfig:
    name: str
    api_key: str
    base_url: str
    model: str

@dataclass(frozen=True)
class Settings:
    llm_provider: str = field(default_factory=lambda: _env("LLM_PROVIDER", "gemini"))

    gemini_api_key: str = field(default_factory=lambda: _env("GEMINI_API_KEY"))
    gemini_model: str = field(default_factory=lambda: _env("GEMINI_MODEL", "gemini-2.0-flash"))

    groq_api_key: str = field(default_factory=lambda: _env("GROQ_API_KEY"))
    groq_model: str = field(default_factory=lambda: _env("GROQ_MODEL", "llama-3.3-70b-versatile"))

    openrouter_api_key: str = field(default_factory=lambda: _env("OPENROUTER_API_KEY"))
    openrouter_model: str = field(
        default_factory=lambda: _env("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free")
    )

    ollama_base_url: str = field(
        default_factory=lambda: _env("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    )
    ollama_model: str = field(default_factory=lambda: _env("OLLAMA_MODEL", "llama3.1:8b"))

    llm_cache_dir: str = field(default_factory=lambda: _env("LLM_CACHE_DIR", ".cache/llm"))
    llm_cache_enabled: bool = field(default_factory=lambda: _env_bool("LLM_CACHE_ENABLED", True))

    GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
    GROQ_BASE_URL = "https://api.groq.com/openai/v1"
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

    def provider_config(self, name: str | None = None) -> ProviderConfig:
        name = (name or self.llm_provider).strip().lower()
        if name == "gemini":
            return ProviderConfig("gemini", self.gemini_api_key, self.GEMINI_BASE_URL, self.gemini_model)
        if name == "groq":
            return ProviderConfig("groq", self.groq_api_key, self.GROQ_BASE_URL, self.groq_model)
        if name == "openrouter":
            return ProviderConfig(
                "openrouter", self.openrouter_api_key, self.OPENROUTER_BASE_URL, self.openrouter_model
            )
        if name == "ollama":
            # Ollama ignores the key, but the OpenAI SDK requires a non-empty string.
            return ProviderConfig("ollama", "ollama", self.ollama_base_url, self.ollama_model)
        raise ValueError(f"Unknown LLM provider: {name!r}")

    def fallback_order(self) -> list[str]:
        order = [self.llm_provider]
        for name, key in [
            ("gemini", self.gemini_api_key),
            ("groq", self.groq_api_key),
            ("openrouter", self.openrouter_api_key),
            ("ollama", "ollama"),
        ]:
            if name not in order and key:
                order.append(name)
        return order

settings = Settings()
