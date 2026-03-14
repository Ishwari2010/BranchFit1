#!/usr/bin/env python3
"""
Diagnose issues with the adaptive questioning system.
"""

import json
import pickle
import numpy as np
from flask import Flask
import sys
import os

# Add current directory to path to import from app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def analyze_questions_and_model():
    """Analyze the mismatch between questions and model expectations."""
    
    print("="*60)
    print("ADAPTIVE SYSTEM DIAGNOSIS")
    print("="*60)
    
    # Load model
    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        print(f"✓ Model loaded: {model.n_features_in_} features expected")
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        return
    
    # Load questions
    try:
        with open('adaptive_questions.json', 'r') as f:
            questions = json.load(f)
        
        screening_count = len(questions['initial_screening'])
        adaptive_count = len(questions['adaptive_pool'])
        total_questions = screening_count + adaptive_count
        
        print(f"✓ Questions loaded:")
        print(f"  Initial screening: {screening_count}")
        print(f"  Adaptive pool: {adaptive_count}")
        print(f"  Total available: {total_questions}")
        
    except Exception as e:
        print(f"✗ Error loading questions: {e}")
        return
    
    # Check for issues
    print(f"\n🔍 ISSUE ANALYSIS:")
    
    # Issue 1: Feature count mismatch
    if model.n_features_in_ != total_questions:
        print(f"❌ FEATURE MISMATCH:")
        print(f"   Model expects: {model.n_features_in_} features")
        print(f"   Available questions: {total_questions}")
        print(f"   Difference: {abs(model.n_features_in_ - total_questions)}")
    else:
        print(f"✅ Feature count matches: {model.n_features_in_}")
    
    # Issue 2: Check for duplicate questions
    all_questions = questions['initial_screening'] + questions['adaptive_pool']
    unique_questions = list(set(all_questions))
    
    if len(all_questions) != len(unique_questions):
        duplicates = len(all_questions) - len(unique_questions)
        print(f"❌ DUPLICATE QUESTIONS: {duplicates} duplicates found")
    else:
        print(f"✅ No duplicate questions")
    
    # Issue 3: Test model predictions
    print(f"\n🧪 MODEL PREDICTION TEST:")
    
    # Test with different input patterns
    test_cases = [
        ("All neutral (3)", [3] * model.n_features_in_),
        ("All positive (5)", [5] * model.n_features_in_),
        ("All negative (1)", [1] * model.n_features_in_),
        ("Mixed pattern", [1,2,3,4,5] * (model.n_features_in_ // 5 + 1))[:model.n_features_in_]
    ]
    
    for name, pattern in test_cases:
        test_input = np.array(pattern).reshape(1, -1)
        
        # Scale the input (assuming we have scaler)
        try:
            with open('scaler.pkl', 'rb') as f:
                scaler = pickle.load(f)
            scaled_input = scaler.transform(test_input)
        except:
            scaled_input = test_input
        
        probabilities = model.predict_proba(scaled_input)[0]
        prediction = model.predict(scaled_input)[0]
        
        print(f"  {name}:")
        print(f"    Prediction: {prediction}")
        print(f"    Probabilities: {probabilities}")
        print(f"    Max prob: {max(probabilities):.3f}, Min prob: {min(probabilities):.3f}")
        print(f"    Std dev: {np.std(probabilities):.3f}")

def test_adaptive_logic():
    """Test the adaptive questioning logic."""
    
    print(f"\n🔄 ADAPTIVE LOGIC TEST:")
    
    app = Flask(__name__)
    app.secret_key = 'test'
    
    with app.test_request_context():
        from flask import session
        
        # Import functions from app
        from app import (
            initialize_session, 
            get_next_question_index, 
            compute_probabilities,
            eliminate_low_probability_branches,
            INTERMEDIATE_CHECKPOINT
        )
        
        # Test session initialization
        initialize_session()
        print(f"✅ Session initialized")
        
        # Simulate answering screening questions
        print(f"📝 Simulating {INTERMEDIATE_CHECKPOINT} screening questions...")
        
        for i in range(INTERMEDIATE_CHECKPOINT):
            # Get next question
            q_idx = get_next_question_index()
            if q_idx is None:
                print(f"❌ No question returned at step {i}")
                break
            
            # Add to sequence
            session['question_sequence'] = session.get('question_sequence', []) + [q_idx]
            
            # Add mock response
            responses = session.get('responses', {})
            responses[q_idx] = 3 + (i % 3)  # Vary responses: 3, 4, 5, 3, 4, 5...
            session['responses'] = responses
            
            session['current_question'] = i + 1
            
            print(f"  Q{i+1}: Index {q_idx}, Response {responses[q_idx]}")
        
        # Test probability computation
        try:
            probabilities = compute_probabilities()
            print(f"✅ Probabilities computed: {probabilities}")
        except Exception as e:
            print(f"❌ Error computing probabilities: {e}")
            return
        
        # Test elimination
        try:
            eliminate_low_probability_branches()
            eliminated = session.get('eliminated_branches', [])
            print(f"✅ Branches eliminated: {eliminated}")
        except Exception as e:
            print(f"❌ Error in elimination: {e}")

def suggest_fixes():
    """Suggest fixes for identified issues."""
    
    print(f"\n🔧 SUGGESTED FIXES:")
    print(f"1. MODEL ACCURACY:")
    print(f"   - Current accuracy (61.4%) is low")
    print(f"   - Try increasing n_estimators to 200-500")
    print(f"   - Add feature engineering or selection")
    print(f"   - Check data quality and balance")
    
    print(f"\n2. FEATURE MISMATCH:")
    print(f"   - Ensure question count matches model features")
    print(f"   - Either add more questions or retrain with fewer features")
    
    print(f"\n3. QUESTION REPETITION:")
    print(f"   - Check question selection logic")
    print(f"   - Ensure proper tracking of asked questions")
    
    print(f"\n4. ADAPTIVE THRESHOLD:")
    print(f"   - Current elimination threshold: 15%")
    print(f"   - Try lowering to 10% for more aggressive elimination")
    print(f"   - Or increase to 20% for more conservative elimination")

if __name__ == "__main__":
    analyze_questions_and_model()
    test_adaptive_logic()
    suggest_fixes()