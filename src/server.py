import mcp.types as types
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from search import search_web
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
        server_version="0.3",
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
                name="search-web",
                description="Searches the web using SearxNG.",
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


        if name == "search-web":
            lang: str = arguments.get("language")
            query: str = arguments.get("query")

            if not query:
                raise ValueError("No query provided.")

            result_text: str = await search_web(query, lang)

            return [
                types.TextContent(
                    type="text",
                    text=result_text
                )
            ]

        else:
            raise ValueError(f"Unknown tool: {name}")

    return server, init_options


