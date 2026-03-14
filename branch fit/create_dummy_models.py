#!/usr/bin/env python3
"""
Create dummy model and scaler files for testing the Flask app.
This will allow the app to run even if the original pickle files are corrupted.
"""

import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

def create_dummy_models():
    """Create dummy model and scaler files that match the expected interface."""
    
    print("Creating dummy model and scaler files...")
    
    # Create a dummy Random Forest model
    # Based on the app code, it expects 40 features and 5 classes (branches)
    n_features = 40
    n_classes = 5
    
    # Create dummy training data
    X_dummy = np.random.rand(100, n_features)
    y_dummy = np.random.randint(0, n_classes, 100)
    
    # Train a simple model
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X_dummy, y_dummy)
    
    # Create and fit a scaler
    scaler = StandardScaler()
    scaler.fit(X_dummy)
    
    # Save the model
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print(f"✓ Created model.pkl with {n_features} features, {n_classes} classes")
    
    # Save the scaler
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    print(f"✓ Created scaler.pkl with {n_features} features")
    
    # Test loading
    try:
        with open('model.pkl', 'rb') as f:
            test_model = pickle.load(f)
        with open('scaler.pkl', 'rb') as f:
            test_scaler = pickle.load(f)
        print("✓ Successfully tested loading both files")
        
        # Test prediction
        test_features = np.random.rand(1, n_features)
        scaled_features = test_scaler.transform(test_features)
        probabilities = test_model.predict_proba(scaled_features)
        print(f"✓ Test prediction successful: {probabilities.shape}")
        
    except Exception as e:
        print(f"✗ Error testing files: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = create_dummy_models()
    if success:
        print("\n" + "="*50)
        print("SUCCESS: Dummy model files created!")
        print("You can now run 'py app.py' to test the Flask app")
        print("="*50)
    else:
        print("\n" + "="*50)
        print("FAILED: Could not create dummy model files")
        print("="*50)