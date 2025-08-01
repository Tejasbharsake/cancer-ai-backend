"""
Test script for the FastAPI doctor explanation endpoint
"""

import requests
import json

def test_explanation_endpoint():
    """Test the /explain endpoint with sample data"""
    
    # Sample patient data
    test_patient = {
        "name": "Mary Johnson",
        "age": 58,
        "gender": "Female",
        "bmi": 27.2,
        "smoking_status": "Never",
        "family_history": 1,
        "blood_pressure": 130,
        "cholesterol": 210,
        "glucose": 95,
        "white_blood_cells": 7.2,
        "platelet_count": 260,
        "hemoglobin": 13.8,
        "symptom_count": 3,
        "fatigue_level": 3,
        "pain_level": 2,
        "weight_loss": 0,
        "night_sweats": 1,
        "appetite_loss": 0
    }
    
    try:
        print("🧪 Testing Doctor Explanation Endpoint...")
        print(f"   Patient: {test_patient['name']}")
        print(f"   Age: {test_patient['age']}, Gender: {test_patient['gender']}")
        
        response = requests.post(
            "http://localhost:8000/explain",
            json=test_patient,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Doctor Explanation Test: PASSED")
            print("\n" + "="*60)
            print("👨‍⚕️ DOCTOR'S EXPLANATION")
            print("="*60)
            print("\n📋 EXPLANATION:")
            print(result['explanation'])
            print("\n💊 RECOMMENDATIONS:")
            print(result['recommendations'])
            print("\n📅 NEXT STEPS:")
            print(result['next_steps'])
            print(f"\n🎯 CONFIDENCE INTERPRETATION:")
            print(result['confidence_interpretation'])
            
            if result.get('error'):
                print(f"\n⚠️  Note: {result['error']}")
            
            return True
        else:
            print("❌ Doctor Explanation Test: FAILED")
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Doctor Explanation Test: FAILED - {e}")
        return False

def test_combined_workflow():
    """Test the complete workflow: prediction + explanation"""
    
    test_patient = {
        "name": "Robert Wilson",
        "age": 72,
        "gender": "Male",
        "bmi": 31.5,
        "smoking_status": "Current",
        "family_history": 0,
        "blood_pressure": 155,
        "cholesterol": 240,
        "glucose": 120,
        "white_blood_cells": 9.1,
        "platelet_count": 310,
        "hemoglobin": 12.5,
        "symptom_count": 5,
        "fatigue_level": 4,
        "pain_level": 4,
        "weight_loss": 1,
        "night_sweats": 1,
        "appetite_loss": 1
    }
    
    print("\n" + "="*60)
    print("🔄 TESTING COMBINED WORKFLOW")
    print("="*60)
    
    # Step 1: Get prediction
    try:
        print("Step 1: Getting prediction...")
        pred_response = requests.post(
            "http://localhost:8000/predict",
            json=test_patient,
            headers={"Content-Type": "application/json"}
        )
        
        if pred_response.status_code == 200:
            prediction = pred_response.json()
            print(f"✅ Prediction: {prediction['predicted_cancer_type']} ({prediction['confidence_score']:.1%})")
        else:
            print("❌ Prediction failed")
            return False
            
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        return False
    
    # Step 2: Get explanation
    try:
        print("Step 2: Getting doctor explanation...")
        exp_response = requests.post(
            "http://localhost:8000/explain",
            json=test_patient,
            headers={"Content-Type": "application/json"}
        )
        
        if exp_response.status_code == 200:
            explanation = exp_response.json()
            print("✅ Explanation generated successfully")
            
            print(f"\n👨‍⚕️ Complete Medical Assessment for {test_patient['name']}:")
            print(f"   Prediction: {prediction['predicted_cancer_type']} ({prediction['confidence_score']:.1%})")
            print(f"   Confidence: {explanation['confidence_interpretation']}")
            print(f"   Explanation Length: {len(explanation['explanation'])} characters")
            print(f"   Recommendations: {len(explanation['recommendations'])} characters")
            print(f"   Next Steps: {len(explanation['next_steps'])} characters")
            
            return True
        else:
            print("❌ Explanation failed")
            return False
            
    except Exception as e:
        print(f"❌ Explanation failed: {e}")
        return False

def main():
    print("=" * 60)
    print("🏥 TESTING DOCTOR EXPLANATION API")
    print("=" * 60)
    
    # Test 1: Basic explanation endpoint
    explanation_ok = test_explanation_endpoint()
    
    # Test 2: Combined workflow
    workflow_ok = test_combined_workflow()
    
    print("\n" + "=" * 60)
    if explanation_ok and workflow_ok:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Your Doctor Explanation API is working perfectly")
        print("📚 API Documentation: http://localhost:8000/docs")
    else:
        print("❌ SOME TESTS FAILED")
        print("   Please check the server logs for more details")
    print("=" * 60)

if __name__ == "__main__":
    main()