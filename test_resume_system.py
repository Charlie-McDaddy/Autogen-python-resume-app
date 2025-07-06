"""
Test script for QPS Resume Writing System
========================================

This script provides comprehensive testing for the resume writing system
with different scenarios and validation.
"""

import asyncio
import json
import os
from typing import Dict

from resume_system import ResumeWritingSystem


class ResumeSystemTester:
    """Test harness for the resume writing system"""
    
    def __init__(self):
        """Initialize the tester"""
        self.system = None
        
    async def setup(self):
        """Set up the testing environment"""
        # Load API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️  Warning: OPENAI_API_KEY not found in environment")
            print("   Set your API key: export OPENAI_API_KEY='your-key-here'")
        
        # Initialize system
        self.system = ResumeWritingSystem(api_key=api_key)
        print("✅ Resume writing system initialized")
    
    async def teardown(self):
        """Clean up after testing"""
        if self.system:
            await self.system.close()
            print("✅ System cleanup completed")
    
    def get_test_scenarios(self) -> Dict[str, Dict]:
        """Get different test scenarios"""
        
        scenarios = {
            "senior_constable_to_sergeant": {
                "user_data": {
                    "name": "Sarah Johnson",
                    "current_rank": "Senior Constable",
                    "current_position": "Community Liaison Officer",
                    "location": "Brisbane",
                    "years_experience": 7,
                    "target_position": "Sergeant - Community Engagement",
                    "target_location": "Gold Coast",
                    "job_example": """In 2023, as a Senior Constable at Brisbane Station, I was assigned to address rising community tensions in the multicultural Sunnybank area following several incidents between different ethnic groups. The situation required immediate intervention to prevent escalation while building long-term relationships. I coordinated with community leaders from Vietnamese, Chinese, and Pacific Islander communities to establish a regular dialogue forum, developed culturally appropriate engagement strategies, and trained 6 junior officers in cross-cultural communication techniques, resulting in a 40% reduction in reported community tensions over 6 months."""
                },
                "position_requirements": {
                    "key_accountabilities": """- Lead strategic community engagement initiatives across Gold Coast district
- Develop and mobilize team of 8 community liaison officers
- Build and maintain enduring relationships with diverse community stakeholders  
- Foster inclusive workplace that reflects community diversity
- Demonstrate sound governance in program management and compliance
- Drive accountability for community engagement metrics and KPIs""",
                    
                    "position_description": """POSITION: Sergeant - Community Engagement Team Leader
LOCATION: Gold Coast District
CLASSIFICATION: Police Officer - Sergeant
REPORTS TO: Senior Sergeant - Operations

OPERATIONAL REQUIREMENTS:
- Supervise team of 8 community liaison officers
- Manage district-wide community engagement programs
- Coordinate with local government and community organizations
- Oversee budget management for community programs ($200k annually)
- Lead crisis communication and community response

LOCATION FACTORS:
- Gold Coast's diverse multicultural population
- High tourist areas requiring specialized engagement
- Rapid urban development and changing demographics
- Strong community expectations for transparent policing""",
                    
                    "lc4q_competencies": """Vision:
- Leads strategically
- Stimulates ideas and innovation
- Leads change in complex environments
- Makes insightful decisions

Results:
- Develops and mobilises talent
- Builds enduring relationships
- Inspires others
- Drives accountability and outcomes

Accountability:
- Fosters healthy and inclusive workplaces
- Pursues continuous growth
- Demonstrates sound governance"""
                }
            },
            
            "constable_to_senior_constable": {
                "user_data": {
                    "name": "Michael Chen",
                    "current_rank": "Constable",
                    "current_position": "General Duties Officer",
                    "location": "Ipswich",
                    "years_experience": 4,
                    "target_position": "Senior Constable - Traffic Enforcement",
                    "target_location": "Brisbane",
                    "job_example": """In 2023, as a Constable at Ipswich Station, I was assigned to address increasing traffic incidents on the Warrego Highway corridor during peak hours. The situation involved multiple serious accidents causing significant delays and public safety concerns. I developed and implemented a proactive traffic enforcement strategy, coordinating with Transport and Main Roads Queensland to identify high-risk areas, established mobile enforcement points during peak periods, and delivered road safety education programs to three local schools. This resulted in a 25% reduction in serious traffic incidents and earned recognition from the District Traffic Coordinator for innovative problem-solving."""
                },
                "position_requirements": {
                    "key_accountabilities": """- Lead traffic safety initiatives and enforcement strategies in Brisbane metropolitan area
- Mentor and develop 2-3 junior officers in traffic enforcement techniques
- Build relationships with transport authorities and road safety stakeholders
- Maintain professional standards in all traffic enforcement activities
- Demonstrate sound judgment in discretionary enforcement decisions""",
                    
                    "position_description": """POSITION: Senior Constable - Traffic Enforcement Specialist
LOCATION: Brisbane Metropolitan District
CLASSIFICATION: Police Officer - Senior Constable
REPORTS TO: Sergeant - Traffic Operations

OPERATIONAL REQUIREMENTS:
- Conduct specialized traffic enforcement operations
- Investigate serious traffic incidents and crashes
- Provide mentoring to 2-3 junior officers
- Deliver road safety education programs to schools and community groups
- Operate specialized traffic enforcement equipment

LOCATION FACTORS:
- Brisbane's complex metropolitan traffic environment
- High-volume intersections and highway corridors
- Diverse road user demographics
- Integration with council and transport authority initiatives""",
                    
                    "lc4q_competencies": """Vision:
- Stimulates ideas and innovation
- Makes insightful decisions

Results:
- Develops and mobilises talent
- Builds enduring relationships

Accountability:
- Pursues continuous growth
- Demonstrates sound governance"""
                }
            }
        }
        
        return scenarios
    
    async def test_scenario(self, scenario_name: str, scenario_data: Dict):
        """Test a specific scenario"""
        print(f"\n{'='*60}")
        print(f"🧪 TESTING SCENARIO: {scenario_name}")
        print(f"{'='*60}")
        
        try:
            # Extract data
            user_data = scenario_data["user_data"]
            position_requirements = scenario_data["position_requirements"]
            
            print(f"👤 User: {user_data['name']}")
            print(f"📊 Current: {user_data['current_rank']} - {user_data['current_position']}")
            print(f"🎯 Target: {user_data['target_position']}")
            print(f"📍 Location: {user_data['location']} → {user_data['target_location']}")
            print(f"⏰ Experience: {user_data['years_experience']} years")
            
            print(f"\n🚀 Starting resume creation process...")
            print(f"{'─'*60}")
            
            # Run the resume creation
            await self.system.create_resume_with_console(user_data, position_requirements)
            
            print(f"\n✅ Scenario '{scenario_name}' completed successfully!")
            
        except Exception as e:
            print(f"\n❌ Error in scenario '{scenario_name}': {str(e)}")
            raise
    
    async def run_quick_test(self):
        """Run a quick test with minimal output"""
        print("\n🔍 RUNNING QUICK TEST")
        print("="*40)
        
        # Use a simplified scenario
        user_data = {
            "name": "Test Officer",
            "current_rank": "Constable",
            "target_position": "Senior Constable",
            "job_example": "Led a community engagement initiative that improved police-public relations"
        }
        
        position_requirements = {
            "key_accountabilities": "- Lead tactical operations\n- Mentor junior officers\n- Maintain professional standards",
            "position_description": "POSITION: Senior Constable - General Duties\nLOCATION: Brisbane\nOPERATIONAL REQUIREMENTS: General policing duties",
            "lc4q_competencies": """Vision:
- Makes insightful decisions

Results:
- Develops and mobilises talent

Accountability:
- Demonstrates sound governance"""
        }
        
        try:
            result = await self.system.create_resume(user_data, position_requirements)
            print(f"✅ Quick test completed successfully!")
            print(f"📊 Messages exchanged: {result['total_turns']}")
            print(f"🏁 Stop reason: {result['stop_reason']}")
            
        except Exception as e:
            print(f"❌ Quick test failed: {str(e)}")
    
    async def run_all_tests(self):
        """Run all test scenarios"""
        print("\n🧪 RUNNING ALL TEST SCENARIOS")
        print("="*50)
        
        scenarios = self.get_test_scenarios()
        
        for scenario_name, scenario_data in scenarios.items():
            try:
                await self.test_scenario(scenario_name, scenario_data)
                print(f"✅ {scenario_name}: PASSED")
            except Exception as e:
                print(f"❌ {scenario_name}: FAILED - {str(e)}")
                continue
        
        print(f"\n{'='*50}")
        print("🏁 All tests completed!")


async def main():
    """Main testing function"""
    print("🧪 QPS Resume Writing System - Test Suite")
    print("="*50)
    
    # Initialize tester
    tester = ResumeSystemTester()
    
    try:
        # Set up
        await tester.setup()
        
        # Get user choice
        print("\nSelect test mode:")
        print("1. Quick test (fast validation)")
        print("2. Single scenario test")
        print("3. All scenarios test")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            await tester.run_quick_test()
        elif choice == "2":
            scenarios = tester.get_test_scenarios()
            print("\nAvailable scenarios:")
            for i, name in enumerate(scenarios.keys(), 1):
                print(f"{i}. {name}")
            
            scenario_choice = input(f"\nSelect scenario (1-{len(scenarios)}): ").strip()
            try:
                scenario_index = int(scenario_choice) - 1
                scenario_name = list(scenarios.keys())[scenario_index]
                await tester.test_scenario(scenario_name, scenarios[scenario_name])
            except (ValueError, IndexError):
                print("❌ Invalid scenario selection")
        elif choice == "3":
            await tester.run_all_tests()
        else:
            print("❌ Invalid choice")
    
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"❌ Test suite error: {str(e)}")
    
    finally:
        # Clean up
        await tester.teardown()


if __name__ == "__main__":
    asyncio.run(main())