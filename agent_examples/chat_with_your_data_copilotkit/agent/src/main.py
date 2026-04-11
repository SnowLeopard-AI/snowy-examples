import logging
import os

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format=os.environ.get("LOG_FORMAT", "%(levelname)s - %(name)s - %(message)s"),
)

from starlette.routing import Route

from agent import DataState, StateDeps, agent
from chart_recommendation import chart_recommendation_endpoint

app = agent.to_ag_ui(
    deps=StateDeps(DataState()),
    routes=[
        Route("/chart-recommendation", chart_recommendation_endpoint, methods=["POST"]),
    ],
)

if __name__ == "__main__":
    # run the app
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
