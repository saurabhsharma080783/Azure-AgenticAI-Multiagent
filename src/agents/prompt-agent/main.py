import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer

from azure.identity import DefaultAzureCredential


SYSTEM_PROMPT = """
You are a Prompt Optimization Agent.

Your responsibilities:

1. Improve prompt clarity.
2. Remove ambiguity.
3. Identify missing information.
4. Enhance prompt effectiveness.
5. Produce an optimized prompt.

Return your output in markdown.
"""


def main():

    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        credential=DefaultAzureCredential(),
    )

    prompt_agent = Agent(
        client=client,
        name="PromptOptimizationAgent",
        instructions=SYSTEM_PROMPT,
    )

    server = ResponsesHostServer(prompt_agent)

    server.run()


if __name__ == "__main__":
    main()