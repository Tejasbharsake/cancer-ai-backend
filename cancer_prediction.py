import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import warnings
warnings.filterwarnings('ignore')

class CancerPredictor:
    """
    A comprehensive cancer prediction system using machine learning.
    This class handles data preprocessing, model training, and prediction.
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = None
        self.cancer_types = None
        
    def generate_synthetic_cancer_data(self, n_samples=1000):
        """
        Generate synthetic cancer data for demonstration purposes.
        In a real scenario, you would load actual cancer datasets.
        """
        np.random.seed(42)
        
        # Define cancer types
        cancer_types = ['Breast', 'Lung', 'Colon', 'Prostate', 'Melanoma', 'Leukemia']
        
        # Generate synthetic features based on typical cancer biomarkers
        data = {
            'age': np.random.normal(65, 15, n_samples),
            'gender': np.random.choice(['Male', 'Female'], n_samples),
            'bmi': np.random.normal(25, 5, n_samples),
            'smoking_history': np.random.choice(['Never', 'Former', 'Current'], n_samples),
            'family_history': np.random.choice([0, 1], n_samples),
            'ca125': np.random.normal(20, 10, n_samples),  # Ovarian cancer marker
            'psa': np.random.normal(4, 2, n_samples),      # Prostate cancer marker
            'cea': np.random.normal(3, 1.5, n_samples),    # Colon cancer marker
            'afp': np.random.normal(10, 5, n_samples),     # Liver cancer marker
            'hcg': np.random.normal(5, 2, n_samples),      # Testicular cancer marker
            'ldh': np.random.normal(150, 50, n_samples),   # General cancer marker
            'platelet_count': np.random.normal(250, 50, n_samples),
            'white_blood_cells': np.random.normal(7, 2, n_samples),
            'red_blood_cells': np.random.normal(4.5, 0.5, n_samples),
            'hemoglobin': np.random.normal(14, 2, n_samples),
            'creatinine': np.random.normal(1, 0.3, n_samples),
            'glucose': np.random.normal(100, 20, n_samples),
            'cholesterol': np.random.normal(200, 40, n_samples),
            'blood_pressure_systolic': np.random.normal(120, 20, n_samples),
            'blood_pressure_diastolic': np.random.normal(80, 10, n_samples),
        }
        
        df = pd.DataFrame(data)
        
        # Create cancer type labels based on feature patterns
        cancer_labels = []
        for i in range(n_samples):
            # Simple rule-based assignment for demonstration
            if df.loc[i, 'gender'] == 'Female' and df.loc[i, 'ca125'] > 25:
                cancer_labels.append('Breast')
            elif df.loc[i, 'smoking_history'] in ['Current', 'Former'] and df.loc[i, 'age'] > 60:
                cancer_labels.append('Lung')
            elif df.loc[i, 'age'] > 70 and df.loc[i, 'cea'] > 4:
                cancer_labels.append('Colon')
            elif df.loc[i, 'gender'] == 'Male' and df.loc[i, 'psa'] > 6:
                cancer_labels.append('Prostate')
            elif df.loc[i, 'afp'] > 15:
                cancer_labels.append('Melanoma')
            else:
                cancer_labels.append('Leukemia')
        
        df['cancer_type'] = cancer_labels
        return df
    
    def preprocess_data(self, df):
        """
        Preprocess the data for machine learning.
        """
        # Separate features and target
        X = df.drop('cancer_type', axis=1)
        y = df['cancer_type']
        
        # Store feature names and cancer types
        self.feature_names = X.columns.tolist()
        self.cancer_types = y.unique().tolist()
        
        # Encode categorical variables
        categorical_cols = ['gender', 'smoking_history']
        self.label_encoders = {}
        for col in categorical_cols:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            self.label_encoders[col] = le
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale numerical features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def train_model(self, X_train, y_train):
        """
        Train the Random Forest model.
        """
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_train, y_train)
        
    def evaluate_model(self, X_test, y_test):
        """
        Evaluate the model performance.
        """
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)
        
        print("Model Performance:")
        print("=" * 50)
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        return y_pred, y_pred_proba
    
    def predict_cancer(self, patient_data):
        """
        Predict cancer type and probability for a new patient.
        
        Args:
            patient_data (dict): Dictionary containing patient features
            
        Returns:
            dict: Prediction results with cancer type and probabilities
        """
        if self.model is None:
            raise ValueError("Model not trained. Please train the model first.")
        
        # Convert patient data to DataFrame
        df_patient = pd.DataFrame([patient_data])
        
        # Encode categorical variables
        categorical_cols = ['gender', 'smoking_history']
        for col in categorical_cols:
            if col in df_patient.columns:
                df_patient[col] = self.label_encoders[col].transform(df_patient[col])
        
        # Ensure all required features are present
        missing_features = set(self.feature_names) - set(df_patient.columns)
        if missing_features:
            for feature in missing_features:
                df_patient[feature] = 0  # Default value for missing features
        
        # Reorder columns to match training data
        df_patient = df_patient[self.feature_names]
        
        # Scale the features
        patient_scaled = self.scaler.transform(df_patient)
        
        # Make prediction
        predicted_cancer = self.model.predict(patient_scaled)[0]
        probabilities = self.model.predict_proba(patient_scaled)[0]
        
        # Create probability dictionary
        prob_dict = dict(zip(self.cancer_types, probabilities))
        
        # Sort probabilities in descending order
        sorted_probs = sorted(prob_dict.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'predicted_cancer_type': predicted_cancer,
            'confidence': prob_dict[predicted_cancer],
            'all_probabilities': prob_dict,
            'top_predictions': sorted_probs[:3]  # Top 3 predictions
        }
    
    def save_model(self, filepath='cancer_model.pkl'):
        """
        Save the trained model and preprocessing objects.
        """
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_names': self.feature_names,
            'cancer_types': self.cancer_types
        }
        joblib.dump(model_data, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath='cancer_model.pkl'):
        """
        Load a trained model and preprocessing objects.
        """
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.label_encoders = model_data['label_encoders']
        self.feature_names = model_data['feature_names']
        self.cancer_types = model_data['cancer_types']
        print(f"Model loaded from {filepath}")


def predict_cancer_type_and_probability(patient_data, model_path=None):
    """
    Main function to predict cancer type and probability.
    
    Args:
        patient_data (dict): Dictionary containing patient features
        model_path (str): Path to saved model file (optional)
        
    Returns:
        dict: Prediction results with cancer type and probabilities
    """
    predictor = CancerPredictor()
    
    # If model path is provided, load existing model
    if model_path:
        try:
            predictor.load_model(model_path)
        except FileNotFoundError:
            print("Model file not found. Training new model...")
            model_path = None
    
    # If no model path or model loading failed, train new model
    if not model_path:
        print("Generating synthetic cancer data...")
        df = predictor.generate_synthetic_cancer_data(n_samples=1000)
        
        print("Preprocessing data...")
        X_train, X_test, y_train, y_test = predictor.preprocess_data(df)
        
        print("Training Random Forest model...")
        predictor.train_model(X_train, y_train)
        
        print("Evaluating model...")
        predictor.evaluate_model(X_test, y_test)
        
        # Save the trained model
        predictor.save_model()
    
    # Make prediction
    print("\nMaking prediction for patient...")
    result = predictor.predict_cancer(patient_data)
    
    return result


# Example usage and demonstration
if __name__ == "__main__":
    # Example patient data
    example_patient = {
        'age': 68,
        'gender': 'Female',
        'bmi': 26.5,
        'smoking_history': 'Former',
        'family_history': 1,
        'ca125': 35.2,
        'psa': 3.8,
        'cea': 2.1,
        'afp': 8.5,
        'hcg': 4.2,
        'ldh': 165,
        'platelet_count': 280,
        'white_blood_cells': 8.2,
        'red_blood_cells': 4.3,
        'hemoglobin': 13.8,
        'creatinine': 0.9,
        'glucose': 105,
        'cholesterol': 220,
        'blood_pressure_systolic': 135,
        'blood_pressure_diastolic': 85
    }
    
    # Make prediction
    prediction_result = predict_cancer_type_and_probability(example_patient)
    
    print("\n" + "="*60)
    print("CANCER PREDICTION RESULTS")
    print("="*60)
    print(f"Predicted Cancer Type: {prediction_result['predicted_cancer_type']}")
    print(f"Confidence: {prediction_result['confidence']:.2%}")
    print("\nAll Probabilities:")
    for cancer_type, prob in prediction_result['all_probabilities'].items():
        print(f"  {cancer_type}: {prob:.2%}")
    
    print("\nTop 3 Predictions:")
    for i, (cancer_type, prob) in enumerate(prediction_result['top_predictions'], 1):
        print(f"  {i}. {cancer_type}: {prob:.2%}") 