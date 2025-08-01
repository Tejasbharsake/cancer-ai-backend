from simple_cancer_predictor import predict_cancer_type

def test_cancer_prediction():
    """Test the cancer prediction function with different patient scenarios"""
    
    # Test Case 1: Female patient with breast cancer risk factors
    print("="*60)
    print("TEST CASE 1: Female patient with breast cancer risk factors")
    print("="*60)
    patient1 = {
        'age': 55,
        'gender': 'Female',
        'bmi': 28.0,
        'smoking_status': 'Never',
        'family_history': 1,
        'blood_pressure': 125,
        'cholesterol': 180,
        'glucose': 95,
        'white_blood_cells': 6.8,
        'platelet_count': 240,
        'hemoglobin': 13.5,
        'symptom_count': 2,
        'fatigue_level': 2,
        'pain_level': 1,
        'weight_loss': 0,
        'night_sweats': 0,
        'appetite_loss': 0
    }
    
    result1 = predict_cancer_type(patient1)
    print(f"Predicted Cancer Type: {result1['predicted_cancer_type']}")
    print(f"Confidence Score: {result1['confidence_score']:.2%}")
    print("Top 3 Predictions:")
    for i, (cancer_type, prob) in enumerate(result1['top_3_predictions'], 1):
        print(f"  {i}. {cancer_type}: {prob:.2%}")
    
    # Test Case 2: Male patient with lung cancer risk factors
    print("\n" + "="*60)
    print("TEST CASE 2: Male patient with lung cancer risk factors")
    print("="*60)
    patient2 = {
        'age': 65,
        'gender': 'Male',
        'bmi': 22.0,
        'smoking_status': 'Current',
        'family_history': 0,
        'blood_pressure': 140,
        'cholesterol': 220,
        'glucose': 110,
        'white_blood_cells': 8.5,
        'platelet_count': 260,
        'hemoglobin': 12.8,
        'symptom_count': 5,
        'fatigue_level': 4,
        'pain_level': 4,
        'weight_loss': 1,
        'night_sweats': 1,
        'appetite_loss': 1
    }
    
    result2 = predict_cancer_type(patient2)
    print(f"Predicted Cancer Type: {result2['predicted_cancer_type']}")
    print(f"Confidence Score: {result2['confidence_score']:.2%}")
    print("Top 3 Predictions:")
    for i, (cancer_type, prob) in enumerate(result2['top_3_predictions'], 1):
        print(f"  {i}. {cancer_type}: {prob:.2%}")
    
    # Test Case 3: Elderly patient with colon cancer risk factors
    print("\n" + "="*60)
    print("TEST CASE 3: Elderly patient with colon cancer risk factors")
    print("="*60)
    patient3 = {
        'age': 75,
        'gender': 'Male',
        'bmi': 26.0,
        'smoking_status': 'Former',
        'family_history': 1,
        'blood_pressure': 130,
        'cholesterol': 200,
        'glucose': 105,
        'white_blood_cells': 7.2,
        'platelet_count': 250,
        'hemoglobin': 13.0,
        'symptom_count': 3,
        'fatigue_level': 3,
        'pain_level': 2,
        'weight_loss': 0,
        'night_sweats': 0,
        'appetite_loss': 0
    }
    
    result3 = predict_cancer_type(patient3)
    print(f"Predicted Cancer Type: {result3['predicted_cancer_type']}")
    print(f"Confidence Score: {result3['confidence_score']:.2%}")
    print("Top 3 Predictions:")
    for i, (cancer_type, prob) in enumerate(result3['top_3_predictions'], 1):
        print(f"  {i}. {cancer_type}: {prob:.2%}")
    
    # Test Case 4: Patient with leukemia symptoms
    print("\n" + "="*60)
    print("TEST CASE 4: Patient with leukemia symptoms")
    print("="*60)
    patient4 = {
        'age': 45,
        'gender': 'Female',
        'bmi': 24.0,
        'smoking_status': 'Never',
        'family_history': 0,
        'blood_pressure': 115,
        'cholesterol': 180,
        'glucose': 90,
        'white_blood_cells': 12.0,  # Elevated
        'platelet_count': 180,      # Low
        'hemoglobin': 10.5,         # Low
        'symptom_count': 6,         # High symptom count
        'fatigue_level': 5,         # High fatigue
        'pain_level': 3,
        'weight_loss': 1,
        'night_sweats': 1,
        'appetite_loss': 1
    }
    
    result4 = predict_cancer_type(patient4)
    print(f"Predicted Cancer Type: {result4['predicted_cancer_type']}")
    print(f"Confidence Score: {result4['confidence_score']:.2%}")
    print("Top 3 Predictions:")
    for i, (cancer_type, prob) in enumerate(result4['top_3_predictions'], 1):
        print(f"  {i}. {cancer_type}: {prob:.2%}")

if __name__ == "__main__":
    test_cancer_prediction() 