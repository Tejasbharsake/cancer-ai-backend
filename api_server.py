"""
FastAPI server for Cancer Prediction System
Handles prediction requests from React frontend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from simple_cancer_predictor import predict_cancer_type
from datetime import datetime
from doctor_explanation_fallback import generate_fallback_explanation
from openai_doctor_explanation import generate_explanation_for_prediction

# Load environment variables
load_dotenv()

app = FastAPI(title="Cancer Prediction API", version="1.0.0")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class PatientData(BaseModel):
    name: str
    age: int
    gender: str
    bmi: float
    smoking_status: str
    family_history: int
    blood_pressure: int
    cholesterol: int
    glucose: int
    white_blood_cells: float
    platelet_count: int
    hemoglobin: float
    symptom_count: int
    fatigue_level: int
    pain_level: int
    weight_loss: int
    night_sweats: int
    appetite_loss: int

class PredictionResponse(BaseModel):
    predicted_cancer_type: str
    confidence_score: float
    patient_name: str
    prediction_id: Optional[str] = None

class DoctorExplanationResponse(BaseModel):
    explanation: str
    recommendations: str
    next_steps: str
    confidence_interpretation: str
    full_response: str
    error: Optional[str] = None

# Initialize Supabase client
def get_supabase_client():
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        return None
    
    try:
        return create_client(supabase_url, supabase_key)
    except Exception as e:
        print(f"Failed to connect to Supabase: {e}")
        return None

@app.get("/")
async def root():
    return {"message": "Cancer Prediction API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Cancer Prediction API"}

@app.post("/predict", response_model=PredictionResponse)
async def predict_cancer(patient_data: PatientData):
    """
    Predict cancer type based on patient data
    """
    try:
        # Convert Pydantic model to dict for the prediction function
        patient_dict = {
            'age': patient_data.age,
            'gender': patient_data.gender,
            'bmi': patient_data.bmi,
            'smoking_status': patient_data.smoking_status,
            'family_history': patient_data.family_history,
            'blood_pressure': patient_data.blood_pressure,
            'cholesterol': patient_data.cholesterol,
            'glucose': patient_data.glucose,
            'white_blood_cells': patient_data.white_blood_cells,
            'platelet_count': patient_data.platelet_count,
            'hemoglobin': patient_data.hemoglobin,
            'symptom_count': patient_data.symptom_count,
            'fatigue_level': patient_data.fatigue_level,
            'pain_level': patient_data.pain_level,
            'weight_loss': patient_data.weight_loss,
            'night_sweats': patient_data.night_sweats,
            'appetite_loss': patient_data.appetite_loss
        }
        
        # Make prediction using the existing model
        print(f"Making prediction for {patient_data.name}...")
        prediction_result = predict_cancer_type(patient_dict)
        
        # Store prediction in Supabase (optional)
        prediction_id = None
        supabase = get_supabase_client()
        
        if supabase:
            try:
                # Store prediction in database
                db_data = {
                    'name': patient_data.name,
                    'age': patient_data.age,
                    'gender': patient_data.gender,
                    'prediction_result': prediction_result['predicted_cancer_type'],
                    'confidence_score': prediction_result['confidence_score'],
                    'created_at': datetime.now().isoformat()
                }
                
                response = supabase.table('predictions').insert(db_data).execute()
                if response.data:
                    prediction_id = response.data[0]['id']
                    print(f"Stored prediction in database with ID: {prediction_id}")
                    
            except Exception as e:
                print(f"Failed to store prediction in database: {e}")
                # Continue without storing - don't fail the prediction
        
        # Return prediction response
        return PredictionResponse(
            predicted_cancer_type=prediction_result['predicted_cancer_type'],
            confidence_score=prediction_result['confidence_score'],
            patient_name=patient_data.name,
            prediction_id=prediction_id
        )
        
    except Exception as e:
        print(f"Prediction error: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to make prediction: {str(e)}"
        )

@app.post("/explain", response_model=DoctorExplanationResponse)
async def generate_doctor_explanation(patient_data: PatientData):
    """
    Generate a doctor-style explanation for cancer prediction
    """
    try:
        # Convert Pydantic model to dict for the prediction function
        patient_dict = {
            'age': patient_data.age,
            'gender': patient_data.gender,
            'bmi': patient_data.bmi,
            'smoking_status': patient_data.smoking_status,
            'family_history': patient_data.family_history,
            'blood_pressure': patient_data.blood_pressure,
            'cholesterol': patient_data.cholesterol,
            'glucose': patient_data.glucose,
            'white_blood_cells': patient_data.white_blood_cells,
            'platelet_count': patient_data.platelet_count,
            'hemoglobin': patient_data.hemoglobin,
            'symptom_count': patient_data.symptom_count,
            'fatigue_level': patient_data.fatigue_level,
            'pain_level': patient_data.pain_level,
            'weight_loss': patient_data.weight_loss,
            'night_sweats': patient_data.night_sweats,
            'appetite_loss': patient_data.appetite_loss,
            'name': patient_data.name
        }
        
        # Make prediction first
        print(f"Making prediction for explanation for {patient_data.name}...")
        prediction_result = predict_cancer_type(patient_dict)
        
        # Try OpenAI first, fallback to template-based explanation
        try:
            openai_key = os.getenv('OPENAI_API_KEY')
            if openai_key:
                explanation = generate_explanation_for_prediction(
                    patient_dict, prediction_result, openai_key
                )
                if "error" not in explanation:
                    return DoctorExplanationResponse(**explanation)
        except Exception as e:
            print(f"OpenAI explanation failed: {e}")
        
        # Use fallback explanation
        print("Using fallback explanation generator...")
        explanation = generate_fallback_explanation(patient_dict, prediction_result)
        
        return DoctorExplanationResponse(**explanation)
        
    except Exception as e:
        print(f"Explanation generation error: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate explanation: {str(e)}"
        )

@app.get("/predictions")
async def get_recent_predictions(limit: int = 10):
    """
    Get recent predictions from the database
    """
    supabase = get_supabase_client()
    
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection not available")
    
    try:
        response = supabase.table('predictions').select('*').order('created_at', desc=True).limit(limit).execute()
        return {"predictions": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch predictions: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("Starting Cancer Prediction API server...")
    print("API will be available at: http://localhost:8000")
    print("API docs will be available at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)