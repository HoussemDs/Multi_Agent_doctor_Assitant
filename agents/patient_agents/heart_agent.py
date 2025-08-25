from typing import Dict, List, Any, Optional
from ..base_agent import BaseAgent
from langchain_core.language_models import BaseChatModel
from pydantic import Field

class HeartPatientAgent(BaseAgent):
    """Agent for handling patients with cardiac conditions."""
    
    def initialize(self):
        """Initialize the heart patient agent with specialized system prompt."""
        self.system_prompt = f"You are {self.name}, a cardiac care specialist. Provide concise assessments of heart conditions, emergency response coordination, and cardiac care recommendations. Prioritize patient safety for life-threatening conditions."
    
    def process_patient_data(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process patient data and provide cardiac assessment with urgency rating."""
        # Extract relevant cardiac information
        symptoms = patient_data.get('symptoms', [])
        vital_signs = patient_data.get('vital_signs', {})
        medical_history = patient_data.get('medical_history', [])
        medications = patient_data.get('medications', [])
        
        # Check for critical cardiac symptoms
        cardiac_symptoms = ['chest pain', 'chest pressure', 'shortness of breath', 'palpitations', 
                           'dizziness', 'fainting', 'sweating', 'nausea', 'jaw pain', 'arm pain']
        
        has_cardiac_symptoms = any(symptom in ' '.join(symptoms).lower() for symptom in cardiac_symptoms)
        
        # Generate cardiac assessment - more concise prompt
        assessment_prompt = f"Provide urgent cardiac assessment for: {patient_data.get('age')}-year-old {patient_data.get('gender')} with symptoms: {', '.join(symptoms) if symptoms else 'None'}, vitals: BP {vital_signs.get('blood_pressure_systolic', 'N/A')}/{vital_signs.get('blood_pressure_diastolic', 'N/A')}, HR {vital_signs.get('heart_rate', 'N/A')}, history: {', '.join(medical_history[:2]) if medical_history else 'None'}. Provide: 1. Cardiac risk level 2. Potential conditions 3. Immediate actions 4. Need for emergency services (Yes/No)"
        
        cardiac_assessment = self.process_input(assessment_prompt)
        
        # Determine emergency status
        emergency_prompt = f"""
        Based on the following patient information, determine if this is a cardiac emergency requiring immediate medical attention:
        
        - Age: {patient_data.get('age', 'Unknown')}
        - Gender: {patient_data.get('gender', 'Unknown')}
        - Symptoms: {', '.join(symptoms) if symptoms else 'None reported'}
        - Vital Signs: {vital_signs}
        - Medical History: {', '.join(medical_history) if medical_history else 'None available'}
        
        Respond with only 'Yes' or 'No' followed by a brief explanation.
        """
        
        emergency_response = self.process_input(emergency_prompt)
        is_emergency = emergency_response.lower().startswith('yes')
        
        # Generate emergency instructions if needed
        emergency_instructions = ""
        if is_emergency:
            instructions_prompt = f"""
            Please provide clear emergency instructions for a patient with the following cardiac symptoms:
            {', '.join(symptoms) if symptoms else 'None reported'}
            
            Include step-by-step instructions for the patient or caregiver until emergency services arrive.
            """
            emergency_instructions = self.process_input(instructions_prompt)
        
        return {
            "patient_status": "cardiac",
            "cardiac_assessment": cardiac_assessment,
            "is_emergency": is_emergency,
            "emergency_instructions": emergency_instructions,
            "requires_doctor_attention": True,
            "follow_up_interval": "immediate" if is_emergency else "24 hours"
        }
    
    def generate_cardiac_care_plan(self, patient_data: Dict[str, Any], cardiologist_input: Optional[str] = None) -> str:
        """Generate a cardiac care plan based on patient data and cardiologist input."""
        care_plan_prompt = f"""
        Please generate a comprehensive cardiac care plan for:
        
        Patient Information:
        - Name: {patient_data.get('name', 'Unknown')}
        - Age: {patient_data.get('age', 'Unknown')}
        - Gender: {patient_data.get('gender', 'Unknown')}
        - Cardiac Symptoms: {', '.join(patient_data.get('symptoms', [])) if patient_data.get('symptoms') else 'None reported'}
        - Vital Signs: {patient_data.get('vital_signs', 'Not available')}
        - Medical History: {', '.join(patient_data.get('medical_history', [])) if patient_data.get('medical_history') else 'None available'}
        - Current Medications: {', '.join(patient_data.get('medications', [])) if patient_data.get('medications') else 'None reported'}
        
        {f'Cardiologist Input: {cardiologist_input}' if cardiologist_input else ''}
        
        Include:
        1. Cardiac monitoring recommendations
        2. Medication management
        3. Lifestyle modifications for heart health
        4. Warning signs requiring immediate attention
        5. Follow-up schedule with cardiology
        """
        
        return self.process_input(care_plan_prompt)
    
    def coordinate_emergency_response(self, patient_data: Dict[str, Any]) -> str:
        """Coordinate emergency response for a cardiac patient."""
        emergency_prompt = f"""
        Please provide emergency response coordination instructions for:
        
        Patient Information:
        - Name: {patient_data.get('name', 'Unknown')}
        - Age: {patient_data.get('age', 'Unknown')}
        - Gender: {patient_data.get('gender', 'Unknown')}
        - Location: {patient_data.get('location', 'Unknown')}
        - Cardiac Symptoms: {', '.join(patient_data.get('symptoms', [])) if patient_data.get('symptoms') else 'None reported'}
        - Vital Signs: {patient_data.get('vital_signs', 'Not available')}
        
        Include:
        1. Instructions for calling emergency services
        2. Information to provide to emergency responders
        3. Immediate actions while waiting for help
        4. Preparation for hospital transport
        """
        
        return self.process_input(emergency_prompt)