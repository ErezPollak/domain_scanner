import os
import sys
import warnings

from domain_scanner.crew import DomainScanner

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def get_target_domain():
    return os.getenv("TARGET_DOMAIN", "example.com")


async def run():
    """
    Run the crew.
    """
    inputs = {"domain": get_target_domain()}

    try:
        await DomainScanner().crew().akickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


async def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {"domain": get_target_domain()}
    try:
        await (
            DomainScanner()
            .crew()
            .atrain(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


async def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        await DomainScanner().crew().areplay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


async def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {"domain": get_target_domain()}

    try:
        await (
            DomainScanner()
            .crew()
            .atest(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
        )

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


async def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception(
            "No trigger payload provided. Please provide JSON payload as argument."
        )

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "domain": "example.com",
    }

    try:
        result = await DomainScanner().crew().akickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
