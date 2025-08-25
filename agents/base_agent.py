from typing import Dict, List, Any, Optional
import time
import random

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from utils.config import Config

class BaseAgent(BaseModel):
    """Base agent class for the Agentic Doctor system."""
    
    name: str = Field(..., description="Name of the agent")
    role: str = Field(..., description="Role of the agent in the system")
    llm: BaseChatModel = Field(..., description="Language model for the agent")
    system_prompt: str = Field(..., description="System prompt for the agent")
    memory: List[Dict[str, Any]] = Field(default_factory=list, description="Memory of the agent's conversations")
    
    def __init__(self, **data):
        super().__init__(**data)
        self.initialize()
    
    def initialize(self):
        """Initialize the agent with any necessary setup."""
        pass
    
    def get_prompt(self) -> ChatPromptTemplate:
        """Get the prompt template for the agent."""
        return ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{input}")
        ])
    
    def process_input(self, input_text: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Process input and generate a response with rate limiting and error handling."""
        messages = [SystemMessage(content=self.system_prompt)]
        
        # Add memory context if available
        if self.memory:
            for message in self.memory:
                if message["role"] == "human":
                    messages.append(HumanMessage(content=message["content"]))
                elif message["role"] == "ai":
                    messages.append(AIMessage(content=message["content"]))
        
        # Add current input
        messages.append(HumanMessage(content=input_text))
        
        # Add rate limiting with exponential backoff
        max_retries = 5
        base_delay = 1  # Base delay in seconds
        
        for attempt in range(max_retries):
            try:
                # Add a small random delay before API call to avoid simultaneous requests
                time.sleep(random.uniform(0.1, 0.5))
                
                # Generate response
                response = self.llm.invoke(messages)
                
                # Update memory
                self.memory.append({"role": "human", "content": input_text})
                self.memory.append({"role": "ai", "content": response.content})
                
                return response.content
                
            except Exception as e:
                # Check if this is the last retry
                if attempt == max_retries - 1:
                    error_msg = f"Error after {max_retries} attempts: {str(e)}"
                    print(f"[{self.name}] {error_msg}")
                    
                    # Return a fallback response
                    fallback_response = f"I apologize, but I'm currently experiencing technical difficulties. {error_msg}"
                    self.memory.append({"role": "human", "content": input_text})
                    self.memory.append({"role": "ai", "content": fallback_response})
                    return fallback_response
                
                # Calculate delay with exponential backoff and jitter
                delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                print(f"[{self.name}] API call failed: {str(e)}. Retrying in {delay:.2f} seconds...")
                time.sleep(delay)
    
    def clear_memory(self):
        """Clear the agent's memory."""
        self.memory = []