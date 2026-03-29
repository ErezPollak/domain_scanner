from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew

# Import all custom tools
from domain_scanner.tools.domain_tools import (
    dns_lookup,
    fetch_website,
    security_headers,
    extract_metadata,
    detect_tech_stack,
    discover_subdomains,
    analyze_ssl_certificate,
    crawl_website,
    measure_performance,
    analyze_sitemap,
    analyze_robots,
    scan_ports,
)


@CrewBase
class DomainScanner:
    """AI Crew for analyzing and scanning a web domain"""

    agents: list[Agent]
    tasks: list[Task]

    # -------------------------------------------------
    # Agents
    # -------------------------------------------------

    @agent
    def recon_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["recon_agent"],
            tools=[analyze_robots, dns_lookup, discover_subdomains, scan_ports],
            verbose=True,
            cache=True,
        )

    @agent
    def tech_stack_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["tech_stack_agent"],
            tools=[detect_tech_stack],
            verbose=True,
            cache=True,
        )

    @agent
    def infrastructure_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["infrastructure_agent"],
            tools=[dns_lookup, analyze_ssl_certificate],
            verbose=True,
            cache=True,
        )

    @agent
    def security_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["security_agent"],
            tools=[security_headers, analyze_ssl_certificate],
            verbose=True,
            cache=True,
        )

    @agent
    def performance_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["performance_agent"],
            tools=[measure_performance],
            verbose=True,
            cache=True,
        )

    @agent
    def website_content_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["website_content_agent"],
            tools=[
                analyze_robots,
                analyze_sitemap,
                fetch_website,
                extract_metadata,
                crawl_website,
            ],
            verbose=True,
            cache=True,
        )

    @agent
    def ux_ui_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["ux_ui_agent"],
            tools=[analyze_sitemap, fetch_website, extract_metadata, crawl_website],
            verbose=True,
            cache=True,
        )

    @agent
    def trust_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["trust_agent"],
            verbose=True,
            cache=True,
        )

    @agent
    def report_agent(self) -> Agent:
        return Agent(config=self.agents_config["report_agent"], cache=True)

    # -------------------------------------------------
    # Tasks
    # -------------------------------------------------

    @task
    def reconnaissance_task(self) -> Task:
        return Task(config=self.tasks_config["reconnaissance_task"])

    @task
    def tech_stack_analysis_task(self) -> Task:
        return Task(config=self.tasks_config["tech_stack_analysis_task"])

    @task
    def infrastructure_analysis_task(self) -> Task:
        return Task(config=self.tasks_config["infrastructure_analysis_task"])

    @task
    def security_analysis_task(self) -> Task:
        return Task(config=self.tasks_config["security_analysis_task"])

    @task
    def performance_analysis_task(self) -> Task:
        return Task(config=self.tasks_config["performance_analysis_task"])

    @task
    def website_content_analysis_task(self) -> Task:
        return Task(config=self.tasks_config["website_content_analysis_task"])

    @task
    def ux_ui_analysis_task(self) -> Task:
        return Task(config=self.tasks_config["ux_ui_analysis_task"])

    @task
    def trust_evaluation_task(self) -> Task:
        return Task(config=self.tasks_config["trust_evaluation_task"])

    @task
    def report_generation_task(self) -> Task:
        return Task(config=self.tasks_config["report_generation_task"])

    # -------------------------------------------------
    # Crew
    # -------------------------------------------------

    @crew
    def crew(self) -> Crew:
        """Creates the DomainScanner crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            cache=True,
        )
