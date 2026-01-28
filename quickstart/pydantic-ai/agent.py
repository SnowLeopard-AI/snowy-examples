import os
import sys

from pydantic_ai import Agent, RunContext
from snowleopard import SnowLeopardClient

# Get model from environment variable with default
# PydanticAI model format: 'provider:model-name' (e.g., 'anthropic:claude-sonnet-4-5', 'openai:gpt-4o')
MODEL_NAME = os.environ.get('MODEL_NAME', 'anthropic:claude-sonnet-4-5')

# Create a pydantic agent.
# Note! This requires the appropriate API key env var for the model provider
agent = Agent(
    MODEL_NAME,
    instructions='Be concise, reply with one sentence.',
)

# Instantiate your Snow Leopard Client.
# Note! This requires env var SNOWLEOPARD_API_KEY
snowy = SnowLeopardClient()

# This is a datafile id that corresponds to a superheroes.db datafile uploaded at http//try.snowleopard.ai
datafile_id = os.environ.get('SNOWLEOPARD_DATAFILE_ID')
if not datafile_id:
    print("environment variable SNOWLEOPARD_DATAFILE_ID required", file=sys.stderr)
    sys.exit(1)

# Define the get_data tool for your agent. This allows the agent to retrieve data using Snow Leopard
# The docstring becomes the tool description, so this is part of the agent context.
@agent.tool
def get_data(ctx: RunContext[str], user_query: str) -> str:
    """
    Retrieve superhero data.
    Superhero/comic book character database
    Contains physical characteristics and publication history
    """
    print(f"[Tool Call]: get_data {user_query}")
    response = snowy.retrieve(user_query=user_query, datafile_id=datafile_id)
    print(f"[Tool Response]: {response}")
    return str(response)
