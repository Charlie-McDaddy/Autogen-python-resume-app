"""
Web Interface for QPS Resume Writing System
==========================================

A simple web interface using Streamlit for the resume writing system.
"""

import streamlit as st
import asyncio
import json
import os
from datetime import datetime
from resume_system import ResumeWritingSystem

# Configure Streamlit page
st.set_page_config(
    page_title="QPS Resume Writing System",
    page_icon="👮‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c5aa0;
        border-bottom: 2px solid #2c5aa0;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.375rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.375rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.375rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'resume_system' not in st.session_state:
        st.session_state.resume_system = None
    if 'system_initialized' not in st.session_state:
        st.session_state.system_initialized = False
    if 'resume_result' not in st.session_state:
        st.session_state.resume_result = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'workflow_stage' not in st.session_state:
        st.session_state.workflow_stage = 'input'  # input, initial_scoring, rewrite, feedback, final
    if 'initial_scoring' not in st.session_state:
        st.session_state.initial_scoring = None
    if 'rewritten_example' not in st.session_state:
        st.session_state.rewritten_example = None
    if 'user_feedback' not in st.session_state:
        st.session_state.user_feedback = ""
    if 'final_result' not in st.session_state:
        st.session_state.final_result = None

def check_api_key():
    """Check if OpenAI API key is available"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # Try to get from secrets (Streamlit Cloud)
        try:
            api_key = st.secrets["OPENAI_API_KEY"]
        except:
            return None
    return api_key

async def initialize_system():
    """Initialize the resume writing system"""
    try:
        api_key = check_api_key()
        if not api_key:
            st.error("⚠️ OpenAI API key not found. Please set OPENAI_API_KEY environment variable or add it to Streamlit secrets.")
            return False
        
        if not st.session_state.system_initialized:
            st.session_state.resume_system = ResumeWritingSystem(api_key=api_key)
            st.session_state.system_initialized = True
        
        return True
    except Exception as e:
        st.error(f"❌ Failed to initialize system: {str(e)}")
        return False

def display_header():
    """Display the main header"""
    st.markdown('<h1 class="main-header">👮‍♂️ QPS Resume Writing System</h1>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">Intelligent multi-agent system for creating compelling QPS promotion resumes</div>', unsafe_allow_html=True)

def collect_user_data():
    """Collect user data through the interface"""
    st.markdown('<h2 class="section-header">👤 Officer Information</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name", placeholder="e.g., John Smith")
        current_rank = st.selectbox(
            "Current Rank",
            ["Constable", "Senior Constable", "Sergeant", "Senior Sergeant", "Inspector"]
        )
        current_position = st.text_input("Current Position", placeholder="e.g., General Duties Officer")
        location = st.text_input("Current Location", placeholder="e.g., Brisbane")
    
    with col2:
        target_position = st.text_input("Target Position", placeholder="e.g., Sergeant - Team Leader")
        target_location = st.text_input("Target Location", placeholder="e.g., Gold Coast")
        years_experience = st.number_input("Years of Experience", min_value=1, max_value=40, value=5)
    
    st.markdown('<h3 class="section-header">💼 Job Example Input</h3>', unsafe_allow_html=True)
    
    job_example = st.text_area(
        "Describe a specific work example/situation you want to use in your resume:",
        height=150,
        placeholder="""Example: In 2023, as a Senior Constable at Brisbane Station, I was tasked with leading a community engagement initiative to address youth crime in the local area. The situation involved rising complaints from residents about antisocial behavior and petty theft by local youth. I coordinated with community leaders, schools, and youth services to develop a comprehensive engagement program..."""
    )
    
    return {
        "name": name,
        "current_rank": current_rank,
        "current_position": current_position,
        "location": location,
        "years_experience": years_experience,
        "target_position": target_position,
        "target_location": target_location,
        "job_example": job_example
    }

def collect_position_requirements():
    """Collect position requirements"""
    st.markdown('<h2 class="section-header">📄 Position Requirements</h2>', unsafe_allow_html=True)
    
    # Key Accountabilities
    st.markdown('<h3 class="section-header">🎯 Key Accountabilities</h3>', unsafe_allow_html=True)
    key_accountabilities = st.text_area(
        "List the key accountabilities for the target position:",
        height=150,
        key="key_accountabilities",
        placeholder="""Example:
- Lead strategic community engagement initiatives across the district
- Develop and mobilize team of community liaison officers  
- Build enduring relationships with community stakeholders
- Foster inclusive workplace culture reflecting community diversity
- Demonstrate sound governance in program management"""
    )
    
    # Position Description
    st.markdown('<h3 class="section-header">📋 Position Description</h3>', unsafe_allow_html=True)
    position_description = st.text_area(
        "Provide the general position description and operational requirements:",
        height=150,
        key="position_description",
        placeholder="""Example:
POSITION: Sergeant - Community Engagement Team Leader
LOCATION: Gold Coast District
REPORTS TO: Senior Sergeant - Operations

OPERATIONAL REQUIREMENTS:
- Supervise team of 8 community liaison officers
- Manage district-wide community engagement programs
- Coordinate with local government and community organizations
- Oversee budget management for community programs ($200k annually)"""
    )
    
    # LC4Q Competencies
    st.markdown('<h3 class="section-header">🏆 LC4Q Competencies Required</h3>', unsafe_allow_html=True)
    st.markdown("Copy and paste the specific LC4Q competencies required for this position and rank level:")
    
    lc4q_competencies = st.text_area(
        "LC4Q Competencies (copy from position description or competency framework):",
        height=200,
        key="lc4q_competencies",
        placeholder="""Example format:

Vision:
- Leads strategically
- Stimulates ideas and innovation  
- Makes insightful decisions

Results:
- Develops and mobilises talent
- Builds enduring relationships
- Drives accountability and outcomes

Accountability:
- Fosters healthy and inclusive workplaces
- Demonstrates sound governance
- Pursues continuous growth"""
    )
    
    return {
        "key_accountabilities": key_accountabilities,
        "position_description": position_description,
        "lc4q_competencies": lc4q_competencies
    }

async def score_initial_example(user_data, position_requirements):
    """Score the initial job example provided by the user"""
    try:
        if not await initialize_system():
            return None
        
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        
        progress_placeholder.progress(0.2)
        status_placeholder.info("📊 Scoring initial example...")
        
        result = await st.session_state.resume_system.score_initial_example(user_data, position_requirements)
        
        progress_placeholder.progress(1.0)
        status_placeholder.success("✅ Initial scoring completed!")
        
        return result
        
    except Exception as e:
        st.error(f"❌ Error during initial scoring: {str(e)}")
        return None

async def rewrite_example(user_data, position_requirements, initial_scores):
    """Rewrite the example to better meet position requirements"""
    try:
        if not await initialize_system():
            return None
        
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        
        progress_placeholder.progress(0.5)
        status_placeholder.info("✏️ Rewriting example to improve scores...")
        
        result = await st.session_state.resume_system.rewrite_example(user_data, position_requirements, initial_scores)
        
        progress_placeholder.progress(1.0)
        status_placeholder.success("✅ Example rewrite completed!")
        
        return result
        
    except Exception as e:
        st.error(f"❌ Error during example rewrite: {str(e)}")
        return None

async def process_final_resume(user_data, position_requirements, rewritten_example, user_feedback):
    """Process final resume with user feedback"""
    try:
        if not await initialize_system():
            return None
        
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        
        progress_placeholder.progress(0.8)
        status_placeholder.info("🔄 Processing with your feedback...")
        
        result = await st.session_state.resume_system.create_final_resume(
            user_data, position_requirements, rewritten_example, user_feedback
        )
        
        progress_placeholder.progress(1.0)
        status_placeholder.success("✅ Final resume completed!")
        
        return result
        
    except Exception as e:
        st.error(f"❌ Error during final processing: {str(e)}")
        return None

def display_initial_scoring(scoring_result):
    """Display initial scoring results"""
    if not scoring_result:
        return
    
    st.markdown('<h2 class="section-header">📊 Initial Example Scoring</h2>', unsafe_allow_html=True)
    
    # Display scores
    col1, col2, col3 = st.columns(3)
    
    with col1:
        context_score = scoring_result.get('context_score', 0)
        st.metric("Context Score", f"{context_score}/7", 
                 delta=f"Target: ≥4", delta_color="normal" if context_score >= 4 else "inverse")
    
    with col2:
        complexity_score = scoring_result.get('complexity_score', 0)
        st.metric("Complexity Score", f"{complexity_score}/7",
                 delta=f"Target: ≥4", delta_color="normal" if complexity_score >= 4 else "inverse")
    
    with col3:
        initiative_score = scoring_result.get('initiative_score', 0)
        st.metric("Initiative Score", f"{initiative_score}/7",
                 delta=f"Target: ≥4", delta_color="normal" if initiative_score >= 4 else "inverse")
    
    # Overall assessment
    overall_score = (context_score + complexity_score + initiative_score) / 3
    if overall_score >= 4:
        st.success(f"✅ Overall Score: {overall_score:.1f}/7 - Meets requirements!")
    else:
        st.warning(f"⚠️ Overall Score: {overall_score:.1f}/7 - Needs improvement")
    
    # Detailed feedback
    st.markdown("### 📝 Detailed Feedback")
    
    with st.expander("Context Scoring Details"):
        st.write(f"**Score:** {context_score}/7")
        st.write(f"**Feedback:** {scoring_result.get('context_feedback', 'No feedback available')}")
        if 'context_suggestions' in scoring_result:
            st.write("**Suggestions:**")
            for suggestion in scoring_result['context_suggestions']:
                st.write(f"• {suggestion}")
    
    with st.expander("Complexity Scoring Details"):
        st.write(f"**Score:** {complexity_score}/7")
        st.write(f"**Feedback:** {scoring_result.get('complexity_feedback', 'No feedback available')}")
        if 'complexity_suggestions' in scoring_result:
            st.write("**Suggestions:**")
            for suggestion in scoring_result['complexity_suggestions']:
                st.write(f"• {suggestion}")
    
    with st.expander("Initiative Scoring Details"):
        st.write(f"**Score:** {initiative_score}/7")
        st.write(f"**Feedback:** {scoring_result.get('initiative_feedback', 'No feedback available')}")
        if 'initiative_suggestions' in scoring_result:
            st.write("**Suggestions:**")
            for suggestion in scoring_result['initiative_suggestions']:
                st.write(f"• {suggestion}")

def display_rewritten_example(rewrite_result):
    """Display the rewritten example"""
    if not rewrite_result:
        return
    
    st.markdown('<h2 class="section-header">✏️ Improved Example</h2>', unsafe_allow_html=True)
    
    # LC4Q Category
    lc4q_category = rewrite_result.get('lc4q_category', 'Unknown')
    category_colors = {
        'Vision': '🔮',
        'Results': '🎯', 
        'Accountability': '⚖️'
    }
    category_icon = category_colors.get(lc4q_category, '📋')
    
    st.info(f"{category_icon} **Best LC4Q Fit:** {lc4q_category}")
    st.write(f"**Reasoning:** {rewrite_result.get('category_reasoning', 'No reasoning provided')}")
    
    # Display the rewritten example
    st.markdown("### 📝 Rewritten STAR Example")
    rewritten_example = rewrite_result.get('rewritten_example', {})
    
    st.markdown("**Year, Rank, Location:**")
    st.write(rewritten_example.get('year_rank_location', 'Not provided'))
    
    st.markdown("**Situation:**")
    st.write(rewritten_example.get('situation', 'Not provided'))
    
    st.markdown("**Task:**")
    st.write(rewritten_example.get('task', 'Not provided'))
    
    st.markdown("**Action:**")
    st.write(rewritten_example.get('action', 'Not provided'))
    
    st.markdown("**Result:**")
    st.write(rewritten_example.get('result', 'Not provided'))
    
    # Improvements made
    st.markdown("### 🔧 Key Improvements")
    improvements = rewrite_result.get('improvements_made', [])
    for improvement in improvements:
        st.write(f"✅ {improvement}")
    
    # New scores
    if 'improved_scores' in rewrite_result:
        st.markdown("### 📈 Projected Scores")
        improved_scores = rewrite_result['improved_scores']
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Context", f"{improved_scores.get('context', 0)}/7")
        with col2:
            st.metric("Complexity", f"{improved_scores.get('complexity', 0)}/7")
        with col3:
            st.metric("Initiative", f"{improved_scores.get('initiative', 0)}/7")

def collect_user_feedback():
    """Collect user feedback on the rewritten example"""
    st.markdown('<h2 class="section-header">💬 Your Feedback</h2>', unsafe_allow_html=True)
    
    st.markdown("Please review the rewritten example above and provide your feedback:")
    
    feedback = st.text_area(
        "What changes would you like to make? What aspects should be emphasized or modified?",
        height=150,
        key="user_feedback_input",
        placeholder="""Example feedback:
- Please emphasize the stakeholder management aspect more
- The result should mention specific metrics or outcomes
- Add more detail about the leadership challenges faced
- Highlight the innovation aspect of the solution
- Connect better to the target position requirements"""
    )
    
    return feedback

def display_results(result):
    """Display the resume creation results"""
    if not result:
        return
    
    st.markdown('<h2 class="section-header">📊 Results</h2>', unsafe_allow_html=True)
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Messages", result.get('total_turns', 0))
    
    with col2:
        st.metric("Status", "✅ Complete" if result.get('success', False) else "❌ Error")
    
    with col3:
        st.metric("Stop Reason", result.get('stop_reason', 'Unknown'))
    
    # Messages
    if 'messages' in result and result['messages']:
        st.markdown('<h3 class="section-header">💬 Agent Conversations</h3>', unsafe_allow_html=True)
        
        # Create expandable sections for messages
        for i, message in enumerate(result['messages']):
            with st.expander(f"Message {i+1}: {getattr(message, 'source', 'Unknown')}"):
                st.write(f"**Content:** {getattr(message, 'content', 'No content')}")
                if hasattr(message, 'metadata'):
                    st.write(f"**Metadata:** {message.metadata}")
    
    # Download option
    st.markdown('<h3 class="section-header">💾 Download Results</h3>', unsafe_allow_html=True)
    
    # Prepare download data
    download_data = {
        "timestamp": datetime.now().isoformat(),
        "user_data": st.session_state.get('user_data', {}),
        "result": {
            "success": result.get('success', False),
            "total_turns": result.get('total_turns', 0),
            "stop_reason": result.get('stop_reason', 'Unknown'),
            "messages": [str(msg) for msg in result.get('messages', [])]
        }
    }
    
    st.download_button(
        label="📥 Download Results (JSON)",
        data=json.dumps(download_data, indent=2),
        file_name=f"qps_resume_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

def display_sidebar():
    """Display sidebar with system information"""
    with st.sidebar:
        st.markdown("### 🔧 System Information")
        
        # API key status
        api_key = check_api_key()
        if api_key:
            st.success("✅ API Key Configured")
        else:
            st.error("❌ API Key Missing")
        
        # System status
        if st.session_state.system_initialized:
            st.success("✅ System Initialized")
        else:
            st.warning("⚠️ System Not Initialized")
        
        st.markdown("---")
        
        st.markdown("### 📋 Workflow Steps")
        
        # Show current stage
        stages = {
            'input': '📝 Step 1: Input Information',
            'initial_scoring': '📊 Step 2: Initial Scoring', 
            'rewrite': '✏️ Step 3: Improve Example',
            'feedback': '💬 Step 4: Your Feedback',
            'final': '🎯 Step 5: Final Resume'
        }
        
        current_stage = st.session_state.workflow_stage
        for stage_key, stage_name in stages.items():
            if stage_key == current_stage:
                st.success(f"**{stage_name}** ← Current")
            else:
                st.write(stage_name)
        
        st.markdown("---")
        st.markdown("### 🎯 Enhanced Process")
        st.markdown("""
        1. **Input** - Provide job example and position details
        2. **Initial Scoring** - Score your example (Context/Complexity/Initiative)
        3. **Improvement** - AI rewrites example + identifies LC4Q category
        4. **Feedback** - Provide your input for refinements
        5. **Final Resume** - Complete multi-agent processing
        """)
        
        st.markdown("---")
        
        st.markdown("### 🎯 Success Criteria")
        st.markdown("""
        - All examples score ≥4 in all areas
        - 100% Key Accountability coverage
        - 100% LC4Q competency coverage
        - Professional presentation
        - Clear transferable skills
        """)

def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Display header
    display_header()
    
    # Display sidebar
    display_sidebar()
    
    # Main content - Enhanced workflow with stages
    if st.session_state.workflow_stage == 'input':
        display_input_stage()
    elif st.session_state.workflow_stage == 'initial_scoring':
        display_scoring_stage()
    elif st.session_state.workflow_stage == 'rewrite':
        display_rewrite_stage()
    elif st.session_state.workflow_stage == 'feedback':
        display_feedback_stage()
    elif st.session_state.workflow_stage == 'final':
        display_final_stage()

def display_input_stage():
    """Display the input collection stage"""
    st.markdown('<h1 class="main-header">📝 Step 1: Provide Your Information</h1>', unsafe_allow_html=True)
    
    # Collect user data
    user_data = collect_user_data()
    
    # Collect position requirements
    position_requirements = collect_position_requirements()
    
    # Validation
    if not user_data["name"] or not position_requirements["key_accountabilities"] or not position_requirements["position_description"] or not position_requirements["lc4q_competencies"]:
        st.warning("⚠️ Please fill in all required fields before proceeding.")
        return
    
    # Store in session state
    st.session_state.user_data = user_data
    st.session_state.position_requirements = position_requirements
    
    # Next step button
    if st.button("📊 Score My Example", type="primary", disabled=st.session_state.processing):
        st.session_state.workflow_stage = 'initial_scoring'
        st.rerun()

def display_scoring_stage():
    """Display the initial scoring stage"""
    st.markdown('<h1 class="main-header">📊 Step 2: Initial Example Scoring</h1>', unsafe_allow_html=True)
    
    if st.session_state.initial_scoring is None:
        if st.button("🔍 Analyze My Example", type="primary", disabled=st.session_state.processing):
            st.session_state.processing = True
            
            with st.spinner("Analyzing your example... This may take a minute."):
                result = asyncio.run(score_initial_example(
                    st.session_state.user_data, 
                    st.session_state.position_requirements
                ))
                st.session_state.initial_scoring = result
            
            st.session_state.processing = False
            st.rerun()
    else:
        # Display scoring results
        display_initial_scoring(st.session_state.initial_scoring)
        
        # Next step buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Back to Edit", type="secondary"):
                st.session_state.workflow_stage = 'input'
                st.rerun()
        with col2:
            if st.button("✏️ Improve Example", type="primary"):
                st.session_state.workflow_stage = 'rewrite'
                st.rerun()

def display_rewrite_stage():
    """Display the example rewrite stage"""
    st.markdown('<h1 class="main-header">✏️ Step 3: Improve Your Example</h1>', unsafe_allow_html=True)
    
    if st.session_state.rewritten_example is None:
        if st.button("🔧 Rewrite My Example", type="primary", disabled=st.session_state.processing):
            st.session_state.processing = True
            
            with st.spinner("Rewriting your example... This may take a few minutes."):
                result = asyncio.run(rewrite_example(
                    st.session_state.user_data,
                    st.session_state.position_requirements,
                    st.session_state.initial_scoring
                ))
                st.session_state.rewritten_example = result
            
            st.session_state.processing = False
            st.rerun()
    else:
        # Display rewritten example
        display_rewritten_example(st.session_state.rewritten_example)
        
        # Next step buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Back to Scoring", type="secondary"):
                st.session_state.workflow_stage = 'initial_scoring'
                st.rerun()
        with col2:
            if st.button("💬 Provide Feedback", type="primary"):
                st.session_state.workflow_stage = 'feedback'
                st.rerun()

def display_feedback_stage():
    """Display the user feedback stage"""
    st.markdown('<h1 class="main-header">💬 Step 4: Your Feedback</h1>', unsafe_allow_html=True)
    
    # Show the rewritten example for reference
    with st.expander("📖 Review Rewritten Example", expanded=False):
        display_rewritten_example(st.session_state.rewritten_example)
    
    # Collect feedback
    feedback = collect_user_feedback()
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⬅️ Back to Review", type="secondary"):
            st.session_state.workflow_stage = 'rewrite'
            st.rerun()
    
    with col2:
        if st.button("✅ No Changes Needed", type="secondary"):
            st.session_state.user_feedback = ""
            st.session_state.workflow_stage = 'final'
            st.rerun()
    
    with col3:
        if st.button("🔄 Apply Feedback", type="primary", disabled=not feedback):
            st.session_state.user_feedback = feedback
            st.session_state.workflow_stage = 'final'
            st.rerun()

def display_final_stage():
    """Display the final processing stage"""
    st.markdown('<h1 class="main-header">🎯 Step 5: Final Resume</h1>', unsafe_allow_html=True)
    
    if st.session_state.final_result is None:
        # Show what will be processed
        if st.session_state.user_feedback:
            st.info(f"📝 **Your Feedback:** {st.session_state.user_feedback}")
        else:
            st.info("✅ Processing with the improved example (no additional changes requested)")
        
        if st.button("🚀 Generate Final Resume", type="primary", disabled=st.session_state.processing):
            st.session_state.processing = True
            
            with st.spinner("Creating your final resume... This may take several minutes."):
                result = asyncio.run(process_final_resume(
                    st.session_state.user_data,
                    st.session_state.position_requirements,
                    st.session_state.rewritten_example,
                    st.session_state.user_feedback
                ))
                st.session_state.final_result = result
            
            st.session_state.processing = False
            st.rerun()
    else:
        # Display final results
        st.success("✅ Your resume has been completed!")
        display_results(st.session_state.final_result)
        
        # Option to start over
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Start Over", type="secondary"):
                # Reset all session state
                for key in ['workflow_stage', 'initial_scoring', 'rewritten_example', 'user_feedback', 'final_result']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.session_state.workflow_stage = 'input'
                st.rerun()
        
        with col2:
            if st.button("💬 Provide More Feedback", type="primary"):
                st.session_state.workflow_stage = 'feedback'
                st.session_state.final_result = None  # Clear to allow re-processing
                st.rerun()

if __name__ == "__main__":
    main()