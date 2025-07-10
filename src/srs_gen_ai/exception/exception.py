class ApplicationError(Exception):
    """Base class for all application-specific exceptions."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class ConfigurationError(ApplicationError):
    """Raised when configuration is missing or incorrect."""
    pass

class DataValidationError(ApplicationError):
    """Raised when data fails validation checks."""
    pass

class ExternalServiceError(ApplicationError):
    """Raised when an external API or service fails."""
    pass


# Testing
if __name__ == "__main__":
    try:
        raise ConfigurationError("Missing API key in config file.")
    except ApplicationError as e:
        print(f"Caught ApplicationError: {e.__class__.__name__} - {e.message}")
