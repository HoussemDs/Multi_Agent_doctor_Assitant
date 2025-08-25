# Agentic Doctor System: Patient Flow Explanation

This document explains how patients flow through the Agentic Doctor System, including the interactions between different agents and the decision-making process.

## System Overview

The Agentic Doctor System uses multiple specialized AI agents to process patient data and provide appropriate medical care recommendations. Each agent has a specific role in the patient care workflow.

```mermaid
graph TD
    A[Patient Data Input] --> B[Data Processor]
    B --> C{Patient Category}
    C -->|Normal| D[Normal Patient Agent]
    C -->|Sick| E[Sick Patient Agent]
    C -->|Cardiac| F[Heart Patient Agent]
    
    D -->|No Doctor Needed| G[Generate Health Report]
    E -->|Doctor Needed?| H{Requires Doctor?}
    F -->|Always to Doctor| I[Consult Cardiologist]
    
    H -->|No| J[Generate Care Recommendations]
    H -->|Yes| K[Consult Primary Doctor]
    
    I --> L[Generate Treatment Plan]
    K --> M[Generate Treatment Plan]
    
    L --> N[Generate Cardiac Care Plan]
    
    G --> O[Final Patient Report]
    J --> O
    M --> O
    N --> O
```

## Detailed Patient Flow

### 1. Initial Data Processing

- **Input**: Patient data (name, age, gender, vital signs, symptoms, medical history)
- **Process**: `DataProcessor` validates and categorizes the patient
- **Output**: Patient category (normal, sick, or cardiac)

### 2. Patient Categorization Logic

The system categorizes patients based on the following criteria:

- **Cardiac Patient**: 
  - Has cardiac symptoms (chest pain, shortness of breath, etc.)
  - OR has heart-related medical history

- **Sick Patient**:
  - Has symptoms AND abnormal vital signs
  - OR has more than 2 symptoms

- **Normal Patient**:
  - No significant symptoms
  - Normal vital signs

### 3. Agent Assignment

Based on the category, the patient is assigned to a specialized agent:

- **Normal Patient** → `NormalPatientAgent`
- **Sick Patient** → `SickPatientAgent`
- **Cardiac Patient** → `HeartPatientAgent`

### 4. Patient Processing by Agent Type

#### Normal Patient Flow

```mermaid
sequenceDiagram
    participant P as Patient Data
    participant N as Normal Patient Agent
    participant D as Doctor (if needed)
    
    P->>N: Patient Information
    N->>N: Process Patient Data
    Note over N: Generates wellness recommendations
    Note over N: Creates check-up schedule
    N->>N: Generate Health Report
    Note over N: Includes preventive care
    Note over N: Includes lifestyle optimization
```

#### Sick Patient Flow

```mermaid
sequenceDiagram
    participant P as Patient Data
    participant S as Sick Patient Agent
    participant D as Doctor
    
    P->>S: Patient Information
    S->>S: Process Patient Data
    Note over S: Assesses symptoms
    Note over S: Determines severity
    
    alt Requires Doctor Attention
        S->>D: Consult Doctor
        D->>D: Analyze Patient Data
        D->>D: Create Treatment Plan
    else No Doctor Needed
        S->>S: Generate Care Recommendations
    end
```

#### Cardiac Patient Flow

```mermaid
sequenceDiagram
    participant P as Patient Data
    participant H as Heart Patient Agent
    participant C as Cardiologist
    
    P->>H: Patient Information
    H->>H: Process Patient Data
    Note over H: Cardiac assessment
    Note over H: Emergency determination
    
    alt Is Emergency
        H->>H: Generate Emergency Instructions
        H->>H: Coordinate Emergency Response
    end
    
    H->>C: Consult Cardiologist
    C->>C: Analyze Patient Data
    C->>C: Create Treatment Plan
    H->>H: Generate Cardiac Care Plan
```

### 5. Doctor Consultation Process

When a patient requires doctor attention:

1. The patient agent forwards the case to the appropriate specialist:
   - Normal/Sick patients → Primary Care Doctor
   - Cardiac patients → Cardiologist

2. The doctor agent:
   - Analyzes patient data
   - Provides a medical assessment
   - Creates a treatment plan

3. For cardiac patients, additional steps occur:
   - The Heart Patient Agent generates a specialized cardiac care plan
   - In emergency cases, emergency instructions and response coordination are provided

### 6. Output Generation

The system generates a comprehensive markdown report for each patient that includes:

- Patient information and category
- Agent assessment
- Doctor consultation (if applicable)
- Treatment plan (if applicable)
- Specialized care plans (for cardiac patients)
- Health reports (for normal patients)
- Care recommendations (for sick patients not requiring doctor attention)

## Sample Patient Examples

### John Smith (Normal Patient)

- **Flow**: Patient Data → DataProcessor → NormalPatientAgent → Health Report
- **Key Actions**: Wellness recommendations, preventive care, check-up schedule
- **Output**: Health report with lifestyle optimization suggestions

### Emily Johnson (Sick Patient)

- **Flow**: Patient Data → DataProcessor → SickPatientAgent → Doctor → Treatment Plan
- **Key Actions**: Symptom assessment, doctor consultation, treatment planning
- **Output**: Treatment plan addressing fever, cough, and other symptoms

### Robert Davis (Cardiac Patient)

- **Flow**: Patient Data → DataProcessor → HeartPatientAgent → Cardiologist → Treatment Plan → Cardiac Care Plan
- **Key Actions**: Cardiac assessment, cardiologist consultation, specialized care planning
- **Output**: Comprehensive cardiac care plan with monitoring recommendations

### Margaret Wilson (Emergency Cardiac Patient)

- **Flow**: Patient Data → DataProcessor → HeartPatientAgent → Emergency Response → Cardiologist → Treatment Plan → Cardiac Care Plan
- **Key Actions**: Emergency instructions, emergency response coordination, urgent care planning
- **Output**: Emergency cardiac care plan with immediate action steps

## Agent Communication

Agents communicate through structured data and text responses:

1. Patient agents process raw patient data and generate assessments
2. Doctor agents receive patient assessments and generate medical recommendations
3. Specialized agents (like the Heart Patient Agent) can request consultations from specialists

Each agent maintains its own memory of interactions, allowing for contextual understanding throughout the patient care process.

## Conclusion

The Agentic Doctor System provides a comprehensive approach to patient care through specialized AI agents. By categorizing patients and routing them to appropriate agents, the system ensures that each patient receives the right level of care for their condition.