# CrewAI + Snow Leopard Example

CrewAI is a framework in which you can define multiple agents, collectively called a "crew", which
perform tasks together.  The `crewai` package includes a code generator that makes an example crew
package.  This example modifies the generated crew to define and use a Snow Leopard tool to help a
user plan the next meetings for a game discussion club.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) package manager (tested with `uv` version 0.9.9+)
- [Snow Leopard API key](https://auth.snowleopard.ai/account/api_keys)

## Setup

1. Download and prepare the dataset
    1. This example uses a dataset of metacritic scores for games
        1. Download the `.csv` version of the dataset from here: https://www.kaggle.com/datasets/destring/metacritic-reviewed-games-since-2000
        1. The downloaded archive contains `result.csv`
    1. A script is included for converting the `.csv` version of the dataset to a sqlite file; to use this script:
        1. `uv run scripts/preparedata.py result.csv metacritic.sqlite`
1. Upload the sqlite file to [try.snowleopard.ai](https://try.snowleopard.ai)
1. Copy `.env.example` to `.env` in the same directory as this file and set values for the following environment variables:
    1. `SNOWLEOPARD_API_KEY`: a [Snow Leopard API key](https://auth.snowleopard.ai/account/api_keys)
    1. `SNOWLEOPARD_DATAFILE_ID`: the `File ID` from [try.snowleopard.ai](https://try.snowleopard.ai)
    1. `OPENAI_API_KEY`: an OpenAI API Key

## Usage

1. Run `uv run gameclub`

## Summary of agent creation process

1. Generate code using crewai tools (followed instructions from: https://github.com/crewAIInc/crewAI)
    1. Install `crewai`
    1. Run `uv run crewai create crew gameclub`
        1. For this example, we chose: openai (1), gpt-4o (5)
        1. This tool generated the the `gameclub` package with two agents, a `researcher` and `reporting analyst`
        1. The code generator produces a python package in its own directory, which we placed in `packages/` as `packages/gameclub`
1. We edited several of the files for use with [Snow Leopard Playground](https://try.snowleopard.ai)
    1. Edit `gameclub/src/gameclub/config/*.yaml` files to use appropriate prompts for the agents and tasks; note the names of replacement variables in prompt strings
    1. Edit `gameclub/src/gameclub/tools/custom_tool.py` to define `SnowLeopardMetacriticTool`
    1. Edit `gameclub/src/gameclub/crew.py` to instantiate `SnowLeopardMetacriticTool` and pass it to the `researcher` agent's `tools` kwarg list
    1. Edit `gameclub/src/gameclub/main.py` to edit the `inputs` `dict` in the `run()` function; `input` keys need to match the replacement variable names in the `*.yaml` files
