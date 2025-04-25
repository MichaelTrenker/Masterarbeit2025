from pydantic import BaseModel, Field,StrictFloat




class BasePromptingModelInContext(BaseModel):
    probabilityEstimation: StrictFloat = Field(
        description=(
            "A numerical probability (between 0 and 1) that event1 will occur, "
            "based on the provided context."
        ),
        ge=0.0,
        le=1.0
    )
    probabilityEstimationConditional: StrictFloat = Field(
        description=(
            "A numerical probability (between 0 and 1) that event1 will occur "
            "given that event2 has already occurred, based on the provided context."
        ),
        ge=0.0,
        le=1.0
    )
    llmConfidence: StrictFloat = Field(
        description=(
            "A measure of the Large Language Model's confidence in both probability estimates, "
            "ranging from 0.0 (no confidence) to 1.0 (complete certainty)."
        ),
        ge=0.0,
        le=1.0
    )







class ChainOfThoughtPromptingModel(BaseModel):
    """
    Represents a model for estimating probabilities using chain-of-thought prompting.

    Attributes:
        event1 (str): A detailed description of the first event.
        event2 (Optional[str]): A detailed description of the second event, if applicable.
        probabilityEstimation (Optional[float]): The estimated probability based on step-by-step reasoning.
        llmConfidence (float): The LLM's confidence level in its estimation.
        reasoningSteps (str): The step-by-step reasoning process provided by the LLM.
    """
    probabilityEstimation: float = Field(
        description="The estimated probability that event1 will happen, if there is also an event 2 provided then the probability that event1 will happen given event2 has happened."
    )
    llmConfidence: float = Field(
        description="The confidence level of the probability estimation, ranging from 0 (completely unsure) to 1 (completely certain)."
    )
    reasoningSteps: str = Field(
        description="The step-by-step reasoning process that led to the probability estimation. But please without bullet points. Just a plain text."
    )
 