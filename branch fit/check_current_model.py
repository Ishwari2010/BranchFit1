#!/usr/bin/env python3
"""
Check which model is currently being used - dummy or original trained model.
"""

import pickle
import numpy as np
from datetime import datetime
import os

def analyze_model_file(filename):
    """Analyze a model file to determine if it's dummy or real."""
    
    print(f"\nAnalyzing {filename}:")
    
    if not os.path.exists(filename):
        print(f"  ✗ File does not exist")
        return
    
    # Check file modification time
    mod_time = os.path.getmtime(filename)
    mod_date = datetime.fromtimestamp(mod_time)
    print(f"  Last modified: {mod_date}")
    
    try:
        with open(filename, 'rb') as f:
            model = pickle.load(f)
        
        print(f"  Model type: {type(model).__name__}")
        
        if hasattr(model, 'n_estimators'):
            print(f"  Number of estimators: {model.n_estimators}")
        
        if hasattr(model, 'random_state'):
            print(f"  Random state: {model.random_state}")
        
        if hasattr(model, 'n_features_in_'):
            print(f"  Features: {model.n_features_in_}")
        
        if hasattr(model, 'n_classes_'):
            print(f"  Classes: {model.n_classes_}")
        
        # Test prediction to see behavior
        if hasattr(model, 'n_features_in_'):
            test_data = np.random.rand(1, model.n_features_in_)
            probabilities = model.predict_proba(test_data)[0]
            print(f"  Sample prediction: {probabilities}")
            
            # Check if it looks like a dummy model (very uniform or simple patterns)
            prob_std = np.std(probabilities)
            print(f"  Prediction std dev: {prob_std:.4f}")
            
            if prob_std < 0.1:
                print("  ⚠️  LOW VARIANCE - This might be a dummy model!")
            else:
                print("  ✓ Good variance - Likely a real trained model")
        
    except Exception as e:
        print(f"  ✗ Error loading: {e}")

def compare_models():
    """Compare current model with backup to see which is which."""
    
    print("="*60)
    print("MODEL ANALYSIS")
    print("="*60)
    
    # Analyze current model
    analyze_model_file("model.pkl")
    
    # Analyze backup model
    analyze_model_file("model.pkl.backup")
    
    # Check file sizes
    print(f"\nFile sizes:")
    if os.path.exists("model.pkl"):
        size_current = os.path.getsize("model.pkl")
        print(f"  model.pkl: {size_current:,} bytes")
    
    if os.path.exists("model.pkl.backup"):
        size_backup = os.path.getsize("model.pkl.backup")
        print(f"  model.pkl.backup: {size_backup:,} bytes")
        
        if os.path.exists("model.pkl"):
            if abs(size_current - size_backup) > 1000:
                print("  ⚠️  Significant size difference - files are different!")
            else:
                print("  ✓ Similar sizes")

if __name__ == "__main__":
    compare_models()