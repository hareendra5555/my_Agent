from copilot.config import Settings

def test_provider_config_resolves_gemini():
    s = Settings(llm_provider="gemini", gemini_api_key="abc", gemini_model="gemini-2.0-flash")
    p = s.provider_config()
    assert p.name == "gemini"
    assert p.api_key == "abc"
    assert "generativelanguage" in p.base_url

def test_fallback_order_puts_default_first_and_skips_missing_keys():
    s = Settings(llm_provider="groq", groq_api_key="k", gemini_api_key="", openrouter_api_key="")
    order = s.fallback_order()
    assert order[0] == "groq"
    assert "gemini" not in order
    assert "openrouter" not in order
    assert "ollama" in order

def test_unknown_provider_raises():
    s = Settings()
    try:
        s.provider_config("not-a-real-provider")
        assert False, "expected ValueError"
    except ValueError:
        pass