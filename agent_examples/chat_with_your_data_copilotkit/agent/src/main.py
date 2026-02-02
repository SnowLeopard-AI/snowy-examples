import logging
import os

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format=os.environ.get("LOG_FORMAT", "%(levelname)s - %(name)s - %(message)s"),
)

from agent import DataState, StateDeps, agent

app = agent.to_ag_ui(deps=StateDeps(DataState()))

if __name__ == "__main__":
    # run the app
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
