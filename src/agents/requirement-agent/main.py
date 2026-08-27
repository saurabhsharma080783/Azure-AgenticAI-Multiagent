import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer

from azure.identity import DefaultAzureCredential


SYSTEM_PROMPT = """
You are a Requirement Gathering Agent.

Your responsibilities:

1. Understand business requirements.
2. Extract functional requirements.
3. Extract non-functional requirements.
4. Identify constraints and assumptions.
5. Produce a structured requirement summary.

Return your output in markdown.
"""


def main():

    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        credential=DefaultAzureCredential(),
    )

    requirement_agent = Agent(
        client=client,
        name="RequirementAgent",
        instructions=SYSTEM_PROMPT,
    )

    server = ResponsesHostServer(requirement_agent)

    server.run()


if __name__ == "__main__":
    main()