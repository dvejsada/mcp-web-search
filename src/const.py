import os

# Get Tavily API key
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    print("No TAVILY API key provided.")
RESULT_NUMBER = int(os.environ.get("RESULT_NUMBER",5))

SEARXNG_FALLBACK = bool(os.getenv("SEARXNG_FALLBACK", False))

# Get SearxNG settings if enabled as fallback option
SEARXNG_INSTANCE = os.environ.get("SEARXNG_URL", None)
if SEARXNG_FALLBACK:
    if not SEARXNG_INSTANCE:
        raise ValueError("Missing SearxNG URL in environment variables.")
RELEVANCE_LIMIT = float(os.environ.get("RELEVANCE_LIMIT",0.1))




