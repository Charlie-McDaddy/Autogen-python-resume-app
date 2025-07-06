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
import PyPDF2
from docx import Document
import io

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

def extract_text_from_pdf(uploaded_file):
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"Error reading PDF file: {str(e)}")
        return None

def extract_text_from_docx(uploaded_file):
    """Extract text from uploaded DOCX file"""
    try:
        doc = Document(uploaded_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"Error reading DOCX file: {str(e)}")
        return None

def extract_text_from_txt(uploaded_file):
    """Extract text from uploaded TXT file"""
    try:
        # Convert bytes to string
        text = str(uploaded_file.read(), "utf-8")
        return text.strip()
    except Exception as e:
        st.error(f"Error reading TXT file: {str(e)}")
        return None

def process_uploaded_file(uploaded_file):
    """Process uploaded file and extract text based on file type"""
    if uploaded_file is None:
        return None
    
    file_type = uploaded_file.type
    file_name = uploaded_file.name.lower()
    
    if file_type == "application/pdf" or file_name.endswith('.pdf'):
        return extract_text_from_pdf(uploaded_file)
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or file_name.endswith('.docx'):
        return extract_text_from_docx(uploaded_file)
    elif file_type == "text/plain" or file_name.endswith('.txt'):
        return extract_text_from_txt(uploaded_file)
    else:
        st.error(f"Unsupported file type: {file_type}. Please upload PDF, DOCX, or TXT files.")
        return None

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
    st.markdown('<h2 class="section-header">💼 Job Example Input</h2>', unsafe_allow_html=True)
    
    job_example = st.text_area(
        "Describe a specific work example/situation you want to use in your resume:",
        height=150,
        placeholder="""Example: In 2023, as a Senior Constable at Brisbane Station, I was tasked with leading a community engagement initiative to address youth crime in the local area. The situation involved rising complaints from residents about antisocial behavior and petty theft by local youth. I coordinated with community leaders, schools, and youth services to develop a comprehensive engagement program..."""
    )
    
    return {
        "job_example": job_example
    }

def collect_position_requirements():
    """Collect position requirements"""
    st.markdown('<h2 class="section-header">📄 Position Requirements</h2>', unsafe_allow_html=True)
    
    # Key Accountabilities
    st.markdown('<h3 class="section-header">🎯 Key Accountabilities</h3>', unsafe_allow_html=True)
    
    # Option to choose input method
    ka_input_method = st.radio(
        "How would you like to provide Key Accountabilities?",
        ["Type/Paste Text", "Upload File"],
        key="ka_input_method",
        horizontal=True
    )
    
    key_accountabilities = ""
    if ka_input_method == "Type/Paste Text":
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
    else:
        uploaded_ka_file = st.file_uploader(
            "Upload Key Accountabilities file (PDF, DOCX, or TXT)",
            type=['pdf', 'docx', 'txt'],
            key="ka_file_uploader"
        )
        if uploaded_ka_file is not None:
            extracted_text = process_uploaded_file(uploaded_ka_file)
            if extracted_text:
                key_accountabilities = extracted_text
                st.success(f"✅ Successfully extracted text from {uploaded_ka_file.name}")
                with st.expander("Preview extracted text"):
                    st.text_area("Extracted Key Accountabilities:", value=extracted_text, height=150, disabled=True)
    
    # Position Description
    st.markdown('<h3 class="section-header">📋 Position Description</h3>', unsafe_allow_html=True)
    
    # Option to choose input method
    pd_input_method = st.radio(
        "How would you like to provide Position Description?",
        ["Type/Paste Text", "Upload File"],
        key="pd_input_method",
        horizontal=True
    )
    
    position_description = ""
    if pd_input_method == "Type/Paste Text":
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
    else:
        uploaded_pd_file = st.file_uploader(
            "Upload Position Description file (PDF, DOCX, or TXT)",
            type=['pdf', 'docx', 'txt'],
            key="pd_file_uploader"
        )
        if uploaded_pd_file is not None:
            extracted_text = process_uploaded_file(uploaded_pd_file)
            if extracted_text:
                position_description = extracted_text
                st.success(f"✅ Successfully extracted text from {uploaded_pd_file.name}")
                with st.expander("Preview extracted text"):
                    st.text_area("Extracted Position Description:", value=extracted_text, height=150, disabled=True)
    
    # LC4Q Competencies
    st.markdown('<h3 class="section-header">🏆 LC4Q Competencies Required</h3>', unsafe_allow_html=True)
    
    # Option to choose input method
    lc4q_input_method = st.radio(
        "How would you like to provide LC4Q Competencies?",
        ["Type/Paste Text", "Upload File"],
        key="lc4q_input_method",
        horizontal=True
    )
    
    lc4q_competencies = ""
    if lc4q_input_method == "Type/Paste Text":
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
    else:
        uploaded_lc4q_file = st.file_uploader(
            "Upload LC4Q Competencies file (PDF, DOCX, or TXT)",
            type=['pdf', 'docx', 'txt'],
            key="lc4q_file_uploader"
        )
        if uploaded_lc4q_file is not None:
            extracted_text = process_uploaded_file(uploaded_lc4q_file)
            if extracted_text:
                lc4q_competencies = extracted_text
                st.success(f"✅ Successfully extracted text from {uploaded_lc4q_file.name}")
                with st.expander("Preview extracted text"):
                    st.text_area("Extracted LC4Q Competencies:", value=extracted_text, height=200, disabled=True)
    
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
        st.write("🔍 **Diagnostic Information:**")
        
        # 1. Validate input data with detailed logging
        st.write("**Step 1: Input Validation**")
        if not user_data:
            st.error("❌ Missing user data")
            return None
        if not position_requirements:
            st.error("❌ Missing position requirements")
            return None
        if not rewritten_example:
            st.error("❌ Missing rewritten example")
            return None
            
        st.success("✅ All input data present")
        st.write(f"- User data keys: {list(user_data.keys())}")
        st.write(f"- Position req keys: {list(position_requirements.keys())}")
        st.write(f"- Rewritten example keys: {list(rewritten_example.keys())}")
        st.write(f"- User feedback length: {len(user_feedback) if user_feedback else 0}")
        
        # 2. Check event loop status
        st.write("**Step 2: Event Loop Diagnostics**")
        try:
            import asyncio
            current_loop = None
            try:
                current_loop = asyncio.get_running_loop()
                st.warning(f"⚠️ Event loop already running: {current_loop}")
                st.write("This may cause asyncio.run() conflicts")
            except RuntimeError:
                st.success("✅ No running event loop detected")
        except Exception as e:
            st.error(f"❌ Event loop check failed: {e}")
        
        # 3. System initialization check
        st.write("**Step 3: System Initialization**")
        if not await initialize_system():
            st.error("❌ Failed to initialize system")
            return None
        st.success("✅ System initialization successful")
        
        # 4. Check system state
        st.write("**Step 4: System State Validation**")
        if not st.session_state.resume_system:
            st.error("❌ Resume system not initialized in session state")
            return None
        st.success("✅ Resume system found in session state")
        
        # 5. Check AutoGen team status
        st.write("**Step 5: AutoGen Team Diagnostics**")
        try:
            team = st.session_state.resume_system.team
            agents = st.session_state.resume_system.agents
            # SelectorGroupChat uses _participants, not participants
            participant_count = len(getattr(team, '_participants', []))
            st.success(f"✅ Team initialized with {participant_count} participants")
            st.write(f"- Available agents: {list(agents.keys())}")
            st.write(f"- Team type: {type(team).__name__}")
        except Exception as e:
            st.error(f"❌ AutoGen team check failed: {e}")
            return None
        
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        
        progress_placeholder.progress(0.1)
        status_placeholder.info("🔄 Starting final processing...")
        
        progress_placeholder.progress(0.3)
        status_placeholder.info("🔄 Calling create_final_resume...")
        
        # 6. Attempt the actual processing with timeout
        st.write("**Step 6: Final Resume Processing**")
        try:
            # Add timeout to prevent hanging
            result = await asyncio.wait_for(
                st.session_state.resume_system.create_final_resume(
                    user_data, position_requirements, rewritten_example, user_feedback
                ),
                timeout=300  # 5 minute timeout
            )
            
            progress_placeholder.progress(1.0)
            status_placeholder.success("✅ Final resume completed!")
            st.success("✅ Processing completed successfully!")
            
            return result
            
        except asyncio.TimeoutError:
            st.error("❌ Processing timed out after 5 minutes")
            return None
        except Exception as e:
            st.error(f"❌ Processing failed: {type(e).__name__}: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
            return None
        
    except Exception as e:
        st.error(f"❌ Diagnostic error: {type(e).__name__}: {str(e)}")
        st.write("**Full error details:**")
        import traceback
        st.code(traceback.format_exc())
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
    
    st.markdown('<h2 class="section-header">✏️ Enhanced Example (Australian English)</h2>', unsafe_allow_html=True)
    
    # Show original example for comparison
    if 'original_example' in rewrite_result:
        with st.expander("📖 View Original Example for Comparison"):
            st.write("**Your Original Example:**")
            st.write(rewrite_result['original_example'])
    
    # Show raw agent content for debugging if available
    if 'raw_agent_content' in rewrite_result and rewrite_result['raw_agent_content']:
        with st.expander("🔍 Agent Content Analysis", expanded=False):
            st.write("**Agent responses received:**")
            for i, agent_data in enumerate(rewrite_result['raw_agent_content']):
                st.write(f"**{agent_data['source']}** ({agent_data['length']} chars)")
                st.code(agent_data['content'])
                st.write("---")
    
    # Show the longest agent response if available
    if 'longest_agent_response' in rewrite_result:
        longest = rewrite_result['longest_agent_response']
        st.markdown("### 📝 Primary Agent Response")
        st.write(f"**Source:** {longest['source']}")
        
        # Try to format the content nicely
        content = longest['content']
        if 'situation:' in content.lower() or 'task:' in content.lower():
            # It's already in STAR format
            st.markdown(content)
        else:
            # Show as formatted text
            st.write(content)
        
        st.markdown("---")
    
    # Check if we have agent messages to parse
    if 'messages' in rewrite_result and rewrite_result['messages']:
        with st.expander("🤖 Complete Agent Conversation", expanded=False):
            st.write(f"**Total messages:** {len(rewrite_result['messages'])}")
            
            for i, message in enumerate(rewrite_result['messages']):
                message_content = getattr(message, 'content', str(message))
                message_source = getattr(message, 'source', f'Agent {i+1}')
                
                if len(message_content) > 50:  # Only show meaningful messages
                    st.write(f"**Message {i+1} - {message_source}:**")
                    st.code(message_content)
                    st.write("---")
    
    # Try to show structured results first, then fallback to raw content
    has_structured_content = False
    
    # If we have structured results, display them
    if 'lc4q_category' in rewrite_result and 'rewritten_example' in rewrite_result:
        # Check if the rewritten example has actual content (not just defaults)
        example = rewrite_result.get('rewritten_example', {})
        if (example.get('situation', '') not in ['Enhanced situation context', 'From original example'] and
            len(example.get('situation', '')) > 50):
            has_structured_content = True
    
    if has_structured_content:
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
        
        # Display the rewritten example if available
        if 'rewritten_example' in rewrite_result:
            st.markdown("### 📝 Enhanced STAR Example")
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
            if 'improvements_made' in rewrite_result:
                st.markdown("### 🔧 Key Enhancements")
                improvements = rewrite_result.get('improvements_made', [])
                for improvement in improvements:
                    st.write(f"✅ {improvement}")
            
            # New scores
            if 'improved_scores' in rewrite_result:
                st.markdown("### 📈 Target Scores (6-7 Level)")
                improved_scores = rewrite_result['improved_scores']
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    score = improved_scores.get('context', 0)
                    st.metric("Context", f"{score}/7",
                             delta="Very Proficient" if score >= 6 else "Needs Enhancement",
                             delta_color="normal" if score >= 6 else "inverse")
                with col2:
                    score = improved_scores.get('complexity', 0)
                    st.metric("Complexity", f"{score}/7",
                             delta="Very Proficient" if score >= 6 else "Needs Enhancement",
                             delta_color="normal" if score >= 6 else "inverse")
                with col3:
                    score = improved_scores.get('initiative', 0)
                    st.metric("Initiative", f"{score}/7",
                             delta="Very Proficient" if score >= 6 else "Needs Enhancement",
                             delta_color="normal" if score >= 6 else "inverse")
    
    else:
        # Fallback: Show the actual agent content since structured extraction failed
        st.warning("⚠️ **Structured content extraction incomplete.** Showing agent-generated content below:")
        
        if 'messages' in rewrite_result and rewrite_result['messages']:
            # Find and display the most relevant agent outputs
            for message in rewrite_result['messages']:
                content = getattr(message, 'content', str(message))
                source = getattr(message, 'source', 'Unknown')
                
                # Show content from key agents that likely contains the rewritten example
                if source in ['STARWriting', 'Orchestrator'] and len(content) > 200:
                    st.markdown(f"### 📝 Enhanced Example from {source}")
                    
                    # Try to format the content nicely
                    if 'situation:' in content.lower() or 'task:' in content.lower():
                        # It's already in STAR format
                        st.markdown(content)
                    else:
                        # Show as formatted text
                        st.write(content)
                    
                    st.markdown("---")
        
        # Show the default structured view as backup
        if 'rewritten_example' in rewrite_result:
            st.markdown("### 📋 Extracted Structure (May Need Manual Review)")
            example = rewrite_result['rewritten_example']
            
            st.markdown("**Year, Rank, Location:**")
            st.write(example.get('year_rank_location', 'Not extracted'))
            
            st.markdown("**Situation:**")
            st.write(example.get('situation', 'Not extracted'))
            
            st.markdown("**Task:**")
            st.write(example.get('task', 'Not extracted'))
            
            st.markdown("**Action:**")
            st.write(example.get('action', 'Not extracted'))
            
            st.markdown("**Result:**")
            st.write(example.get('result', 'Not extracted'))
    
    # Enhancement notice
    st.success("🇦🇺 **Australian Language Applied:** The enhanced example uses Australian spelling (organised, realised, recognised) and professional Australian public service terminology.")

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
    
    st.markdown('<h2 class="section-header">🎯 Your Final Resume</h2>', unsafe_allow_html=True)
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        feedback_status = "✅ Applied" if result.get('feedback_incorporated', False) else "➖ None"
        st.metric("User Feedback", feedback_status)
    
    with col2:
        st.metric("Status", "✅ Complete" if result.get('success', False) else "❌ Error")
    
    with col3:
        final_example = result.get('final_example', {})
        lc4q_category = final_example.get('lc4q_category', 'Unknown')
        st.metric("LC4Q Category", lc4q_category)
    
    # Display user feedback if applied
    if result.get('user_feedback_applied'):
        st.info(f"📝 **Applied Feedback:** {result['user_feedback_applied']}")
    
    # Display the final example
    if 'final_example' in result and 'rewritten_example' in result['final_example']:
        st.markdown('<h3 class="section-header">📝 Your Enhanced STAR Example</h3>', unsafe_allow_html=True)
        
        final_example = result['final_example']
        rewritten_example = final_example['rewritten_example']
        
        # LC4Q Category with icon
        lc4q_category = final_example.get('lc4q_category', 'Unknown')
        category_colors = {
            'Vision': '🔮',
            'Results': '🎯',
            'Accountability': '⚖️'
        }
        category_icon = category_colors.get(lc4q_category, '📋')
        
        st.success(f"{category_icon} **LC4Q Competency Area:** {lc4q_category}")
        
        # Display the STAR example
        st.markdown("#### 📋 Final STAR Structure")
        
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
        
        # Show improvements made
        if 'improvements_made' in final_example and final_example['improvements_made']:
            st.markdown("#### 🔧 Key Enhancements Applied")
            for improvement in final_example['improvements_made']:
                st.write(f"✅ {improvement}")
        
        # Show target scores
        if 'improved_scores' in final_example:
            st.markdown("#### 📈 Target Performance Scores")
            improved_scores = final_example['improved_scores']
            col1, col2, col3 = st.columns(3)
            
            with col1:
                score = improved_scores.get('context', 0)
                st.metric("Context", f"{score}/7",
                         delta="Very Proficient" if score >= 6 else "Needs Enhancement",
                         delta_color="normal" if score >= 6 else "inverse")
            with col2:
                score = improved_scores.get('complexity', 0)
                st.metric("Complexity", f"{score}/7",
                         delta="Very Proficient" if score >= 6 else "Needs Enhancement",
                         delta_color="normal" if score >= 6 else "inverse")
            with col3:
                score = improved_scores.get('initiative', 0)
                st.metric("Initiative", f"{score}/7",
                         delta="Very Proficient" if score >= 6 else "Needs Enhancement",
                         delta_color="normal" if score >= 6 else "inverse")
    
    else:
        st.warning("⚠️ No structured final example found in results.")
        
        # Show agent conversation details in a collapsible section
        with st.expander("🤖 View Complete Agent Conversations", expanded=False):
            st.markdown("**Complete multi-agent conversation log:**")
            for i, message in enumerate(result['messages']):
                with st.expander(f"Message {i+1}: {getattr(message, 'source', 'Unknown')}"):
                    st.write(f"**Content:** {getattr(message, 'content', 'No content')}")
                    if hasattr(message, 'metadata'):
                        st.write(f"**Metadata:** {message.metadata}")
    
    # Success message and next steps
    st.markdown("---")
    st.success("🎉 **Resume Creation Complete!** Your QPS promotion resume has been created using advanced multi-agent AI processing with Australian English and targeting 6-7 level performance.")
    
    st.info("""
    **What was accomplished:**
    ✅ Your original example was preserved and enhanced
    ✅ Australian spelling and grammar applied throughout
    ✅ Targeted 6-7 level scoring (Very Proficient to Advanced)
    ✅ LC4Q competencies addressed
    ✅ Key Accountabilities coverage verified
    ✅ Transferable skills articulated
    ✅ Quality assurance completed
    """)
    
    # Download option
    st.markdown('<h3 class="section-header">💾 Download Your Resume</h3>', unsafe_allow_html=True)
    
    # Prepare comprehensive download data
    download_data = {
        "timestamp": datetime.now().isoformat(),
        "user_data": st.session_state.get('user_data', {}),
        "position_requirements": st.session_state.get('position_requirements', {}),
        "initial_scoring": st.session_state.get('initial_scoring', {}),
        "rewritten_example": st.session_state.get('rewritten_example', {}),
        "user_feedback": st.session_state.get('user_feedback', ''),
        "final_result": {
            "success": result.get('success', False),
            "total_turns": result.get('total_turns', 0),
            "stop_reason": result.get('stop_reason', 'Unknown'),
            "messages": [str(msg) for msg in result.get('messages', [])]
        }
    }
    
    st.download_button(
        label="📥 Download Complete Resume Package (JSON)",
        data=json.dumps(download_data, indent=2),
        file_name=f"qps_resume_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
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
        1. **Input** - Provide your authentic job example and position details
        2. **Initial Scoring** - Score your example (Context/Complexity/Initiative)
        3. **Enhancement** - AI enhances YOUR example (preserves authenticity) + Australian English
        4. **Feedback** - Provide your input for refinements
        5. **Final Resume** - Complete multi-agent processing targeting 6-7 scores
        """)
        
        st.markdown("---")
        
        st.markdown("### 🎯 Enhanced Success Criteria")
        st.markdown("""
        - All examples score 6-7 (Very Proficient to Advanced)
        - 100% Key Accountability coverage
        - 100% LC4Q competency coverage
        - Australian spelling and grammar
        - Authentic examples enhanced (not replaced)
        - Clear transferable skills articulation
        """)

def extract_final_resume_content(messages):
    """Extract structured resume content from agent messages"""
    resume_content = {}
    
    # Look for structured content in the messages
    for message in messages:
        content = getattr(message, 'content', str(message))
        source = getattr(message, 'source', 'Unknown')
        
        # Look for JSON-like structured content
        if '{' in content and '}' in content:
            try:
                # Try to extract JSON content
                import re
                json_matches = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', content)
                for json_str in json_matches:
                    try:
                        parsed = json.loads(json_str)
                        if isinstance(parsed, dict):
                            resume_content.update(parsed)
                    except:
                        continue
            except:
                pass
        
        # Look for STAR format content
        if 'situation:' in content.lower() or 'task:' in content.lower() or 'action:' in content.lower() or 'result:' in content.lower():
            resume_content['star_example'] = content
        
        # Look for scoring content
        if 'score' in content.lower() and ('context' in content.lower() or 'complexity' in content.lower() or 'initiative' in content.lower()):
            resume_content['scoring_analysis'] = content
        
        # Look for competency analysis
        if 'lc4q' in content.lower() or 'vision' in content.lower() or 'results' in content.lower() or 'accountability' in content.lower():
            resume_content['competency_analysis'] = content
    
    return resume_content if resume_content else None

def display_structured_resume(resume_content):
    """Display structured resume content in a user-friendly format"""
    
    # Display STAR example if available
    if 'star_example' in resume_content:
        st.markdown("### 📝 Enhanced STAR Example")
        st.markdown(resume_content['star_example'])
    
    # Display scoring analysis if available
    if 'scoring_analysis' in resume_content:
        st.markdown("### 📊 Final Scoring Analysis")
        st.markdown(resume_content['scoring_analysis'])
    
    # Display competency analysis if available
    if 'competency_analysis' in resume_content:
        st.markdown("### 🏆 LC4Q Competency Coverage")
        st.markdown(resume_content['competency_analysis'])
    
    # Display any other structured content
    for key, value in resume_content.items():
        if key not in ['star_example', 'scoring_analysis', 'competency_analysis']:
            st.markdown(f"### {key.replace('_', ' ').title()}")
            if isinstance(value, dict):
                st.json(value)
            else:
                st.markdown(str(value))

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
    if not user_data["job_example"] or not position_requirements["key_accountabilities"] or not position_requirements["position_description"] or not position_requirements["lc4q_competencies"]:
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
                try:
                    # Handle asyncio event loop conflicts
                    try:
                        loop = asyncio.get_running_loop()
                        # Use thread approach if event loop exists
                        import concurrent.futures
                        
                        def run_scoring_in_thread():
                            new_loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(new_loop)
                            try:
                                return new_loop.run_until_complete(score_initial_example(
                                    st.session_state.user_data,
                                    st.session_state.position_requirements
                                ))
                            finally:
                                new_loop.close()
                        
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            future = executor.submit(run_scoring_in_thread)
                            result = future.result(timeout=120)  # 2 minute timeout
                            
                    except RuntimeError:
                        # No event loop running
                        result = asyncio.run(score_initial_example(
                            st.session_state.user_data,
                            st.session_state.position_requirements
                        ))
                    
                    st.session_state.initial_scoring = result
                    
                except Exception as e:
                    st.error(f"❌ Scoring failed: {type(e).__name__}: {str(e)}")
                    st.session_state.initial_scoring = None
            
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
                try:
                    # Handle asyncio event loop conflicts
                    try:
                        loop = asyncio.get_running_loop()
                        # Use thread approach if event loop exists
                        import concurrent.futures
                        
                        def run_rewrite_in_thread():
                            new_loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(new_loop)
                            try:
                                return new_loop.run_until_complete(rewrite_example(
                                    st.session_state.user_data,
                                    st.session_state.position_requirements,
                                    st.session_state.initial_scoring
                                ))
                            finally:
                                new_loop.close()
                        
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            future = executor.submit(run_rewrite_in_thread)
                            result = future.result(timeout=300)  # 5 minute timeout
                            
                    except RuntimeError:
                        # No event loop running
                        result = asyncio.run(rewrite_example(
                            st.session_state.user_data,
                            st.session_state.position_requirements,
                            st.session_state.initial_scoring
                        ))
                    
                    st.session_state.rewritten_example = result
                    
                except Exception as e:
                    st.error(f"❌ Rewrite failed: {type(e).__name__}: {str(e)}")
                    st.session_state.rewritten_example = None
            
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
    
    # Show what will be processed if no result yet
    if st.session_state.final_result is None:
        if st.session_state.user_feedback:
            st.info(f"📝 **Your Feedback:** {st.session_state.user_feedback}")
        else:
            st.info("✅ Processing with the improved example (no additional changes requested)")
        
        if st.button("🚀 Generate Final Resume", type="primary", disabled=st.session_state.processing):
            st.session_state.processing = True
            
            with st.spinner("Creating your final resume... This may take several minutes."):
                # Fix asyncio event loop conflict by using proper async handling
                try:
                    # Check if we're already in an event loop
                    try:
                        loop = asyncio.get_running_loop()
                        st.warning("⚠️ Running in existing event loop - using create_task approach")
                        # If we're in a loop, we need to use a different approach
                        # Create a new thread to run the async function
                        import concurrent.futures
                        import threading
                        
                        def run_async_in_thread():
                            # Create new event loop in thread
                            new_loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(new_loop)
                            try:
                                return new_loop.run_until_complete(process_final_resume(
                                    st.session_state.user_data,
                                    st.session_state.position_requirements,
                                    st.session_state.rewritten_example,
                                    st.session_state.user_feedback
                                ))
                            finally:
                                new_loop.close()
                        
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            future = executor.submit(run_async_in_thread)
                            result = future.result(timeout=600)  # 10 minute timeout
                            
                    except RuntimeError:
                        # No event loop running, safe to use asyncio.run()
                        st.info("✅ No existing event loop - using asyncio.run()")
                        result = asyncio.run(process_final_resume(
                            st.session_state.user_data,
                            st.session_state.position_requirements,
                            st.session_state.rewritten_example,
                            st.session_state.user_feedback
                        ))
                    
                    st.session_state.final_result = result
                    st.success("✅ Processing completed! Results are displayed below.")
                    
                except concurrent.futures.TimeoutError:
                    st.error("❌ Process timed out after 10 minutes. Please try again.")
                    st.session_state.final_result = None
                except Exception as e:
                    st.error(f"❌ Execution error: {type(e).__name__}: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
                    st.session_state.final_result = None
            
            st.session_state.processing = False
    
    # Display final results if available
    if st.session_state.final_result is not None:
        st.markdown("---")
        st.success("✅ Your resume has been completed!")
        display_results(st.session_state.final_result)
        
        # Option to start over
        st.markdown("---")
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