import httpx
import os
import asyncio

async def request(url, params):
    async with httpx.AsyncClient() as client:
        response = await client.request(url=url, method="GET", params=params, timeout=30.0)
        response.raise_for_status()
        return response.json()

def search_web(query, lang):

    searxng_instance = os.environ["SEARXNG_URL"]

    if not searxng_instance:
        ValueError("Missing SearxNG URL in environment variables.")

    params: dict = {"q": query, "format":"json"}

    if lang:
        params["language"] = lang

    search_results = asyncio.run(request(searxng_instance, params))

    # Keep only result with relevance over 2
    relevant_results: list = []
    for result in search_results["results"]:
        if result["score"] > 2:
            relevant_results.append(result)

    # If there are more than 10 relevant results, pass only ten most relevant
    if len(relevant_results) > 10:
        relevant_results = relevant_results[10:]

    # If there is no relevant result, return this information
    if len(relevant_results) == 0:
        return "No relevant result found"

    # Format all results to text.
    formatted_result: str = "Web search results:\n***\n"
    for result in relevant_results:
        formatted_result += (f"Title: {result['title']}\n"
                f"Content: {result['content']}\n"
                f"URL: {result['url']}\n"
                f"Score: {result['score']}\n"
                f"***\n")

    return formatted_result



