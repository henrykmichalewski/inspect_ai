from typing import Annotated

from pydantic import Field

from inspect_ai.tool import tool
from inspect_ai.util import store


@tool
def submit_answer(
    answer: Annotated[
        str, Field(description="The Python function string for the answer")
    ],
) -> str:
    """The agent calls this once it is confident.

    Args:
        answer: The Python function string for the answer.

    Returns:
        The submitted answer.
    """
    store().set("submitted_answer", answer)
    return answer
