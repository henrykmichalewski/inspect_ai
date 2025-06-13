from typing import Annotated
from pydantic import Field
from inspect_ai.tool import tool


@tool
def submit_answer(
    answer: Annotated[int, Field(description="The numeric answer to the current sample")]
) -> int:
    """The agent calls this once it is confident. Returns the same integer so the framework can log it."""
    return answer
