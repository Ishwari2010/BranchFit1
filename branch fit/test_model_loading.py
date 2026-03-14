#!/usr/bin/env python3
"""
Test loading the actual model and scaler files to diagnose the issue.
"""

import pickle
import warnings

def test_model_loading():
    """Test loading model and scaler with detailed error reporting."""
    
    print("Testing model and scaler loading...")
    
    # Test model.pkl
    print("\n1. Testing model.pkl:")
    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        print(f"✓ Model loaded successfully: {type(model).__name__}")
        if hasattr(model, 'n_features_in_'):
            print(f"  Features expected: {model.n_features_in_}")
        if hasattr(model, 'n_classes_'):
            print(f"  Number of classes: {model.n_classes_}")
        
        # Test a prediction
        import numpy as np
        test_data = np.random.rand(1, model.n_features_in_)
        pred = model.predict_proba(test_data)
        print(f"  Test prediction shape: {pred.shape}")
        
    except Exception as e:
        print(f"✗ Model loading failed: {e}")
        print(f"  Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
    
    # Test scaler.pkl
    print("\n2. Testing scaler.pkl:")
    try:
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        print(f"✓ Scaler loaded successfully: {type(scaler).__name__}")
        if hasattr(scaler, 'n_features_in_'):
            print(f"  Features expected: {scaler.n_features_in_}")
        
        # Test scaling
        import numpy as np
        if hasattr(scaler, 'n_features_in_'):
            test_data = np.random.rand(1, scaler.n_features_in_)
            scaled = scaler.transform(test_data)
            print(f"  Test scaling shape: {scaled.shape}")
        
    except Exception as e:
        print(f"✗ Scaler loading failed: {e}")
        print(f"  Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()

def test_with_warnings():
    """Test with warnings to see sklearn version issues."""
    print("\n3. Testing with sklearn version warnings:")
    
    # Capture warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        try:
            with open('model.pkl', 'rb') as f:
                model = pickle.load(f)
            
            if w:
                print("Warnings detected:")
                for warning in w:
                    print(f"  {warning.category.__name__}: {warning.message}")
            else:
                print("No warnings")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_model_loading()
    test_with_warnings()