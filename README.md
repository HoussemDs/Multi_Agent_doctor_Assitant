# Agentic Doctor System

A multiagent system that processes patient data and facilitates communication between doctors to provide appropriate care based on patient conditions.

## Features

- Specialized agents for different patient conditions (normal, sick, heart problems)
- Integration with Groq API for advanced language processing
- Automated conversation flows between agents and doctors
- Patient data processing and analysis

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on the provided `.env.example` template and add your Groq API keys
4. Run the application:
   ```
   python main.py
   ```

## Project Structure

```
├── agents/                 # Agent implementations
│   ├── base_agent.py       # Base agent class
│   ├── doctor_agent.py     # Doctor agent implementation
│   └── patient_agents/     # Specialized patient condition agents
│       ├── normal_agent.py
│       ├── sick_agent.py
│       └── heart_agent.py
├── data/                   # Sample patient data
│   └── patient_records.py  # Sample patient records
├── utils/                  # Utility functions
│   ├── config.py           # Configuration utilities
│   └── data_processor.py   # Data processing utilities
├── .env                    # Environment variables
├── main.py                 # Application entry point
└── requirements.txt        # Project dependencies
```

## Usage

The system processes patient data and initiates appropriate agent conversations based on the patient's condition. Doctors can interact with the system to receive recommendations and provide feedback.

When you run the application, it will:
1. Process patient data from the sample records
2. Generate detailed medical reports based on patient conditions
3. Save the reports as markdown files in the `output` directory

## License

MIT