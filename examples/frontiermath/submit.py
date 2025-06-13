from typing import Annotated

from pydantic import Field

from inspect_ai.tool import tool
from inspect_ai.util import store


@tool
def submit_answer(
    answer: Annotated[
        str,
        Field(
            description=(
                "Source code for a Python function named `answer` that "
                "returns the solution"
            )
        ),
    ],
) -> str:
    """The agent calls this once it is confident.

    Args:
        answer: Source code of an ``answer`` function that returns the solution.

    Returns:
        The submitted function code.
    """
    store().set("submitted_answer", answer)
    return answer
