"""
Content Generation Crew
=======================
CrewAI multi-agent system for content creation and publishing.
RISK: MEDIUM - Can publish content externally but no financial access.
"""

from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI


llm = ChatOpenAI(model="gpt-4", temperature=0.7)
search_tool = SerperDevTool()


# Agents
researcher = Agent(
    role="Content Researcher",
    goal="Research topics thoroughly for accurate content",
    backstory="Investigative journalist with fact-checking expertise",
    tools=[search_tool],
    llm=llm,
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Create engaging, well-structured content",
    backstory="Award-winning copywriter and blogger",
    tools=[],
    llm=llm,
    verbose=True
)

editor = Agent(
    role="Editor",
    goal="Polish content and ensure quality standards",
    backstory="Senior editor with 15 years at major publications",
    tools=[],
    llm=llm,
    verbose=True
)

# Tasks
research_task = Task(
    description="Research the topic: {topic}",
    expected_output="Comprehensive research notes with sources",
    agent=researcher
)

writing_task = Task(
    description="Write a blog post based on research",
    expected_output="1000-word blog post",
    agent=writer,
    context=[research_task]
)

editing_task = Task(
    description="Edit and polish the blog post",
    expected_output="Final edited blog post ready for publication",
    agent=editor,
    context=[writing_task]
)

# Crew
content_crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    process=Process.sequential,
    verbose=True
)


if __name__ == "__main__":
    result = content_crew.kickoff(inputs={"topic": "AI Security Best Practices"})
    print(result)
