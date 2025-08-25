from typing import Dict, List, Any, Optional
from ..base_agent import BaseAgent
from langchain_core.language_models import BaseChatModel
from pydantic import Field

class SickPatientAgent(BaseAgent):
    """Agent for handling patients with general illness conditions."""
    
    def initialize(self):
        """Initialize the sick patient agent with specialized system prompt."""
        self.system_prompt = f"""
        You are {self.name}, a medical assistant specializing in general illness assessment and care coordination.
        Your role is to handle patients with various illness conditions, focusing on:
        
        1. Symptom assessment and triage
        2. Initial care recommendations
        3. Determining urgency and appropriate level of care
        4. Coordinating with appropriate medical professionals
        5. Patient education about their condition
        
        When interacting with patients or doctors, maintain a professional and empathetic tone.
        Prioritize patient safety and ensure timely medical intervention when needed.
        """
    
    def process_patient_data(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process patient data and provide illness assessment."""
        # Extract relevant information
        symptoms = patient_data.get('symptoms', [])
        vital_signs = patient_data.get('vital_signs', {})
        medical_history = patient_data.get('medical_history', [])
        medications = patient_data.get('medications', [])
        
        # Generate symptom assessment
        assessment_prompt = f"""
        Please assess the following patient symptoms and provide an initial evaluation:
        
        Patient Information:
        - Age: {patient_data.get('age', 'Unknown')}
        - Gender: {patient_data.get('gender', 'Unknown')}
        - Symptoms: {', '.join(symptoms) if symptoms else 'None reported'}
        - Vital Signs: {vital_signs}
        - Medical History: {', '.join(medical_history) if medical_history else 'None available'}
        - Current Medications: {', '.join(medications) if medications else 'None reported'}
        
        Provide:
        1. Potential causes of these symptoms
        2. Severity assessment (mild, moderate, severe)
        3. Recommended next steps
        """
        
        symptom_assessment = self.process_input(assessment_prompt)
        
        # Determine if doctor attention is required
        severity_prompt = f"""
        Based on the following patient information, determine if immediate doctor attention is required:
        
        - Age: {patient_data.get('age', 'Unknown')}
        - Gender: {patient_data.get('gender', 'Unknown')}
        - Symptoms: {', '.join(symptoms) if symptoms else 'None reported'}
        - Vital Signs: {vital_signs}
        - Medical History: {', '.join(medical_history) if medical_history else 'None available'}
        
        Respond with only 'Yes' or 'No' followed by a brief explanation.
        """
        
        doctor_attention_response = self.process_input(severity_prompt)
        requires_doctor = doctor_attention_response.lower().startswith('yes')
        
        # Determine appropriate follow-up interval
        if requires_doctor:
            follow_up = "24 hours"
        else:
            follow_up = "72 hours"
        
        return {
            "patient_status": "sick",
            "symptom_assessment": symptom_assessment,
            "requires_doctor_attention": requires_doctor,
            "follow_up_interval": follow_up,
            "care_recommendations": self._generate_care_recommendations(patient_data)
        }
    
    def _generate_care_recommendations(self, patient_data: Dict[str, Any]) -> str:
        """Generate care recommendations based on patient data."""
        symptoms = patient_data.get('symptoms', [])
        
        care_prompt = f"""
        Please provide home care recommendations for a patient with the following symptoms:
        {', '.join(symptoms) if symptoms else 'No specific symptoms reported'}
        
        Include:
        1. Symptom management techniques
        2. Over-the-counter medication recommendations (if appropriate)
        3. Rest and hydration guidance
        4. Warning signs that would require immediate medical attention
        """
        
        return self.process_input(care_prompt)
    
    def generate_referral(self, patient_data: Dict[str, Any], assessment: str) -> str:
        """Generate a referral to the appropriate medical professional."""
        referral_prompt = f"""
        Based on the following patient information and assessment, generate an appropriate medical referral:
        
        Patient Information:
        - Name: {patient_data.get('name', 'Unknown')}
        - Age: {patient_data.get('age', 'Unknown')}
        - Gender: {patient_data.get('gender', 'Unknown')}
        - Symptoms: {', '.join(patient_data.get('symptoms', [])) if patient_data.get('symptoms') else 'None reported'}
        - Medical History: {', '.join(patient_data.get('medical_history', [])) if patient_data.get('medical_history') else 'None available'}
        
        Assessment: {assessment}
        
        Please specify:
        1. Type of specialist recommended (if any)
        2. Urgency of the referral (routine, urgent, emergency)
        3. Recommended timeframe for appointment
        4. Any preparations or tests needed before the appointment
        """
        
        return self.process_input(referral_prompt)