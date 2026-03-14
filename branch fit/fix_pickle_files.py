#!/usr/bin/env python3
"""
Attempt to recover corrupted pickle files (model.pkl and scaler.pkl).
This script tries multiple recovery methods to restore your trained models.
"""

import pickle
import os
import shutil

def backup_original_files():
    """Create backups of the original files before attempting fixes."""
    files_to_backup = ['model.pkl', 'scaler.pkl']
    
    for filename in files_to_backup:
        if os.path.exists(filename):
            backup_name = f"{filename}.backup"
            shutil.copy2(filename, backup_name)
            print(f"✓ Created backup: {backup_name}")

def try_fix_pickle_file(filename):
    """Try multiple methods to fix a corrupted pickle file."""
    
    print(f"\nAttempting to fix {filename}...")
    
    if not os.path.exists(filename):
        print(f"✗ File {filename} does not exist")
        return False
    
    # Method 1: Try loading normally first
    try:
        with open(filename, 'rb') as f:
            obj = pickle.load(f)
        print(f"✓ {filename} loads normally - no corruption detected")
        return True
    except Exception as e:
        print(f"✗ Normal loading failed: {e}")
    
    # Method 2: Try reading and cleaning the file
    try:
        print("Attempting to clean file data...")
        with open(filename, 'rb') as f:
            data = f.read()
        
        print(f"Original file size: {len(data)} bytes")
        print(f"First 50 bytes: {data[:50]}")
        
        # Remove any carriage returns that might have been introduced
        original_len = len(data)
        data_cleaned = data.replace(b'\r\n', b'\n').replace(b'\r', b'')
        
        if len(data_cleaned) != original_len:
            print(f"Removed {original_len - len(data_cleaned)} carriage return characters")
            
            # Try to load the cleaned data
            try:
                obj = pickle.loads(data_cleaned)
                
                # Save the fixed file
                fixed_filename = f"{filename}.fixed"
                with open(fixed_filename, 'wb') as f:
                    pickle.dump(obj, f)
                
                print(f"✓ Successfully fixed {filename} -> {fixed_filename}")
                return True
                
            except Exception as e2:
                print(f"✗ Cleaned data still fails: {e2}")
        else:
            print("No carriage returns found to remove")
    
    except Exception as e:
        print(f"✗ Could not read file: {e}")
    
    # Method 3: Try to read with different protocols
    try:
        print("Trying different pickle protocols...")
        with open(filename, 'rb') as f:
            data = f.read()
        
        # Try loading with different protocols
        for protocol in [0, 1, 2, 3, 4, 5]:
            try:
                obj = pickle.loads(data, encoding='latin1')
                print(f"✓ Successfully loaded with encoding='latin1'")
                
                # Save the fixed file
                fixed_filename = f"{filename}.fixed"
                with open(fixed_filename, 'wb') as f:
                    pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
                
                print(f"✓ Saved fixed file: {fixed_filename}")
                return True
                
            except Exception:
                continue
                
    except Exception as e:
        print(f"✗ Protocol attempts failed: {e}")
    
    # Method 4: Check if it's a text file that was accidentally saved as binary
    try:
        print("Checking if file was saved as text...")
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(100)
        
        if 'sklearn' in content or 'pickle' in content:
            print("✗ File appears to be text-encoded - this cannot be automatically fixed")
            print("You'll need to retrain your model")
        
    except Exception:
        pass
    
    print(f"✗ Could not fix {filename}")
    return False

def main():
    """Main recovery process."""
    print("="*60)
    print("Pickle File Recovery Tool")
    print("="*60)
    
    # Create backups first
    backup_original_files()
    
    # Try to fix both files
    files_to_fix = ['model.pkl', 'scaler.pkl']
    results = {}
    
    for filename in files_to_fix:
        results[filename] = try_fix_pickle_file(filename)
    
    print("\n" + "="*60)
    print("RECOVERY RESULTS:")
    print("="*60)
    
    all_fixed = True
    for filename, success in results.items():
        status = "✓ FIXED" if success else "✗ FAILED"
        print(f"{filename}: {status}")
        if not success:
            all_fixed = False
    
    if all_fixed:
        print("\n✓ All files recovered successfully!")
        print("You can now replace the original files with the .fixed versions:")
        for filename in files_to_fix:
            if os.path.exists(f"{filename}.fixed"):
                print(f"  move {filename}.fixed {filename}")
    else:
        print("\n✗ Some files could not be recovered.")
        print("Options:")
        print("1. Check if you have the original model files elsewhere")
        print("2. Retrain your model from scratch")
        print("3. Use Git to restore from a previous commit if available")

if __name__ == "__main__":
    main()