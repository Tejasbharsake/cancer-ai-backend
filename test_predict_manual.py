"""
Manual test examples for the FastAPI /predict endpoint
"""

import requests
import json

# Example 1: High-risk patient
high_risk_patient = {
    "name": "John Smith",
    "age": 72,
    "gender": "Male",
    "bmi": 32.0,
    "smoking_status": "Current",
    "family_history": 1,
    "blood_pressure": 160,
    "cholesterol": 280,
    "glucose": 140,
    "white_blood_cells": 9.5,
    "platelet_count": 320,
    "hemoglobin": 12.0,
    "symptom_count": 5,
    "fatigue_level": 5,
    "pain_level": 4,
    "weight_loss": 1,
    "night_sweats": 1,
    "appetite_loss": 1
}

# Example 2: Low-risk patient
low_risk_patient = {
    "name": "Sarah Johnson",
    "age": 35,
    "gender": "Female",
    "bmi": 22.5,
    "smoking_status": "Never",
    "family_history": 0,
    "blood_pressure": 110,
    "cholesterol": 180,
    "glucose": 90,
    "white_blood_cells": 6.5,
    "platelet_count": 240,
    "hemoglobin": 14.2,
    "symptom_count": 1,
    "fatigue_level": 2,
    "pain_level": 1,
    "weight_loss": 0,
    "night_sweats": 0,
    "appetite_loss": 0
}

def test_patient(patient_data, description):
    """Test a patient and display results"""
    print(f"\n🧪 Testing: {description}")
    print(f"   Patient: {patient_data['name']}")
    print(f"   Age: {patient_data['age']}, Gender: {patient_data['gender']}")
    print(f"   Smoking: {patient_data['smoking_status']}, BMI: {patient_data['bmi']}")
    
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json=patient_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Prediction: {result['predicted_cancer_type']}")
            print(f"   📊 Confidence: {result['confidence_score']:.2%}")
            if result.get('prediction_id'):
                print(f"   🆔 Stored with ID: {result['prediction_id'][:8]}...")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"   ❌ Request failed: {e}")

def main():
    print("=" * 60)
    print("🏥 MANUAL CANCER PREDICTION TESTS")
    print("=" * 60)
    
    # Test high-risk patient
    test_patient(high_risk_patient, "High-Risk Patient (Elderly, Smoker)")
    
    # Test low-risk patient  
    test_patient(low_risk_patient, "Low-Risk Patient (Young, Healthy)")
    
    print("\n" + "=" * 60)
    print("📚 API Documentation available at: http://localhost:8000/docs")
    print("🔗 API Base URL: http://localhost:8000")
    print("=" * 60)

if __name__ == "__main__":
    main()