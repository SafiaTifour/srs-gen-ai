import os
from dotenv import load_dotenv
from groq import Groq
from config_loader import ConfigLoader

class ModelLoader:
    def __init__(self, config_loader: ConfigLoader):
        self.config_loader = config_loader
        self.model = None
        self.model_name = None
        # Load environment variables
        load_dotenv()

    def load_model(self):
        """Load the Groq model based on configuration"""
        try:
            # Get API key from environment variables
            api_key = os.getenv('GROQ_API_KEY')
            if not api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables")
            
            # Get model name from config
            self.model_name = self.config_loader.get_model_name()
            
            # Initialize Groq client
            self.model = Groq(api_key=api_key)
            
            print(f"Successfully loaded Groq model: {self.model_name}")
            
        except Exception as e:
            raise Exception(f"Error loading model: {str(e)}")

    def get_model(self):
        """Get the loaded model, loading it if not already loaded"""
        if self.model is None:
            self.load_model()
        return self.model

    def generate_response(self, prompt, max_tokens=1000, temperature=0.7):
        """Generate a response using the loaded model"""
        if self.model is None:
            self.load_model()
        
        try:
            response = self.model.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")


# Example usage
if __name__ == "__main__":
    try:
        # Initialize components
        config_loader = ConfigLoader()
        model_loader = ModelLoader(config_loader)
        
        # Load and get model
        model = model_loader.get_model()
        
        # Test the model
        response = model_loader.generate_response("Hello, how are you?")
        print(f"Model response: {response}")
        
    except Exception as e:
        print(f"Error: {str(e)}")