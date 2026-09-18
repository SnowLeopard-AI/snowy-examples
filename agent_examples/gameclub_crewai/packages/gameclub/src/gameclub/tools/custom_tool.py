import json
import os

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from snowleopard import SnowLeopardClient
from snowleopard.models import APIError, ErrorSchemaData
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
        instance_id = os.getenv('SNOWLEOPARD_INSTANCE_ID')
        if not instance_id:
            raise RuntimeError('SNOWLEOPARD_INSTANCE_ID is not set')
        # SNOWLEOPARD_API_KEY must be set to instantiate the client
        sl_client = SnowLeopardClient()
        retrieve_response = sl_client.retrieve(user_query=question, instance_id=instance_id)
        if isinstance(retrieve_response, APIError):
            return json.dumps({'error': f'{retrieve_response.responseStatus}: {retrieve_response.description}'})
        if not retrieve_response.data:
            return json.dumps({'error': 'no data returned'})
        # the last data item holds the final query; earlier items are intermediate steps
        data = retrieve_response.data[-1]
        if isinstance(data, ErrorSchemaData):
            return json.dumps({'error': data.error, 'query': data.query})
        return json.dumps(data.rows)
