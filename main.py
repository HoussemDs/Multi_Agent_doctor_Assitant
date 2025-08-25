import os
import sys
from typing import Dict, List, Any, Optional
import threading
import random

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import time
import markdown

from agents.base_agent import BaseAgent
from agents.doctor_agent import DoctorAgent
from agents.patient_agents.normal_agent import NormalPatientAgent
from agents.patient_agents.sick_agent import SickPatientAgent
from agents.patient_agents.heart_agent import HeartPatientAgent

from utils.config import Config
from utils.data_processor import DataProcessor
from data.patient_records import get_sample_patient, get_all_sample_patients

def initialize_llm(agent_name=None):
    """Initialize the language model with Groq API.
    
    Args:
        agent_name: Optional name to identify which agent is using this LLM instance
                   This helps with debugging and logging
    """
    try:
        # Get a Groq API key - the Config class will alternate between available keys
        api_key = Config.get_groq_api_key()
        model_name = Config.get_model_name()
        
        # Add a small random delay (0-1 seconds) to avoid simultaneous API calls
        time.sleep(random.uniform(0, 1))
        
        llm = ChatGroq(
            groq_api_key=api_key,
            model_name=model_name
        )
        
        if Config.is_debug_mode():
            agent_str = f" for {agent_name}" if agent_name else ""
            print(f"Initialized LLM{agent_str} with model: {model_name}")
        
        return llm
    except Exception as e:
        print(f"Error initializing language model: {e}")
        sys.exit(1)

def initialize_agents():
    """Initialize all agents in the system with separate LLM instances."""
    # Create doctor agent with its own LLM instance
    doctor = DoctorAgent(
        name="Dr. Sarah Chen",
        role="Primary Care Physician",
        llm=initialize_llm("doctor"),
        system_prompt="",  # Will be set in initialize method
        specialization="Internal Medicine",
        experience_years=15
    )
    
    # Create specialist doctor agent with its own LLM instance
    cardiologist = DoctorAgent(
        name="Dr. James Wilson",
        role="Cardiology Specialist",
        llm=initialize_llm("cardiologist"),
        system_prompt="",  # Will be set in initialize method
        specialization="Cardiology",
        experience_years=20
    )
    
    # Create patient agents with their own LLM instances
    normal_agent = NormalPatientAgent(
        name="Wellness Assistant",
        role="Normal Patient Handler",
        llm=initialize_llm("normal_agent"),
        system_prompt=""  # Will be set in initialize method
    )
    
    sick_agent = SickPatientAgent(
        name="Illness Assistant",
        role="Sick Patient Handler",
        llm=initialize_llm("sick_agent"),
        system_prompt=""  # Will be set in initialize method
    )
    
    heart_agent = HeartPatientAgent(
        name="Cardiac Assistant",
        role="Heart Patient Handler",
        llm=initialize_llm("heart_agent"),
        system_prompt=""  # Will be set in initialize method
    )
    
    return {
        "doctor": doctor,
        "cardiologist": cardiologist,
        "normal_agent": normal_agent,
        "sick_agent": sick_agent,
        "heart_agent": heart_agent
    }

def process_patient(patient_data: Dict[str, Any], agents: Dict[str, BaseAgent]):
    """Process a patient through the appropriate agent workflow and save results to markdown."""
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.getcwd(), "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create a markdown file for this patient
    patient_name = patient_data['name'].replace(" ", "_")
    markdown_file = os.path.join(output_dir, f"{patient_name}.md")
    
    # Initialize markdown content
    markdown_content = f"# Patient Report: {patient_data['name']}\n\n"
    
    print(f"\n\n{'='*50}")
    print(f"Processing patient: {patient_data['name']}")
    print(f"{'='*50}\n")
    
    # Validate patient data
    if not DataProcessor.validate_patient_data(patient_data):
        error_msg = "Error: Invalid patient data. Missing required fields."
        print(error_msg)
        markdown_content += f"## Error\n\n{error_msg}\n\n"
        with open(markdown_file, 'w') as f:
            f.write(markdown_content)
        return
    
    # Categorize patient
    patient_category = DataProcessor.categorize_patient(patient_data)
    print(f"Patient category: {patient_category.upper()}\n")
    markdown_content += f"## Patient Category\n\n{patient_category.upper()}\n\n"
    
    # Add patient information to markdown
    markdown_content += "## Patient Information\n\n"
    markdown_content += f"- **Name**: {patient_data.get('name', 'Unknown')}\n"
    markdown_content += f"- **Age**: {patient_data.get('age', 'Unknown')}\n"
    markdown_content += f"- **Gender**: {patient_data.get('gender', 'Unknown')}\n"
    
    # Add vital signs if available
    if 'vital_signs' in patient_data and patient_data['vital_signs']:
        markdown_content += "\n### Vital Signs\n\n"
        for key, value in patient_data['vital_signs'].items():
            markdown_content += f"- **{key.replace('_', ' ').title()}**: {value}\n"
    
    # Add symptoms if available
    if 'symptoms' in patient_data and patient_data['symptoms']:
        markdown_content += "\n### Symptoms\n\n"
        for symptom in patient_data['symptoms']:
            markdown_content += f"- {symptom}\n"
    
    # Add medical history if available
    if 'medical_history' in patient_data and patient_data['medical_history']:
        markdown_content += "\n### Medical History\n\n"
        for history in patient_data['medical_history']:
            markdown_content += f"- {history}\n"
    
    # Select appropriate agent based on patient category
    if patient_category == 'cardiac':
        primary_agent = agents['heart_agent']
        specialist = agents['cardiologist']
    elif patient_category == 'sick':
        primary_agent = agents['sick_agent']
        specialist = agents['doctor']
    else:  # normal
        primary_agent = agents['normal_agent']
        specialist = agents['doctor']
    
    # Process patient data with appropriate agent
    print(f"Primary agent: {primary_agent.name} ({primary_agent.role})")
    agent_assessment = primary_agent.process_patient_data(patient_data)
    
    print("\nAgent Assessment:")
    print(f"Status: {agent_assessment.get('patient_status', 'Unknown')}")
    print(f"Requires doctor attention: {agent_assessment.get('requires_doctor_attention', False)}")
    print(f"Follow-up interval: {agent_assessment.get('follow_up_interval', 'Unknown')}")
    
    markdown_content += f"\n## Agent Assessment\n\n"
    markdown_content += f"- **Status**: {agent_assessment.get('patient_status', 'Unknown')}\n"
    markdown_content += f"- **Requires doctor attention**: {agent_assessment.get('requires_doctor_attention', False)}\n"
    markdown_content += f"- **Follow-up interval**: {agent_assessment.get('follow_up_interval', 'Unknown')}\n"
    
    # If emergency cardiac case, show emergency instructions
    if patient_category == 'cardiac' and agent_assessment.get('is_emergency', False):
        print("\n⚠️ EMERGENCY CARDIAC SITUATION DETECTED ⚠️")
        print("\nEmergency Instructions:")
        print(agent_assessment.get('emergency_instructions', 'Seek immediate medical attention'))
        
        markdown_content += "\n### ⚠️ EMERGENCY CARDIAC SITUATION DETECTED ⚠️\n\n"
        markdown_content += "**Emergency Instructions:**\n\n"
        markdown_content += agent_assessment.get('emergency_instructions', 'Seek immediate medical attention') + "\n\n"
        
        # Coordinate emergency response
        print("\nCoordinating emergency response...")
        emergency_response = primary_agent.coordinate_emergency_response(patient_data)
        print(emergency_response)
        markdown_content += f"**Emergency Response:**\n\n{emergency_response}\n\n"
    
    # If doctor attention required, consult with specialist
    if agent_assessment.get('requires_doctor_attention', False):
        print(f"\nConsulting with specialist: {specialist.name} ({specialist.specialization})")
        markdown_content += f"\n## Specialist Consultation\n\n"
        markdown_content += f"Consulting with: **{specialist.name}** ({specialist.specialization})\n\n"
        
        # Doctor analyzes patient data
        doctor_assessment = specialist.analyze_patient_data(patient_data)
        print("\nDoctor Assessment:")
        print(doctor_assessment)
        markdown_content += f"### Doctor Assessment\n\n{doctor_assessment}\n\n"
        
        # Create treatment plan
        print("\nGenerating treatment plan...")
        treatment_plan = specialist.create_treatment_plan(patient_data, doctor_assessment)
        print("\nTreatment Plan:")
        print(treatment_plan)
        markdown_content += f"### Treatment Plan\n\n{treatment_plan}\n\n"
        
        # For cardiac patients, create specialized cardiac care plan
        if patient_category == 'cardiac':
            print("\nGenerating specialized cardiac care plan...")
            cardiac_plan = primary_agent.generate_cardiac_care_plan(patient_data, doctor_assessment)
            print("\nCardiac Care Plan:")
            print(cardiac_plan)
            markdown_content += f"### Cardiac Care Plan\n\n{cardiac_plan}\n\n"
    else:
        # For normal patients, generate health report
        if patient_category == 'normal':
            print("\nGenerating health report...")
            health_report = primary_agent.generate_health_report(patient_data)
            print("\nHealth Report:")
            print(health_report)
            markdown_content += f"## Health Report\n\n{health_report}\n\n"
        # For sick patients not requiring immediate doctor attention
        elif patient_category == 'sick':
            print("\nGenerating care recommendations...")
            care_recommendations = agent_assessment.get('care_recommendations', 'No specific recommendations available')
            print("\nCare Recommendations:")
            print(care_recommendations)
            markdown_content += f"## Care Recommendations\n\n{care_recommendations}\n\n"
    
    # Save markdown content to file
    with open(markdown_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"\n{'='*50}")
    print(f"Completed processing for patient: {patient_data['name']}")
    print(f"Report saved to: {markdown_file}")
    print(f"{'='*50}\n")

def main():
    """Main application entry point."""
    print("Initializing Agentic Doctor System...")
    
    # Initialize agents (each with its own LLM instance)
    agents = initialize_agents()
    print("All agents initialized successfully.")
    
    # Process only normal and heart patients to reduce API load
    selected_patients = {
        "normal": get_sample_patient("normal"),
        "heart": get_sample_patient("heart")
    }
    
    print("\nNote: Only processing normal and heart patients to avoid API rate limits.\n")
    
    for patient_type, patient_data in selected_patients.items():
        # Process the patient
        process_patient(patient_data, agents)
        
        # Add a delay between patients to avoid hitting API rate limits
        # This gives time for the API rate limits to reset
        if patient_type != list(selected_patients.keys())[-1]:  # Skip delay after the last patient
            delay = random.uniform(3, 6)  # Longer delay between 3-6 seconds
            print(f"\nWaiting {delay:.1f} seconds before processing next patient...")
            time.sleep(delay)
    
    print("\nAll patients processed successfully.")

if __name__ == "__main__":
    main()