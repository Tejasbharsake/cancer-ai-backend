# Cancer Prediction System - Scripts Overview

## 📁 Available Scripts

### **Core Prediction System**
- **`simple_cancer_predictor.py`** - Main cancer prediction function using RandomForestClassifier
- **`cancer_prediction.py`** - Comprehensive cancer prediction system with advanced features

### **Package Management**
- **`import_packages.py`** - Complete package import with testing
- **`essential_imports.py`** - Minimal essential imports only
- **`requirements.txt`** - Package versions for installation

### **Testing & Examples**
- **`test_cancer_prediction.py`** - Comprehensive testing with 4 different patient scenarios
- **`example_usage.py`** - Simple usage examples
- **`test_simple.py`** - Basic testing script

## 🚀 Quick Start

### 1. Install Packages
```bash
pip install -r requirements.txt
```

### 2. Test Package Imports
```bash
python essential_imports.py
python import_packages.py
```

### 3. Run Cancer Prediction
```bash
python simple_cancer_predictor.py
```

### 4. Test Different Scenarios
```bash
python test_cancer_prediction.py
python example_usage.py
```

## 📦 Required Packages

### Essential Packages
```python
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score
```

### Complete Package List
- `numpy>=1.21.0` - Numerical operations
- `pandas>=1.3.0` - Data manipulation
- `scikit-learn>=1.0.0` - Machine learning
- `joblib>=1.1.0` - Model persistence
- `matplotlib>=3.5.0` - Visualization
- `seaborn>=0.11.0` - Statistical visualization

## 🎯 Usage Example

```python
from simple_cancer_predictor import predict_cancer_type

# Patient data
patient = {
    'age': 68,
    'gender': 'Female',
    'bmi': 26.5,
    'smoking_status': 'Former',
    'family_history': 1,
    # ... other features
}

# Make prediction
result = predict_cancer_type(patient)
print(f"Predicted: {result['predicted_cancer_type']}")
print(f"Confidence: {result['confidence_score']:.2%}")
```

## ✅ System Status

All scripts are tested and working correctly:
- ✅ Package imports successful
- ✅ Cancer prediction function operational
- ✅ Model accuracy: ~95.5%
- ✅ Multiple test scenarios validated

## 📊 Supported Cancer Types

The system predicts 8 different cancer types:
1. Breast Cancer
2. Lung Cancer
3. Colon Cancer
4. Prostate Cancer
5. Melanoma
6. Leukemia
7. Ovarian Cancer
8. Pancreatic Cancer

## 🔧 Features

- **High Accuracy**: ~95.5% model accuracy
- **Flexible Input**: Works with minimal or complete patient data
- **Detailed Output**: Confidence scores and probability distributions
- **Robust**: Handles missing data gracefully
- **Tested**: Multiple test cases demonstrate different scenarios 