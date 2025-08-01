"""
OpenAI GPT-powered Doctor Explanation Generator
Generates professional medical explanations for cancer predictions
"""

import openai
import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional

# Load environment variables
load_dotenv()

class DoctorExplanationGenerator:
    def __init__(self, api_key: str = None):
        """
        Initialize the OpenAI client
        
        Args:
            api_key (str): OpenAI API key. If None, will try to get from environment
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it directly.")
        
        # Initialize OpenAI client
        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def generate_doctor_explanation(
        self, 
        patient_name: str,
        age: int,
        gender: str,
        predicted_cancer_type: str,
        confidence_score: float,
        symptoms: Dict[str, Any],
        medical_data: Dict[str, Any] = None
    ) -> Dict[str, str]:
        """
        Generate a doctor-style explanation of the cancer prediction
        
        Args:
            patient_name (str): Patient's name
            age (int): Patient's age
            gender (str): Patient's gender
            predicted_cancer_type (str): Predicted cancer type
            confidence_score (float): Confidence score (0-1)
            symptoms (dict): Patient symptoms and levels
            medical_data (dict): Additional medical data
            
        Returns:
            dict: Contains explanation, recommendations, and next_steps
        """
        
        # Prepare symptom description
        symptom_description = self._format_symptoms(symptoms)
        
        # Prepare medical data description
        medical_description = self._format_medical_data(medical_data) if medical_data else ""
        
        # Create the prompt for GPT
        prompt = self._create_doctor_prompt(
            patient_name, age, gender, predicted_cancer_type, 
            confidence_score, symptom_description, medical_description
        )
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an experienced oncologist providing a professional medical explanation. Be compassionate, clear, and thorough while maintaining medical accuracy. Always emphasize the importance of further medical evaluation."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            # Parse the response
            full_response = response.choices[0].message.content
            
            # Split the response into sections
            sections = self._parse_response_sections(full_response)
            
            return {
                "explanation": sections.get("explanation", full_response),
                "recommendations": sections.get("recommendations", ""),
                "next_steps": sections.get("next_steps", ""),
                "full_response": full_response,
                "confidence_interpretation": self._interpret_confidence(confidence_score)
            }
            
        except Exception as e:
            return {
                "error": f"Failed to generate explanation: {str(e)}",
                "explanation": f"Based on the AI analysis, there is a {confidence_score:.1%} likelihood of {predicted_cancer_type} cancer. Please consult with a healthcare professional for proper diagnosis and treatment.",
                "recommendations": "Immediate consultation with an oncologist is recommended.",
                "next_steps": "Schedule an appointment with your healthcare provider as soon as possible."
            }
    
    def _format_symptoms(self, symptoms: Dict[str, Any]) -> str:
        """Format symptoms into a readable description"""
        symptom_parts = []
        
        if symptoms.get('fatigue_level', 0) > 2:
            symptom_parts.append(f"significant fatigue (level {symptoms['fatigue_level']}/5)")
        
        if symptoms.get('pain_level', 0) > 2:
            symptom_parts.append(f"pain (level {symptoms['pain_level']}/5)")
        
        if symptoms.get('weight_loss', 0):
            symptom_parts.append("unexplained weight loss")
        
        if symptoms.get('night_sweats', 0):
            symptom_parts.append("night sweats")
        
        if symptoms.get('appetite_loss', 0):
            symptom_parts.append("loss of appetite")
        
        if symptoms.get('symptom_count', 0) > 0:
            symptom_parts.append(f"total of {symptoms['symptom_count']} reported symptoms")
        
        return ", ".join(symptom_parts) if symptom_parts else "minimal symptoms reported"
    
    def _format_medical_data(self, medical_data: Dict[str, Any]) -> str:
        """Format medical data into a readable description"""
        data_parts = []
        
        if medical_data.get('bmi'):
            bmi = medical_data['bmi']
            if bmi > 30:
                data_parts.append(f"BMI of {bmi} (obese)")
            elif bmi > 25:
                data_parts.append(f"BMI of {bmi} (overweight)")
            else:
                data_parts.append(f"BMI of {bmi} (normal)")
        
        if medical_data.get('smoking_status'):
            smoking = medical_data['smoking_status']
            if smoking == 'Current':
                data_parts.append("current smoker")
            elif smoking == 'Former':
                data_parts.append("former smoker")
        
        if medical_data.get('family_history'):
            data_parts.append("family history of cancer")
        
        if medical_data.get('blood_pressure', 0) > 140:
            data_parts.append(f"elevated blood pressure ({medical_data['blood_pressure']} mmHg)")
        
        return ", ".join(data_parts) if data_parts else ""
    
    def _create_doctor_prompt(
        self, patient_name: str, age: int, gender: str, 
        cancer_type: str, confidence: float, symptoms: str, medical_data: str
    ) -> str:
        """Create the prompt for OpenAI"""
        
        return f"""
Please provide a professional medical explanation for the following patient case:

Patient: {patient_name}
Age: {age} years old
Gender: {gender}
AI Prediction: {cancer_type} cancer
Confidence Level: {confidence:.1%}

Symptoms: {symptoms}
Medical History: {medical_data}

Please structure your response with the following sections:

**EXPLANATION:**
Provide a clear, compassionate explanation of what this prediction means, considering the patient's age, gender, and symptoms. Explain the cancer type in understandable terms.

**RECOMMENDATIONS:**
List specific medical recommendations, tests, or lifestyle changes that would be appropriate.

**NEXT STEPS:**
Outline the immediate next steps the patient should take, including which specialists to see and timeline for follow-up.

Remember to:
- Be compassionate and reassuring while being honest
- Emphasize that this is an AI prediction and requires medical confirmation
- Use language appropriate for a patient consultation
- Include relevant medical context for the specific cancer type
- Address any risk factors mentioned in the medical history
"""
    
    def _parse_response_sections(self, response: str) -> Dict[str, str]:
        """Parse the GPT response into sections"""
        sections = {}
        current_section = None
        current_content = []
        
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            
            if '**EXPLANATION:**' in line.upper():
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'explanation'
                current_content = []
            elif '**RECOMMENDATIONS:**' in line.upper():
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'recommendations'
                current_content = []
            elif '**NEXT STEPS:**' in line.upper():
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'next_steps'
                current_content = []
            elif line and not line.startswith('**'):
                current_content.append(line)
        
        # Add the last section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    def _interpret_confidence(self, confidence: float) -> str:
        """Interpret the confidence score in medical terms"""
        if confidence >= 0.9:
            return "Very high confidence - strong indicators present"
        elif confidence >= 0.7:
            return "High confidence - multiple risk factors align"
        elif confidence >= 0.5:
            return "Moderate confidence - some indicators present"
        elif confidence >= 0.3:
            return "Low confidence - limited indicators"
        else:
            return "Very low confidence - minimal risk factors"


def generate_explanation_for_prediction(
    patient_data: Dict[str, Any], 
    prediction_result: Dict[str, Any],
    openai_api_key: str = None
) -> Dict[str, str]:
    """
    Convenience function to generate explanation from prediction data
    
    Args:
        patient_data (dict): Patient information and symptoms
        prediction_result (dict): Cancer prediction results
        openai_api_key (str): OpenAI API key
        
    Returns:
        dict: Generated explanation sections
    """
    
    try:
        generator = DoctorExplanationGenerator(openai_api_key)
        
        # Extract symptoms
        symptoms = {
            'fatigue_level': patient_data.get('fatigue_level', 1),
            'pain_level': patient_data.get('pain_level', 1),
            'weight_loss': patient_data.get('weight_loss', 0),
            'night_sweats': patient_data.get('night_sweats', 0),
            'appetite_loss': patient_data.get('appetite_loss', 0),
            'symptom_count': patient_data.get('symptom_count', 0)
        }
        
        # Extract medical data
        medical_data = {
            'bmi': patient_data.get('bmi', 0),
            'smoking_status': patient_data.get('smoking_status', ''),
            'family_history': patient_data.get('family_history', 0),
            'blood_pressure': patient_data.get('blood_pressure', 0),
            'cholesterol': patient_data.get('cholesterol', 0),
            'glucose': patient_data.get('glucose', 0)
        }
        
        return generator.generate_doctor_explanation(
            patient_name=patient_data.get('name', 'Patient'),
            age=patient_data.get('age', 0),
            gender=patient_data.get('gender', 'Unknown'),
            predicted_cancer_type=prediction_result.get('predicted_cancer_type', 'Unknown'),
            confidence_score=prediction_result.get('confidence_score', 0),
            symptoms=symptoms,
            medical_data=medical_data
        )
        
    except Exception as e:
        return {
            "error": f"Failed to generate explanation: {str(e)}",
            "explanation": "Unable to generate detailed explanation at this time.",
            "recommendations": "Please consult with a healthcare professional.",
            "next_steps": "Schedule an appointment with your doctor."
        }


# Example usage and testing
if __name__ == "__main__":
    # Example patient data
    sample_patient = {
        'name': 'John Smith',
        'age': 65,
        'gender': 'Male',
        'bmi': 28.5,
        'smoking_status': 'Former',
        'family_history': 1,
        'fatigue_level': 4,
        'pain_level': 3,
        'weight_loss': 1,
        'night_sweats': 0,
        'appetite_loss': 1,
        'symptom_count': 4
    }
    
    sample_prediction = {
        'predicted_cancer_type': 'Lung',
        'confidence_score': 0.78
    }
    
    # Get OpenAI API key from environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ OpenAI API key not found in environment variables")
        print("   Please set OPENAI_API_KEY in your .env file")
        return
    
    print("=" * 60)
    print("🏥 GENERATING DOCTOR EXPLANATION")
    print("=" * 60)
    
    explanation = generate_explanation_for_prediction(
        sample_patient, 
        sample_prediction, 
        api_key
    )
    
    if "error" in explanation:
        print(f"❌ Error: {explanation['error']}")
    else:
        print(f"👨‍⚕️ Doctor's Explanation for {sample_patient['name']}:")
        print(f"   Prediction: {sample_prediction['predicted_cancer_type']} ({sample_prediction['confidence_score']:.1%})")
        print("\n📋 EXPLANATION:")
        print(explanation['explanation'])
        print("\n💊 RECOMMENDATIONS:")
        print(explanation['recommendations'])
        print("\n📅 NEXT STEPS:")
        print(explanation['next_steps'])
        print(f"\n🎯 CONFIDENCE INTERPRETATION:")
        print(explanation['confidence_interpretation'])