from http_request import make_request
from const import SEARXNG_INSTANCE, RESULT_NUMBER, RELEVANCE_LIMIT


async def search_by_searxng(query: str, lang: str | None = None) -> str:

    params: dict = {"q": query, "format":"json"}

    if lang:
        params["language"] = lang

    search_results = await make_request(SEARXNG_INSTANCE, params)

    # Keep only result with relevance over set relevance limit
    relevant_results: list = []
    for result in search_results["results"]:
        if result["score"] > RELEVANCE_LIMIT:
            relevant_results.append(result)

    # If there are more than 10 relevant results, pass only ten most relevant
    if len(relevant_results) > RESULT_NUMBER:
        relevant_results = relevant_results[RESULT_NUMBER:]

    # If there is no relevant result, return this information
    if len(relevant_results) == 0:
        return "No relevant result found."

    # Format all results to text.
    formatted_result: str = "Web search results:\n***\n"
    for result in relevant_results:
        formatted_result += (f"Title: {result['title']}\n"
                f"Content: {result['content']}\n"
                f"URL: {result['url']}\n"
                f"Score: {result['score']}\n"
                f"***\n")

    return formatted_result



