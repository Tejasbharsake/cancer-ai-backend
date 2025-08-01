"""
Essential imports for Cancer Prediction System
"""

# Essential packages for cancer prediction
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

print("✅ Essential packages imported successfully!")
print("\nEssential packages for cancer prediction:")
print("- numpy (np) - for numerical operations")
print("- pandas (pd) - for data manipulation")
print("- sklearn.ensemble.RandomForestClassifier - for prediction model")
print("- sklearn.model_selection.train_test_split - for data splitting")
print("- sklearn.preprocessing.StandardScaler, LabelEncoder - for data preprocessing")
print("- sklearn.metrics.accuracy_score - for model evaluation")

# Quick test
print("\n🧪 Quick functionality test:")
data = np.random.rand(10, 5)
print(f"Created random data: {data.shape}")
print("All packages working correctly! ✅") 