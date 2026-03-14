#!/usr/bin/env python3
"""
Debug the session data type issue by testing the exact scenario.
"""

def test_string_int_comparison():
    """Test the exact comparison that's failing."""
    
    print("Testing string vs int comparison...")
    
    # This is what's happening in the session
    responses = {
        '0': 4,    # Keys are strings
        '1': 3,
        '2': 5
    }
    
    EXPECTED_FEATURES = 40
    
    print(f"Session responses: {responses}")
    print(f"Expected features: {EXPECTED_FEATURES}")
    
    # Test the original problematic code
    print("\n1. Testing original problematic code:")
    try:
        for q_idx, answer in responses.items():
            print(f"  Comparing q_idx='{q_idx}' (type: {type(q_idx)}) < {EXPECTED_FEATURES} (type: {type(EXPECTED_FEATURES)})")
            if q_idx < EXPECTED_FEATURES:  # This will fail
                print(f"    Would set feature[{q_idx}] = {answer}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    # Test the fixed code
    print("\n2. Testing fixed code:")
    try:
        for q_idx_str, answer in responses.items():
            q_idx = int(q_idx_str)  # Convert to int
            print(f"  Comparing q_idx={q_idx} (type: {type(q_idx)}) < {EXPECTED_FEATURES} (type: {type(EXPECTED_FEATURES)})")
            if q_idx < EXPECTED_FEATURES:
                print(f"    ✓ Would set feature[{q_idx}] = {answer}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

if __name__ == "__main__":
    test_string_int_comparison()