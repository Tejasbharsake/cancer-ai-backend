import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

def predict_cancer_type(patient_data):
    """
    Predict cancer type using RandomForestClassifier based on patient data.
    
    Args:
        patient_data (dict): Dictionary containing patient features including:
            - age (int): Patient age
            - gender (str): 'Male' or 'Female'
            - symptoms (list): List of symptoms
            - family_history (bool): Whether there's family history of cancer
            - bmi (float): Body Mass Index
            - smoking_status (str): 'Never', 'Former', or 'Current'
            - blood_pressure (int): Systolic blood pressure
            - cholesterol (int): Cholesterol level
            - glucose (int): Blood glucose level
            - white_blood_cells (float): White blood cell count
            - platelet_count (int): Platelet count
            - hemoglobin (float): Hemoglobin level
    
    Returns:
        dict: Prediction results with cancer type and confidence score
    """
    
    # Generate dummy dataset for demonstration
    def generate_dummy_data(n_samples=1000):
        """Generate synthetic cancer data for training"""
        np.random.seed(42)
        
        # Define cancer types
        cancer_types = ['Breast', 'Lung', 'Colon', 'Prostate', 'Melanoma', 'Leukemia', 'Ovarian', 'Pancreatic']
        
        data = {
            'age': np.random.normal(65, 15, n_samples),
            'gender': np.random.choice(['Male', 'Female'], n_samples),
            'bmi': np.random.normal(25, 5, n_samples),
            'smoking_status': np.random.choice(['Never', 'Former', 'Current'], n_samples),
            'family_history': np.random.choice([0, 1], n_samples),
            'blood_pressure': np.random.normal(120, 20, n_samples),
            'cholesterol': np.random.normal(200, 40, n_samples),
            'glucose': np.random.normal(100, 20, n_samples),
            'white_blood_cells': np.random.normal(7, 2, n_samples),
            'platelet_count': np.random.normal(250, 50, n_samples),
            'hemoglobin': np.random.normal(14, 2, n_samples),
            'symptom_count': np.random.poisson(3, n_samples),  # Number of symptoms
            'fatigue_level': np.random.randint(1, 6, n_samples),  # 1-5 scale
            'pain_level': np.random.randint(1, 6, n_samples),  # 1-5 scale
            'weight_loss': np.random.choice([0, 1], n_samples),  # 0=no, 1=yes
            'night_sweats': np.random.choice([0, 1], n_samples),  # 0=no, 1=yes
            'appetite_loss': np.random.choice([0, 1], n_samples),  # 0=no, 1=yes
        }
        
        df = pd.DataFrame(data)
        
        # Create cancer type labels based on feature patterns
        cancer_labels = []
        for i in range(n_samples):
            # Rule-based assignment for demonstration
            if df.loc[i, 'gender'] == 'Female' and df.loc[i, 'age'] > 50:
                cancer_labels.append('Breast')
            elif df.loc[i, 'smoking_status'] in ['Current', 'Former'] and df.loc[i, 'age'] > 60:
                cancer_labels.append('Lung')
            elif df.loc[i, 'age'] > 70 and df.loc[i, 'family_history'] == 1:
                cancer_labels.append('Colon')
            elif df.loc[i, 'gender'] == 'Male' and df.loc[i, 'age'] > 60:
                cancer_labels.append('Prostate')
            elif df.loc[i, 'symptom_count'] > 4 and df.loc[i, 'fatigue_level'] > 3:
                cancer_labels.append('Leukemia')
            elif df.loc[i, 'gender'] == 'Female' and df.loc[i, 'age'] > 45:
                cancer_labels.append('Ovarian')
            elif df.loc[i, 'weight_loss'] == 1 and df.loc[i, 'appetite_loss'] == 1:
                cancer_labels.append('Pancreatic')
            else:
                cancer_labels.append('Melanoma')
        
        df['cancer_type'] = cancer_labels
        return df
    
    # Generate training data
    print("Generating training data...")
    df = generate_dummy_data(n_samples=1000)
    
    # Prepare features and target
    feature_columns = ['age', 'bmi', 'family_history', 'blood_pressure', 'cholesterol', 
                      'glucose', 'white_blood_cells', 'platelet_count', 'hemoglobin',
                      'symptom_count', 'fatigue_level', 'pain_level', 'weight_loss',
                      'night_sweats', 'appetite_loss']
    
    X = df[feature_columns]
    y = df['cancer_type']
    
    # Encode categorical variables
    le_gender = LabelEncoder()
    le_smoking = LabelEncoder()
    
    # Add encoded categorical features
    X['gender_encoded'] = le_gender.fit_transform(df['gender'])
    X['smoking_encoded'] = le_smoking.fit_transform(df['smoking_status'])
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest model
    print("Training Random Forest model...")
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train_scaled, y_train)
    
    # Evaluate model
    y_pred = rf_model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy:.2%}")
    
    # Prepare patient data for prediction
    patient_features = []
    
    # Extract features from patient_data
    for col in feature_columns:
        if col in patient_data:
            patient_features.append(patient_data[col])
        else:
            # Default values for missing features
            defaults = {
                'age': 65, 'bmi': 25, 'family_history': 0, 'blood_pressure': 120,
                'cholesterol': 200, 'glucose': 100, 'white_blood_cells': 7,
                'platelet_count': 250, 'hemoglobin': 14, 'symptom_count': 3,
                'fatigue_level': 3, 'pain_level': 3, 'weight_loss': 0,
                'night_sweats': 0, 'appetite_loss': 0
            }
            patient_features.append(defaults.get(col, 0))
    
    # Add encoded categorical features
    if 'gender' in patient_data:
        patient_features.append(le_gender.transform([patient_data['gender']])[0])
    else:
        patient_features.append(0)  # Default to first category
    
    if 'smoking_status' in patient_data:
        patient_features.append(le_smoking.transform([patient_data['smoking_status']])[0])
    else:
        patient_features.append(0)  # Default to first category
    
    # Convert to numpy array and reshape
    patient_features = np.array(patient_features).reshape(1, -1)
    
    # Scale patient features
    patient_scaled = scaler.transform(patient_features)
    
    # Make prediction
    predicted_cancer = rf_model.predict(patient_scaled)[0]
    probabilities = rf_model.predict_proba(patient_scaled)[0]
    
    # Get confidence score
    confidence = max(probabilities)
    
    # Get all cancer types and their probabilities
    cancer_types = rf_model.classes_
    cancer_probabilities = dict(zip(cancer_types, probabilities))
    
    # Sort by probability (descending)
    sorted_probabilities = sorted(cancer_probabilities.items(), key=lambda x: x[1], reverse=True)
    
    return {
        'predicted_cancer_type': predicted_cancer,
        'confidence_score': confidence,
        'all_probabilities': cancer_probabilities,
        'top_3_predictions': sorted_probabilities[:3],
        'model_accuracy': accuracy
    }


# Example usage
if __name__ == "__main__":
    # Example patient data
    example_patient = {
        'age': 68,
        'gender': 'Female',
        'bmi': 26.5,
        'smoking_status': 'Former',
        'family_history': 1,
        'blood_pressure': 135,
        'cholesterol': 220,
        'glucose': 105,
        'white_blood_cells': 8.2,
        'platelet_count': 280,
        'hemoglobin': 13.8,
        'symptom_count': 4,
        'fatigue_level': 4,
        'pain_level': 3,
        'weight_loss': 0,
        'night_sweats': 1,
        'appetite_loss': 0
    }
    
    # Make prediction
    result = predict_cancer_type(example_patient)
    
    print("\n" + "="*50)
    print("CANCER PREDICTION RESULTS")
    print("="*50)
    print(f"Predicted Cancer Type: {result['predicted_cancer_type']}")
    print(f"Confidence Score: {result['confidence_score']:.2%}")
    print(f"Model Accuracy: {result['model_accuracy']:.2%}")
    
    print("\nAll Cancer Type Probabilities:")
    for cancer_type, prob in result['all_probabilities'].items():
        print(f"  {cancer_type}: {prob:.2%}")
    
    print("\nTop 3 Predictions:")
    for i, (cancer_type, prob) in enumerate(result['top_3_predictions'], 1):
        print(f"  {i}. {cancer_type}: {prob:.2%}") 