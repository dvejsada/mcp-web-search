import mcp.types as types
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from searxng import search_by_searxng
from tavily_api import tavily_search, tavily_extract
import logging


def create_server():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("mcp-search")
    logger.setLevel(logging.DEBUG)
    logger.info("Starting MCP Search")

    # Initialize base MCP server
    server = Server("mcp_search")

    init_options = InitializationOptions(
        server_name="mcp-search",
        server_version="0.4",
        capabilities=server.get_capabilities(
            notification_options=NotificationOptions(),
            experimental_capabilities={},
        ),
    )

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """
        List available tools.
        Each tool specifies its arguments using JSON Schema validation.
        Name must be maximum of 64 characters
        """
        return [
            types.Tool(
                name="Search_web",
                description="Searches the web.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Query to search."
                        },
                        "lang": {
                            "type": "string",
                            "description": "Code of the language for search (e.g. cs, en, de)."
                        }
                    },
                    "required": ["query"]
                }
            ),
            types.Tool(
                name="Extract_webpage",
                description="Extracts text from provided URL.",
                inputSchema={
                    "$schema": "http://json-schema.org/draft-07/schema#",
                    "type": "object",
                    "properties": {
                        "urls": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "minItems": 1,
                            "maxItems": 20
                        }
                    },
                    "required": ["urls"],
                    "additionalProperties": False
                }
            )
        ]

    @server.call_tool()
    async def handle_call_tool(
            name: str, arguments: dict | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """
        Handle tool execution requests.
        """
        if not arguments:
            raise ValueError("Missing arguments")


        if name == "Search_web":
            lang: str = arguments.get("language")
            query: str = arguments.get("query")

            if not query:
                raise ValueError("No query provided.")

            result_text: str = await tavily_search(query, lang)

            return [
                types.TextContent(
                    type="text",
                    text=result_text
                )
            ]

        if name == "Extract_webpage":
            urls: list = arguments.get("urls")

            if not 1 <= len(urls) <= 20:
                raise ValueError("Must be between 1 and 20 URLs to extract")

            result_text: str = await tavily_extract(urls)

            return [
                types.TextContent(
                    type="text",
                    text=result_text
                )
            ]

        else:
            raise ValueError(f"Unknown tool: {name}")

    return server, init_options


