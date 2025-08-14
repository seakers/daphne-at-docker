#!/usr/bin/env python3
"""
Test script for physics diagnosis chatbot functionality.

This script tests the integration between the chatbot and physics diagnosis system.
"""

import sys
import os

# Add the daphne_brain directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'daphne_brain'))

def test_physics_diagnosis_function():
    """Test the physics diagnosis function directly."""
    try:
        from AT.dialogue.dialogue_functions import run_physics_diagnosis
        
        print("🔬 Testing physics diagnosis function...")
        
        # Test with a short duration
        result = run_physics_diagnosis(10)
        
        print(f"✅ Physics diagnosis result: {result['status']}")
        print(f"📊 Message: {result['message']}")
        
        if result['status'] == 'success':
            print(f"📈 Duration: {result['duration_seconds']} seconds")
            print(f"📋 Diagnosis report keys: {list(result['diagnosis_report'].keys())}")
            
            # Check if physics_diagnosis_data exists
            if 'physics_diagnosis_data' in result['diagnosis_report']:
                pdata = result['diagnosis_report']['physics_diagnosis_data']
                print(f"🎯 Most probable anomaly: {pdata.get('most_probable_anomaly', 'N/A')}")
                print(f"📊 Probability: {pdata.get('probability', 'N/A')}")
                print(f"🔍 Component anomalies: {len(pdata.get('component_anomalies', []))}")
                print(f"📈 Actual telemetry points: {len(pdata.get('actual_telemetry', []))}")
            else:
                print("❌ No physics_diagnosis_data in report")
        else:
            print(f"❌ Error: {result.get('error_message', 'Unknown error')}")
            
        return result['status'] == 'success'
        
    except Exception as e:
        print(f"❌ Error testing physics diagnosis function: {e}")
        return False

def test_command_type_loading():
    """Test that the new command type can be loaded."""
    try:
        import json
        
        command_file = 'daphne_brain/AT/dialogue/command_types/Diagnosis/2003.json'
        
        if os.path.exists(command_file):
            with open(command_file, 'r') as f:
                command_data = json.load(f)
            
            print("✅ Command type file loaded successfully")
            print(f"📋 Type: {command_data.get('type')}")
            print(f"🎯 Objective: {command_data.get('objective')}")
            print(f"🔧 Function: {command_data.get('function', {}).get('run_template', 'N/A')}")
            
            return True
        else:
            print(f"❌ Command type file not found: {command_file}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing command type loading: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Physics Diagnosis Chatbot Integration")
    print("=" * 50)
    
    tests = [
        ("Command Type Loading", test_command_type_loading),
        ("Physics Diagnosis Function", test_physics_diagnosis_function),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running test: {test_name}")
        print("-" * 30)
        
        if test_func():
            print(f"✅ {test_name}: PASSED")
            passed += 1
        else:
            print(f"❌ {test_name}: FAILED")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Physics diagnosis chatbot integration is working.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
