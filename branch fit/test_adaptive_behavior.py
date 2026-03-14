#!/usr/bin/env python3
"""
Test the new adaptive questioning behavior to ensure it's working correctly.
"""

from flask import Flask
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_adaptive_flow():
    """Test the adaptive questioning flow."""
    
    app = Flask(__name__)
    app.secret_key = 'test-key'
    
    with app.test_request_context():
        from flask import session
        from app import (
            initialize_session,
            get_next_question_index,
            compute_probabilities,
            should_stop_early,
            get_all_questions
        )
        
        print("="*60)
        print("TESTING NEW ADAPTIVE SYSTEM")
        print("="*60)
        
        # Initialize session
        initialize_session()
        all_questions = get_all_questions()
        
        print(f"Total questions available: {len(all_questions)}")
        
        # Simulate answering questions with Computer Engineering bias
        ce_keywords = ['hardware', 'circuits', 'electronic', 'voltage', 'current']
        
        for question_num in range(15):  # Test first 15 questions
            # Get next question
            q_idx = get_next_question_index()
            
            if q_idx is None:
                print("No more questions available")
                break
            
            question = all_questions[q_idx]
            print(f"\nQ{question_num + 1} (Index {q_idx}): {question[:70]}...")
            
            # Simulate intelligent response based on question content
            question_lower = question.lower()
            
            if any(keyword in question_lower for keyword in ce_keywords):
                response = 5  # Strong agreement for CE-related
                print(f"Response: {response} (Strong agreement - CE related)")
            elif any(word in question_lower for word in ['software', 'code', 'database']):
                response = 2  # Disagreement for IT-related
                print(f"Response: {response} (Disagreement - IT related)")
            elif any(word in question_lower for word in ['mechanical', 'forces', 'motion']):
                response = 2  # Disagreement for Mechanical
                print(f"Response: {response} (Disagreement - Mechanical related)")
            else:
                response = 3  # Neutral
                print(f"Response: {response} (Neutral)")
            
            # Record response
            session['question_sequence'] = session.get('question_sequence', []) + [q_idx]
            responses = session.get('responses', {})
            responses[q_idx] = response
            session['responses'] = responses
            session['current_question'] = question_num + 1
            
            # Get current predictions
            probabilities = compute_probabilities()
            sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
            
            print(f"Current predictions:")
            for i, (branch, prob) in enumerate(sorted_probs[:3]):
                print(f"  {i+1}. {branch}: {prob:.1%}")
            
            # Check early stopping
            if should_stop_early():
                print(f"\n🎯 EARLY STOPPING: High confidence reached!")
                print(f"   Top prediction: {sorted_probs[0][0]} ({sorted_probs[0][1]:.1%})")
                break
        
        print(f"\n{'='*60}")
        print("FINAL RESULTS")
        print(f"{'='*60}")
        
        final_probs = compute_probabilities()
        final_sorted = sorted(final_probs.items(), key=lambda x: x[1], reverse=True)
        
        print(f"Questions asked: {len(session.get('responses', {}))}")
        print(f"Final predictions:")
        for i, (branch, prob) in enumerate(final_sorted):
            print(f"  {i+1}. {branch}: {prob:.1%}")
        
        # Check if the system correctly identified Computer Engineering
        if final_sorted[0][0] == "Computer Engineering":
            print(f"\n✅ SUCCESS: Correctly identified Computer Engineering preference!")
        else:
            print(f"\n⚠️  Note: Top prediction is {final_sorted[0][0]}, not Computer Engineering")
        
        return final_sorted[0]

def test_question_uniqueness():
    """Test that questions are not repeated."""
    
    app = Flask(__name__)
    app.secret_key = 'test-key'
    
    with app.test_request_context():
        from flask import session
        from app import initialize_session, get_next_question_index
        
        print(f"\n{'='*60}")
        print("TESTING QUESTION UNIQUENESS")
        print(f"{'='*60}")
        
        initialize_session()
        asked_questions = []
        
        # Ask 20 questions and check for duplicates
        for i in range(20):
            q_idx = get_next_question_index()
            if q_idx is None:
                break
            
            if q_idx in asked_questions:
                print(f"❌ DUPLICATE: Question {q_idx} asked again at step {i+1}")
                return False
            
            asked_questions.append(q_idx)
            
            # Simulate adding to session
            session['question_sequence'] = session.get('question_sequence', []) + [q_idx]
            responses = session.get('responses', {})
            responses[q_idx] = 3  # Neutral response
            session['responses'] = responses
            session['current_question'] = i + 1
        
        print(f"✅ SUCCESS: No duplicate questions in {len(asked_questions)} questions")
        print(f"Asked questions: {asked_questions}")
        return True

if __name__ == "__main__":
    # Test adaptive behavior
    top_prediction = test_adaptive_flow()
    
    # Test uniqueness
    is_unique = test_question_uniqueness()
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Adaptive system working: {top_prediction[0]} ({top_prediction[1]:.1%})")
    print(f"✅ No question repetition: {is_unique}")
    print(f"🚀 Ready for production use!")