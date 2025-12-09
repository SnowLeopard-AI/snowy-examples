import logging
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from datetime import datetime
from pandas import DataFrame
from typing import Dict, Any, List
import yaml

from snowleopard import SnowLeopardPlaygroundClient, models
from openai import OpenAI

load_dotenv()

# from playground.sl_playground.util_settings import CAMPAIGN_ACTION_MAP, CAMPAIGN__REQUEST_MAP
CAMPAIGN_PATH = os.path.join(Path(__file__).resolve().parent, 'campaign_map.yaml')
with open(CAMPAIGN_PATH, 'r', encoding='utf-8') as f:
    CAMPAIGN__REQUEST_MAP = yaml.safe_load(f)
CAMPAIGN_ACTION_MAP = {w: k for k, v in CAMPAIGN__REQUEST_MAP.items() for w in v['words']}

# Create logger
logLevel = logging.WARNING
logger = logging.getLogger("mkt_agent")
logger.setLevel(logLevel)
console = logging.StreamHandler()
console.setLevel(logLevel)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console.setFormatter(formatter)
logger.addHandler(console)

SNOWLEOPARD_API_KEY = os.getenv("SNOWLEOPARD_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATAFILE_ID = os.getenv("DATAFILE_ID")


class CampaignCoPilot:
    """
    Main agent that orchestrates campaign intelligence using SnowLeopard SQL Query SDK
    with ChatGPT formatting for final responses

    Usage:
        agent = CampaignCoPilot(datafile_id="your_datafile_id")
        response = agent.chat("Who should I contact today?")
    """

    DEFAULT_MAX_ROWS = 20

    def __init__(
        self,
        datafile_id: str,
        api_key: str = None,
        openai_api_key: str = None,
        data_only: bool = False,
        max_display_rows: int = DEFAULT_MAX_ROWS,
        use_gpt_formatting: bool = True
    ):
        """
        Initialize agent with SnowLeopard client sdk and OpenAI

        Args:
            datafile_id: Database ID for SnowLeopard
            api_key: Optional SnowLeopard API key (if not provided, reads from env)
            openai_api_key: Optional OpenAI API key (if not provided, reads from env)
            data_only: If True, only retrieve data without natural language response
            max_display_rows: Maximum rows to display in results
            use_gpt_formatting: If True, use ChatGPT to format final responses
        """
        try:
            # Initialize SnowLeopard client
            api_key = api_key or os.environ.get('SNOWLEOPARD_API_KEY')
            if api_key:
                self.sl_client = SnowLeopardPlaygroundClient(api_key=api_key)
            else:
                raise ValueError("SNOWLEOPARD_API_KEY not found. Please provide api_key parameter or set environment variable.")

            # Initialize OpenAI client
            self.use_gpt_formatting = use_gpt_formatting
            if use_gpt_formatting:
                openai_api_key = openai_api_key or os.environ.get('OPENAI_API_KEY')
                if openai_api_key:
                    self.openai_client = OpenAI(api_key=openai_api_key)
                else:
                    logger.warning("OPENAI_API_KEY not found. Disabling GPT formatting.")
                    self.use_gpt_formatting = False

            self.datafile_id = datafile_id
            self.conversation_history = []
            self.query_history = []
            self.data_only = data_only
            self.dataset_info = None
            self.max_display_rows = max_display_rows

            print("🔧 Initializing Campaign Co-Pilot...")
            # Initialize by getting dataset info
            self._initialize_dataset_info()
            print(self.dataset_info)

        except ImportError:
            raise ImportError("Required clients not found. Please install: pip install snowleopard-client openai")
        except Exception as e:
            raise Exception(f"Failed to initialize Campaign Co-Pilot: {e}")

    def _initialize_dataset_info(self):
        """Get basic dataset information for context"""
        try:
            dataset_info = self.ask_question(
                "Summarize the data.",
                data_only=True
                )
            if dataset_info and len(dataset_info) > 0:
                self.dataset_info = dataset_info[0].iat[0, 0]
                logger.debug(f"📊 Dataset: {self.dataset_info}")
                logger.debug("✅ Agent initialized with dataset information")
            else:
                logger.warning("⚠️ No dataset info returned")
                self.dataset_info = "Unknown dataset"
        except Exception as e:
            logger.exception(f"⚠️ Could not initialize dataset info: {e}")
            self.dataset_info = "Unknown dataset"

    def ask_question(self, question: str, data_only=None) -> List[DataFrame]:
        """
        Use SnowLeopard SDK to get data with streaming support

        Args:
            question: Natural language question
        Returns:
            list of DataFrames
        """
        # Use SnowLeopard's retrieve method
        # result: models.RetrieveResponse = self.sl_client.retrieve(self.datafile_id, question) if self.data_only else self.sl_client.response(self.datafile_id, question)
        result = None
        response_status, sql_list = None, None
        if data_only is None:
            data_only = self.data_only

        if data_only:
            result = self.sl_client.retrieve(self.datafile_id, question)
            response_status = result.responseStatus
            sql_list = [data.query for data in result.data]
            logger.debug(f"📡 Received response: {response_status}")
        else:
            # response() yields multiple updates - wait for the last one
            reply = []
            for partial_result in self.sl_client.response(self.datafile_id, question):
                response_status = getattr(partial_result, 'responseStatus', None)
                reply.append(partial_result)

                if response_status == 'SUCCESS':
                    result = partial_result
                    sql_list = [data.query for data in reply[1].data]
                    logger.debug(f"📡 Received response: {response_status}")

        if not result:
            logger.error("No response received from SnowLeopard")
            return []

        if response_status == 'SUCCESS':
            self.query_history.append({
                'timestamp': datetime.now(),
                'question': question,
                'type': 'natural_language',
                'response_status': response_status,
                'sql_list': sql_list,
                })
            return self._extract_data_from_result(result.llmResponse if isinstance(result, models.ResponseLLMResult) else result.data)
        else:
            logger.error(f"Failed to answer question: {question}, status: {result.responseStatus}")
            self.query_history.append({
                'timestamp': datetime.now(),
                'question': question,
                'type': 'natural_language',
                'response_status': response_status,
                'response_body': result.data,
                })
            # logger.debug(f"Failed to answer question: {question}, response_status: {response_status}, response_body: {result.data}")
            return []

    def _extract_data_from_result(self, result_data_list, use_pandas=True) -> List[DataFrame]:
        """
        Extract DataFrame from SnowLeopard result

        Args:
            result_data_list: List of result data from SnowLeopard
            use_pandas: If True, convert to DataFrame
        Returns:
            List of data/DataFrames with the data
        """
        if not result_data_list:
            return []
        result_data_list = result_data_list if isinstance(result_data_list, list) else [result_data_list]

        records = []
        for data in result_data_list:
            if hasattr(data, "query"): # isinstance(data, models.RetrieveResponse):
                # Log the query for transparency
                logger.debug(f"   📝 SQL Generated&Executed {data.schemaId}({data.schemaType}) [{len(data.rows)} rows]: {data.query}")
            if isinstance(data, str):
                records.append(data)
            elif isinstance(data, models.SchemaData):
                records.append(DataFrame(data.rows) if use_pandas else data.rows)
            elif isinstance(data, dict) and 'complete_answer' in data:
                records.append(data['complete_answer'])
            else:
                records.append(data)

        return records

    def _format_result(self, result: list) -> str:
        """Format SnowLeopard result for display"""
        if not result:
            return "No data available"

        formatted_result = []
        for dataset in result:
            if 'complete_answer' in dataset:
                formatted_result.append(str(dataset['complete_answer']))
            if isinstance(dataset, DataFrame) and not dataset.empty:
                formatted_result.append(dataset.head(self.max_display_rows).to_string(index=False))
            elif isinstance(dataset, str) and dataset:
                formatted_result.append(dataset)

        return '\n\n'.join(formatted_result) if formatted_result else "No data available"

    def _format_with_gpt(
        self,
        raw_response: str,
        user_question: str,
        action_type: str
    ) -> str:
        """
        Use ChatGPT to format the raw data response into a polished, actionable message

        Args:
            raw_response: Raw data output from SnowLeopard queries
            user_question: Original user question
            action_type: Type of action (e.g., 'analyze_performance', 'recommend_contacts')
        Returns:
            Formatted, professional response
        """
        if not self.use_gpt_formatting:
            return raw_response

        try:
            # Get the workflow name for context
            workflow_name = CAMPAIGN__REQUEST_MAP.get(action_type, {}).get('name', action_type)

            # Create a prompt for GPT to format the response
            system_prompt = """You are a marketing analytics assistant helping format campaign data into clear, actionable insights.

Your job is to take raw SQL query results and transform them into:
1. Clear, executive-ready summaries
2. Key insights and trends highlighted
3. Specific, actionable recommendations
4. Professional formatting with appropriate emojis and structure

Keep responses concise but informative. Use bullet points for clarity. Highlight numbers and percentages.
Focus on what matters most for marketing decision-makers."""

            user_prompt = f"""The user asked: "{user_question}"

This triggered the workflow: {workflow_name}

Here is the raw data from our analysis:

{raw_response}

Please format this into a clear, professional response that:
- Starts with a brief executive summary (2-3 sentences)
- Presents key findings with specific numbers
- Highlights important trends or patterns
- Ends with 2-3 actionable recommendations

Keep the tone professional but conversational. Use formatting to make it scannable."""

            # Call ChatGPT
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",  # or "gpt-4o-mini" for faster/cheaper responses
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )

            formatted_response = response.choices[0].message.content
            logger.debug("✨ Response formatted with ChatGPT")

            return formatted_response

        except Exception as e:
            logger.error(f"Failed to format with GPT: {e}")
            # Fall back to raw response if GPT formatting fails
            return raw_response

    def chat(self, user_message: str) -> Dict[str, Any]:
        """
        Main conversational interface with agentic reasoning and GPT formatting

        Args:
            user_message: User's question or command
        Returns:
            Dict with 'message' (formatted response), 'data' (raw data), 'sql' (queries used)
        """
        self.conversation_history.append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now()
            })

        logger.debug(f"\n💭 Processing: '{user_message}'")

        # Route to an appropriate handler based on intent
        message_lower = user_message.lower()

        try:
            words = re.findall(r'\b\w+\b', message_lower)
            campaign_action_name = next(
                (CAMPAIGN_ACTION_MAP.get(word) for word in words if word in CAMPAIGN_ACTION_MAP),
                None
                )
            # campaign_action_name = next((CAMPAIGN_ACTION_MAP.get(m.group(0)) for m in re.finditer(r'\b\w+\b', message_lower)), None)
            campaign_action = CAMPAIGN__REQUEST_MAP.get(campaign_action_name)

            if not campaign_action:
                campaign_action_name = 'general_query'
                logger.debug(f"🔍 Action: {campaign_action_name}")
                total_steps = 1
                result = self.ask_question(user_message)
                raw_response = self._format_result(result)
            else:
                logger.debug(f"🎯 Action: {campaign_action_name}")
                logger.debug(campaign_action['name'])
                total_steps = len(campaign_action['steps'])
                result = []

                for step in campaign_action['steps']:
                    print(f"   Step {step['id']}/{total_steps}: {step['step']}...")
                    question = step.get('question')

                    if not question:
                        question = step['question_template'].format(user_message=user_message)

                    res = self.ask_question(question)
                    result.append(self._format_result(res))

                raw_response = '\n\n'.join(result)

            # Format the response with ChatGPT
            formatted_response = self._format_with_gpt(
                raw_response=raw_response,
                user_question=user_message,
                action_type=campaign_action_name
            )

            self.conversation_history.append({
                'action_type': campaign_action_name,
                'role': 'agent',
                'content': formatted_response,
                'raw_content': raw_response,
                'timestamp': datetime.now()
                })

            return {
                'action_type': campaign_action_name,
                'message': formatted_response,
                'raw_message': raw_response,
                'sql_queries': [elem['sql_list'] for elem in self.query_history[-total_steps:] if 'sql_list' in elem]
            }

        except Exception as e:
            logger.exception("Error processing request")
            error_response = {
                'message': f"❌ Error processing request: {str(e)}\n\nPlease try rephrasing your question or check your database connection.",
                'type': 'error',
                'error': str(e)
                }
            self.conversation_history.append({
                'role': 'agent',
                'content': error_response,
                'timestamp': datetime.now()
                })
            return error_response

    def get_query_history(self) -> List[Dict]:
        """Get history of all queries executed"""
        return self.query_history

    def get_conversation_history(self) -> List[Dict]:
        """Get full conversation history"""
        return self.conversation_history


def example_usage():
    """
    Example: How to use Campaign Co-Pilot with SnowLeopard
    """

    print("=" * 80)
    print("🤖 CAMPAIGN CO-PILOT - POWERED BY SNOWLEOPARD")
    print("=" * 80)

    """
    Initialize with your database ID
    You can set SNOWLEOPARD_API_KEY as environment variable or pass it directly

    Option 1: Using environment variable
    export SNOWLEOPARD_API_KEY="your_api_key_here"
    agent = CampaignCoPilot(datafile_id="your_database_id")

    Option 2: Passing API key directly
    agent = CampaignCoPilot(
        datafile_id="your_database_id",
        api_key="your_api_key_here"
        )
    """

    print("\n📋 Ask questions")

    print("\n" + "=" * 80)
    print("✅ Campaign Co-Pilot ready to use with your SnowLeopard database!")
    print("=" * 80)


def run_interactive(agent):
    """Interactive chat mode"""
    print("Campaign Co-Pilot ready! Ask me anything...")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ['exit', 'quit']:
            break

        response = agent.chat(user_input)
        print(f"\n🤖 Agent:\n{response['message']}\n")

        # Optionally show SQL queries
        if response.get('sql_queries'):
            print(f"📝 SQL Queries executed: {len(response['sql_queries'])}")


def run_analysis(agent):
    """Run predefined analyses"""
    print("\n" + "=" * 80)
    print("📊 RUNNING COMPREHENSIVE ANALYSIS")
    print("=" * 80 + "\n")

    analyses = [
        ("Analyze performance", "📈 Performance Analysis"),
        ("Who should I contact?", "🎯 Contact Recommendations"),
        ("Optimize strategy", "🚀 Strategy Optimization")
        ]

    # Generate a report
    report = {}
    for query, title in analyses:
        print(f"\n{title}")
        print("-" * 40)
        response = agent.chat(query)
        report[query] = response
        print(response['message'])

    return report


if __name__ == "__main__":
    try:
        agent = CampaignCoPilot(
            datafile_id=DATAFILE_ID,
            api_key=SNOWLEOPARD_API_KEY,
            data_only=False,
            openai_api_key=OPENAI_API_KEY,
            use_gpt_formatting=True
            )

        # Choose mode
        mode = input("Choose mode: (1) Interactive Chat, (2) Run Performance Analysis: ")

        if mode == "2":
            run_analysis(agent)
        else:
            run_interactive(agent)

    except Exception as e:
        logger.exception('Failed to initialize agent')
        print("\n❌ Error: Make sure you have set SNOWLEOPARD_API_KEY and OPENAI_API_KEY environment variables")
        example_usage()
