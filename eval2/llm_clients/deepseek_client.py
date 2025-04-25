import logging

from langchain.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from llm_clients.llm_client import LLMClient
from models.ProbabilityEstimationModelTwoEvents import BasePromptingModelInContext
from utilities.error_handler import ErrorHandler
from utilities.load_prompt import load_prompt
from dotenv import load_dotenv
import os

load_dotenv()

class DeepSeekClient(LLMClient):
    """
    Client for interacting with OpenAI's language models to analyze company data and news articles.
    """

    def __init__(self):
        """
        Initializes the OpenAIClient with configuration settings for OpenAI's model and establishes API access.

        Configurations include API keys and model settings as specified in the system's configuration.
        """
        super().__init__(os.getenv("openai_model"))
        self.logger = logging.getLogger(__name__)

        self.llm = ChatOpenAI(model=os.getenv("deepseek_model"),
                              openai_api_key=os.getenv("deepseek_api_key"),
                              temperature= float(os.getenv("temperature")),
                              base_url = "https://api.deepseek.com/v1")



    def estimate_probability_two_events_in_context(self, event1, event2, template):
        return self._generic_estimate(event1=event1, event2=event2, template=template, model=BasePromptingModelInContext)

    def _generic_estimate(self, event1, event2=None, template=None, model=None):
        """
        Generic method to estimate probabilities for different configurations of events and models.

        Args:
            event1 (str): Description of the first event.
            event2 (str, optional): Description of the second event. Defaults to None.
            template (str): The template string to use for the prompt.
            model (BaseModel): The Pydantic model class to parse the output into.

        Returns:
            model: Parsed probability estimation model.
        """
        pydantic_parser = PydanticOutputParser(pydantic_object=model)
        format_instructions = pydantic_parser.get_format_instructions()

        prompt = ChatPromptTemplate.from_template(load_prompt(template))
        messages = prompt.format_messages(
            event1=event1,
            event2=event2,
            format_instructions=format_instructions
        )

        output = self.llm.invoke(messages).content
        self.logger.info(f"Got response from llm: {output}")

        try:
            return pydantic_parser.parse(output)
        except OutputParserException as ex:
            self.logger.warning("Could not parse LLM output as Pydantic model. Retrying...")
            ErrorHandler().handle_error(f"Failed to parse LLM output {ex}", "_generic_estimate", exit_on_failure=False)
            try:
                output = self.llm.invoke(messages).content
                return pydantic_parser.parse(output)
            except OutputParserException as ex:
                self.logger.warning("Parsing failed again. Returning None.")
                ErrorHandler().handle_error(f"Failed to parse LLM output {ex}", "_generic_estimate", exit_on_failure=False)
                return None
