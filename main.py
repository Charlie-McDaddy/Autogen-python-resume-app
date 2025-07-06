"""
QPS Resume Writing System - Simple Entry Point
=============================================

A simple entry point for the QPS Resume Writing Multi-Agent System.
For full functionality, use resume_system.py or the web interface.
"""

import asyncio
import os
from dotenv import load_dotenv
from resume_system import ResumeWritingSystem

load_dotenv()

async def main():
    """Simple demonstration of the resume writing system"""
    
    print("🚀 QPS Resume Writing System")
    print("=" * 40)
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("   Please set your OpenAI API key:")
        print("   export OPENAI_API_KEY='your-key-here'")
        return
    
    # Sample data for demonstration
    user_data = {
        "name": "Demo Officer",
        "current_rank": "Senior Constable",
        "current_position": "Community Liaison Officer",
        "location": "Brisbane",
        "years_experience": 6,
        "target_position": "Sergeant - Community Engagement",
        "target_location": "Gold Coast",
        "job_example": """In 2023, as a Senior Constable in Brisbane, I led a multi-agency response to address increasing antisocial behavior in the local shopping precinct. The situation required coordination between police, council, security services, and community groups to develop a sustainable solution that balanced enforcement with community engagement."""
    }
    
    position_requirements = {
        "key_accountabilities": """- Lead strategic community engagement initiatives across the district
- Develop and mobilize community liaison team of 6 officers
- Build enduring relationships with diverse community stakeholders
- Foster inclusive workplace culture reflecting community diversity""",
        
        "position_description": """POSITION: Sergeant - Community Engagement
LOCATION: Gold Coast District
REPORTS TO: Senior Sergeant - Operations

OPERATIONAL REQUIREMENTS:
- Manage community engagement programs across Gold Coast district
- Coordinate with local government and community organizations
- Oversee community liaison team of 6 officers""",
        
        "lc4q_competencies": """Vision:
- Leads strategically
- Stimulates ideas and innovation

Results:
- Builds enduring relationships
- Develops and mobilises talent

Accountability:
- Fosters healthy and inclusive workplaces"""
    }
    
    try:
        # Initialize the system
        print("🔧 Initializing resume writing system...")
        system = ResumeWritingSystem(api_key=api_key)
        
        print("📝 Creating resume with demo data...")
        print("   This may take several minutes...")
        print()
        
        # Create resume with console output
        await system.create_resume_with_console(user_data, position_requirements)
        
        print("\n" + "=" * 40)
        print("✅ Demo completed successfully!")
        print("\n💡 For full functionality:")
        print("   - Run: python test_resume_system.py")
        print("   - Or: streamlit run resume_web_interface.py")
        
        # Clean up
        await system.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n🔍 Troubleshooting:")
        print("   - Check your OpenAI API key")
        print("   - Ensure all dependencies are installed")
        print("   - Run: pip install -r requirements.txt")

if __name__ == "__main__":
    asyncio.run(main())