#!/usr/bin/env python3
"""
Simple test script for the Cancer Prediction System
"""

from cancer_prediction import predict_cancer_type_and_probability

def main():
    print("🧬 AI Cancer Prediction System - Simple Test")
    print("=" * 50)
    
    # Test patient data
    patient = {
        'age': 55,
        'gender': 'Female',
        'bmi': 27.0,
        'smoking_history': 'Never',
        'family_history': 1,
        'ca125': 40.0,  # Elevated - suspicious for breast cancer
        'psa': 2.0,
        'cea': 2.5,
        'afp': 8.0,
        'hcg': 3.0,
        'ldh': 150,
        'platelet_count': 250,
        'white_blood_cells': 7.0,
        'red_blood_cells': 4.2,
        'hemoglobin': 13.5,
        'creatinine': 0.8,
        'glucose': 95,
        'cholesterol': 200,
        'blood_pressure_systolic': 120,
        'blood_pressure_diastolic': 80
    }
    
    print("Patient Data:")
    print(f"  Age: {patient['age']}")
    print(f"  Gender: {patient['gender']}")
    print(f"  CA125: {patient['ca125']} (Elevated)")
    print(f"  Family History: {'Yes' if patient['family_history'] else 'No'}")
    
    print("\n🔍 Analyzing patient data...")
    
    # Make prediction
    result = predict_cancer_type_and_probability(patient)
    
    print("\n📊 PREDICTION RESULTS")
    print("=" * 50)
    print(f"🎯 Predicted Cancer Type: {result['predicted_cancer_type']}")
    print(f"📈 Confidence: {result['confidence']:.2%}")
    
    print("\n📋 All Probabilities:")
    for cancer_type, prob in result['all_probabilities'].items():
        print(f"  {cancer_type}: {prob:.2%}")
    
    print("\n🏆 Top 3 Predictions:")
    for i, (cancer_type, prob) in enumerate(result['top_predictions'], 1):
        print(f"  {i}. {cancer_type}: {prob:.2%}")
    
    print("\n" + "=" * 50)
    print("✅ Test completed successfully!")
    print("⚠️  Note: This is a demonstration using synthetic data.")
    print("   For real medical applications, consult healthcare professionals.")

if __name__ == "__main__":
    main() 