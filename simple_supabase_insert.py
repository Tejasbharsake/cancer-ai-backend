"""
Simple Supabase connection and data insertion for Cancer Predictions
"""

from supabase import create_client, Client
from simple_cancer_predictor import predict_cancer_type
from datetime import datetime

def connect_to_supabase(supabase_url: str, supabase_key: str):
    """
    Connect to Supabase
    
    Args:
        supabase_url (str): Your Supabase project URL
        supabase_key (str): Your Supabase anon/public key
    
    Returns:
        Client: Supabase client instance
    """
    try:
        supabase = create_client(supabase_url, supabase_key)
        print("✅ Connected to Supabase successfully!")
        return supabase
    except Exception as e:
        print(f"❌ Failed to connect to Supabase: {e}")
        return None

def insert_prediction_data(supabase: Client, name: str, age: int, gender: str, 
                          prediction_result: str, confidence_score: float):
    """
    Insert prediction data into the 'predictions' table
    
    Args:
        supabase (Client): Supabase client
        name (str): Patient name
        age (int): Patient age
        gender (str): Patient gender
        prediction_result (str): Predicted cancer type
        confidence_score (float): Confidence score (0-1)
    
    Returns:
        dict: Inserted record data or None if failed
    """
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
            print(f"   Age: {age}")
            print(f"   Gender: {gender}")
            print(f"   Prediction: {prediction_result}")
            print(f"   Confidence: {confidence_score:.2%}")
            return response.data[0]
        else:
            print("❌ Failed to insert data")
            return None
            
    except Exception as e:
        print(f"❌ Error inserting data: {e}")
        return None

def predict_and_insert(supabase: Client, name: str, patient_data: dict):
    """
    Make a cancer prediction and insert the result into Supabase
    
    Args:
        supabase (Client): Supabase client
        name (str): Patient name
        patient_data (dict): Patient data for prediction
    
    Returns:
        dict: Inserted record data or None if failed
    """
    try:
        # Make prediction using our cancer predictor
        print(f"🔬 Making prediction for {name}...")
        result = predict_cancer_type(patient_data)
        
        # Extract data for storage
        prediction_result = result['predicted_cancer_type']
        confidence_score = result['confidence_score']
        age = patient_data.get('age', 0)
        gender = patient_data.get('gender', 'Unknown')
        
        # Insert into Supabase
        return insert_prediction_data(
            supabase=supabase,
            name=name,
            age=age,
            gender=gender,
            prediction_result=prediction_result,
            confidence_score=confidence_score
        )
        
    except Exception as e:
        print(f"❌ Error in predict_and_insert: {e}")
        return None

def get_recent_predictions(supabase: Client, limit: int = 5):
    """
    Get recent predictions from the database
    
    Args:
        supabase (Client): Supabase client
        limit (int): Maximum number of records to retrieve
    
    Returns:
        list: List of prediction records
    """
    try:
        response = supabase.table('predictions').select('*').order('created_at', desc=True).limit(limit).execute()
        return response.data
    except Exception as e:
        print(f"❌ Error retrieving predictions: {e}")
        return []

def main():
    """Example usage"""
    
    # Replace with your actual Supabase credentials
    SUPABASE_URL = "YOUR_SUPABASE_URL"
    SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"
    
    # Check if credentials are provided
    if SUPABASE_URL == "YOUR_SUPABASE_URL" or SUPABASE_KEY == "YOUR_SUPABASE_ANON_KEY":
        print("⚠️  Please update the Supabase credentials!")
        print("\n📋 To get your credentials:")
        print("   1. Go to your Supabase project dashboard")
        print("   2. Navigate to Settings > API")
        print("   3. Copy the Project URL and anon/public key")
        print("\n📋 Create the predictions table with this SQL:")
        print("""
        CREATE TABLE predictions (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            age INTEGER NOT NULL,
            gender VARCHAR(10) NOT NULL,
            prediction_result VARCHAR(50) NOT NULL,
            confidence_score DECIMAL(5,4) NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """)
        return
    
    # Connect to Supabase
    supabase = connect_to_supabase(SUPABASE_URL, SUPABASE_KEY)
    if not supabase:
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
    
    # Make prediction and insert
    print("\n" + "="*50)
    print("MAKING PREDICTION AND INSERTING INTO SUPABASE")
    print("="*50)
    
    inserted_record = predict_and_insert(supabase, "Jane Doe", patient_data)
    
    if inserted_record:
        print("\n📊 Retrieving recent predictions...")
        recent_predictions = get_recent_predictions(supabase, limit=5)
        
        print(f"\nRecent predictions ({len(recent_predictions)} records):")
        for pred in recent_predictions:
            print(f"  - {pred['name']} ({pred['age']}): {pred['prediction_result']} ({pred['confidence_score']:.2%})")

if __name__ == "__main__":
    main() 