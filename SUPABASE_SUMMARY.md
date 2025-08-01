# Supabase Integration for Cancer Prediction System

## 📦 Available Supabase Scripts

### **1. Basic Supabase Connection (`simple_supabase_insert.py`)**
- Simple connection and data insertion
- Hardcoded credentials (for testing)
- Basic error handling

### **2. Advanced Supabase Connection (`supabase_connection.py`)**
- Full-featured class-based approach
- Comprehensive error handling
- Additional features like data retrieval
- Support for JSONB data storage

### **3. Environment Variable Connection (`supabase_with_env.py`)**
- Secure credential management
- Environment variable support
- Better for production use

## 🚀 Quick Start Guide

### **Step 1: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 2: Set Up Supabase**
1. Create account at [supabase.com](https://supabase.com)
2. Create new project
3. Get your credentials from Settings → API
4. Create the predictions table using the provided SQL

### **Step 3: Choose Your Connection Method**

#### **Option A: Basic Connection (Testing)**
```python
# Update credentials in simple_supabase_insert.py
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-anon-key-here"

# Run the script
python simple_supabase_insert.py
```

#### **Option B: Environment Variables (Production)**
```bash
# Set environment variables
export SUPABASE_URL="https://your-project-id.supabase.co"
export SUPABASE_KEY="your-anon-key-here"

# Or create a .env file
echo "SUPABASE_URL=https://your-project-id.supabase.co" > .env
echo "SUPABASE_KEY=your-anon-key-here" >> .env

# Run the script
python supabase_with_env.py
```

## 📊 Database Schema

### **Predictions Table**
```sql
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
```

## 🔧 Usage Examples

### **Basic Data Insertion**
```python
from simple_supabase_insert import connect_to_supabase, insert_prediction_data

# Connect
supabase = connect_to_supabase(SUPABASE_URL, SUPABASE_KEY)

# Insert data
insert_prediction_data(
    supabase=supabase,
    name="John Doe",
    age=45,
    gender="Male",
    prediction_result="Lung",
    confidence_score=0.8750
)
```

### **Prediction and Storage**
```python
from simple_supabase_insert import predict_and_insert

# Patient data
patient_data = {
    'age': 68,
    'gender': 'Female',
    'bmi': 26.5,
    'smoking_status': 'Former',
    'family_history': 1,
    # ... other features
}

# Make prediction and store
result = predict_and_insert(supabase, "Jane Doe", patient_data)
```

### **Advanced Usage with Class**
```python
from supabase_connection import SupabaseCancerPredictor

# Initialize
predictor = SupabaseCancerPredictor(SUPABASE_URL, SUPABASE_KEY)

# Test connection
predictor.test_connection()

# Make prediction and store
result = predictor.predict_and_store(
    name="Jane Doe",
    patient_data=patient_data,
    notes="Patient with breast cancer risk factors"
)

# Get recent predictions
recent = predictor.get_all_predictions(limit=10)
```

## 🔒 Security Best Practices

### **1. Environment Variables**
```bash
# Set in your shell
export SUPABASE_URL="your-url"
export SUPABASE_KEY="your-key"

# Or use .env file
SUPABASE_URL=your-url
SUPABASE_KEY=your-key
```

### **2. Row Level Security (RLS)**
```sql
-- Enable RLS
ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Enable insert for authenticated users only" 
ON predictions FOR INSERT 
TO authenticated 
WITH CHECK (true);

CREATE POLICY "Enable read access for all users" 
ON predictions FOR SELECT 
TO authenticated 
USING (true);
```

### **3. API Key Management**
- Never commit API keys to version control
- Use environment variables or secure key management
- Rotate keys regularly
- Use appropriate key permissions

## 📈 Monitoring and Analytics

### **View Data in Supabase Dashboard**
1. Go to Table Editor
2. Select predictions table
3. View all records

### **SQL Queries for Analytics**
```sql
-- Get all predictions
SELECT * FROM predictions ORDER BY created_at DESC;

-- Count by cancer type
SELECT prediction_result, COUNT(*) 
FROM predictions 
GROUP BY prediction_result;

-- Average confidence by type
SELECT prediction_result, AVG(confidence_score) 
FROM predictions 
GROUP BY prediction_result;

-- Recent predictions
SELECT name, prediction_result, confidence_score, created_at
FROM predictions 
ORDER BY created_at DESC 
LIMIT 10;
```

## 🛠️ Troubleshooting

### **Common Issues**

1. **Connection Failed**
   - Check URL and key format
   - Verify project is active
   - Check internet connection

2. **Table Not Found**
   - Ensure table name is correct
   - Check if table exists in dashboard
   - Verify schema permissions

3. **Permission Denied**
   - Check RLS policies
   - Verify API key permissions
   - Ensure proper authentication

### **Error Messages**
- `"relation does not exist"` → Create table
- `"permission denied"` → Check RLS/policies
- `"invalid API key"` → Verify credentials

## 📋 File Structure

```
AI Cancer Prediction Dashboard/
├── simple_supabase_insert.py      # Basic Supabase connection
├── supabase_connection.py         # Advanced class-based connection
├── supabase_with_env.py          # Environment variable connection
├── SUPABASE_SETUP.md             # Detailed setup guide
├── SUPABASE_SUMMARY.md           # This summary file
├── requirements.txt               # Updated with supabase package
└── simple_cancer_predictor.py    # Cancer prediction function
```

## ✅ Status Check

- ✅ Supabase package installed
- ✅ Connection scripts created
- ✅ Database schema defined
- ✅ Security practices documented
- ✅ Error handling implemented
- ✅ Usage examples provided

## 🎯 Next Steps

1. **Set up Supabase project** following the setup guide
2. **Create the predictions table** using the provided SQL
3. **Update credentials** in your chosen script
4. **Test the connection** with a simple prediction
5. **Deploy to production** using environment variables

Your cancer prediction system is now ready to store predictions in Supabase! 🎉 