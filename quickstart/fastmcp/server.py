import os
import sys

from fastmcp import FastMCP
from snowleopard import SnowLeopardClient

mcp = FastMCP("Snowy")

# Instantiate your Snow Leopard Client.
# Note! This requires env var SNOWLEOPARD_API_KEY
snowy = SnowLeopardClient()

# This is the id of your Snow Leopard Cloud instance, found on the Connection Info tab at https://cloud.snowleopard.ai
instance_id = os.environ.get('SNOWLEOPARD_INSTANCE_ID')
if not instance_id:
    print("environment variable SNOWLEOPARD_INSTANCE_ID required", file=sys.stderr)
    sys.exit(1)

# Our snowy mcp server will expose a single tool "get_data" that allows agents to retrieve data from SnowLeopard
@mcp.tool
def get_data(user_query: str):
    """
    Retrieve superhero data.
    Superhero/comic book character database
    Contains physical characteristics and publication history
    """
    return snowy.retrieve(user_query=user_query, instance_id=instance_id)


if __name__ == "__main__":
    mcp.run()
