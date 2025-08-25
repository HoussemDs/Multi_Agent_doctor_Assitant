# Visual Patient Journey Guide

## John Smith's Journey (Normal Patient)

```
┌─────────────────┐
│ John Smith Data │
│ Age: 35         │
│ Normal vitals   │
│ No symptoms     │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Data Processor  │
│ Categorizes as  │
│ NORMAL PATIENT  │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Normal Agent    │
│ "Wellness       │
│  Assistant"     │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Process Patient │
│ Data            │
│                 │
│ • Creates       │
│   wellness      │
│   recommendations│
│                 │
│ • Sets up       │
│   check-up      │
│   schedule      │
│                 │
│ • No doctor     │
│   needed        │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Generate Health │
│ Report          │
│                 │
│ • Preventive    │
│   care          │
│                 │
│ • Lifestyle     │
│   optimization  │
│                 │
│ • Follow-up     │
│   timeline      │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Final Report    │
│ Saved as        │
│ John_Smith.md   │
└─────────────────┘
```

## Robert Davis's Journey (Heart Patient)

```
┌─────────────────┐
│ Robert Davis    │
│ Data            │
│ Age: 68         │
│ High BP: 165/95 │
│ Chest pain      │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Data Processor  │
│ Categorizes as  │
│ CARDIAC PATIENT │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Heart Agent     │
│ "Cardiac        │
│  Assistant"     │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Process Patient │
│ Data            │
│                 │
│ • Cardiac       │
│   assessment    │
│                 │
│ • Emergency     │
│   determination │
│                 │
│ • Always needs  │
│   doctor        │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Consult with    │
│ Cardiologist    │
│ "Dr. James      │
│  Wilson"        │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Doctor          │
│ Assessment      │
│                 │
│ • Analyzes      │
│   cardiac data  │
│                 │
│ • Provides      │
│   diagnosis     │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Treatment Plan  │
│                 │
│ • Medications   │
│ • Lifestyle     │
│   changes       │
│ • Follow-up     │
│   schedule      │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Cardiac Care    │
│ Plan            │
│                 │
│ • Specialized   │
│   heart care    │
│                 │
│ • Monitoring    │
│   instructions  │
│                 │
│ • Warning signs │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Final Report    │
│ Saved as        │
│ Robert_Davis.md │
└─────────────────┘
```

## What Actually Happens in the Code

### 1. System Initialization
```
main() → initialize_agents() → Creates all agent instances with their own LLMs
```

### 2. Patient Selection
```
main() → Selects John Smith (normal) and Robert Davis (heart) for processing
```

### 3. Patient Processing Loop
```
For each patient:
  process_patient(patient_data, agents)
```

### 4. Inside process_patient()

1. **Create output directory and markdown file**
   ```
   Create output/John_Smith.md or output/Robert_Davis.md
   ```

2. **Validate and categorize patient**
   ```
   DataProcessor.validate_patient_data()
   DataProcessor.categorize_patient() → Returns 'normal' or 'cardiac'
   ```

3. **Select appropriate agent**
   ```
   For John: primary_agent = normal_agent, specialist = doctor
   For Robert: primary_agent = heart_agent, specialist = cardiologist
   ```

4. **Process with primary agent**
   ```
   agent_assessment = primary_agent.process_patient_data(patient_data)
   ```

5. **Determine if doctor is needed**
   ```
   For John: requires_doctor_attention = False
   For Robert: requires_doctor_attention = True
   ```

6. **For John (no doctor needed):**
   ```
   health_report = normal_agent.generate_health_report(patient_data)
   ```

7. **For Robert (doctor needed):**
   ```
   doctor_assessment = cardiologist.analyze_patient_data(patient_data)
   treatment_plan = cardiologist.create_treatment_plan(patient_data, doctor_assessment)
   cardiac_plan = heart_agent.generate_cardiac_care_plan(patient_data, doctor_assessment)
   ```

8. **Save final report**
   ```
   Write markdown_content to output/[Patient_Name].md
   ```

## Key Decision Points

1. **Patient Categorization**
   - Based on symptoms, vital signs, and medical history
   - Determines which agent handles the patient

2. **Doctor Attention Required?**
   - Normal patients: Never need doctor
   - Heart patients: Always need doctor
   - Sick patients: Depends on severity

3. **Emergency Status (for heart patients)**
   - If emergency, additional emergency instructions are generated

## The End Result

Two markdown files are created:

1. **output/John_Smith.md**
   - Contains health report with preventive care recommendations

2. **output/Robert_Davis.md**
   - Contains doctor assessment, treatment plan, and cardiac care plan