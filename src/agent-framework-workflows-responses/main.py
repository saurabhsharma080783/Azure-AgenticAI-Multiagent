import os
import sys

sys.path.append("../")

from agents.requirement_agent import RequirementGatheringAgent
from agents.prompt_optimization_agent import PromptOptimizationAgent
from agents.solution_build_analyst_agent import SolutionBuildAnalystAgent

from agent_framework import (
    Agent,
    AgentExecutor,
    WorkflowBuilder
)

from agent_framework.foundry import (
    FoundryChatClient
)

from agent_framework_foundry_hosting import (
    ResponsesHostServer
)

from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()


def main():

    client = FoundryChatClient(
        project_endpoint=os.environ[
            "FOUNDRY_PROJECT_ENDPOINT"
        ],
        model=os.environ[
            "AZURE_AI_MODEL_DEPLOYMENT_NAME"
        ],
        credential=DefaultAzureCredential(),
    )

    requirement_agent = Agent(
        client=client,
        name="RequirementGatheringAgent",
        instructions=
            RequirementGatheringAgent.SYSTEM_PROMPT
    )

    optimization_agent = Agent(
        client=client,
        name="PromptOptimizationAgent",
        instructions=
            PromptOptimizationAgent.SYSTEM_PROMPT
    )

    solution_agent = Agent(
        client=client,
        name="SolutionBuildAnalystAgent",
        instructions=
            SolutionBuildAnalystAgent.SYSTEM_PROMPT
    )

    requirement_executor = AgentExecutor(
        requirement_agent,
        context_mode="last_agent"
    )

    optimization_executor = AgentExecutor(
        optimization_agent,
        context_mode="last_agent"
    )

    solution_executor = AgentExecutor(
        solution_agent,
        context_mode="last_agent"
    )

    workflow = (
        WorkflowBuilder(
            start_executor=requirement_executor,
            output_executors=[
                solution_executor
            ],
        )
        .add_edge(
            requirement_executor,
            optimization_executor
        )
        .add_edge(
            optimization_executor,
            solution_executor
        )
        .build()
        .as_agent()
    )

    server = ResponsesHostServer(workflow)

    server.run()


if __name__ == "__main__":
    main()
x