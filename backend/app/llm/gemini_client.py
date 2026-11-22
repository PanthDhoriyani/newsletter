import json
import httpx
import structlog
from app.config import settings
from app.llm.quota_manager import quota_manager

log = structlog.get_logger()

class GeminiClient:
    def __init__(self):
        self.api_key = settings.gemini_api_key
        self.model = "gemini-1.5-flash"
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        if not quota_manager.can_use_gemini() or not self.api_key:
            log.warning("gemini_quota_exceeded_or_missing_falling_back_to_groq")
            from app.llm.groq_client import groq_client
            return await groq_client.generate(system_prompt, user_prompt)

        url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
        
        payload = {
            "system_instruction": {
                "parts": [{"text": system_prompt}]
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": user_prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "topP": 0.95,
                "maxOutputTokens": 4096
            }
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    quota_manager.increment_gemini()
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            return parts[0].get("text", "")
                    return ""
                else:
                    log.error("gemini_api_error", status_code=res.status_code, body=res.text)
                    from app.llm.groq_client import groq_client
                    return await groq_client.generate(system_prompt, user_prompt)
        except Exception as e:
            log.error("gemini_call_exception", error=str(e))
            from app.llm.groq_client import groq_client
            return await groq_client.generate(system_prompt, user_prompt)

    async def generate_json(self, system_prompt: str, user_prompt: str) -> dict:
        prompt_with_json = user_prompt + "\n\nCRITICAL: Respond ONLY with a valid JSON object. No explanation, no code fences."
        raw_text = await self.generate(system_prompt, prompt_with_json)
        
        # Clean markdown codeblocks
        cleaned = raw_text.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            cleaned = "\n".join(lines).strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            log.warning("gemini_json_decode_failed_retrying_via_groq", raw=cleaned[:200])
            from app.llm.groq_client import groq_client
            return await groq_client.generate_json(system_prompt, user_prompt)

gemini_client = GeminiClient()
