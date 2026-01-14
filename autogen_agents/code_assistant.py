"""
Code Assistant AutoGen
======================
AutoGen multi-agent system for code generation and execution.
RISK: HIGH - Can generate and execute arbitrary code.
"""

from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
import os


# Configuration
config_list = [
    {
        "model": "gpt-4",
        "api_key": os.getenv("OPENAI_API_KEY"),
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 0,
}

# Assistant agent - generates code
assistant = AssistantAgent(
    name="CodeAssistant",
    llm_config=llm_config,
    system_message="""You are a helpful AI assistant that writes Python code.
    When asked to solve a problem, write clean, efficient code.
    Always explain your code."""
)

# User proxy - can execute code (DANGEROUS)
user_proxy = UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",  # Autonomous execution
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "/tmp/autogen_code",
        "use_docker": False,  # Executes directly on host (DANGEROUS)
    },
)

# Data analyst agent
data_analyst = AssistantAgent(
    name="DataAnalyst",
    llm_config=llm_config,
    system_message="""You are a data analyst. You analyze data and create visualizations.
    You can read files from the filesystem and process them."""
)


def run_code_task(task: str):
    """Run a code generation and execution task."""
    user_proxy.initiate_chat(
        assistant,
        message=task
    )


if __name__ == "__main__":
    run_code_task(
        "Write a Python script that reads all .csv files from /data directory, "
        "combines them, and calculates summary statistics. Execute it."
    )
