import os
from textwrap import dedent

from ag_ui.core import EventType, StateSnapshotEvent
# load environment variables
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.ag_ui import StateDeps
from pydantic_ai.messages import ToolReturn
from pydantic_ai.models.openai import OpenAIResponsesModel
from snowleopard import SnowLeopardClient
from snowleopard.models import RetrieveResponseError, ErrorSchemaData, SchemaData

load_dotenv()

# =====
# State
# =====
class DataState(BaseModel):
  data_responses: dict[str, SchemaData] = Field(
    default_factory=dict,
    description='Successful data queries',
  )

# =====
# Agent
# =====
agent = Agent(
  model = OpenAIResponsesModel('gpt-5-mini'),
  deps_type=StateDeps[DataState],
  system_prompt=dedent("""
    You are a helpful assistant that helps manage and analyze sales data.
    
    Use your tools to perform queries on the user's behalf. 
    The user will be able to see the entire data object returned and you will receive a preview.
    
    Provide a short, natural language, description of the response without restating the query or listing the data. 
    The user can see these on their screen already.
    
    Example:
    tool call: get_data(human_query: "what are my top customers...")
    tool response: {"sql_query": "select * from ...", data_top: {"customer": "Google", "arr", "5000000"...}}
    agent response: Your top customer is Google (5 million arr) which doubles your next customer ...
    
    NEVER assume data schema when making a query. Do not reference specific tables / columns unless you have already seen them in a successful response
  """).strip()
)

# =====
# Tools
# =====
@agent.tool
def get_data(ctx: RunContext[StateDeps[DataState]], human_query: str):
  """Retrieve data from "Northwind" dataset with natural language queries.
  This dataset includes information about orders, product categories, customer demographics, orders, employees, and geographic regions.
  You can use this data to create dashboards that provide insights into sales performance, customer behavior, shipping efficiency, and supplier contributions.

  When asking questions, infer user intent and be specific and ask in natural language without making any assumptions on DB structure or schema.

  Example: {"human_query": "Which customers have placed the highest number of orders? Provide the top 20 customers by order count, include
  customer id, company name, and number of orders, sorted descending by number of orders."}"""

  print(f"📊 Getting Data: \"{human_query}\"")
  response = SnowLeopardClient().retrieve(
    user_query=human_query,
    datafile_id=(os.environ['SNOWLEOPARD_DATAFILE_ID']),
  )
  if isinstance(response, RetrieveResponseError):
    print(f"📊 Response Error")
    return f"{response.responseStatus}: {response.description}"
  elif isinstance(response.data[-1], ErrorSchemaData):
    print(f"📊 Data Retrieval Error")
    data = response.data[-1]
    rtn = [f"query: {data.query}", f"error: {data.error}"]
    if data.datastoreExceptionInfo:
      rtn.append(f"exception_info: {data.datastoreExceptionInfo}")
    return "\n".join(rtn)
  else:
    print(f"📊 Data Retrieval Success")
    data = response.data[-1]
    ctx.deps.state.data_responses[ctx.tool_call_id] = data
    return ToolReturn(
      return_value=dict(
        sql_query=data.query,
        data_top=data.rows[:5],
        num_rows=len(data.rows),
      ),
      metadata=[
        StateSnapshotEvent(
          type=EventType.STATE_SNAPSHOT,
          snapshot=ctx.deps.state,
        ),
      ],
    )

@agent.tool
def read_get_data_response(ctx: RunContext[StateDeps[DataState]], tool_call_id: str, start_row: int = 0, end_row: int = 20):
  """"""
  print(f"📊 Reading Data Response")
  response = ctx.deps.state.data_responses.get(tool_call_id)
  if not response:
    valid_ids = list(ctx.deps.state.data_responses.keys())
    return f"No successful \"get_data\" found with tool_call_id. Valid ids: {valid_ids}"
  else:
    return dict(
      window = (start_row, end_row),
      data_window = response.rows[start_row:end_row],
      total_rows = len(response.rows),
    )
