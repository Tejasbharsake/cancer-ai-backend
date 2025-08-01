"""
Fallback Doctor Explanation Generator (without OpenAI)
Generates professional medical explanations for cancer predictions using templates
"""

from typing import Dict, Any
import random

class FallbackDoctorExplanationGenerator:
    def __init__(self):
        """Initialize the fallback explanation generator"""
        self.cancer_info = {
            'Lung': {
                'description': 'Lung cancer is a type of cancer that begins in the lungs and can spread to other parts of the body.',
                'risk_factors': ['smoking', 'age over 65', 'family history', 'exposure to radon or asbestos'],
                'symptoms': ['persistent cough', 'chest pain', 'shortness of breath', 'weight loss', 'fatigue'],
                'tests': ['chest X-ray', 'CT scan', 'biopsy', 'PET scan'],
                'specialists': ['pulmonologist', 'oncologist']
            },
            'Breast': {
                'description': 'Breast cancer occurs when cells in breast tissue grow uncontrollably.',
                'risk_factors': ['age', 'family history', 'genetic mutations (BRCA1/BRCA2)', 'hormone exposure'],
                'symptoms': ['breast lump', 'breast pain', 'skin changes', 'nipple discharge'],
                'tests': ['mammography', 'breast ultrasound', 'biopsy', 'MRI'],
                'specialists': ['breast surgeon', 'oncologist']
            },
            'Colorectal': {
                'description': 'Colorectal cancer begins in the colon or rectum and is often preventable with screening.',
                'risk_factors': ['age over 50', 'family history', 'inflammatory bowel disease', 'diet high in red meat'],
                'symptoms': ['changes in bowel habits', 'blood in stool', 'abdominal pain', 'weight loss'],
                'tests': ['colonoscopy', 'CT scan', 'blood tests (CEA)', 'biopsy'],
                'specialists': ['gastroenterologist', 'colorectal surgeon', 'oncologist']
            },
            'Prostate': {
                'description': 'Prostate cancer develops in the prostate gland and is common in older men.',
                'risk_factors': ['age over 65', 'family history', 'race (higher in African Americans)', 'diet'],
                'symptoms': ['difficulty urinating', 'blood in urine', 'pelvic pain', 'erectile dysfunction'],
                'tests': ['PSA blood test', 'digital rectal exam', 'biopsy', 'MRI'],
                'specialists': ['urologist', 'oncologist']
            },
            'Pancreatic': {
                'description': 'Pancreatic cancer is a serious form of cancer that develops in the pancreas.',
                'risk_factors': ['smoking', 'diabetes', 'family history', 'chronic pancreatitis'],
                'symptoms': ['abdominal pain', 'weight loss', 'jaundice', 'new-onset diabetes'],
                'tests': ['CT scan', 'MRI', 'endoscopic ultrasound', 'biopsy'],
                'specialists': ['gastroenterologist', 'oncologist', 'pancreatic surgeon']
            },
            'Melanoma': {
                'description': 'Melanoma is the most serious type of skin cancer that develops in melanocytes.',
                'risk_factors': ['UV exposure', 'fair skin', 'family history', 'multiple moles'],
                'symptoms': ['changing moles', 'new skin growths', 'asymmetrical spots', 'irregular borders'],
                'tests': ['skin biopsy', 'dermoscopy', 'sentinel lymph node biopsy', 'imaging studies'],
                'specialists': ['dermatologist', 'oncologist']
            }
        }
    
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
        Generate a doctor-style explanation using templates
        """
        
        cancer_info = self.cancer_info.get(predicted_cancer_type, self.cancer_info['Lung'])
        
        # Generate explanation
        explanation = self._generate_explanation(
            patient_name, age, gender, predicted_cancer_type, 
            confidence_score, symptoms, medical_data, cancer_info
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            predicted_cancer_type, symptoms, medical_data, cancer_info
        )
        
        # Generate next steps
        next_steps = self._generate_next_steps(predicted_cancer_type, cancer_info)
        
        return {
            "explanation": explanation,
            "recommendations": recommendations,
            "next_steps": next_steps,
            "confidence_interpretation": self._interpret_confidence(confidence_score),
            "full_response": f"{explanation}\n\nRECOMMENDATIONS:\n{recommendations}\n\nNEXT STEPS:\n{next_steps}"
        }
    
    def _generate_explanation(self, patient_name, age, gender, cancer_type, confidence, symptoms, medical_data, cancer_info):
        """Generate the main explanation"""
        
        confidence_text = self._get_confidence_text(confidence)
        risk_factors = self._identify_risk_factors(age, gender, medical_data, cancer_info)
        symptom_analysis = self._analyze_symptoms(symptoms)
        
        explanation = f"""Dear {patient_name},

Based on our AI analysis of your medical information, there is a {confidence:.1%} likelihood that you may be at risk for {cancer_type.lower()} cancer. {confidence_text}

{cancer_info['description']}

Your risk assessment is based on several factors:
- Age: {age} years old
- Gender: {gender}
{risk_factors}

Symptom Analysis:
{symptom_analysis}

It's important to understand that this is a preliminary AI assessment and not a definitive diagnosis. Many conditions can present with similar symptoms, and further medical evaluation is essential for accurate diagnosis."""

        return explanation
    
    def _generate_recommendations(self, cancer_type, symptoms, medical_data, cancer_info):
        """Generate medical recommendations"""
        
        recommendations = f"""Based on your risk profile, I recommend the following:

IMMEDIATE MEDICAL EVALUATION:
• Schedule an appointment with your primary care physician within 1-2 weeks
• Discuss your symptoms and risk factors in detail
• Request appropriate screening tests

RECOMMENDED TESTS:
"""
        
        for test in cancer_info['tests']:
            recommendations += f"• {test.title()}\n"
        
        recommendations += f"""
LIFESTYLE MODIFICATIONS:
• Maintain a healthy diet rich in fruits and vegetables
• Exercise regularly as tolerated
• Avoid tobacco and limit alcohol consumption
• Follow up on any chronic medical conditions

MONITORING:
• Keep a symptom diary noting any changes
• Report any new or worsening symptoms immediately
• Follow recommended screening schedules for your age group"""

        return recommendations
    
    def _generate_next_steps(self, cancer_type, cancer_info):
        """Generate next steps"""
        
        specialists = ", ".join(cancer_info['specialists'])
        
        next_steps = f"""IMMEDIATE ACTIONS (Within 1-2 weeks):
1. Contact your primary care physician to discuss these findings
2. Schedule a comprehensive physical examination
3. Bring a list of all current symptoms and medications

FOLLOW-UP CARE (Within 2-4 weeks):
1. Complete recommended diagnostic tests
2. Consider consultation with specialists: {specialists}
3. Discuss family history and genetic counseling if appropriate

ONGOING MONITORING:
1. Attend all scheduled appointments
2. Follow through with recommended treatments or surveillance
3. Maintain open communication with your healthcare team
4. Seek immediate medical attention for any concerning new symptoms

Remember: Early detection and treatment significantly improve outcomes for most types of cancer. This AI assessment is a tool to help guide your healthcare decisions, but professional medical evaluation is essential."""

        return next_steps
    
    def _identify_risk_factors(self, age, gender, medical_data, cancer_info):
        """Identify relevant risk factors"""
        risk_factors = []
        
        if age > 65:
            risk_factors.append("- Advanced age (increased risk)")
        elif age > 50:
            risk_factors.append("- Age over 50 (moderate risk factor)")
        
        if medical_data:
            if medical_data.get('smoking_status') == 'Current':
                risk_factors.append("- Current smoking (significant risk factor)")
            elif medical_data.get('smoking_status') == 'Former':
                risk_factors.append("- Former smoking history (elevated risk)")
            
            if medical_data.get('family_history'):
                risk_factors.append("- Family history of cancer (genetic predisposition)")
            
            if medical_data.get('bmi', 0) > 30:
                risk_factors.append("- Obesity (BMI > 30, increased risk)")
        
        return "\n".join(risk_factors) if risk_factors else "- No major risk factors identified"
    
    def _analyze_symptoms(self, symptoms):
        """Analyze patient symptoms"""
        symptom_analysis = []
        
        fatigue = symptoms.get('fatigue_level', 1)
        if fatigue > 3:
            symptom_analysis.append(f"- Significant fatigue (level {fatigue}/5) - concerning symptom")
        elif fatigue > 2:
            symptom_analysis.append(f"- Moderate fatigue (level {fatigue}/5) - worth monitoring")
        
        pain = symptoms.get('pain_level', 1)
        if pain > 3:
            symptom_analysis.append(f"- Significant pain (level {pain}/5) - requires evaluation")
        elif pain > 2:
            symptom_analysis.append(f"- Moderate pain (level {pain}/5) - should be assessed")
        
        if symptoms.get('weight_loss'):
            symptom_analysis.append("- Unexplained weight loss - important warning sign")
        
        if symptoms.get('night_sweats'):
            symptom_analysis.append("- Night sweats - can indicate systemic illness")
        
        if symptoms.get('appetite_loss'):
            symptom_analysis.append("- Loss of appetite - concerning symptom")
        
        symptom_count = symptoms.get('symptom_count', 0)
        if symptom_count > 3:
            symptom_analysis.append(f"- Multiple symptoms present ({symptom_count}) - comprehensive evaluation needed")
        
        return "\n".join(symptom_analysis) if symptom_analysis else "- Minimal symptoms reported - good prognostic sign"
    
    def _get_confidence_text(self, confidence):
        """Get confidence interpretation text"""
        if confidence >= 0.8:
            return "This represents a high-confidence prediction with multiple risk factors present."
        elif confidence >= 0.6:
            return "This represents a moderate-confidence prediction with several indicators present."
        elif confidence >= 0.4:
            return "This represents a low-to-moderate confidence prediction with some risk factors identified."
        else:
            return "This represents a low-confidence prediction with minimal risk factors present."
    
    def _interpret_confidence(self, confidence: float) -> str:
        """Interpret the confidence score in medical terms"""
        if confidence >= 0.9:
            return "Very high confidence - multiple strong indicators present"
        elif confidence >= 0.7:
            return "High confidence - several risk factors align"
        elif confidence >= 0.5:
            return "Moderate confidence - some indicators present"
        elif confidence >= 0.3:
            return "Low confidence - limited indicators"
        else:
            return "Very low confidence - minimal risk factors"


def generate_fallback_explanation(
    patient_data: Dict[str, Any], 
    prediction_result: Dict[str, Any]
) -> Dict[str, str]:
    """
    Generate explanation using fallback method (no OpenAI required)
    """
    
    generator = FallbackDoctorExplanationGenerator()
    
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


# Test the fallback generator
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
    
    print("=" * 60)
    print("🏥 GENERATING FALLBACK DOCTOR EXPLANATION")
    print("=" * 60)
    
    explanation = generate_fallback_explanation(sample_patient, sample_prediction)
    
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