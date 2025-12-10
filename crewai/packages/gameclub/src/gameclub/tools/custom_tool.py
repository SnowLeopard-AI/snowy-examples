import json
import os

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from snowleopard import SnowLeopardPlaygroundClient
from typing import Type


class SnowLeopardMetacriticToolInput(BaseModel):
    """Input schema for SnowLeopardMetacriticToolInput."""
    question: str = Field(..., description="natural language question describing the data to search for.")


class SnowLeopardMetacriticTool(BaseTool):
    name: str = "Snow Leopard Metacritic Data"
    description: str = (
        "the Snow Leopard Metacritic Data tool takes a natural language question, performs "
        "a search of a database for relevant data, and returns a JSON structure containing the "
        "retrieved data.  this database contains Metacritic metascores for game titles, the "
        "platform(s) on which those games were released, the userscore for each title, and the "
        "release date of each title."
    )
    args_schema: Type[BaseModel] = SnowLeopardMetacriticToolInput

    def _run(self, question: str) -> str:
        datafile_id = os.getenv('GAMECLUB_DATAFILE_ID')
        if datafile_id is None:
            raise RuntimeError('GAMECLUB_DATAFILE_ID is not set')
        # SNOWLEOPARD_API_KEY must be set to instantiate the client
        sl_client = SnowLeopardPlaygroundClient()
        retrieve_response = sl_client.retrieve(datafile_id, question)
        return json.dumps(retrieve_response.data[0].rows)
