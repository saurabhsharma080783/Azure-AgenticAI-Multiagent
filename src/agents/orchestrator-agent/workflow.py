from agent_client import AgentClient

client = AgentClient()

async def run_workflow(user_input):

    requirements = await client.invoke_requirement_agent(
        user_input
    )

    optimized_prompt = await client.invoke_prompt_agent(
        requirements
    )

    solution = await client.invoke_solution_agent(
        optimized_prompt
    )

    return {
        "requirements": requirements,
        "optimized_prompt": optimized_prompt,
        "solution": solution
    }