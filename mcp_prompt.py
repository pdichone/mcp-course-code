from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Prompt Tester")


@mcp.prompt()
def get_prompt(topic: str) -> str:
    """
    Returns a prompt for the given topic which will do a detailed analysis on the topic.
    Args:
        topic (str): The topic to analyze.
    """
    return (
        f"Do a comprehensive, detailed analysis on the topic of {topic}. and provide a summary of the key points. "
        "The analysis should be thorough and cover all relevant aspects of the topic. "
        "The summary should be concise and highlight the most important findings. "
    )


if __name__ == "__main__":
    mcp.run()
