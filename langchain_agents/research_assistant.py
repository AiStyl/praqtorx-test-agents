"""
Research Assistant Agent
========================
LangChain agent for research and summarization tasks.
RISK: HIGH - Has external API access and can store data.
"""

from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
import requests
import os


# External search
search = DuckDuckGoSearchRun()


def search_web(query: str) -> str:
    """Search the web for information."""
    return search.run(query)


# External API call
def call_external_api(endpoint: str, data: dict) -> str:
    """Call an external API with data."""
    response = requests.post(endpoint, json=data, timeout=30)
    return response.json()


# Store to cloud
def store_to_s3(content: str, key: str) -> str:
    """Store content to S3 bucket."""
    # Would use boto3 in production
    return f"Stored {len(content)} bytes to s3://research-data/{key}"


# Read from database (read-only)
def read_documents(query: str) -> str:
    """Read documents from internal database."""
    return f"Found 5 documents matching: {query}"


tools = [
    Tool(
        name="WebSearch",
        func=search_web,
        description="Search the web for current information"
    ),
    Tool(
        name="ExternalAPI",
        func=call_external_api,
        description="Call external APIs with data"
    ),
    Tool(
        name="StoreS3",
        func=store_to_s3,
        description="Store results to S3 cloud storage"
    ),
    Tool(
        name="ReadDocuments",
        func=read_documents,
        description="Search internal document database"
    ),
]

llm = ChatOpenAI(model="gpt-4", temperature=0)

prompt = PromptTemplate.from_template("""
You are a research assistant. Help users find and analyze information.

Question: {input}
{agent_scratchpad}
""")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


if __name__ == "__main__":
    result = agent_executor.invoke({
        "input": "Research the latest AI security trends and summarize"
    })
    print(result)
