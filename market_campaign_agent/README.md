# 🚀 Marketing Campaign Co-Pilot Agent

AI-powered marketing analytics assistant combining:
- SnowLeopard for natural-language → SQL querying
- OpenAI GPT for polished, executive-ready insights
- Agentic multi-step workflows for deeper analysis

## ✨ Features

- 🔍 **Agentic Workflows**: Automatically executes multi-step analyses based on natural language queries
- 📊 **Performance Analytics**: Track conversion rates, campaign metrics, and temporal trends
- 🎯 **Contact Recommendations**: Identify high-potential customers using ML-driven scoring
- ⏰ **Timing Analysis**: Optimize outreach timing based on historical performance
- 🚀 **Strategy Optimization**: Get data-driven recommendations to improve campaign ROI
- ✨ **GPT-Formatted Responses**: Professional, executive-ready insights with actionable recommendations

## 📥 Prerequesits
Prepare Database (from Kaggle CSV) - see https://www.kaggle.com/datasets/prakharrathi25/banking-dataset-marketing-targets
download file, unzip and create sqlite3 database from csv file:
```sh
unzip archive.zip
tbl=marketing_campaign_dataset
mv train.csv $tbl.csv
sqlite3 "$tbl.db" <<EOF
.mode csv
.separator ";"
.import $tbl.csv $tbl
EOF
```

Upload to SnowLeopard → copy the DATAFILE_ID.

## 📦 Installation
1. Clone repository
```sh
git clone git@github.com:SnowLeopard-AI/snowy-examples.git
cd snowy-examples/market_campaign_agent
```

2. Install dependencies
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

3. Create .env
`cp .env.example .env`

    Fill in:
    - `SNOWLEOPARD_API_KEY` ([Get one here](https://0647839.propelauthtest.com/account/api_keys))
    - `OPENAI_API_KEY` ([Get one here](https://platform.openai.com/api-keys))
    - `DATAFILE_ID` ([try.snowleopard.ai](https://try.snowleopard.ai) - copy ID)

### ▶️ Running the Agent
`python3 market_campaign_agent.py`


Choose:

1 — Interactive chat

2 — Run full analysis report


### 🧠 Example queries

- “How is the campaign performing?”
- “Who should I contact today?”
- “Compare segments by job and education”
- “Why did conversions drop?”
- "what is the number of subscriptions in November?"

## 🛠 Custom Workflows
### Adding New Workflows
Modify or extend campaign_map.yaml.
```yaml
custom_workflow:
  name: "🎯 AGENTIC WORKFLOW: Custom Analysis"
  steps:
    - id: 1
      question: "Your SQL-friendly question here"
      step: "Description of what this step does"
    - id: 2
      question: "Follow-up question"
      step: "Next step description"
  words:
    - trigger
    - keywords
    - for
    - workflow
```
