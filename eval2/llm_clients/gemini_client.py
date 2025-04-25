import logging
import os
from dotenv import load_dotenv

from langchain.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.prompts import ChatPromptTemplate

from llm_clients.llm_client import LLMClient
from models.ProbabilityEstimationModelTwoEvents import BasePromptingModelInContext

from utilities.error_handler import ErrorHandler
from utilities.load_prompt import load_prompt

import google.generativeai as genai

load_dotenv()

class GeminiClient(LLMClient):
    """
    Client for interacting with Gemini language models (Google Generative AI).
    """

    def __init__(self):
        """
        Initializes the GeminiClient with API key and model.
        """
        super().__init__(os.getenv("gemini_model"))
        self.logger = logging.getLogger(__name__)
        self.model_name = os.getenv("gemini_model")
        genai.configure(api_key=os.getenv("gemini_api_key"))
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={
                "temperature": float(os.getenv("temperature")),
            }
        )


    def estimate_probability_two_events_in_context(self, event1, event2, template):
        return self._generic_estimate(event1=event1, event2=event2, template=template, model=BasePromptingModelInContext)

    def _generic_estimate(self, event1, event2=None, template=None, model=None):
        """
        Generic method to estimate probabilities using Gemini.

        Args:
            event1 (str): First event description.
            event2 (str, optional): Second event description.
            template (str): Prompt template filename.
            model (BaseModel): Pydantic model class to parse output.

        Returns:
            model: Parsed output or None on failure.
        """
        pydantic_parser = PydanticOutputParser(pydantic_object=model)
        format_instructions = pydantic_parser.get_format_instructions()

        prompt = ChatPromptTemplate.from_template(load_prompt(template))
        messages = prompt.format_messages(
            event1=event1,
            event2=event2,
            format_instructions=format_instructions
        )
        # Gemini needs plain string input, so we flatten the messages
        prompt_text = "\n".join([m.content for m in messages])

        try:
            response = self.model.generate_content(prompt_text)
            output = response.text
            self.logger.info(f"Got response from Gemini: {output}")
            return pydantic_parser.parse(output)
        except OutputParserException as ex:
            self.logger.warning("Could not parse Gemini output as Pydantic model. Retrying...")
            ErrorHandler().handle_error(f"Failed to parse Gemini output {ex}", "_generic_estimate", exit_on_failure=False)
            try:
                response = self.model.generate_content(prompt_text)
                output = response.text
                return pydantic_parser.parse(output)
            except OutputParserException as ex:
                self.logger.warning("Parsing failed again. Returning None.")
                ErrorHandler().handle_error(f"Failed to parse Gemini output {ex}", "_generic_estimate", exit_on_failure=False)
                return None
