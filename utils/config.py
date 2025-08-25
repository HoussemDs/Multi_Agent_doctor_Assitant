import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional
import threading

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration utility for the Agentic Doctor system."""
    
    # Thread-local storage to track which API key each thread is using
    _thread_local = threading.local()
    # Lock for synchronizing access to the API key counter
    _api_key_lock = threading.Lock()
    # Counter to alternate between API keys
    _api_key_counter = 0
    
    @staticmethod
    def get_groq_api_key() -> str:
        """Get the Groq API key from environment variables, alternating between available keys."""
        # Try to get API key from thread-local storage first
        if hasattr(Config._thread_local, 'api_key'):
            return Config._thread_local.api_key
        
        # Alternate between API keys
        with Config._api_key_lock:
            key_num = Config._api_key_counter % 2 + 1  # Alternate between 1 and 2
            Config._api_key_counter += 1
        
        # Get the API key from environment variables
        api_key = os.getenv(f"GROQ_API_KEY_{key_num}")
        if not api_key:
            # Fall back to the other key if one is missing
            other_key_num = 2 if key_num == 1 else 1
            api_key = os.getenv(f"GROQ_API_KEY_{other_key_num}")
            if not api_key:
                raise ValueError("No GROQ API keys found in environment variables. Please check your .env file.")
        
        # Store the API key in thread-local storage
        Config._thread_local.api_key = api_key
        return api_key
    
    @staticmethod
    def get_model_name() -> str:
        """Get the model name from environment variables."""
        model_name = os.getenv("MODEL_NAME", "llama3-70b-8192")
        return model_name
    
    @staticmethod
    def is_debug_mode() -> bool:
        """Check if debug mode is enabled."""
        debug = os.getenv("DEBUG", "False")
        return debug.lower() in ("true", "1", "t")
    
    @staticmethod
    def get_all_config() -> Dict[str, Any]:
        """Get all configuration values as a dictionary."""
        return {
            "groq_api_key": Config.get_groq_api_key(),
            "model_name": Config.get_model_name(),
            "debug": Config.is_debug_mode()
        }