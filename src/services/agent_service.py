from swarm import Swarm
from src.config.agents import user_interface_agent, product_info_agent, validation_agent, setup_completion_agent
import asyncio

client = Swarm()

async def get_initial_message_async():
    response = await asyncio.to_thread(client.run, agent=user_interface_agent, messages=[{"role": "user", "content": "Hi!"}])
    return response.messages[-1]["content"]

async def process_product_data_async(product_data):
    product_info_response = await asyncio.to_thread(client.run, agent=product_info_agent, messages=[{"role": "user", "content": product_data}])
    product_info = product_info_response.messages[-1]["content"]

    validation_response = await asyncio.to_thread(client.run, agent=validation_agent, messages=[{"role": "user", "content": product_info}])
    validation_result = validation_response.messages[-1]["content"]

    if "error" in validation_result.lower():
        raise ValueError(f"Validation failed: {validation_result}")

    setup_response = await asyncio.to_thread(client.run, agent=setup_completion_agent, messages=[{"role": "user", "content": validation_result}])
    setup_result = setup_response.messages[-1]["content"]

    return {
        "product_info": product_info,
        "validation_result": validation_result,
        "setup_result": setup_result
    }