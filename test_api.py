"""
Test script for the FastAPI cancer prediction endpoint
"""

import requests
import json

def test_api_health():
    """Test if the API is running"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ API Health Check: PASSED")
            print(f"   Response: {response.json()}")
            return True
        else:
            print("❌ API Health Check: FAILED")
            return False
    except Exception as e:
        print(f"❌ API Health Check: FAILED - {e}")
        return False

def test_prediction_endpoint():
    """Test the prediction endpoint with sample data"""
    
    # Sample patient data
    test_patient = {
        "name": "Test Patient API",
        "age": 65,
        "gender": "Female",
        "bmi": 28.5,
        "smoking_status": "Former",
        "family_history": 1,
        "blood_pressure": 140,
        "cholesterol": 220,
        "glucose": 110,
        "white_blood_cells": 8.0,
        "platelet_count": 280,
        "hemoglobin": 13.5,
        "symptom_count": 3,
        "fatigue_level": 4,
        "pain_level": 3,
        "weight_loss": 1,
        "night_sweats": 0,
        "appetite_loss": 1
    }
    
    try:
        print("\n🧪 Testing Prediction Endpoint...")
        print(f"   Patient: {test_patient['name']}")
        
        response = requests.post(
            "http://localhost:8000/predict",
            json=test_patient,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Prediction Test: PASSED")
            print(f"   Predicted Cancer Type: {result['predicted_cancer_type']}")
            print(f"   Confidence Score: {result['confidence_score']:.2%}")
            print(f"   Patient Name: {result['patient_name']}")
            if result.get('prediction_id'):
                print(f"   Prediction ID: {result['prediction_id']}")
            return True
        else:
            print("❌ Prediction Test: FAILED")
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Prediction Test: FAILED - {e}")
        return False

def main():
    print("=" * 60)
    print("🧪 TESTING CANCER PREDICTION API")
    print("=" * 60)
    
    # Test 1: Health Check
    health_ok = test_api_health()
    
    if not health_ok:
        print("\n❌ API is not running. Please start the server first:")
        print("   python api_server.py")
        return
    
    # Test 2: Prediction Endpoint
    prediction_ok = test_prediction_endpoint()
    
    print("\n" + "=" * 60)
    if health_ok and prediction_ok:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Your API is ready to receive requests from the frontend")
    else:
        print("❌ SOME TESTS FAILED")
        print("   Please check the server logs for more details")
    print("=" * 60)

if __name__ == "__main__":
    main()