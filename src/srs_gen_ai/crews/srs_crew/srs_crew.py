import yaml
from pathlib import Path
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from srs_gen_ai.utils.llm_loader import LLMLoader


def load_yaml(file_path: str):
    base_path = Path(__file__).resolve().parent
    yaml_path = base_path / file_path
    if not yaml_path.exists():
        raise FileNotFoundError(f"YAML file not found: {yaml_path}")
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@CrewBase
class SRSCrew:
    """SRS Multi-Agent Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        # Load YAML at instance level
        self.llm = LLMLoader().get_llm()
        self.agents_config = load_yaml("config/agents.yaml")
        self.tasks_config = load_yaml("config/tasks.yaml")


    # ------------------------
    # AGENTS
    # ------------------------
        
    @agent
    def requirement_extractor(self) -> Agent:
        return Agent(config=self.agents_config["requirement_extractor"], llm=self.llm)

    @agent
    def classifier(self) -> Agent:
        return Agent(config=self.agents_config["classifier"], llm=self.llm)

    @agent
    def srs_writer(self) -> Agent:
        return Agent(config=self.agents_config["srs_writer"], llm=self.llm)

    @agent
    def consistency_checker(self) -> Agent:
        return Agent(config=self.agents_config["consistency_checker"], llm=self.llm)

    @agent
    def latex_generator(self) -> Agent:
        return Agent(config=self.agents_config["latex_generator"], llm=self.llm)

    # ------------------------
    # TASKS
    # ------------------------
    @task
    def extract_requirements(self) -> Task:
        return Task(config=self.tasks_config["extract_requirements"])

    @task
    def classify_requirements(self) -> Task:
        return Task(config=self.tasks_config["classify_requirements"])

    @task
    def write_srs_document(self) -> Task:
        return Task(config=self.tasks_config["write_srs_document"])

    @task
    def validate_consistency(self) -> Task:
        return Task(config=self.tasks_config["validate_consistency"])

    @task
    def generate_latex_srs(self) -> Task:
        return Task(config=self.tasks_config["generate_latex_srs"])

    # ------------------------
    # CREW
    # ------------------------
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )