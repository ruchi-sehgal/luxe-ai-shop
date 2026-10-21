import pytest
from pydantic_evals import Case, Dataset

from backend.chatbot.agent import agent

cases = [
    Case(
        name="basic colour and price",
        inputs="white shirt under 1000",
        expected_output={"keyword": "shirt", "colour": "white", "max_price": 1000.0},
    ),
    Case(
        name="category not confused with item type",
        inputs="shirt for men",
        expected_output={"keyword": "shirt", "category": "men"},
    ),
    Case(
        name="jeans keyword extracted",
        inputs="blue jeans under 2000",
        expected_output={"keyword": "jeans", "colour": "blue", "max_price": 2000.0},
    ),
    Case(
        name="no fabricated popularity claims",
        inputs="top 3 most popular items",
        expected_output={"keyword": None, "category": None},
    ),
]

dataset = Dataset(name="chatbot_filter_extraction", cases=cases)


async def run_filter(inputs: str) -> dict:
    result = await agent.run(inputs)
    return result.output.model_dump(exclude={"reply", "limit"})


@pytest.mark.asyncio
async def test_chatbot_golden_set():
    report = await dataset.evaluate(run_filter)
    for case in report.cases:
        expected = cases[[c.name for c in cases].index(case.name)].expected_output
        for key, value in expected.items():
            assert case.output.get(key) == value, (
                f"{case.name}: expected {key}={value!r}, got {case.output.get(key)!r}"
            )