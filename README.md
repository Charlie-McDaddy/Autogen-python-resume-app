# QPS Resume Writing Multi-Agent System

A sophisticated multi-agent AI system designed to assist Queensland Police Service (QPS) officers in writing compelling resumes for internal promotions. The system employs 13 specialized AutoGen agents that collaborate to ensure resume examples meet all assessment criteria and achieve competitive scores.

## 🚀 Features

- **Intelligent Multi-Agent Collaboration**: 13 specialized agents working together
- **QPS-Specific Requirements**: Built for Queensland Police Service promotion criteria
- **LC4Q Framework Integration**: Ensures all leadership competencies are covered
- **STAR Methodology**: Structures examples using proven Situation-Task-Action-Result format
- **Automated Scoring**: Evaluates examples against Context, Complexity, and Initiative criteria
- **Quality Assurance**: Comprehensive final review and polish
- **Web Interface**: User-friendly Streamlit interface for easy interaction

## 🏗️ Architecture

### Agent Hierarchy

```
┌─────────────────────────────────────┐
│          Orchestrator Agent         │
│      (Process Management)           │
└──────────────┬──────────────────────┘
               │
    ┌──────────┴──────────┬─────────────┬──────────────┐
    │                     │             │              │
┌───▼────────┐  ┌────────▼────────┐  ┌─▼──────────┐  ┌─▼────────────┐
│ Readiness  │  │Position Analysis │  │  Example   │  │    STAR      │
│Assessment  │  │     Agent        │  │ Selection  │  │   Writing    │
│   Agent    │  │                  │  │   Agent    │  │    Agent     │
└────────────┘  └─────────────────┘  └────────────┘  └──────────────┘
                                                              │
                          ┌───────────────────────────────────┘
                          │
       ┌──────────────────┼─────────────────────┐
       │                  │                     │
┌──────▼──────┐  ┌────────▼────────┐  ┌────────▼────────┐
│   Scoring   │  │      LC4Q       │  │  Transferable   │
│   Agents    │  │  Competency     │  │     Skills      │
│   (3)       │  │   Agents (3)    │  │     Agent       │
└─────────────┘  └─────────────────┘  └─────────────────┘
       │                  │
       │     ┌────────────┴──────────────┐
       │     │                           │
       └─────┼────────────┐              │
             │            │              │
    ┌────────▼───┐  ┌─────▼────┐  ┌─────▼──────┐
    │  Context   │  │  Vision  │  │   Quality  │
    │  Scoring   │  │  Agent   │  │ Assurance  │
    │   Agent    │  │          │  │   Agent    │
    └────────────┘  └──────────┘  └────────────┘
    ┌─────────────┐  ┌───────────┐
    │ Complexity  │  │  Results  │
    │  Scoring    │  │   Agent   │
    │   Agent     │  │           │
    └─────────────┘  └───────────┘
    ┌─────────────┐  ┌────────────────┐
    │ Initiative  │  │ Accountability │
    │  Scoring    │  │     Agent      │
    │   Agent     │  │                │
    └─────────────┘  └────────────────┘
```

### 13 Specialized Agents

1. **Orchestrator Agent** - Coordinates workflow and manages agent interactions
2. **Readiness Assessment Agent** - Evaluates promotion readiness using 6 key criteria
3. **Position Analysis Agent** - Extracts and maps position requirements
4. **Example Selection Agent** - Recommends optimal work examples
5. **STAR Writing Agent** - Structures examples using STAR methodology
6. **Context Scoring Agent** - Evaluates contextual relevance (1-7 scale)
7. **Complexity Scoring Agent** - Assesses example complexity relative to rank
8. **Initiative Scoring Agent** - Measures proactive leadership behaviors
9. **Vision Agent** - Ensures Vision competencies (LC4Q) are demonstrated
10. **Results Agent** - Validates Results competencies (LC4Q)
11. **Accountability Agent** - Verifies Accountability competencies (LC4Q)
12. **Transferable Skills Agent** - Articulates transferable skills explicitly
13. **Quality Assurance Agent** - Final review and polish

## 📋 Requirements

- Python 3.8+
- OpenAI API key
- AutoGen AgentChat framework
- Streamlit (for web interface)

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd AutoGen
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

4. **Configure API key:**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

## 🚀 Usage

### Command Line Interface

#### Basic Usage
```bash
python main.py
```

#### Test the System
```bash
python test_resume_system.py
```

### Web Interface

Launch the Streamlit web interface:
```bash
streamlit run resume_web_interface.py
```

Then open your browser to `http://localhost:8501`

### Programmatic Usage

```python
import asyncio
from resume_system import ResumeWritingSystem

async def create_resume():
    # Initialize system
    system = ResumeWritingSystem(api_key="your-api-key")
    
    # User data
    user_data = {
        "name": "John Smith",
        "current_rank": "Senior Constable",
        "target_position": "Sergeant - Team Leader",
        "experience_summary": [
            "Led community engagement initiatives",
            "Managed complex investigations"
        ]
    }
    
    # Position document
    position_document = """
    POSITION: Sergeant - Team Leader
    KEY ACCOUNTABILITIES:
    Vision: Lead strategic initiatives
    Results: Develop team capabilities
    Accountability: Foster inclusive culture
    """
    
    # Create resume
    result = await system.create_resume(user_data, position_document)
    
    # Clean up
    await system.close()
    
    return result

# Run
result = asyncio.run(create_resume())
```

## 📊 Success Criteria

The system targets these success metrics:

- ✅ 90% of examples score ≥4 in Context, Complexity, and Initiative
- ✅ 100% coverage of relevant Key Accountabilities (KAs)
- ✅ 100% coverage of required LC4Q competencies
- ✅ Professional format and presentation
- ✅ Clear transferable skills articulation

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `RESUME_SYSTEM_DEBUG` | Enable debug mode | `false` |
| `RESUME_SYSTEM_MAX_TURNS` | Maximum agent turns | `100` |
| `RESUME_SYSTEM_TIMEOUT` | System timeout (seconds) | `3600` |

### System Configuration

The system can be configured through the `ResumeWritingSystem` constructor:

```python
system = ResumeWritingSystem(
    api_key="your-key",
    model="gpt-4o",  # Model to use
    max_turns=80,    # Max conversation turns
    temperature=0.3  # Model temperature
)
```

## 🧪 Testing

### Run All Tests
```bash
python test_resume_system.py
```

### Test Scenarios

The system includes several test scenarios:

1. **Senior Constable to Sergeant** - Community engagement role
2. **Constable to Senior Constable** - Traffic enforcement specialist

### Quick Test
```bash
python test_resume_system.py
# Select option 1 for quick test
```

## 📁 File Structure

```
AutoGen/
├── main.py                    # Simple entry point
├── resume_system.py           # Core system implementation
├── resume_web_interface.py    # Streamlit web interface
├── test_resume_system.py      # Comprehensive test suite
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── CLAUDE.md                 # Claude Code guidance
├── PRD.md                    # Product Requirements Document
└── README.md                 # This file
```

## 🎯 Workflow Process

1. **User Input** - Officer information and target position
2. **Readiness Assessment** - Evaluate promotion readiness
3. **Position Analysis** - Extract key requirements from position description
4. **Example Selection** - Recommend optimal work examples
5. **STAR Writing** - Structure examples using STAR methodology
6. **Multi-Agent Scoring** - Evaluate Context, Complexity, Initiative
7. **LC4Q Verification** - Ensure all competencies are covered
8. **Skills Articulation** - Highlight transferable skills
9. **Quality Assurance** - Final review and polish
10. **Iteration** - Refine until all criteria are met

## 🔍 Scoring System

### Context Scoring (1-7 scale)
- 1-2: Very Limited/Limited
- 3: Basic
- 4: Adequate ✅
- 5: Proficient
- 6: Very Proficient
- 7: Advanced

### Target Scores
- **Context**: ≥4 (Adequate)
- **Complexity**: ≥4 (Appropriate to rank)
- **Initiative**: ≥4 (Proactive leadership)

## 📚 Documentation

- **PRD.md** - Complete Product Requirements Document
- **CLAUDE.md** - Developer guidance for Claude Code
- **Inline Documentation** - Comprehensive code comments

## 🤝 Contributing

1. Follow the existing code structure and patterns
2. Add comprehensive docstrings and comments
3. Include test cases for new features
4. Update documentation as needed

## 📄 License

This project is designed for Queensland Police Service internal use. Please ensure compliance with organizational policies and data handling requirements.

## 🆘 Support

For issues or questions:

1. Check the test suite for examples: `test_resume_system.py`
2. Review the PRD for detailed requirements: `PRD.md`
3. Examine agent system messages for behavior details

## 🔒 Security Notes

- API keys are handled securely through environment variables
- No user data is stored permanently
- All processing occurs locally or through OpenAI API
- Follow QPS data handling protocols when using with real officer information