from inspect_ai import Task, task
from inspect_ai.dataset import Sample

# Attempt to import solver & scorer from the current package first (installed mode)
try:
    from .agent import frontiermath_agent
    from .scorer import verification_code_scorer
except ImportError:  # Fallback when running the file directly
    from agent import frontiermath_agent
    from scorer import verification_code_scorer

# -----------------------------------------------------------------------------
#  Problem definitions
# -----------------------------------------------------------------------------
# Each problem is defined by a plain‑English question and its verified answer.
# If you would like to add or remove problems, simply edit this list.
# -----------------------------------------------------------------------------
PROBLEMS: list[tuple[str, int]] = [
    (
        "Find the sum of all multiples of 4 or 7 below 2000.",
        712_717,
    ),
    (
        "Find the sum of the odd Fibonacci numbers not exceeding ten million.",
        19_544_084,
    ),
    (
        "What is the largest prime factor of 13195?",
        29,
    ),
    (
        "Find the difference between the square of the sum and the sum of the squares of the first 100 natural numbers.",
        25_164_150,
    ),
]


def _make_sample(question: str, answer: int) -> Sample:
    """Factory that wraps a question/answer pair in a :class:`~inspect_ai.dataset.Sample`."""
    return Sample(
        input=question,
        metadata={
            "answer_type": "Python int",
            "verification_code": f"def verify(a):\n    return a == {answer}",
        },
    )


@task
def project_euler_like():
    """A task bundle of Project‑Euler‑style warm‑up problems.

    The task re‑uses the ``frontiermath_agent`` solver and the
    ``verification_code_scorer`` exactly as the original *project_euler*
    task, but exposes a fresh set of numeric puzzles so you can benchmark
    agents on slightly different maths while keeping the same evaluation
    plumbing.
    """

    return Task(
        dataset=[_make_sample(q, a) for q, a in PROBLEMS],
        solver=[frontiermath_agent()],
        scorer=verification_code_scorer(),
    )
