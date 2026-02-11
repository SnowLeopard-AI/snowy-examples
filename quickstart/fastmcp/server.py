import os
import sys

from fastmcp import FastMCP
from snowleopard import SnowLeopardClient

mcp = FastMCP("Snowy")

# Instantiate your Snow Leopard Client.
# Note! This requires env var SNOWLEOPARD_API_KEY
snowy = SnowLeopardClient()

# This is a datafile id that corresponds to a superheroes.db datafile uploaded at https://try.snowleopard.ai
datafile_id = os.environ.get('SNOWLEOPARD_DATAFILE_ID')
if not datafile_id:
    print("environment variable SNOWLEOPARD_DATAFILE_ID required", file=sys.stderr)
    sys.exit(1)

# Our snowy mcp server will expose a single tool "get_data" that allows agents to retrieve data from SnowLeopard
@mcp.tool
def get_data(user_query: str):
    """
    Retrieve superhero data.
    Superhero/comic book character database
    Contains physical characteristics and publication history
    """
    return snowy.retrieve(user_query=user_query, datafile_id=datafile_id)


if __name__ == "__main__":
    mcp.run()
