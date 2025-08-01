"""
Supabase connection and data insertion for Cancer Prediction System
"""

import os
from supabase import create_client, Client
from simple_cancer_predictor import predict_cancer_type
from datetime import datetime
import json

class SupabaseCancerPredictor:
    def __init__(self, supabase_url: str, supabase_key: str):
        """
        Initialize Supabase connection
        
        Args:
            supabase_url (str): Your Supabase project URL
            supabase_key (str): Your Supabase anon/public key
        """
        self.supabase: Client = create_client(supabase_url, supabase_key)
        self.table_name = 'predictions'
        
    def test_connection(self):
        """Test the Supabase connection"""
        try:
            # Try to fetch a single row to test connection
            response = self.supabase.table(self.table_name).select('*').limit(1).execute()
            print("✅ Supabase connection successful!")
            return True
        except Exception as e:
            print(f"❌ Supabase connection failed: {e}")
            return False
    
    def create_predictions_table(self):
        """
        Create the predictions table if it doesn't exist
        Note: This is a reference for the table structure
        """
        table_structure = """
        CREATE TABLE predictions (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            age INTEGER NOT NULL,
            gender VARCHAR(10) NOT NULL,
            prediction_result VARCHAR(50) NOT NULL,
            confidence_score DECIMAL(5,4) NOT NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            patient_data JSONB,
            additional_notes TEXT
        );
        """
        print("📋 Table structure reference:")
        print(table_structure)
        print("Note: Create this table in your Supabase dashboard")
    
    def insert_prediction(self, name: str, age: int, gender: str, 
                         prediction_result: str, confidence_score: float,
                         patient_data: dict = None, notes: str = None):
        """
        Insert a prediction record into the predictions table
        
        Args:
            name (str): Patient name
            age (int): Patient age
            gender (str): Patient gender ('Male' or 'Female')
            prediction_result (str): Predicted cancer type
            confidence_score (float): Confidence score (0-1)
            patient_data (dict): Full patient data dictionary
            notes (str): Additional notes
        """
        try:
            data = {
                'name': name,
                'age': age,
                'gender': gender,
                'prediction_result': prediction_result,
                'confidence_score': confidence_score,
                'patient_data': patient_data,
                'additional_notes': notes,
                'created_at': datetime.now().isoformat()
            }
            
            # Remove None values
            data = {k: v for k, v in data.items() if v is not None}
            
            response = self.supabase.table(self.table_name).insert(data).execute()
            
            if response.data:
                print(f"✅ Prediction inserted successfully!")
                print(f"   ID: {response.data[0]['id']}")
                print(f"   Name: {name}")
                print(f"   Prediction: {prediction_result}")
                print(f"   Confidence: {confidence_score:.2%}")
                return response.data[0]
            else:
                print("❌ Failed to insert prediction")
                return None
                
        except Exception as e:
            print(f"❌ Error inserting prediction: {e}")
            return None
    
    def get_all_predictions(self, limit: int = 10):
        """
        Retrieve all predictions from the table
        
        Args:
            limit (int): Maximum number of records to retrieve
        """
        try:
            response = self.supabase.table(self.table_name).select('*').order('created_at', desc=True).limit(limit).execute()
            return response.data
        except Exception as e:
            print(f"❌ Error retrieving predictions: {e}")
            return []
    
    def predict_and_store(self, name: str, patient_data: dict, notes: str = None):
        """
        Make a cancer prediction and store the result in Supabase
        
        Args:
            name (str): Patient name
            patient_data (dict): Patient data for prediction
            notes (str): Additional notes
        """
        try:
            # Make prediction
            print(f"🔬 Making prediction for {name}...")
            result = predict_cancer_type(patient_data)
            
            # Extract data for storage
            prediction_result = result['predicted_cancer_type']
            confidence_score = result['confidence_score']
            age = patient_data.get('age', 0)
            gender = patient_data.get('gender', 'Unknown')
            
            # Store in Supabase
            stored_prediction = self.insert_prediction(
                name=name,
                age=age,
                gender=gender,
                prediction_result=prediction_result,
                confidence_score=confidence_score,
                patient_data=patient_data,
                notes=notes
            )
            
            return stored_prediction
            
        except Exception as e:
            print(f"❌ Error in predict_and_store: {e}")
            return None


def main():
    """Example usage of Supabase connection"""
    
    # Supabase credentials (replace with your actual credentials)
    SUPABASE_URL = "YOUR_SUPABASE_URL"
    SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"
    
    # Check if credentials are provided
    if SUPABASE_URL == "YOUR_SUPABASE_URL" or SUPABASE_KEY == "YOUR_SUPABASE_ANON_KEY":
        print("⚠️  Please update the Supabase credentials in the script!")
        print("   Replace SUPABASE_URL and SUPABASE_KEY with your actual values")
        print("\n📋 To get your credentials:")
        print("   1. Go to your Supabase project dashboard")
        print("   2. Navigate to Settings > API")
        print("   3. Copy the Project URL and anon/public key")
        return
    
    # Initialize connection
    predictor = SupabaseCancerPredictor(SUPABASE_URL, SUPABASE_KEY)
    
    # Test connection
    if not predictor.test_connection():
        return
    
    # Show table structure
    predictor.create_predictions_table()
    
    # Example patient data
    patient_data = {
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
    
    # Make prediction and store
    print("\n" + "="*50)
    print("MAKING PREDICTION AND STORING IN SUPABASE")
    print("="*50)
    
    stored_result = predictor.predict_and_store(
        name="Jane Doe",
        patient_data=patient_data,
        notes="Patient with breast cancer risk factors"
    )
    
    if stored_result:
        print("\n📊 Retrieving recent predictions...")
        recent_predictions = predictor.get_all_predictions(limit=5)
        
        print(f"\nRecent predictions ({len(recent_predictions)} records):")
        for pred in recent_predictions:
            print(f"  - {pred['name']}: {pred['prediction_result']} ({pred['confidence_score']:.2%})")


if __name__ == "__main__":
    main() 