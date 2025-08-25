from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent
from langchain_core.language_models import BaseChatModel
from pydantic import Field

class DoctorAgent(BaseAgent):
    """Doctor agent that provides medical advice and interacts with patient agents."""
    
    specialization: str = Field(default="General Practitioner", description="Medical specialization of the doctor")
    experience_years: int = Field(default=10, description="Years of experience")
    
    def initialize(self):
        """Initialize the doctor agent with specialized system prompt."""
        self.system_prompt = f"You are Dr. {self.name}, a {self.specialization} with {self.experience_years} years of experience. Provide concise medical advice based on patient data. Be clear, compassionate, and prioritize by severity."
    
    def analyze_patient_data(self, patient_data: Dict[str, Any]) -> str:
        """Analyze patient data and provide initial assessment."""
        patient_info = f"Assess patient: {patient_data.get('name', 'Unknown')}, {patient_data.get('age', 'Unknown')}yo {patient_data.get('gender', 'Unknown')}. Vitals: {patient_data.get('vital_signs', 'N/A')}. Symptoms: {patient_data.get('symptoms', 'None')}. History: {patient_data.get('medical_history', 'None')}. Meds: {patient_data.get('medications', 'None')}."
        
        return self.process_input(patient_info)
    
    def consult_with_specialist(self, specialist_agent: BaseAgent, patient_data: Dict[str, Any], question: str) -> str:
        """Consult with a specialist agent about a patient case."""
        consultation_request = f"Specialist consult for {patient_data.get('name', 'Unknown')}, {patient_data.get('age', 'Unknown')}yo {patient_data.get('gender', 'Unknown')}. Vitals: {patient_data.get('vital_signs', 'N/A')}. Symptoms: {patient_data.get('symptoms', 'None')}. History: {patient_data.get('medical_history', 'None')}. Meds: {patient_data.get('medications', 'None')}. Question: {question}"
        
        specialist_response = specialist_agent.process_input(consultation_request)
        
        # Record the consultation in memory
        self.memory.append({"role": "system", "content": f"Consultation with {specialist_agent.name}: {specialist_response}"})
        
        return specialist_response
    
    def create_treatment_plan(self, patient_data: Dict[str, Any], diagnosis: str) -> str:
        """Create a treatment plan based on diagnosis and patient data."""
        treatment_request = f"""
        Based on the following patient information and diagnosis, please create a comprehensive treatment plan:
        
        Patient Information:
        - Name: {patient_data.get('name', 'Unknown')}
        - Age: {patient_data.get('age', 'Unknown')}
        - Gender: {patient_data.get('gender', 'Unknown')}
        - Vital Signs: {patient_data.get('vital_signs', 'Not available')}
        - Medical History: {patient_data.get('medical_history', 'None available')}
        - Current Medications: {patient_data.get('medications', 'None reported')}
        - Allergies: {patient_data.get('allergies', 'None reported')}
        
        Diagnosis: {diagnosis}
        
        Please include:
        1. Recommended medications and dosages
        2. Lifestyle modifications
        3. Follow-up schedule
        4. Warning signs to watch for
        5. Referrals to specialists if necessary
        """
        
        return self.process_input(treatment_request)