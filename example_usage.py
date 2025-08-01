"""
Simple example of how to use the cancer prediction function.
"""

from simple_cancer_predictor import predict_cancer_type

def main():
    """Example usage of the cancer prediction function"""
    
    # Example 1: Basic usage with minimal patient data
    print("Example 1: Basic patient data")
    print("-" * 40)
    
    patient_data = {
        'age': 60,
        'gender': 'Female',
        'bmi': 25.0,
        'family_history': 1
    }
    
    result = predict_cancer_type(patient_data)
    print(f"Predicted Cancer Type: {result['predicted_cancer_type']}")
    print(f"Confidence: {result['confidence_score']:.2%}")
    
    # Example 2: Complete patient data
    print("\nExample 2: Complete patient data")
    print("-" * 40)
    
    complete_patient = {
        'age': 70,
        'gender': 'Male',
        'bmi': 27.5,
        'smoking_status': 'Former',
        'family_history': 1,
        'blood_pressure': 140,
        'cholesterol': 220,
        'glucose': 110,
        'white_blood_cells': 8.0,
        'platelet_count': 250,
        'hemoglobin': 13.5,
        'symptom_count': 3,
        'fatigue_level': 3,
        'pain_level': 2,
        'weight_loss': 0,
        'night_sweats': 0,
        'appetite_loss': 0
    }
    
    result = predict_cancer_type(complete_patient)
    print(f"Predicted Cancer Type: {result['predicted_cancer_type']}")
    print(f"Confidence: {result['confidence_score']:.2%}")
    print("Top 3 Predictions:")
    for i, (cancer_type, prob) in enumerate(result['top_3_predictions'], 1):
        print(f"  {i}. {cancer_type}: {prob:.2%}")
    
    # Example 3: High-risk patient
    print("\nExample 3: High-risk patient")
    print("-" * 40)
    
    high_risk_patient = {
        'age': 65,
        'gender': 'Male',
        'smoking_status': 'Current',
        'family_history': 1,
        'symptom_count': 6,
        'fatigue_level': 5,
        'weight_loss': 1,
        'night_sweats': 1,
        'appetite_loss': 1
    }
    
    result = predict_cancer_type(high_risk_patient)
    print(f"Predicted Cancer Type: {result['predicted_cancer_type']}")
    print(f"Confidence: {result['confidence_score']:.2%}")
    print("All Probabilities:")
    for cancer_type, prob in result['all_probabilities'].items():
        print(f"  {cancer_type}: {prob:.2%}")

if __name__ == "__main__":
    main() 