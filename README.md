# Read me first: pin the MCP SDK to 1.x

**Why:** this course was recorded on the MCP Python SDK **1.x**. A plain `uv add "mcp[cli]"` now
installs **2.x**, where `from mcp.server.fastmcp import FastMCP` fails with `ModuleNotFoundError`
(the class is now `MCPServer`), `FastMCP(host=..., port=...)` moved to `run()`, and the client API
changed. The old lockfile also pinned `mcp` 1.12.4, which has known security flaws, including an
OAuth client that could send credentials to an attacker-chosen authorization server
(GHSA-qx49-fqc8-xw99) and bearer tokens accepted for the wrong resource server (GHSA-w4fh-qvv9-3v23).
Both are fixed in **1.30.0**.

**Install this way to follow the recorded lectures:**

```bash
uv add "mcp[cli]>=1.30,<2"
```

Cloned this repo? Just run `uv sync`. The lockfile already pins `mcp` 1.30.0.
The `legacy-v1` branch stays frozen on this setup: `git checkout legacy-v1`.

**Coming soon:** a new course section on SDK 2.x and the stateless 2026 MCP spec.

| File | What it shows | Run it |
|---|---|---|
| `hello_mcp.py` | Your first tool | `uv run mcp dev hello_mcp.py` |
| `mcp_prompt.py` | Prompts | `uv run mcp dev mcp_prompt.py` |
| `mcp_resources.py` | Resources and resource templates | `uv run mcp dev mcp_resources.py` |
| `sqlite_server.py` | Tools over `db/world.db` | `uv run mcp dev sqlite_server.py` |
| `stream_tester.py` | Streamable HTTP on port 8000 | `uv run stream_tester.py` |

---


For the sqlite_server project:

Here's a comprehensive list of questions/queries you can ask Claude's desktop app to trigger these MCP tools:
🌍 Country Exploration
Basic Country Searches

"Find countries with 'United' in the name"
"Search for countries containing 'Stan'"
"What countries have 'Republic' in their name?"
"Show me countries with 'Island' in the name"
"Find all countries that start with 'A'"

Specific Country Information

"Tell me about the United States"
"Get information about Japan"
"What's the capital of France?"
"Show me details about Brazil"
"Get country information for Germany"

Regional Queries

"What countries are in Europe?"
"Show me all African countries"
"List countries in Asia"
"What countries are in North America?"
"Find countries in Oceania"

Currency-Based Queries

"What countries use the Euro?"
"Which countries use the US Dollar?"
"Show me countries that use the British Pound"
"What countries have their own currency called 'Dollar'?"
"Find countries using the Japanese Yen"

🏙️ City Exploration
City Searches

"Find cities named London"
"Search for cities with 'New' in the name"
"What cities are called Paris?"
"Show me cities named Alexandria"
"Find cities that start with 'San'"

Country-Specific City Queries

"What are the major cities in the United States?"
"Show me cities in Japan"
"List cities in the United Kingdom"
"What cities are in Canada?"
"Find cities in Australia"

Geographic Location Queries

"What cities are near coordinates 40.7, -74.0?" (New York area)
"Find cities near London's coordinates"
"Show me cities around 48.8, 2.3" (Paris area)
"What cities are near 35.6, 139.7?" (Tokyo area)
"Find cities close to 51.5, -0.1" (London coordinates)

📍 State/Province Exploration
State Searches

"Find states with 'New' in the name"
"Search for states containing 'Carolina'"
"What states have 'Island' in their name?"
"Show me states that start with 'M'"
"Find provinces with 'British' in the name"

Country-Specific State Queries

"What states are in the United States?"
"Show me provinces in Canada"
"List states in Australia"
"What administrative divisions does Germany have?"
"Find states in Brazil"

🗺️ Regional Analysis
Region Exploration

"What are all the world regions?"
"Show me the different regions of the world"
"List all continental regions"
"What subregions exist?"
"How is the world divided into regions?"

Subregion Queries

"What subregions are in Asia?" (region_id 3)
"Show me European subregions" (region_id 4)
"What are the subregions of Africa?" (region_id 1)
"List American subregions" (region_id 2)

📊 Statistical and Summary Queries
Database Statistics

"How many countries are in the database?"
"What are the database statistics?"
"Give me a count of all the data"
"How many cities and countries do you have?"
"What's the total amount of geographical data?"
