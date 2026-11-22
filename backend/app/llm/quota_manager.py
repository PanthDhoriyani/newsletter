from datetime import datetime, date, timezone, timedelta
import threading

try:
    from zoneinfo import ZoneInfo
    IST = ZoneInfo("Asia/Kolkata")
except ImportError:
    IST = timezone(timedelta(hours=5, minutes=30))

class QuotaManager:
    def __init__(self):
        self._lock = threading.Lock()
        self._gemini_count = 0
        self._groq_tokens = 0
        self._last_reset = datetime.now(IST).date()

    def _maybe_reset(self):
        today = datetime.now(IST).date()
        if today != self._last_reset:
            self._gemini_count = 0
            self._groq_tokens = 0
            self._last_reset = today

    def can_use_gemini(self, limit: int = 950) -> bool:
        with self._lock:
            self._maybe_reset()
            return self._gemini_count < limit

    def increment_gemini(self):
        with self._lock:
            self._gemini_count += 1

    def get_gemini_remaining(self, limit: int = 950) -> int:
        with self._lock:
            self._maybe_reset()
            return max(0, limit - self._gemini_count)

quota_manager = QuotaManager()
