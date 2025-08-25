from typing import Dict, List, Any, Optional
import json
import os

class DataProcessor:
    """Utility for processing and managing patient data."""
    
    @staticmethod
    def validate_patient_data(patient_data: Dict[str, Any]) -> bool:
        """Validate that patient data contains required fields."""
        required_fields = ['name', 'age', 'gender']
        return all(field in patient_data for field in required_fields)
    
    @staticmethod
    def categorize_patient(patient_data: Dict[str, Any]) -> str:
        """Categorize patient based on their data."""
        # Check for cardiac symptoms
        cardiac_symptoms = ['chest pain', 'chest pressure', 'shortness of breath', 'palpitations', 
                           'dizziness', 'fainting', 'sweating', 'nausea', 'jaw pain', 'arm pain']
        
        symptoms = patient_data.get('symptoms', [])
        has_cardiac_symptoms = any(symptom in ' '.join(symptoms).lower() for symptom in cardiac_symptoms)
        
        # Check vital signs for abnormalities
        vital_signs = patient_data.get('vital_signs', {})
        has_abnormal_vitals = False
        
        if vital_signs:
            # Check heart rate
            heart_rate = vital_signs.get('heart_rate')
            if heart_rate and (heart_rate < 60 or heart_rate > 100):
                has_abnormal_vitals = True
            
            # Check blood pressure
            systolic = vital_signs.get('blood_pressure_systolic')
            diastolic = vital_signs.get('blood_pressure_diastolic')
            if (systolic and systolic > 140) or (diastolic and diastolic > 90):
                has_abnormal_vitals = True
        
        # Determine patient category
        if has_cardiac_symptoms or ('heart' in ' '.join(patient_data.get('medical_history', [])).lower()):
            return 'cardiac'
        elif symptoms and (has_abnormal_vitals or len(symptoms) > 2):
            return 'sick'
        else:
            return 'normal'
    
    @staticmethod
    def save_patient_data(patient_data: Dict[str, Any], file_path: Optional[str] = None) -> str:
        """Save patient data to a JSON file."""
        if not file_path:
            # Create data directory if it doesn't exist
            data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
            os.makedirs(data_dir, exist_ok=True)
            
            # Generate file name based on patient name
            patient_name = patient_data.get('name', 'unknown').lower().replace(' ', '_')
            file_path = os.path.join(data_dir, f"{patient_name}_record.json")
        
        # Save data to file
        with open(file_path, 'w') as f:
            json.dump(patient_data, f, indent=2)
        
        return file_path
    
    @staticmethod
    def load_patient_data(file_path: str) -> Dict[str, Any]:
        """Load patient data from a JSON file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Patient data file not found: {file_path}")
        
        with open(file_path, 'r') as f:
            patient_data = json.load(f)
        
        return patient_data