"""
Import all required packages for the Cancer Prediction System
"""

# Core data science packages
import numpy as np
import pandas as pd

# Scikit-learn packages for machine learning
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Model persistence
import joblib

# Visualization packages (optional but useful)
import matplotlib.pyplot as plt
import seaborn as sns

# Warnings management
import warnings
warnings.filterwarnings('ignore')

def test_imports():
    """Test that all packages are imported correctly"""
    print("✅ All packages imported successfully!")
    print("\nImported packages:")
    print("- numpy (np)")
    print("- pandas (pd)")
    print("- sklearn.ensemble.RandomForestClassifier")
    print("- sklearn.model_selection.train_test_split")
    print("- sklearn.preprocessing.StandardScaler, LabelEncoder")
    print("- sklearn.metrics (accuracy_score, classification_report, confusion_matrix)")
    print("- joblib")
    print("- matplotlib.pyplot (plt)")
    print("- seaborn (sns)")
    
    # Test basic functionality
    print("\n🧪 Testing basic functionality...")
    
    # Test numpy
    arr = np.array([1, 2, 3, 4, 5])
    print(f"NumPy array: {arr}")
    
    # Test pandas
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    print(f"Pandas DataFrame:\n{df}")
    
    # Test sklearn
    rf = RandomForestClassifier(n_estimators=10, random_state=42)
    print(f"RandomForestClassifier created: {type(rf)}")
    
    # Test scaler
    scaler = StandardScaler()
    print(f"StandardScaler created: {type(scaler)}")
    
    print("\n🎉 All tests passed! Packages are ready to use.")

if __name__ == "__main__":
    test_imports() 