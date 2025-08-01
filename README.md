# 🏥 Cancer AI Prediction System

A comprehensive AI-powered cancer prediction system with FastAPI backend, Next.js frontend, and OpenAI-powered doctor explanations.

## 🚀 Features

- **🤖 AI Cancer Prediction**: Machine learning model for cancer type prediction
- **👨‍⚕️ Doctor Explanations**: OpenAI GPT-powered medical explanations
- **💾 Database Integration**: Supabase for storing predictions
- **🌐 Web Interface**: React/Next.js frontend with Tailwind CSS
- **📊 Real-time Results**: Live prediction results and confidence scores
- **🔒 Secure**: Environment-based configuration for API keys

## 🏗️ Architecture

```
├── Backend (Python FastAPI)
│   ├── Cancer Prediction Model
│   ├── OpenAI Integration
│   ├── Supabase Database
│   └── REST API Endpoints
│
├── Frontend (Next.js/React)
│   ├── Patient Input Form
│   ├── Prediction Results
│   ├── Recent Predictions
│   └── Responsive UI
│
└── Database (Supabase)
    └── Predictions Storage
```

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- Supabase Account
- OpenAI API Key (optional)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Tejasbharsake/cancer-ai-backend.git
cd cancer-ai-backend
```

### 2. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env with your credentials
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
OPENAI_API_KEY=your_openai_key  # Optional
```

### 3. Frontend Setup

```bash
cd cancer-ai-web
npm install

# Create environment file
cp .env.local.example .env.local

# Edit .env.local with your Supabase credentials
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_key
```

### 4. Database Setup

Create a table in your Supabase database:

```sql
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INTEGER NOT NULL,
    gender VARCHAR(10) NOT NULL,
    prediction_result VARCHAR(50) NOT NULL,
    confidence_score DECIMAL(5,4) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 🚀 Running the Application

### Start Backend Server

```bash
python api_server.py
```

The API will be available at `http://localhost:8000`

### Start Frontend Server

```bash
cd cancer-ai-web
npm run dev
```

The web app will be available at `http://localhost:3000`

### Start Both Servers

```bash
python start_servers.py
```

## 📚 API Documentation

### Endpoints

- **POST /predict** - Get cancer prediction
- **POST /explain** - Get doctor-style explanation
- **GET /health** - Health check
- **GET /predictions** - Recent predictions
- **GET /docs** - Interactive API documentation

### Example Request

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "age": 65,
    "gender": "Male",
    "bmi": 28.5,
    "smoking_status": "Former",
    "family_history": 1,
    "blood_pressure": 140,
    "cholesterol": 220,
    "glucose": 110,
    "white_blood_cells": 8.0,
    "platelet_count": 280,
    "hemoglobin": 13.5,
    "symptom_count": 3,
    "fatigue_level": 4,
    "pain_level": 3,
    "weight_loss": 1,
    "night_sweats": 0,
    "appetite_loss": 1
  }'
```

## 🧪 Testing

### Test Backend API

```bash
# Test basic functionality
python test_api.py

# Test prediction endpoint
python test_predict_manual.py

# Test doctor explanations
python test_explanation_api.py

# Test Supabase integration
python test_supabase.py
```

### Test Individual Components

```bash
# Test cancer prediction model
python simple_cancer_predictor.py

# Test Supabase connection
python supabase_with_env.py

# Test doctor explanations
python doctor_explanation_fallback.py
```

## 📊 Model Information

The cancer prediction model uses:
- **Algorithm**: Random Forest Classifier
- **Features**: 18 patient characteristics
- **Accuracy**: ~95.5%
- **Cancer Types**: Lung, Breast, Colorectal, Prostate, Pancreatic, Melanoma

### Input Features

- Demographics: Age, Gender, BMI
- Medical History: Smoking status, Family history
- Vital Signs: Blood pressure, Cholesterol, Glucose
- Lab Values: White blood cells, Platelet count, Hemoglobin
- Symptoms: Fatigue level, Pain level, Weight loss, Night sweats, Appetite loss

## 🔧 Configuration

### Environment Variables

**Backend (.env)**
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
OPENAI_API_KEY=your_openai_api_key  # Optional
```

**Frontend (.env.local)**
```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

## 🚨 Important Disclaimers

- **Medical Disclaimer**: This system is for educational purposes only
- **Not a Substitute**: Always consult healthcare professionals for medical advice
- **AI Limitations**: Predictions are based on limited data and should not replace proper medical diagnosis
- **Data Privacy**: Ensure compliance with healthcare data regulations (HIPAA, GDPR)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Tejas Bharsake**
- GitHub: [@Tejasbharsake](https://github.com/Tejasbharsake)

## 🙏 Acknowledgments

- OpenAI for GPT API
- Supabase for database services
- Scikit-learn for machine learning capabilities
- FastAPI and Next.js communities

## 📞 Support

If you have any questions or issues, please:
1. Check the [Issues](https://github.com/Tejasbharsake/cancer-ai-backend/issues) page
2. Create a new issue if needed
3. Contact the maintainer

---

**⚠️ Medical Disclaimer**: This software is for educational and research purposes only. It is not intended to be a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.