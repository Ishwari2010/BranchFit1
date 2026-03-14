#!/usr/bin/env python3
"""
Fix the duplicate questions issue and create a proper 40-question pool.
"""

import json
import pandas as pd

def fix_questions():
    """Create a proper question pool without duplicates."""
    
    print("Fixing question duplicates...")
    
    # Load the original dataset to get all 40 unique questions
    df = pd.read_csv('balanced_branch_dataset.csv')
    
    # Get the first 40 question columns (excluding the target)
    all_questions = list(df.columns[:-1][:40])
    
    print(f"Found {len(all_questions)} unique questions from dataset")
    
    # Create new question structure
    # First 10 for screening, remaining 30 for adaptive pool
    new_questions = {
        "initial_screening": all_questions[:10],
        "adaptive_pool": all_questions[10:40]
    }
    
    print(f"Initial screening: {len(new_questions['initial_screening'])} questions")
    print(f"Adaptive pool: {len(new_questions['adaptive_pool'])} questions")
    
    # Check for duplicates
    all_combined = new_questions['initial_screening'] + new_questions['adaptive_pool']
    unique_combined = list(set(all_combined))
    
    if len(all_combined) == len(unique_combined):
        print("✓ No duplicates found")
    else:
        print(f"❌ Still {len(all_combined) - len(unique_combined)} duplicates")
    
    # Save the fixed questions
    with open('adaptive_questions.json', 'w', encoding='utf-8') as f:
        json.dump(new_questions, f, indent=4, ensure_ascii=False)
    
    print("✓ Fixed questions saved to adaptive_questions.json")
    
    # Display first few questions from each section
    print("\nFirst 3 screening questions:")
    for i, q in enumerate(new_questions['initial_screening'][:3]):
        print(f"  {i+1}. {q[:60]}...")
    
    print("\nFirst 3 adaptive questions:")
    for i, q in enumerate(new_questions['adaptive_pool'][:3]):
        print(f"  {i+1}. {q[:60]}...")

if __name__ == "__main__":
    fix_questions()