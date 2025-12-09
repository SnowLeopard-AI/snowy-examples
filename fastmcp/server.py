import os
import sys

from fastmcp import FastMCP
from snowleopard import SnowLeopardPlaygroundClient

mcp = FastMCP("Snowy")

# Instantiate your SnowLeopard Client.
# Note! This requires envar SNOWLEOPARD_API_KEY
snowy = SnowLeopardPlaygroundClient()

# This is a datafile id that corresponds to a superheroes.db datafile uploaded at https://try.snowleopard.ai
datafile_id = os.environ.get('SNOWLEOPARD_EXAMPLE_DATAFILE_ID')
if not datafile_id:
    print("envar SNOWLEOPARD_EXAMPLE_DATAFILE_ID required", file=sys.stderr)
    sys.exit(1)

# Our snowy mcp server will expose a single tool "get_data" that allows agents to retrieve data from SnowLeopard
@mcp.tool
def get_data(user_query: str):
    """
    Retrieve superhero data.
    Superhero/comic book character database
    Contains physical characteristics and publication history
    """
    return snowy.retrieve(datafile_id, user_query)


if __name__ == "__main__":
    mcp.run()
