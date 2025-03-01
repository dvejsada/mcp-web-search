from tavily import AsyncTavilyClient, InvalidAPIKeyError, MissingAPIKeyError, UsageLimitExceededError
from searxng import search_by_searxng
from const import RESULT_NUMBER, TAVILY_API_KEY, SEARXNG_FALLBACK

class Tavily:
    def __init__(self):

        self.client = AsyncTavilyClient(api_key=TAVILY_API_KEY)

    async def tavily_search(self, query, lang):
        """Performing a search query"""
        try:
            context = await self.client.search(query=query, include_answer=True, max_results=RESULT_NUMBER)
        except InvalidAPIKeyError:
            print("Invalid API key provided. Please check your API key.")
            return "No responses can be found due to invalid API key"
        except MissingAPIKeyError:
            print("Missing API key.")
            return "No responses can be found due to missing API key"
        # Fallback to Searxng if Tavily limit exceeded
        except UsageLimitExceededError:
            print("Usage limit exceeded. Please check your plan's usage limits or consider upgrading.")
            if SEARXNG_FALLBACK:
                alternate_response = search_by_searxng(query, lang)
                return alternate_response
            else:
                return "No responses can be obtained due to usage limit exceeded and no fallback option provided."

        search_result: str = f"Answer: {context['answer']}\n"
        search_result += "Sources:\n---\n"

        for source in context['results']:
            search_result += f"Title: {source['title']}\nURL: {source['url']}\nContent: {source['content']}\n---\n"

        return search_result

    async def tavily_extract(self, urls: list):
        """Extracts the contents of the webpage."""

        response = await self.client.extract(urls=urls, extract_depth="advanced",include_images=False)

        extracted_data: str = ""

        # Printing the extracted raw content
        for result in response["results"]:
            extracted_data += f"URL: {result['url']}"
            extracted_data += f"Raw Content: {result['raw_content']}\n"

        if response["failed_results"]:
            extracted_data += f"Following URLs cannot be extracted:"
            for failed_result in response["failed_results"]:
                extracted_data += f"URL: {failed_result['url']}."
                extracted_data += f"Error: {failed_result['error']}."

        return extracted_data

