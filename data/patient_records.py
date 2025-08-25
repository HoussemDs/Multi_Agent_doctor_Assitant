from typing import Dict, List, Any

# Sample patient data for testing the system

NORMAL_PATIENT = {
    "name": "John Smith",
    "age": 35,
    "gender": "Male",
    "vital_signs": {
        "temperature": 98.6,
        "heart_rate": 72,
        "blood_pressure_systolic": 120,
        "blood_pressure_diastolic": 80,
        "respiratory_rate": 16,
        "oxygen_saturation": 98
    },
    "symptoms": [],
    "medical_history": ["Seasonal allergies"],
    "medications": ["Cetirizine 10mg as needed for allergies"],
    "allergies": ["Pollen"]
}

SICK_PATIENT = {
    "name": "Emily Johnson",
    "age": 42,
    "gender": "Female",
    "vital_signs": {
        "temperature": 101.3,
        "heart_rate": 88,
        "blood_pressure_systolic": 135,
        "blood_pressure_diastolic": 85,
        "respiratory_rate": 20,
        "oxygen_saturation": 96
    },
    "symptoms": ["Fever", "Cough", "Fatigue", "Sore throat"],
    "medical_history": ["Asthma", "Hypertension"],
    "medications": ["Albuterol inhaler", "Lisinopril 10mg daily"],
    "allergies": ["Penicillin"]
}

HEART_PATIENT = {
    "name": "Robert Davis",
    "age": 68,
    "gender": "Male",
    "vital_signs": {
        "temperature": 99.1,
        "heart_rate": 92,
        "blood_pressure_systolic": 165,
        "blood_pressure_diastolic": 95,
        "respiratory_rate": 22,
        "oxygen_saturation": 94
    },
    "symptoms": ["Chest pain", "Shortness of breath", "Dizziness", "Fatigue"],
    "medical_history": ["Coronary artery disease", "Type 2 diabetes", "Previous myocardial infarction (2018)"],
    "medications": ["Aspirin 81mg daily", "Metoprolol 50mg twice daily", "Atorvastatin 40mg daily", "Metformin 1000mg twice daily"],
    "allergies": ["Sulfa drugs"]
}

EMERGENCY_HEART_PATIENT = {
    "name": "Margaret Wilson",
    "age": 74,
    "gender": "Female",
    "location": "123 Main St, Apt 4B",
    "vital_signs": {
        "temperature": 98.8,
        "heart_rate": 110,
        "blood_pressure_systolic": 180,
        "blood_pressure_diastolic": 100,
        "respiratory_rate": 24,
        "oxygen_saturation": 91
    },
    "symptoms": ["Severe chest pain", "Radiating pain to left arm and jaw", "Profuse sweating", "Nausea", "Extreme shortness of breath"],
    "medical_history": ["Hypertension", "Atrial fibrillation", "High cholesterol"],
    "medications": ["Warfarin 5mg daily", "Amlodipine 10mg daily", "Rosuvastatin 20mg daily"],
    "allergies": ["Contrast dye"]
}

# Dictionary of all sample patients
SAMPLE_PATIENTS = {
    "normal": NORMAL_PATIENT,
    "sick": SICK_PATIENT,
    "heart": HEART_PATIENT,
    "emergency": EMERGENCY_HEART_PATIENT
}

def get_sample_patient(patient_type: str) -> Dict[str, Any]:
    """Get a sample patient by type."""
    return SAMPLE_PATIENTS.get(patient_type.lower(), NORMAL_PATIENT)

def get_all_sample_patients() -> Dict[str, Dict[str, Any]]:
    """Get all sample patients."""
    return SAMPLE_PATIENTS