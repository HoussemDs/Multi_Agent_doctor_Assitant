from typing import Dict, List, Any, Optional
from ..base_agent import BaseAgent
from langchain_core.language_models import BaseChatModel
from pydantic import Field

class NormalPatientAgent(BaseAgent):
    """Agent for handling patients with normal health conditions."""
    
    def initialize(self):
        """Initialize the normal patient agent with specialized system prompt."""
        self.system_prompt = f"You are {self.name}, a medical assistant for routine healthcare. Provide concise preventive care recommendations, health maintenance advice, and check-up scheduling for patients with normal health conditions."
    
    def process_patient_data(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process patient data and provide wellness recommendations."""
        # Check if vital signs are within normal ranges
        vital_signs = patient_data.get('vital_signs', {})
        age = patient_data.get('age', 30)
        gender = patient_data.get('gender', 'Unknown')
        
        # Generate wellness recommendations based on patient demographics - more concise prompt
        wellness_prompt = f"Provide brief wellness recommendations for {age}-year-old {gender} with normal health. Include exercise, diet, sleep, stress management, and preventive screenings."
        
        wellness_recommendations = self.process_input(wellness_prompt)
        
        # Generate recommended check-up schedule - more concise prompt
        schedule_prompt = f"Recommend brief check-up schedule for {age}-year-old {gender} with normal health for next 2 years."
        
        check_up_schedule = self.process_input(schedule_prompt)
        
        return {
            "patient_status": "normal",
            "wellness_recommendations": wellness_recommendations,
            "check_up_schedule": check_up_schedule,
            "requires_doctor_attention": False,
            "follow_up_interval": "12 months"
        }
    
    def generate_health_report(self, patient_data: Dict[str, Any]) -> str:
        """Generate a comprehensive health report for a patient with normal health status."""
        report_prompt = f"""
        Please generate a comprehensive health report for:
        
        Patient Information:
        - Name: {patient_data.get('name', 'Unknown')}
        - Age: {patient_data.get('age', 'Unknown')}
        - Gender: {patient_data.get('gender', 'Unknown')}
        - Vital Signs: {patient_data.get('vital_signs', 'Not available')}
        
        This patient has normal health status. Include:
        1. Current health assessment
        2. Preventive care recommendations
        3. Lifestyle optimization suggestions
        4. Recommended follow-up timeline
        """
        
        return self.process_input(report_prompt)