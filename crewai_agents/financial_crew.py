"""
Financial Analysis Crew
=======================
CrewAI multi-agent system for financial analysis and trading.
RISK: CRITICAL - Can execute trades and access financial data.
"""

from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from langchain_openai import ChatOpenAI
import os


# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()


# Custom dangerous tools
def execute_trade(symbol: str, action: str, quantity: int) -> str:
    """Execute a stock trade."""
    return f"EXECUTED: {action} {quantity} shares of {symbol}"


def transfer_funds(amount: float, destination: str) -> str:
    """Transfer funds to external account."""
    return f"TRANSFERRED: ${amount} to {destination}"


def access_portfolio(account_id: str) -> str:
    """Access customer portfolio data."""
    return f"Portfolio for {account_id}: AAPL: 100, GOOGL: 50, MSFT: 75"


# Agents
market_analyst = Agent(
    role="Market Analyst",
    goal="Analyze market trends and identify opportunities",
    backstory="Expert financial analyst with 20 years experience",
    tools=[search_tool, scrape_tool],
    llm=llm,
    verbose=True
)

trader = Agent(
    role="Trader",
    goal="Execute profitable trades based on analysis",
    backstory="Experienced day trader specializing in tech stocks",
    tools=[],  # Trade execution handled separately
    llm=llm,
    verbose=True
)

risk_manager = Agent(
    role="Risk Manager", 
    goal="Ensure all trades comply with risk limits",
    backstory="Former hedge fund risk officer",
    tools=[],
    llm=llm,
    verbose=True
)

# Tasks
analysis_task = Task(
    description="Analyze current market conditions for {sector} sector",
    expected_output="Detailed market analysis with buy/sell recommendations",
    agent=market_analyst
)

trading_task = Task(
    description="Execute recommended trades based on analysis",
    expected_output="Trade execution confirmation",
    agent=trader,
    context=[analysis_task]
)

risk_task = Task(
    description="Review trades for compliance with risk limits",
    expected_output="Risk assessment and approval status",
    agent=risk_manager,
    context=[trading_task]
)

# Crew
financial_crew = Crew(
    agents=[market_analyst, trader, risk_manager],
    tasks=[analysis_task, trading_task, risk_task],
    process=Process.sequential,
    verbose=True
)


if __name__ == "__main__":
    result = financial_crew.kickoff(inputs={"sector": "technology"})
    print(result)
