import json
import logging
from abc import ABC, abstractmethod



from utilities.error_handler import ErrorHandler
from models.ProbabilityEstimationModelTwoEvents import BasePromptingModelInContext
class LLMClientFactory:
    """Factory class to create instances of various LLM (Large Language Models) clients."""

    def __init__(self):
        """
        Initializes the LLMClientFactory with available LLM client types.

        Dynamically imports client classes from a module dedicated to LLM integrations.
        """
        from llm_clients.openai_client import OpenAIClient
        from llm_clients.deepseek_client import DeepSeekClient
        from llm_clients.gemini_client import GeminiClient
        self.clients = {
            "openai": OpenAIClient,
            "deepseek": DeepSeekClient,
            "gemini": GeminiClient
        }

    def get_client(self, client_name,):
        """
        Retrieves an instance of a specified LLM client.

        Args:
            client_name (str): The name of the client to retrieve.

        Returns:
            An instance of the requested LLM client.

        Raises:
            ErrorHandler: Handles the error if an unknown client type is requested, defaulting to the first client.
        """
        if client_name not in self.clients:
            ErrorHandler().handle_error(
                f"Got unknown LLM Client! Using first one ({self.clients[0]}",
                "llm-client-factory", exit_on_failure=False)
            return self.clients[0]()

        return self.clients[client_name]()


class LLMClient(ABC):
    """Abstract base class for LLM clients to analyze data based on a specified model."""

    def __init__(self, model_name):
        """
        Initializes an LLMClient with a specific model.

        Args:
            model_name (str): The name of the model to be used for analysis.
        """
        self.model_name = model_name
        self.logger = logging.getLogger(__name__)


    @abstractmethod
    def estimate_probability_two_events_in_context(self, event1, event2, template) -> BasePromptingModelInContext:
        pass