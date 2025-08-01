"""
Comprehensive Supabase connection and functionality test
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client
from simple_cancer_predictor import predict_cancer_type
from datetime import datetime

# Load environment variables
load_dotenv()

def test_environment_variables():
    """Test if environment variables are loaded correctly"""
    print("🧪 Testing Environment Variables...")
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if supabase_url and supabase_key:
        print("✅ Environment variables loaded successfully")
        print(f"   URL: {supabase_url[:30]}...")
        print(f"   Key: {supabase_key[:30]}...")
        return True
    else:
        print("❌ Environment variables not found")
        return False

def test_supabase_connection():
    """Test Supabase connection"""
    print("\n🧪 Testing Supabase Connection...")
    
    try:
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        supabase = create_client(supabase_url, supabase_key)
        
        # Test connection by trying to access the predictions table
        response = supabase.table('predictions').select('*').limit(1).execute()
        
        print("✅ Supabase connection successful")
        print(f"   Connected to: {supabase_url}")
        return supabase
        
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return None

def test_table_access(supabase: Client):
    """Test table access and structure"""
    print("\n🧪 Testing Table Access...")
    
    try:
        # Try to get recent records
        response = supabase.table('predictions').select('*').order('created_at', desc=True).limit(3).execute()
        
        if response.data:
            print(f"✅ Table access successful - Found {len(response.data)} records")
            print("   Recent predictions:")
            for record in response.data:
                print(f"     - {record.get('name', 'Unknown')}: {record.get('prediction_result', 'N/A')} ({record.get('confidence_score', 0):.2%})")
        else:
            print("✅ Table access successful - No records found (empty table)")
        
        return True
        
    except Exception as e:
        print(f"❌ Table access failed: {e}")
        return False

def test_cancer_prediction():
    """Test cancer prediction functionality"""
    print("\n🧪 Testing Cancer Prediction...")
    
    try:
        # Test patient data
        test_patient = {
            'age': 55,
            'gender': 'Male',
            'bmi': 28.0,
            'smoking_status': 'Current',
            'family_history': 1,
            'blood_pressure': 140,
            'cholesterol': 200,
            'glucose': 110,
            'white_blood_cells': 7.5,
            'platelet_count': 250,
            'hemoglobin': 14.0,
            'symptom_count': 3,
            'fatigue_level': 3,
            'pain_level': 2,
            'weight_loss': 1,
            'night_sweats': 0,
            'appetite_loss': 1
        }
        
        result = predict_cancer_type(test_patient)
        
        print("✅ Cancer prediction successful")
        print(f"   Predicted Type: {result['predicted_cancer_type']}")
        print(f"   Confidence: {result['confidence_score']:.2%}")
        
        return result
        
    except Exception as e:
        print(f"❌ Cancer prediction failed: {e}")
        return None

def test_data_insertion(supabase: Client, prediction_result):
    """Test data insertion into Supabase"""
    print("\n🧪 Testing Data Insertion...")
    
    try:
        test_data = {
            'name': 'Test Patient',
            'age': 55,
            'gender': 'Male',
            'prediction_result': prediction_result['predicted_cancer_type'],
            'confidence_score': prediction_result['confidence_score'],
            'created_at': datetime.now().isoformat()
        }
        
        response = supabase.table('predictions').insert(test_data).execute()
        
        if response.data:
            print("✅ Data insertion successful")
            print(f"   Inserted ID: {response.data[0]['id']}")
            print(f"   Patient: {test_data['name']}")
            print(f"   Prediction: {test_data['prediction_result']}")
            return response.data[0]
        else:
            print("❌ Data insertion failed - No data returned")
            return None
            
    except Exception as e:
        print(f"❌ Data insertion failed: {e}")
        return None

def test_data_retrieval(supabase: Client):
    """Test data retrieval from Supabase"""
    print("\n🧪 Testing Data Retrieval...")
    
    try:
        # Get all test records
        response = supabase.table('predictions').select('*').eq('name', 'Test Patient').execute()
        
        if response.data:
            print(f"✅ Data retrieval successful - Found {len(response.data)} test records")
            for record in response.data:
                print(f"   - ID: {record['id'][:8]}... | {record['name']} | {record['prediction_result']}")
        else:
            print("✅ Data retrieval successful - No test records found")
        
        return response.data
        
    except Exception as e:
        print(f"❌ Data retrieval failed: {e}")
        return None

def cleanup_test_data(supabase: Client):
    """Clean up test data"""
    print("\n🧹 Cleaning up test data...")
    
    try:
        # Delete test records
        response = supabase.table('predictions').delete().eq('name', 'Test Patient').execute()
        
        print("✅ Test data cleanup completed")
        
    except Exception as e:
        print(f"⚠️  Test data cleanup failed: {e}")

def run_all_tests():
    """Run all Supabase tests"""
    print("=" * 60)
    print("🚀 SUPABASE COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    # Test 1: Environment Variables
    if not test_environment_variables():
        print("\n❌ Test suite failed - Environment variables not found")
        return False
    
    # Test 2: Supabase Connection
    supabase = test_supabase_connection()
    if not supabase:
        print("\n❌ Test suite failed - Cannot connect to Supabase")
        return False
    
    # Test 3: Table Access
    if not test_table_access(supabase):
        print("\n❌ Test suite failed - Cannot access predictions table")
        return False
    
    # Test 4: Cancer Prediction
    prediction_result = test_cancer_prediction()
    if not prediction_result:
        print("\n❌ Test suite failed - Cancer prediction not working")
        return False
    
    # Test 5: Data Insertion
    inserted_record = test_data_insertion(supabase, prediction_result)
    if not inserted_record:
        print("\n❌ Test suite failed - Cannot insert data")
        return False
    
    # Test 6: Data Retrieval
    retrieved_data = test_data_retrieval(supabase)
    if retrieved_data is None:
        print("\n❌ Test suite failed - Cannot retrieve data")
        return False
    
    # Test 7: Cleanup
    cleanup_test_data(supabase)
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED SUCCESSFULLY!")
    print("✅ Your Supabase integration is working perfectly")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    run_all_tests()