import json
import httpx
import structlog
from app.config import settings

log = structlog.get_logger()

class GroqClient:
    def __init__(self, model: str = "llama-3.1-70b-versatile"):
        self.api_key = settings.groq_api_key
        self.model = model
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        if not self.api_key:
            log.warning("groq_api_key_missing")
            return ""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.0,
            "max_tokens": 4096
        }

        try:
            async with httpx.AsyncClient(timeout=45.0) as client:
                res = await client.post(self.base_url, json=payload, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    choices = data.get("choices", [])
                    if choices:
                        return choices[0].get("message", {}).get("content", "")
                    return ""
                else:
                    log.error("groq_api_error", status_code=res.status_code, text=res.text)
                    return ""
        except Exception as e:
            log.error("groq_call_exception", error=str(e))
            return ""

    async def generate_json(self, system_prompt: str, user_prompt: str) -> dict:
        prompt_with_json = user_prompt + "\n\nCRITICAL: Return ONLY raw, parseable JSON. Do not wrap in markdown or backticks."
        raw_text = await self.generate(system_prompt, prompt_with_json)
        
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
            # Fallback attempt to extract first and last curly braces
            start = cleaned.find("{")
            end = cleaned.rfind("}")
            if start != -1 and end != -1:
                try:
                    return json.loads(cleaned[start:end+1])
                except Exception:
                    pass
            log.error("groq_json_decode_failed", raw=cleaned[:200])
            return {}

groq_client = GroqClient()
