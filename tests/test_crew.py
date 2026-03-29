from domain_scanner.crew import DomainScanner


def test_crew_instantiation():
    """Test that the crew initializes correctly and binds agents/tasks."""
    crew_instance = DomainScanner()

    # Generate the crew
    crew = crew_instance.crew()

    # Basic sanity checks ensuring config loads without crashing
    assert crew is not None
    assert len(crew.agents) > 0
    assert len(crew.tasks) > 0

    # Check that specific agents exist
    agent_roles = [agent.role for agent in crew.agents]
    # We can check for partial role strings or existence of roles
    assert (
        any("Reconnaissance Specialist" in role for role in agent_roles)
        or len(agent_roles) == 8
    )
