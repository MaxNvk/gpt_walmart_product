from swarm import Agent

user_interface_agent = Agent(
    # model="gpt-3.5-turbo",
    name="User Interface Agent",
    instructions=f"""You are the user interface agent responsible for gathering product information from the user and passing it to the info agent. Guide the user through questions to collect details (e.g., product name, category, features, pricing).
At the end, convert the conversation into a JSON string, parse it, and prepare the data for the next agents. Ensure the JSON is clean, structured, and includes all relevant details for further processing.""",
)

product_info_agent = Agent(
    # model="gpt-3.5-turbo",
    instructions="You are responsible for gathering and structuring product data for Walmart setup.",
)

validation_agent = Agent(
    # model="gpt-3.5-turbo",
    instructions="You validate product data accuracy and check for completeness.",
)

setup_completion_agent = Agent(
    # model="gpt-3.5-turbo",
    instructions="You finalize the setup process, ensuring all requirements are met."
)
