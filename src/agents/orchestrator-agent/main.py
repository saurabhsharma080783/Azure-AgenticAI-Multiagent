import os

REQUIREMENT_AGENT = os.getenv(
    "REQUIREMENT_AGENT_NAME",
    "requirement-agent"
)

PROMPT_AGENT = os.getenv(
    "PROMPT_AGENT_NAME",
    "prompt-agent"
)

SOLUTION_AGENT = os.getenv(
    "SOLUTION_AGENT_NAME",
    "solution-agent"
)

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer

from azure.identity import DefaultAzureCredential


SYSTEM_PROMPT = """
You are an Orchestrator Agent.

Your responsibilities:

1. Understand incoming requests.
2. Determine which specialist agent should handle the request.
3. Route work to:
   - Requirement Agent
   - Prompt Optimization Agent
   - Solution Architect Agent
4. Consolidate outputs.
5. Return a final response.

Always think step-by-step.
"""


def main():

    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        credential=DefaultAzureCredential(),
    )

    orchestrator_agent = Agent(
        client=client,
        name="OrchestratorAgent",
        instructions=SYSTEM_PROMPT,
    )

    server = ResponsesHostServer(orchestrator_agent)

    server.run()


if __name__ == "__main__":
    main()