"""
FAQ Chatbot Agent
=================
LangChain agent for answering FAQs from internal knowledge base.
RISK: LOW - Read-only access to internal knowledge base only.
"""

from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os


# Read-only knowledge base search
def search_knowledge_base(query: str) -> str:
    """Search the internal FAQ knowledge base."""
    # Would use vector DB in production
    faqs = {
        "refund": "Refunds are processed within 5-7 business days.",
        "shipping": "Standard shipping takes 3-5 business days.",
        "hours": "Customer support is available 9am-5pm EST."
    }
    for key, answer in faqs.items():
        if key in query.lower():
            return answer
    return "Please contact support for more specific questions."


def get_product_info(product_id: str) -> str:
    """Get product information from catalog."""
    return f"Product {product_id}: Available, $29.99, In Stock"


tools = [
    Tool(
        name="SearchFAQ",
        func=search_knowledge_base,
        description="Search the FAQ knowledge base for answers"
    ),
    Tool(
        name="ProductInfo",
        func=get_product_info,
        description="Get product details from catalog"
    ),
]

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

prompt = PromptTemplate.from_template("""
You are a helpful FAQ assistant. Answer questions using the knowledge base.
Be concise and helpful.

Question: {input}
{agent_scratchpad}
""")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


if __name__ == "__main__":
    result = agent_executor.invoke({
        "input": "What is your refund policy?"
    })
    print(result)
