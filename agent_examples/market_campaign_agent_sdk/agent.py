import logging
import os
from datetime import datetime
from pandas import DataFrame
from typing import List, Optional

from snowleopard import SnowLeopardPlaygroundClient, models

# Create logger
logLevel = logging.WARNING
logger = logging.getLogger("agent")
logger.setLevel(logLevel)
console = logging.StreamHandler()
console.setLevel(logLevel)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console.setFormatter(formatter)
logger.addHandler(console)


class Agent:
    """
    Base agent class that handles SnowLeopard SQL Query SDK interactions

    This class provides core functionality for:
    - Connecting to SnowLeopard API
    - Asking natural language questions
    - Retrieving and formatting data
    - Maintaining query history

    Usage:
        agent = Agent(datafile_id="your_datafile_id")
        result = agent.ask_question("What are the total sales?")
    """

    DEFAULT_MAX_ROWS = 20

    def __init__(
        self,
        datafile_id: str,
        api_key: Optional[str] = None,
        data_only: bool = False,
        max_display_rows: int = DEFAULT_MAX_ROWS,
        ):
        """
        Initialize agent with SnowLeopard client SDK

        Args:
            datafile_id: Database ID for SnowLeopard
            api_key: Optional SnowLeopard API key (if not provided, reads from env)
            data_only: If True, only retrieve data without natural language response
            max_display_rows: Maximum rows to display in results
        """
        try:
            # Initialize SnowLeopard client
            api_key = api_key or os.environ.get('SNOWLEOPARD_API_KEY')
            if not api_key:
                raise ValueError(
                    "SNOWLEOPARD_API_KEY not found. "
                    "Please provide api_key parameter or set environment variable."
                    )

            self.sl_client = SnowLeopardPlaygroundClient(api_key=api_key)
            self.datafile_id = datafile_id
            self.query_history = []
            self.data_only = data_only
            self.dataset_info = None
            self.max_display_rows = max_display_rows

            logger.info("🔧 Initializing Agent...")
            self._initialize_dataset_info()

        except ImportError:
            raise ImportError(
                "Required clients not found. "
                "Please install: pip install snowleopard-client"
                )
        except Exception as e:
            raise Exception(f"Failed to initialize Agent: {e}")

    def _initialize_dataset_info(self):
        """Get basic dataset information for context"""
        try:
            dataset_info = self.ask_question("Summarize the data.", data_only=True)
            if dataset_info and len(dataset_info) > 0:
                self.dataset_info = dataset_info[0].iat[0, 0]
                logger.debug(f"📊 Dataset: {self.dataset_info}")
                logger.info("✅ Agent initialized with dataset information")
            else:
                logger.warning("⚠️ No dataset info returned")
                self.dataset_info = "Unknown dataset"
        except Exception as e:
            logger.exception(f"⚠️ Could not initialize dataset info: {e}")
            self.dataset_info = "Unknown dataset"

    def ask_question(
        self,
        question: str,
        data_only: Optional[bool] = None
        ) -> List[DataFrame]:
        """
        Use SnowLeopard SDK to get data with streaming support

        Args:
            question: Natural language question
            data_only: Override instance data_only setting if provided
        Returns:
            List of DataFrames containing query results
        """
        result = None
        response_status, sql_list = None, None

        if data_only is None:
            data_only = self.data_only

        try:
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
                        sql_list = [data.query for data in reply[1].data] # assumption that there is at least 2 replies upon 'SUCCESS'
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
                return self._extract_data_from_result(
                    result.llmResponse if isinstance(result, models.ResponseLLMResult)
                    else result.data
                    )
            else:
                logger.error(
                    f"Failed to answer question: {question}, "
                    f"status: {result.responseStatus}"
                    )
                self.query_history.append({
                    'timestamp': datetime.now(),
                    'question': question,
                    'type': 'natural_language',
                    'response_status': response_status,
                    'response_body': result.data,
                    })
                return []

        except Exception as e:
            logger.exception(f"Error in ask_question: {e}")
            return []

    def _extract_data_from_result(
        self,
        result_data_list,
        use_pandas: bool = True
        ) -> List[DataFrame]:
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

        result_data_list = (
            result_data_list if isinstance(result_data_list, list)
            else [result_data_list]
        )

        records = []
        for data in result_data_list:
            if hasattr(data, "query"):
                # Log the query for transparency
                logger.debug(
                    f"   📝 SQL Generated&Executed {data.schemaId}({data.schemaType}) "
                    f"[{len(data.rows)} rows]: {data.query}"
                    )

            if isinstance(data, str):
                records.append(data)
            elif isinstance(data, models.SchemaData):
                records.append(DataFrame(data.rows) if use_pandas else data.rows)
            elif isinstance(data, dict) and 'complete_answer' in data:
                records.append(data['complete_answer'])
            else:
                records.append(data)

        return records

    def format_result(self, result: list) -> str:
        """
        Format SnowLeopard result for display

        Args:
            result: List of DataFrames or strings to format
        Returns:
            Formatted string representation
        """
        if not result:
            return "No data available"

        formatted_result = []
        for dataset in result:
            if isinstance(dataset, dict) and 'complete_answer' in dataset:
                formatted_result.append(str(dataset['complete_answer']))
            elif isinstance(dataset, DataFrame) and not dataset.empty:
                data = dataset.head(self.max_display_rows) if self.max_display_rows > 0 else dataset
                formatted_result.append(
                    data.to_string(index=False)
                    )
            elif isinstance(dataset, str) and dataset:
                formatted_result.append(dataset)

        return '\n\n'.join(formatted_result) if formatted_result else "No data available"

    def get_query_history(self) -> List[dict]:
        """Get history of all queries executed"""
        return self.query_history

    def get_dataset_info(self) -> str:
        """Get dataset information"""
        return self.dataset_info or "Unknown dataset"
