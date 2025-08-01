# Supabase Setup Guide for Cancer Prediction System

## 📋 Prerequisites

1. **Supabase Account**: Sign up at [supabase.com](https://supabase.com)
2. **Python Environment**: Make sure you have Python 3.7+ installed
3. **Required Packages**: Install the updated requirements

## 🚀 Step-by-Step Setup

### 1. Install Required Packages

```bash
pip install -r requirements.txt
```

### 2. Create Supabase Project

1. Go to [supabase.com](https://supabase.com) and sign in
2. Click "New Project"
3. Choose your organization
4. Enter project details:
   - **Name**: `cancer-prediction-system`
   - **Database Password**: Choose a strong password
   - **Region**: Select closest to you
5. Click "Create new project"
6. Wait for project to be ready (2-3 minutes)

### 3. Get Your Credentials

1. In your Supabase dashboard, go to **Settings** → **API**
2. Copy the following:
   - **Project URL** (starts with `https://`)
   - **anon public** key (starts with `eyJ`)

### 4. Create the Predictions Table

1. Go to **Table Editor** in your Supabase dashboard
2. Click **New Table**
3. Use this SQL to create the table:

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

4. Click **Save** to create the table

### 5. Configure Row Level Security (Optional)

For production use, you might want to enable RLS:

```sql
-- Enable RLS
ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;

-- Create policy for inserting data
CREATE POLICY "Enable insert for authenticated users only" 
ON predictions FOR INSERT 
TO authenticated 
WITH CHECK (true);

-- Create policy for viewing data
CREATE POLICY "Enable read access for all users" 
ON predictions FOR SELECT 
TO authenticated 
USING (true);
```

### 6. Update Your Code

Replace the placeholder credentials in your Python files:

```python
# In simple_supabase_insert.py or supabase_connection.py
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-anon-key-here"
```

## 🧪 Testing the Connection

### Test Basic Connection

```bash
python simple_supabase_insert.py
```

### Test Advanced Features

```bash
python supabase_connection.py
```

## 📊 Database Schema

### Predictions Table Structure

| Column | Type | Description |
|--------|------|-------------|
| `id` | SERIAL PRIMARY KEY | Auto-incrementing unique identifier |
| `name` | VARCHAR(255) | Patient name |
| `age` | INTEGER | Patient age |
| `gender` | VARCHAR(10) | Patient gender ('Male' or 'Female') |
| `prediction_result` | VARCHAR(50) | Predicted cancer type |
| `confidence_score` | DECIMAL(5,4) | Confidence score (0.0000 to 1.0000) |
| `created_at` | TIMESTAMP | When the prediction was made |
| `patient_data` | JSONB | Full patient data (optional) |
| `additional_notes` | TEXT | Additional notes (optional) |

## 🔧 Usage Examples

### Basic Insertion

```python
from simple_supabase_insert import connect_to_supabase, insert_prediction_data

# Connect to Supabase
supabase = connect_to_supabase(SUPABASE_URL, SUPABASE_KEY)

# Insert prediction data
insert_prediction_data(
    supabase=supabase,
    name="John Doe",
    age=45,
    gender="Male",
    prediction_result="Lung",
    confidence_score=0.8750
)
```

### Prediction and Insertion

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

# Make prediction and insert
result = predict_and_insert(supabase, "Jane Doe", patient_data)
```

## 🛠️ Troubleshooting

### Common Issues

1. **Connection Failed**
   - Check your Supabase URL and key
   - Ensure your project is active
   - Verify internet connection

2. **Table Not Found**
   - Make sure you created the `predictions` table
   - Check table name spelling
   - Verify you're in the correct schema

3. **Permission Denied**
   - Check Row Level Security settings
   - Verify your API key has correct permissions
   - Ensure table policies are configured correctly

### Error Messages

- `"relation "predictions" does not exist"` → Create the table
- `"permission denied"` → Check RLS policies
- `"invalid API key"` → Verify your credentials

## 📈 Monitoring

### View Data in Supabase Dashboard

1. Go to **Table Editor**
2. Select the `predictions` table
3. View all inserted records

### Query Data

```sql
-- Get all predictions
SELECT * FROM predictions ORDER BY created_at DESC;

-- Get predictions by cancer type
SELECT prediction_result, COUNT(*) 
FROM predictions 
GROUP BY prediction_result;

-- Get average confidence by cancer type
SELECT prediction_result, AVG(confidence_score) 
FROM predictions 
GROUP BY prediction_result;
```

## 🔒 Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Environment Variables**: Use `.env` files for credentials
3. **RLS Policies**: Configure appropriate access controls
4. **Data Validation**: Validate input data before insertion

## 📝 Environment Variables (Recommended)

Create a `.env` file:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-here
```

Then update your code to use environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
```

Don't forget to add `python-dotenv` to your requirements:

```
python-dotenv>=0.19.0
``` 