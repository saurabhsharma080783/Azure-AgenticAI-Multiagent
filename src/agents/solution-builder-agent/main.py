import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer

from azure.identity import DefaultAzureCredential


SYSTEM_PROMPT = """
You are a Solution Architecture Agent.

Your responsibilities:

1. Design Azure solutions.
2. Recommend Azure services.
3. Apply Well-Architected Framework principles.
4. Consider security and scalability.
5. Provide architecture recommendations.

Return output using:

- Executive Summary
- Architecture Design
- Azure Services
- Security Considerations
- Next Steps
"""


def main():

    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        credential=DefaultAzureCredential(),
    )

    solution_agent = Agent(
        client=client,
        name="SolutionArchitectAgent",
        instructions=SYSTEM_PROMPT,
    )

    server = ResponsesHostServer(solution_agent)

    server.run()


if __name__ == "__main__":
    main()