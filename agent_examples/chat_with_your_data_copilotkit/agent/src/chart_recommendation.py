import json
import logging
import os
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIResponsesModel
from starlette.requests import Request
from starlette.responses import JSONResponse

load_dotenv()

logger = logging.getLogger(__name__)

MODEL_NAME = os.environ.get('MODEL_NAME', 'gpt-5.4')


class ChartRecommendation(BaseModel):
    chart_type: Literal['bar', 'area', 'line', 'donut'] = Field(
        description='The recommended chart type.'
    )
    index: str = Field(
        description='The column to use as the x-axis (bar/area/line) or label key (donut).'
    )
    categories: list[str] = Field(
        description='The column(s) to use as data series (bar/area/line) or a single value column (donut). When pivot_column is set, this should contain the single numeric value column to plot.'
    )
    title: str = Field(
        description='A short, descriptive title for the chart.'
    )
    description: str = Field(
        description='A one-line description of what the chart shows.'
    )
    layout: Literal['horizontal', 'vertical'] | None = Field(
        default=None,
        description='Bar chart layout direction. Only applicable when chart_type is "bar".'
    )
    pivot_column: str | None = Field(
        default=None,
        description='Column to pivot into separate data series. When set, each unique value in this column becomes a separate line/bar/area. The "categories" field should then contain the single value column to plot.'
    )


recommendation_agent = Agent(
    model=OpenAIResponsesModel(MODEL_NAME),
    output_type=ChartRecommendation,
    instructions="""You are a data visualization expert. Given a user's question, SQL query, and sample data, recommend the best chart type and column mapping.

Available chart types:
- "bar": Best for comparing discrete categories. Requires an index column (category labels) and one or more numeric categories (values). Set layout to "horizontal" when category labels are long text (more than ~15 characters), "vertical" otherwise.
- "area": Best for time series data where you want to show composition over time (stacked). Requires an index column (x-axis, typically a date or time period) and one or more numeric categories (series).
- "line": Best for time series or ordered data showing trends, especially with multiple breakdown series (non-stacked). Use when comparing trends across groups (e.g., revenue by region over time).
- "donut": Best for showing proportions or distribution of a single metric across a small number of categories (2-8). Requires an index column (label) and exactly one category (the numeric value). Do NOT use donut when there are more than 8 categories.

Pivot column:
When the data contains a breakdown/grouping column (e.g., region, category, product) alongside a time or ordered dimension, set "pivot_column" to the grouping column. This pivots the flat data so each unique value in that column becomes its own series.
- When using pivot_column, "categories" should contain exactly one element: the numeric value column to plot.
- The actual series names will come from the unique values in the pivot column.
- Example: data has columns [month, region, revenue]. Set index="month", pivot_column="region", categories=["revenue"] to get one line per region.

Rules:
- "index" must be a column name that exists in the provided data.
- "categories" must be column names that contain numeric values.
- For donut charts, "categories" must have exactly one element and pivot_column must be null.
- Prefer bar over donut when there are more than 8 distinct values in the index column.
- Prefer line or area when the index column looks like dates or ordered time periods.
- Prefer line over area when there are multiple breakdown series to compare.
- Use the user's original question to understand their intent and pick the most appropriate visualization.
- The title should be concise and describe what the chart visualizes.
- The description should be a single sentence explaining the insight.""",
)


async def chart_recommendation_endpoint(request: Request) -> JSONResponse:
    body = await request.json()
    columns: list[str] = body.get('columns', [])
    sample_rows: list[dict] = body.get('sample_rows', [])
    sql_query: str = body.get('sql_query', '')
    user_question: str = body.get('user_question', '')

    if not columns or not sample_rows:
        return JSONResponse(
            {'error': 'columns and sample_rows are required'},
            status_code=400,
        )

    prompt = f"""User's question: {user_question}

SQL Query: {sql_query}

Columns: {json.dumps(columns)}

Sample data (up to 10 rows):
{json.dumps(sample_rows[:10], indent=2, default=str)}"""

    logger.info('📊 Getting chart recommendation')
    result = await recommendation_agent.run(prompt)
    logger.info(f'📊 Recommended: {result.output.chart_type} chart')
    return JSONResponse(result.output.model_dump())
