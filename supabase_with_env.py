"""
Supabase connection using environment variables for better security
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client
from simple_cancer_predictor import predict_cancer_type
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

def load_supabase_credentials():
    """
    Load Supabase credentials from environment variables
    You can set these in your system or create a .env file
    """
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("⚠️  Supabase credentials not found in environment variables!")
        print("\n📋 Set these environment variables:")
        print("   export SUPABASE_URL=your_supabase_url")
        print("   export SUPABASE_KEY=your_supabase_key")
        print("\n   Or create a .env file with:")
        print("   SUPABASE_URL=your_supabase_url")
        print("   SUPABASE_KEY=your_supabase_key")
        return None, None
    
    return supabase_url, supabase_key

def connect_to_supabase():
    """Connect to Supabase using environment variables"""
    supabase_url, supabase_key = load_supabase_credentials()
    
    if not supabase_url or not supabase_key:
        return None
    
    try:
        supabase = create_client(supabase_url, supabase_key)
        print("✅ Connected to Supabase successfully!")
        return supabase
    except Exception as e:
        print(f"❌ Failed to connect to Supabase: {e}")
        return None

def insert_prediction_with_env(supabase: Client, name: str, age: int, gender: str, 
                              prediction_result: str, confidence_score: float):
    """Insert prediction data using environment-based connection"""
    try:
        data = {
            'name': name,
            'age': age,
            'gender': gender,
            'prediction_result': prediction_result,
            'confidence_score': confidence_score,
            'created_at': datetime.now().isoformat()
        }
        
        response = supabase.table('predictions').insert(data).execute()
        
        if response.data:
            print(f"✅ Data inserted successfully!")
            print(f"   ID: {response.data[0]['id']}")
            print(f"   Name: {name}")
            print(f"   Prediction: {prediction_result}")
            print(f"   Confidence: {confidence_score:.2%}")
            return response.data[0]
        else:
            print("❌ Failed to insert data")
            return None
            
    except Exception as e:
        print(f"❌ Error inserting data: {e}")
        return None

def predict_and_store_with_env(supabase: Client, name: str, patient_data: dict):
    """Make prediction and store using environment-based connection"""
    try:
        print(f"🔬 Making prediction for {name}...")
        result = predict_cancer_type(patient_data)
        
        prediction_result = result['predicted_cancer_type']
        confidence_score = result['confidence_score']
        age = patient_data.get('age', 0)
        gender = patient_data.get('gender', 'Unknown')
        
        return insert_prediction_with_env(
            supabase=supabase,
            name=name,
            age=age,
            gender=gender,
            prediction_result=prediction_result,
            confidence_score=confidence_score
        )
        
    except Exception as e:
        print(f"❌ Error in predict_and_store: {e}")
        return None

def main():
    """Example usage with environment variables"""
    
    # Try to connect using environment variables
    supabase = connect_to_supabase()
    
    if not supabase:
        print("\n💡 To use this script:")
        print("   1. Set your Supabase credentials as environment variables")
        print("   2. Or create a .env file with your credentials")
        print("   3. Install python-dotenv: pip install python-dotenv")
        print("   4. Add 'from dotenv import load_dotenv; load_dotenv()' to the top")
        return
    
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
    
    result = predict_and_store_with_env(supabase, "Jane Doe", patient_data)
    
    if result:
        print("\n🎉 Successfully stored prediction in Supabase!")

if __name__ == "__main__":
    main() 