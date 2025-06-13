from typing import Annotated

from pydantic import Field

from inspect_ai.tool import tool
from inspect_ai.util import store


@tool
def submit_answer(
    answer: Annotated[
        int, Field(description="The numeric answer to the current sample")
    ],
) -> int:
    """The agent calls this once it is confident.

    Args:
        answer: The numeric answer to the current sample.

    Returns:
        The submitted answer.
    """
    store().set("submitted_answer", answer)
    return answer
