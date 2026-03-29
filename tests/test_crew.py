from domain_scanner.crew import DomainScanner


def test_crew_instantiation():
    """Test that the crew initializes correctly and binds agents/tasks."""
    crew_instance = DomainScanner()

    # Generate the crew
    crew = crew_instance.crew()

    # Basic sanity checks ensuring config loads without crashing
    assert crew is not None
    assert len(crew.agents) == 9, f"Expected 9 agents, found {len(crew.agents)}"
    assert len(crew.tasks) == 9, f"Expected 9 tasks, found {len(crew.tasks)}"

    # Check that specific key agents exist
    agent_roles = [agent.role for agent in crew.agents]
    assert any("Cybersecurity Reconnaissance" in role for role in agent_roles)
    assert any("Data Privacy & Trust" in role for role in agent_roles)
