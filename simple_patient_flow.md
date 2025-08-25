# Simple Explanation: How Patients Move Through Our System

## The Basics

Our Agentic Doctor System helps patients get the right care by using AI assistants (agents) that work together. Here's how it works in simple terms:

```
Patient Data → Sort Patient → Right Agent → Care Plan → Final Report
```

## Three Types of Patients

We sort patients into three groups:

1. **Normal Patients** 😊
   - Healthy people who just need checkups
   - Example: John Smith

2. **Sick Patients** 🤒
   - People with common illnesses
   - Example: Emily Johnson

3. **Heart Patients** ❤️
   - People with heart problems
   - Example: Robert Davis

## The Patient Journey

### For Normal Patients (Like John Smith):

```
John's Data → Normal Agent → Health Report
```

- **What happens**: The Normal Agent creates a wellness plan
- **No doctor needed**: The agent handles everything
- **Result**: John gets a health report with lifestyle tips

### For Sick Patients (Like Emily Johnson):

```
Emily's Data → Sick Agent → Doctor? → Yes → Doctor → Treatment Plan
                                    → No → Care Recommendations
```

- **What happens**: The Sick Agent checks how serious the illness is
- **Doctor needed?** The agent decides if a doctor should look at the case
- **Result**: Emily gets either a doctor's treatment plan or simple care tips

### For Heart Patients (Like Robert Davis):

```
Robert's Data → Heart Agent → Emergency? → Yes → Emergency Instructions
                                         → No → Continue
              → Cardiologist → Treatment Plan → Cardiac Care Plan
```

- **What happens**: The Heart Agent checks if it's an emergency
- **Always sees doctor**: All heart patients talk to a heart specialist
- **Result**: Robert gets a specialized heart care plan

## What Each Agent Does

### Normal Patient Agent
- Gives wellness advice
- Suggests checkup schedules
- Creates health reports

### Sick Patient Agent
- Checks symptoms
- Decides if a doctor is needed
- Gives care recommendations

### Heart Patient Agent
- Checks for heart emergencies
- Works with heart specialists
- Creates heart care plans

### Doctor Agent
- Reviews patient information
- Makes diagnoses
- Creates treatment plans

## Real Examples

### John (Normal Patient)
→ Normal Agent → Health Report with exercise and diet tips

### Emily (Sick Patient with fever)
→ Sick Agent → Doctor → Treatment Plan for her fever and cough

### Robert (Heart Patient with chest pain)
→ Heart Agent → Cardiologist → Special Heart Care Plan

## The Final Result

Every patient gets a report saved as a markdown file that includes:
- Their personal information
- What the agents found
- What the doctor said (if they saw one)
- Their treatment or care plan

All of this happens automatically when you run the system!