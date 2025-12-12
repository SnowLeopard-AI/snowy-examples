import logging
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

import yaml
from dotenv import load_dotenv
from openai import OpenAI

from agent import Agent

load_dotenv()

# Load campaign configuration
CAMPAIGN_PATH = os.path.join(Path(__file__).resolve().parent, 'campaign_map.yaml')
with open(CAMPAIGN_PATH, 'r', encoding='utf-8') as f:
    CAMPAIGN_REQUEST_MAP = yaml.safe_load(f)

# Create reverse mapping from keywords to campaign actions
CAMPAIGN_ACTION_MAP = {
    w: k
    for k, v in CAMPAIGN_REQUEST_MAP.items()
    for w in v['words']
    }

# Create logger
logLevel = logging.WARNING
logger = logging.getLogger("campaign_copilot")
logger.setLevel(logLevel)
console = logging.StreamHandler()
console.setLevel(logLevel)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console.setFormatter(formatter)
logger.addHandler(console)

SNOWLEOPARD_API_KEY = os.getenv("SNOWLEOPARD_API_KEY")
SNOWLEOPARD_DATAFILE_ID = os.getenv("SNOWLEOPARD_DATAFILE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class CampaignCoPilot:
    """
    Marketing Campaign Co-Pilot that orchestrates campaign intelligence
    using an Agent (Snow Leopard) for data retrieval and OpenAI for formatting

    Usage:
        copilot = CampaignCoPilot(datafile_id="your_datafile_id")
        response = copilot.chat("Who should I contact today?")
    """

    def __init__(
        self,
        datafile_id: str,
        api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        data_only: bool = False,
        max_display_rows: int = 20,
        use_gpt_formatting: bool = True
    ):
        """
        Initialize Campaign Co-Pilot with Agent and OpenAI

        Args:
            datafile_id: Database ID for Snow Leopard
            api_key: Optional Snow Leopard API key (if not provided, reads from env)
            openai_api_key: Optional OpenAI API key (if not provided, reads from env)
            data_only: If True, only retrieve data without natural language response
            max_display_rows: Maximum rows to display in results
            use_gpt_formatting: If True, use ChatGPT to format final responses
        """
        try:
            print("🔧 Initializing Campaign Co-Pilot...")

            # Initialize base Agent with Snow Leopard
            self.agent = Agent(
                datafile_id=datafile_id,
                api_key=api_key,
                data_only=data_only,
                max_display_rows=max_display_rows
                )

            # Initialize OpenAI client for campaign response formatting
            self.use_gpt_formatting = use_gpt_formatting
            if use_gpt_formatting:
                openai_api_key = openai_api_key or os.environ.get('OPENAI_API_KEY')
                if openai_api_key:
                    self.openai_client = OpenAI(api_key=openai_api_key)
                else:
                    logger.warning("OPENAI_API_KEY not found. Disabling GPT formatting.")
                    self.use_gpt_formatting = False

            self.conversation_history = []

            print(f"📊 Dataset: {self.agent.get_dataset_info()}")
            print("✅ Campaign Co-Pilot ready!")

        except Exception as e:
            raise Exception(f"Failed to initialize Campaign Co-Pilot: {e}")

    def _identify_campaign_action(self, user_message: str) -> tuple:
        """
        Identify the campaign action based on user message keywords

        Args:
            user_message: User's input message
        Returns:
            Tuple of (action_name, action_config)
        """
        message_lower = user_message.lower()
        words = re.findall(r'\b\w+\b', message_lower)

        campaign_action_name = next(
            (CAMPAIGN_ACTION_MAP.get(word) for word in words
             if word in CAMPAIGN_ACTION_MAP),
            None
            )

        if campaign_action_name:
            campaign_action = CAMPAIGN_REQUEST_MAP.get(campaign_action_name)
            return campaign_action_name, campaign_action

        return 'general_query', None

    def _execute_campaign_workflow(
        self,
        campaign_action: Dict,
        user_message: str
        ) -> tuple:
        """
        Execute a multi-step campaign workflow

        Args:
            campaign_action: Campaign action configuration
            user_message: Original user message
        Returns:
            Tuple of (results_list, total_steps)
        """
        print("\n" + "=" * 80)
        print(campaign_action['name'])
        print("=" * 80 + "\n")
        total_steps = len(campaign_action['steps'])
        results = []

        for step in campaign_action['steps']:
            print(f"   Step {step['id']}/{total_steps}: {step['step']}...")

            question = step.get('question')
            if not question:
                question = step['question_template'].format(user_message=user_message)

            result = self.agent.ask_question(question)
            results.append(self.agent.format_result(result))

        return results, total_steps

    def _format_with_gpt(
        self,
        raw_response: str,
        user_question: str,
        action_type: str
        ) -> str:
        """
        Use ChatGPT to format the raw data response into a polished, actionable message

        Args:
            raw_response: Raw data output from Agent queries
            user_question: Original user question
            action_type: Type of action (e.g., 'analyze_performance', 'recommend_contacts')
        Returns:
            Formatted, professional response
        """
        if not self.use_gpt_formatting:
            return raw_response

        try:
            # Get the workflow name for context
            workflow_name = CAMPAIGN_REQUEST_MAP.get(action_type, {}).get('name', action_type)

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
                model="gpt-4o",
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

    def chat(self, user_message: str, question_only=False) -> Dict[str, Any]:
        """
        Main conversational interface with campaign workflow routing

        Args:
            user_message: User's question or command
        Returns:
            Dict with 'message', 'raw_message', 'action_type', 'sql_queries'
        """
        self.conversation_history.append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now()
            })

        logger.debug(f"\n💭 Processing: '{user_message}'")

        try:
            campaign_action_name, campaign_action = 'general_query', None
            if not question_only:
                # Identify campaign action
                campaign_action_name, campaign_action = self._identify_campaign_action(
                    user_message
                    )

            # Execute workflow
            if not campaign_action:
                # General query - single question
                logger.debug(f"🔍 Action: {campaign_action_name}")
                result = self.agent.ask_question(user_message)
                raw_response = self.agent.format_result(result)
                total_steps = 1
            else:
                # Campaign workflow - multiple steps
                logger.debug(f"🎯 Action: {campaign_action_name}")
                logger.debug(f"   Workflow: {campaign_action['name']}")

                results, total_steps = self._execute_campaign_workflow(
                    campaign_action, user_message
                    )
                raw_response = '\n\n'.join(results)

            # Format response with ChatGPT
            formatted_response = self._format_with_gpt(
                raw_response=raw_response,
                user_question=user_message,
                action_type=campaign_action_name
                )

            # Store in conversation history
            self.conversation_history.append({
                'action_type': campaign_action_name,
                'role': 'copilot',
                'content': formatted_response,
                'raw_content': raw_response,
                'timestamp': datetime.now()
                })

            return {
                'action_type': campaign_action_name,
                'message': formatted_response,
                'raw_message': raw_response,
                'sql_queries': [
                    elem['sql_list']
                    for elem in self.agent.get_query_history()[-total_steps:]
                    if 'sql_list' in elem
                    ]
                }

        except Exception as e:
            logger.exception("Error processing request")
            error_response = {
                'message': (
                    f"❌ Error processing request: {str(e)}\n\n"
                    "Please try rephrasing your question or check your database connection."
                ),
                'type': 'error',
                'error': str(e)
                }
            self.conversation_history.append({
                'role': 'copilot',
                'content': error_response,
                'timestamp': datetime.now()
                })
            return error_response

    def get_conversation_history(self) -> List[Dict]:
        """Get full conversation history"""
        return self.conversation_history

    def get_query_history(self) -> List[Dict]:
        """Get history of all queries executed by the agent"""
        return self.agent.get_query_history()


def run_interactive(copilot: CampaignCoPilot):
    """Interactive chat mode"""
    print("\n" + "=" * 80)
    print("Campaign Co-Pilot ready! Ask me anything...")
    print("Type 'exit' to quit")
    print("=" * 80 + "\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ['exit', 'quit']:
            break

        response = copilot.chat(user_input, question_only=True)
        print(f"\n🤖 Co-Pilot:\n{response['message']}\n")

        # Optionally show SQL queries
        if response.get('sql_queries'):
            print(f"📝 SQL Queries executed: {len(response['sql_queries'])}")


def run_campaign_action(copilot: CampaignCoPilot):
    # Choose mode for campaign action by name
    campaign_actions = [c['name'] for c in CAMPAIGN_REQUEST_MAP.values()]

    while True:
        mode = input("  " +
                     "\n  ".join([f"({i + 1}) {name}" for i, name in enumerate(campaign_actions)]) +
                     "\n ask question - it will be parsed to possible pre-defined actions" +
                     "\n\n  exit/quit\n\nSelection:"
                     )

        if mode.lower() in ['exit', 'quit']:
            break

        campaign_action, query = None, None
        try:
            cid = int(mode) - 1
            if 0 < cid < len(campaign_actions):
                campaign_action = campaign_actions[cid]
                query = campaign_actions[cid].split(':')[1] # assumption on name
        except ValueError:
            campaign_action = 'general_query'
            query = mode

        response = copilot.chat(query)
        print(f"\n🤖 Co-Pilot:\n{response['message']}\n")

        # Optionally show SQL queries
        if response.get('sql_queries'):
            print(f"📝 SQL Queries executed: {len(response['sql_queries'])}")


def run_analysis(copilot: CampaignCoPilot):
    """Run predefined campaign analyses"""
    print("\n" + "=" * 80)
    print("📊 RUNNING COMPREHENSIVE CAMPAIGN ANALYSIS")
    print("=" * 80 + "\n")

    analyses = [
        ("Analyze performance", "📈 Performance Analysis"),
        ("Who should I contact?", "🎯 Contact Recommendations"),
        ("Optimize strategy", "🚀 Strategy Optimization")
        ]

    report = {}
    for query, title in analyses:
        # print(f"\n{title}")
        # print("-" * 40)
        response = copilot.chat(query)
        report[query] = response
        print(response['message'])

    return report


if __name__ == "__main__":
    print("=" * 80)
    print("🤖 CAMPAIGN CO-PILOT - POWERED BY SNOW LEOPARD")
    print("=" * 80 + "\n")

    try:
        copilot = CampaignCoPilot(
            datafile_id=SNOWLEOPARD_DATAFILE_ID,
            api_key=SNOWLEOPARD_API_KEY,
            openai_api_key=OPENAI_API_KEY,
            data_only=False,
            use_gpt_formatting=True
            )

        # Choose mode
        mode = input("\nChoose mode:\n  (1) Interactive Chat\n  (2) Run Performance Analysis\n  (3) Run Campaign Analysis\n\nSelection: ")

        if mode == "3":
            run_campaign_action(copilot)
        elif mode == "2":
            run_analysis(copilot)
        else:
            run_interactive(copilot)
        print("\n" + "=" * 80)

    except Exception as e:
        logger.exception('Failed to initialize Campaign Co-Pilot')
        print("\n❌ Error: Make sure you have set SNOWLEOPARD_API_KEY and OPENAI_API_KEY environment variables")
        print("Set them in your .env file or export them in your shell")
