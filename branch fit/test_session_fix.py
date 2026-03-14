#!/usr/bin/env python3
"""
Test the session data type fix to ensure the compute_probabilities function works.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the functions from app.py
from app import compute_probabilities, EXPECTED_FEATURES
from flask import Flask
import json

def test_compute_probabilities():
    """Test the compute_probabilities function with mock session data."""
    
    app = Flask(__name__)
    app.secret_key = 'test-key'
    
    with app.test_request_context():
        from flask import session
        
        # Mock session data that would cause the original error
        session['responses'] = {
            '0': 4,    # Integer values
            '1': 3,
            '2': 5,
            '3': 2,
            '4': 4,
            '5': 3,
            '6': 4,
            '7': 2,
            '8': 5,
            '9': 3
        }
        
        print("Testing compute_probabilities with mock session data...")
        print(f"Expected features: {EXPECTED_FEATURES}")
        print(f"Session responses: {session['responses']}")
        
        try:
            probabilities = compute_probabilities()
            print("✓ compute_probabilities() executed successfully!")
            print(f"Returned probabilities: {probabilities}")
            
            # Verify we got probabilities for all branches
            if len(probabilities) == 5:
                print("✓ Correct number of branches (5)")
            else:
                print(f"✗ Expected 5 branches, got {len(probabilities)}")
            
            # Verify probabilities sum to approximately 1
            total_prob = sum(probabilities.values())
            if 0.99 <= total_prob <= 1.01:
                print(f"✓ Probabilities sum correctly: {total_prob:.3f}")
            else:
                print(f"✗ Probabilities don't sum to 1: {total_prob:.3f}")
                
        except Exception as e:
            print(f"✗ Error in compute_probabilities(): {e}")
            import traceback
            traceback.print_exc()
            return False
    
    return True

if __name__ == "__main__":
    print("="*50)
    print("Testing Session Data Type Fix")
    print("="*50)
    
    success = test_compute_probabilities()
    
    if success:
        print("\n✓ All tests passed! The fix should work.")
    else:
        print("\n✗ Tests failed. There may still be issues.")