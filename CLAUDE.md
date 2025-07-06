# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a sophisticated multi-agent AI system designed for Queensland Police Service (QPS) officers to create compelling resumes for internal promotions. The system employs 13 specialized AutoGen agents that collaborate to ensure resume examples meet all assessment criteria and achieve competitive scores according to the LC4Q framework.

## Architecture

### Core Files
- **main.py**: Simple entry point with demo functionality
- **resume_system.py**: Core multi-agent system implementation with 13 specialized agents
- **resume_web_interface.py**: Streamlit web interface for user interaction
- **test_resume_system.py**: Comprehensive test suite with multiple scenarios
- **PRD.md**: Complete Product Requirements Document

### Agent System
The system uses AutoGen's `SelectorGroupChat` pattern with 13 specialized agents:
1. Orchestrator Agent (workflow coordination)
2. Readiness Assessment Agent (promotion readiness evaluation)
3. Position Analysis Agent (requirement extraction)
4. Example Selection Agent (optimal example recommendation)
5. STAR Writing Agent (structured example creation)
6. Context/Complexity/Initiative Scoring Agents (quality evaluation)
7. Vision/Results/Accountability Agents (LC4Q competency verification)
8. Transferable Skills Agent (skill articulation)
9. Quality Assurance Agent (final review)

## Dependencies

Core libraries:
- `autogen-agentchat>=0.5.0`: Multi-agent framework
- `autogen-ext[openai]>=0.5.0`: OpenAI integration
- `python-dotenv>=1.0.0`: Environment variables
- `pydantic>=2.0.0`: Data validation
- `streamlit>=1.28.0`: Web interface

## Environment Setup

Required environment variables:
- `OPENAI_API_KEY`: OpenAI API key for GPT-4o model access

Optional configuration:
- `RESUME_SYSTEM_DEBUG`: Enable debug mode
- `RESUME_SYSTEM_MAX_TURNS`: Maximum agent conversation turns (default: 100)
- `RESUME_SYSTEM_TIMEOUT`: System timeout in seconds (default: 3600)

## Running the Application

### Quick Demo
```bash
python main.py
```

### Full Testing Suite
```bash
python test_resume_system.py
```

### Web Interface
```bash
streamlit run resume_web_interface.py
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Development Commands

### Test specific scenarios:
```bash
python test_resume_system.py
# Select option 2 for individual scenarios
```

### Lint/Format (if implemented):
```bash
# Add linting commands when available
python -m black .
python -m flake8 .
```

## Key Development Patterns

### Agent Creation Pattern
```python
agent = AssistantAgent(
    name="AgentName",
    model_client=model_client,
    description="Agent purpose for selector",
    system_message="Detailed instructions..."
)
```

### Data Models
All data structures use Pydantic dataclasses for validation:
- `ReadinessAssessment`
- `PositionAnalysis` 
- `STARExample`
- `ScoringResult`
- `CompetencyCheck`

### Workflow Execution
The system uses `SelectorGroupChat` for intelligent agent routing based on context and workflow stage.

## Success Criteria

Target metrics for resume quality:
- All examples score ≥4 in Context, Complexity, Initiative (1-7 scale)
- 100% coverage of Key Accountabilities
- 100% coverage of LC4Q competencies
- Professional presentation and format compliance

## QPS-Specific Requirements

The system is built specifically for Queensland Police Service with:
- LC4Q Leadership Competency Framework integration
- QPS-specific ranking and promotion criteria
- STAR methodology for example structuring
- Multi-agent scoring against QPS assessment rubrics

## Testing Strategy

The test suite includes:
- Quick validation tests
- Full scenario testing (Senior Constable→Sergeant, Constable→Senior Constable)
- Error handling and edge case validation
- Multi-agent interaction verification

## Debugging Notes

- The system uses asyncio extensively - ensure proper await handling
- Agent conversations can be lengthy - monitor for timeout issues
- OpenAI API rate limits may affect performance with complex scenarios
- Use Console output for real-time monitoring of agent interactions