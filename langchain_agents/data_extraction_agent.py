"""
Data Extraction Agent
=====================
LangChain agent for extracting and processing data from multiple sources.
RISK: CRITICAL - Has shell access, file write, and external HTTP capabilities.
"""

from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain.prompts import PromptTemplate
import subprocess
import requests
import os


# Dangerous: Shell command execution
def run_shell_command(command: str) -> str:
    """Execute a shell command and return output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout or result.stderr


# Dangerous: Write to filesystem
def write_file(content: str, filepath: str) -> str:
    """Write content to a file."""
    with open(filepath, 'w') as f:
        f.write(content)
    return f"Written to {filepath}"


# Dangerous: External HTTP requests
def fetch_url(url: str) -> str:
    """Fetch content from a URL."""
    response = requests.get(url, timeout=30)
    return response.text[:5000]


# Dangerous: Database query
def query_database(sql: str) -> str:
    """Execute SQL query against customer database."""
    # In production, this would connect to real DB
    return f"Executed: {sql}"


# Dangerous: Send to external API
def send_to_webhook(data: str, webhook_url: str) -> str:
    """Send data to external webhook."""
    response = requests.post(webhook_url, json={"data": data})
    return f"Sent to {webhook_url}: {response.status_code}"


# Define tools
tools = [
    Tool(
        name="ShellCommand",
        func=run_shell_command,
        description="Execute shell commands on the system"
    ),
    Tool(
        name="WriteFile",
        func=write_file,
        description="Write content to a file on the filesystem"
    ),
    Tool(
        name="FetchURL",
        func=fetch_url,
        description="Fetch content from any URL"
    ),
    Tool(
        name="QueryDatabase",
        func=query_database,
        description="Query the customer database"
    ),
    Tool(
        name="SendWebhook",
        func=send_to_webhook,
        description="Send data to external webhook endpoint"
    ),
]

# LLM setup
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

# Agent prompt
prompt = PromptTemplate.from_template("""
You are a data extraction assistant. You can:
- Execute shell commands
- Read and write files
- Fetch data from URLs
- Query databases
- Send data to webhooks

Question: {input}
{agent_scratchpad}
""")

# Create agent
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


if __name__ == "__main__":
    # Example usage
    result = agent_executor.invoke({
        "input": "Extract all customer emails from the database and save to /tmp/emails.txt"
    })
    print(result)
