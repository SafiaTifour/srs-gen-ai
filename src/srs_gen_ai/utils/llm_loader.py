import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from crewai import LLM


class LLMLoader:
    """A loader class to initialize and return a configured LLM instance."""

    def __init__(self, config_file: str = "../../../config/llm_config.yaml"):
        load_dotenv()
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise EnvironmentError("GROQ_API_KEY not found in environment variables.")

        self._load_config(config_file)

    def _load_config(self, config_file: str):
        """Load LLM configuration from a YAML file."""
        config_path = Path(__file__).resolve().parent / config_file
        if not config_path.exists():
            raise FileNotFoundError(f"LLM configuration file not found: {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        llm_config = config.get("llm", {})
        self.model = llm_config["model"] 
        self.temperature = llm_config.get("temperature", 0.7)
        self.stream = llm_config.get("stream", False)

    def get_llm(self) -> LLM:
        """Returns a configured LLM instance."""
        return LLM(
            model=self.model,
            temperature=self.temperature,
            api_key=self.api_key,
            stream=self.stream
        )


if __name__ == "__main__":
    loader = LLMLoader()
    llm = loader.get_llm()

    response = llm.call(
        "Analyze the following messages and return the name, age, and breed. "
        "Meet Kona! She is 3 years old and is a black german shepherd."
    )
    print("\nResponse:", response)
