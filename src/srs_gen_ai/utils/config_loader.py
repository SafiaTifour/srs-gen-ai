import yaml
from pathlib import Path


class ConfigLoader:
    def __init__(self, config_path="config/config.yaml"):
        self.config_path = config_path
        self.config = None
        self._load_config()

    def _load_config(self):
        """Load configuration from YAML file"""
        try:
            config_file = Path(self.config_path)
            if not config_file.exists():
                raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
            
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        except Exception as e:
            raise Exception(f"Error loading configuration: {str(e)}")

    def get_config(self):
        """Get the full configuration"""
        if not self.config:
            raise Exception("Configuration not loaded")
        return self.config

    def get_llm_config(self):
        """Get LLM configuration"""
        if not self.config:
            raise Exception("Configuration not loaded")
        
        return self.config.get('llm', {})

    def get_groq_config(self):
        """Get Groq-specific configuration"""
        llm_config = self.get_llm_config()
        return llm_config.get('groq', {})

    def get_model_name(self):
        """Get the model name from Groq config"""
        groq_config = self.get_groq_config()
        return groq_config.get('model name', 'deepseek-r1-distill-llama-70b')

    def get_provider(self):
        """Get the provider from Groq config"""
        groq_config = self.get_groq_config()
        return groq_config.get('provider', 'groq')