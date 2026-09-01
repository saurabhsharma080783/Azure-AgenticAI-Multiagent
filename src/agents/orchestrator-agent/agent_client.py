import os

from azure.identity import DefaultAzureCredential

from agent_framework.foundry import FoundryChatClient


class AgentClient:

    def __init__(self):

        self.client = FoundryChatClient(
            project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            credential=DefaultAzureCredential()
        )

    async def invoke_requirement_agent(self, text):

        response = await self.client.complete(
            agent_name="requirement-agent",
            input=text
        )

        return response.output_text

    async def invoke_prompt_agent(self, text):

        response = await self.client.complete(
            agent_name="prompt-agent",
            input=text
        )

        return response.output_text

    async def invoke_solution_agent(self, text):

        response = await self.client.complete(
            agent_name="solution-agent",
            input=text
        )

        return response.output_text