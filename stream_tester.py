from mcp.server.fastmcp import FastMCP
from random import choice

mcp = FastMCP("Random Name Tester 2.0")


@mcp.tool()
def get_random_name(names: list = None) -> str:
    """Gets a random peoples names. The names are stored in a local array
    args:
       names:the user can pass in a list of names to choose from, or it will default to a predefined list.
    """

    # If names is provided and not empty, use it; otherwise use default list
    if names and isinstance(names, list):
        return choice(names)
    else:
        # Use default list of names
        default_names = [
            "Alice",
            "Bob",
            "Charlie",
            "Diana",
            "Eve",
            "Frank",
            "Grace",
            "Hank",
            "Ivy",
            "Jack",
        ]
        return choice(default_names)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
