import os
from dotenv import load_dotenv

load_dotenv()


def get_cache_ttl_seconds() -> int:
    value = os.getenv("CACHE_TTL_SECONDS", "300")
    try:
        return int(value)
    except ValueError:
        return 300