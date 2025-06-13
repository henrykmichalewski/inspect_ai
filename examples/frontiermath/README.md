# FrontierMath Scorer Example

This example demonstrates how to use a custom scorer that verifies a submitted
Python function. The agent provides a `python` tool for exploration and a
`submit_answer` tool used to submit a function named `answer`.

The `project_euler_like.py` task includes a few [Project Euler](https://projecteuler.net/)
style problems. Each problem contains Python code in `metadata['verification_code']`
that defines a `verify(answer)` function. The scorer runs this code inside the
Inspect sandbox to check whether the submitted answer is correct.

To run the evaluation:

```bash
inspect eval examples/frontiermath/project_euler_like.py --model <model-name>
```

Replace `<model-name>` with the ID of the model you want to evaluate. For example, to use Gemini 2.5 Pro, you might run:

```bash
inspect eval examples/frontiermath/project_euler_like.py --model google/gemini-2.5-pro-preview-06-05
```

To compute the mean success rate over 32 attempts and the probability that at least one of those 32 attempts is correct, run:

```bash
inspect eval examples/frontiermath/frontier_math.py \
  --model google/gemini-2.5-pro-preview-06-05 \
  --sandbox docker \
  --log-format=json \
  --epochs 32 \
  --epochs-reducer mean,pass_at_32
```

Here `--epochs 32` repeats each problem 32 times, and `--epochs-reducer` mean,`pass_at_32` generates both the average accuracy and the pass@32 metric for each problem.

**Note:** Ensure that the model ID (e.g., `google/gemini-2.5-pro-preview-06-05`) matches how Gemini 2.5 Pro is configured in your `inspect-ai` environment and that you have the necessary access and API keys set up.

The model will receive the problem statement along with instructions on how to use the
`python` and `submit_answer` tools.
