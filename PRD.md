# Product Requirements Document: QPS Resume Writing Multi-Agent System

## 1. Executive Summary

### 1.1 Product Overview
A sophisticated multi-agent AI system designed to assist Queensland Police Service (QPS) officers in writing compelling resumes for internal promotions. The system employs 12 specialized Autogen agents that collaborate to ensure resume examples meet all assessment criteria and achieve competitive scores.

### 1.2 Objectives
- Automate the complex QPS resume writing process
- Ensure consistent high-quality output scoring ≥4 (adequate) in all categories
- Reduce resume preparation time from days to hours
- Increase shortlisting success rates for QPS officers

### 1.3 Success Metrics
- 90% of examples score ≥4 in Context, Complexity, and Initiative
- 100% coverage of relevant Key Accountabilities (KAs)
- 100% coverage of required LC4Q competencies
- User satisfaction rating ≥4.5/5
- Average time to complete resume <4 hours

## 2. System Architecture

### 2.1 Agent Hierarchy

```
┌─────────────────────────────────────┐
│      Orchestrator Agent             │
│   (Process Management & Flow)       │
└──────────────┬──────────────────────┘
               │
    ┌──────────┴──────────┬─────────────┬──────────────┐
    │                     │             │              │
┌───▼────────┐  ┌────────▼────────┐  ┌─▼──────────┐  ┌─▼────────────┐
│ Readiness  │  │Position Analysis│  │  Example   │  │    STAR      │
│Assessment  │  │     Agent       │  │ Selection  │  │   Writing    │
│   Agent    │  │                 │  │   Agent    │  │    Agent     │
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

### 2.2 Agent Communication Protocol
- **Message Format**: JSON-based structured data
- **Communication Type**: Asynchronous with callback mechanisms
- **State Management**: Shared context store for user data and progress
- **Error Handling**: Graceful degradation with fallback options

## 3. Detailed Agent Specifications

### 3.1 Orchestrator Agent

**Role**: Process coordinator and user interface

**Responsibilities**:
- Initialize user session and collect basic information
- Manage agent workflow and sequencing
- Maintain conversation state and context
- Handle error recovery and retries
- Present final output to user

**Key Functions**:
```python
- initialize_session(user_data)
- route_to_agent(agent_name, task_data)
- aggregate_feedback(agent_responses)
- manage_revision_cycles()
- generate_final_report()
```

**Success Criteria**:
- Smooth user experience with clear progress indicators
- No dropped tasks or lost data
- Efficient routing with <2s latency between agents

### 3.2 Readiness Assessment Agent

**Role**: Evaluate user's preparedness for promotion

**Input Requirements**:
- Current rank and position
- Years of experience
- Recent performance indicators
- Career aspirations

**Key Questions to Assess**:
1. Daily task mastery and efficiency
2. Frequency of positive feedback
3. Peer consultation patterns
4. Initiative-taking behaviors
5. Leadership style alignment
6. Self-belief in capabilities

**Output Format**:
```json
{
  "readiness_score": 0-10,
  "strengths": [],
  "development_areas": [],
  "recommendation": "proceed|develop|wait",
  "feedback": "detailed text"
}
```

### 3.3 Position Analysis Agent

**Role**: Parse and interpret position requirements

**Input Requirements**:
- Position Description (PDF/text)
- Key Accountabilities
- Position/Locality Profile

**Core Functions**:
- Extract and categorize Key Accountabilities
- Map KAs to LC4Q areas (Vision/Results/Accountability)
- Identify location-specific requirements
- Highlight demographic considerations
- Extract operational priorities

**Output Format**:
```json
{
  "position_title": "",
  "rank_level": "",
  "key_accountabilities": {
    "vision": [],
    "results": [],
    "accountability": []
  },
  "location_factors": {},
  "required_competencies": {},
  "operational_priorities": []
}
```

### 3.4 Example Selection Agent

**Role**: Guide users in selecting appropriate work examples

**Process Steps**:
1. Review user's experience inventory
2. Match experiences to KAs
3. Assess example relevance and strength
4. Identify coverage gaps
5. Recommend example combinations

**Evaluation Criteria**:
- Direct relevance to position
- Complexity appropriate to rank
- Recency and currency
- Diversity of skills demonstrated
- Transferability potential

**Output Format**:
```json
{
  "recommended_examples": {
    "vision": [],
    "results": [],
    "accountability": []
  },
  "coverage_analysis": {},
  "gaps_identified": [],
  "improvement_suggestions": []
}
```

### 3.5 STAR Writing Agent

**Role**: Structure examples using STAR methodology

**Components**:
- **Situation**: 1-2 lines context
- **Task**: 1-2 lines challenge/requirement
- **Action**: Detailed HOW with leadership skills
- **Result**: Concrete outcomes with strategic links

**Key Requirements**:
- Incorporate WHAT (technical skills)
- Emphasize HOW (LC4Q behaviors)
- Connect to WHY (strategic impact)
- Maintain professional tone
- Stay within word limits

**Output Format**:
```json
{
  "formatted_example": {
    "year_rank_location": "",
    "situation": "",
    "task": "",
    "action": "",
    "result": ""
  },
  "word_count": 0,
  "competencies_demonstrated": []
}
```

### 3.6 Context Scoring Agent

**Role**: Evaluate contextual relevance (1-7 scale)

**Evaluation Criteria**:
- Direct alignment with Key Accountabilities
- Relevance to position location
- Demographic considerations addressed
- Operational priorities reflected
- Transferable skills articulated

**Scoring Rubric**:
- 1-2: Very Limited/Limited - Not relevant
- 3: Basic - Some relevance
- 4: Adequate - Meets requirements
- 5: Proficient - All elements present
- 6: Very Proficient - Above level
- 7: Advanced - Significantly above

**Output Format**:
```json
{
  "context_score": 1-7,
  "strengths": [],
  "weaknesses": [],
  "improvement_suggestions": [],
  "specific_feedback": ""
}
```

### 3.7 Complexity Scoring Agent

**Role**: Assess example complexity relative to rank

**Evaluation Factors**:
- Stakeholder complexity (internal/external/competing)
- Problem-solving sophistication
- Resource management scale
- Timeline and deadline pressures
- Risk and impact levels
- Decision-making autonomy

**Output Format**:
```json
{
  "complexity_score": 1-7,
  "complexity_elements": {},
  "rank_alignment": "below|at|above",
  "enhancement_suggestions": []
}
```

### 3.8 Initiative Scoring Agent

**Role**: Measure proactive leadership behaviors

**Key Indicators**:
- Self-initiated vs assigned tasks
- Innovation and creative solutions
- Process improvements implemented
- Proactive problem identification
- Independent decision-making
- Going beyond expectations

**Output Format**:
```json
{
  "initiative_score": 1-7,
  "proactive_elements": [],
  "reactive_elements": [],
  "enhancement_opportunities": []
}
```

### 3.9 Vision Agent (LC4Q)

**Role**: Ensure Vision competencies are demonstrated

**Competencies to Verify**:
- Leads strategically
- Stimulates ideas and innovation
- Leads change in complex environments
- Makes insightful decisions

**Behavioral Indicators by Rank**:
- Stored in knowledge base
- Rank-specific requirements
- Examples of strong evidence

**Output Format**:
```json
{
  "competencies_covered": {},
  "gaps": [],
  "behavioral_evidence": {},
  "suggestions": []
}
```

### 3.10 Results Agent (LC4Q)

**Role**: Validate Results competencies

**Competencies to Verify**:
- Develops and mobilises talent
- Builds enduring relationships
- Inspires others
- Drives accountability and outcomes

**Focus Areas**:
- Team leadership evidence
- Stakeholder engagement quality
- Motivational leadership
- Outcome achievement

### 3.11 Accountability Agent (LC4Q)

**Role**: Ensure Accountability competencies

**Competencies to Verify**:
- Fosters healthy and inclusive workplaces
- Pursues continuous growth
- Demonstrates sound governance

**Special Attention**:
- Wellbeing initiatives
- Personal development
- Ethics and compliance
- Risk management

### 3.12 Transferable Skills Agent

**Role**: Articulate transferable skills explicitly

**Key Functions**:
- Identify implicit transferable skills
- Write clear transferability statements
- Connect to new position requirements
- Address location/demographic differences

**Output Format**:
```json
{
  "transferable_skills": [],
  "skill_statements": [],
  "relevance_mapping": {},
  "credibility_score": 0-10
}
```

### 3.13 Quality Assurance Agent

**Role**: Final review and polish

**Checklist Items**:
- Grammar and spelling
- Professional tone
- Word count compliance
- Format requirements
- All criteria addressed
- No missing sections
- Clear structure
- Compelling narrative

## 4. User Journey

### 4.1 Onboarding Flow
1. Welcome and system introduction
2. Current position and target role input
3. Upload Position Description and Profile
4. Readiness assessment questionnaire
5. Experience inventory collection

### 4.2 Example Development Flow
1. Position analysis and requirements mapping
2. Example selection guidance
3. STAR writing for each example
4. Competency verification
5. Scoring evaluation
6. Revision cycles based on scores
7. Transferable skills enhancement

### 4.3 Finalization Flow
1. Quality assurance review
2. Final scoring summary
3. Generate 2-page formatted response
4. Provide improvement roadmap
5. Save session for future reference

## 5. Technical Requirements

### 5.1 Autogen Configuration
```python
# Agent configuration example
context_scoring_agent = AssistantAgent(
    name="Context_Scoring_Agent",
    system_message="""You are an expert at evaluating 
    contextual relevance for QPS positions...""",
    llm_config={
        "temperature": 0.3,
        "model": "gpt-4",
        "timeout": 600,
    }
)
```

### 5.2 Knowledge Base Requirements
- Complete QPS Resume Writing guide
- LC4Q behavioral indicators by rank
- Scoring rubrics and examples
- Common pitfalls database
- Successful example library

### 5.3 Integration Points
- PDF parsing for Position Descriptions
- Document generation for final output
- Session storage for progress saving
- Analytics for success tracking

## 6. Data Flow

### 6.1 Information Architecture
```
User Input → Position Analysis → Requirements Mapping
     ↓              ↓                    ↓
Experience → Example Selection → STAR Writing
     ↓              ↓                    ↓
Drafts → Scoring Evaluation → Competency Check
     ↓              ↓                    ↓
Revisions → Quality Assurance → Final Output
```

### 6.2 State Management
- User profile and progress
- Position requirements cache
- Example drafts and revisions
- Scoring history
- Feedback accumulation

## 7. Performance Requirements

### 7.1 Response Times
- Agent response: <5 seconds
- Full example evaluation: <30 seconds
- Complete session: <4 hours
- Final generation: <1 minute

### 7.2 Quality Metrics
- First-pass score ≥4: 70% target
- Final score ≥4: 95% target
- Competency coverage: 100%
- User satisfaction: ≥4.5/5

## 8. Risk Management

### 8.1 Technical Risks
- LLM API failures: Implement retry logic
- Context length limits: Chunk management
- Inconsistent scoring: Calibration protocols

### 8.2 User Experience Risks
- Overwhelming complexity: Progressive disclosure
- Generic outputs: Personalization emphasis
- Lost progress: Auto-save functionality

## 9. Future Enhancements

### 9.1 Phase 2 Features
- Interview preparation agent
- Historical success pattern analysis
- Peer comparison benchmarking
- Panel feedback integration

### 9.2 Phase 3 Features
- Voice interaction capability
- Real-time collaboration
- Mobile application
- Integration with HR systems

## 10. Success Criteria

### 10.1 Launch Metrics
- 100 successful resumes generated
- 80% user completion rate
- <5% critical error rate
- 4.5+ average user rating

### 10.2 Long-term Metrics
- 25% improvement in shortlisting rates
- 50% reduction in resume preparation time
- 90% user recommendation rate
- Positive ROI within 6 months