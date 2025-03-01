## What is it?

A [Model Context Protocol](https://modelcontextprotocol.io/) Server running over SSE

## What it offers?

Tools for web search and web extraction over Tavily API with local Searxng fallback.

## What do I need?

MCP Client, such is Claude Desktop or [LibreChat](https://github.com/danny-avila/LibreChat)

## How to run this?

Using Docker with precompiled image as per docker-compose.yml. App is listening on port 8960. Do not forget to set the required environment variables.

## How to add to LibreChat

In your librechat.yaml file, add the following section:

```yaml
mcpServers:
  media-creator:
    type: sse # type can optionally be omitted
    url: URL of your docker container # e.g. http://localhost:8957/sse
```

## How to use in LibreChat

After the server is added to LibreChat as per above, restart LibreChat to connect to MCP server and discover tools. Then, create an agent and add the respective tools to agent.

When the agent is used, you may ask the agent to search the web and/or extract information from specific URL(s).

## Contributions

Further contributions are welcomed!