from swarm import Agent

user_interface_agent = Agent(
    # model="gpt-3.5-turbo",
    name="User Interface Agent",
    instructions=f"""You are a user interface agent that handles all interactions with the user. 
    You're interacting directly with user to get all the required information about the product and transfer it to info agent.""",
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
