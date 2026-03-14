#!/usr/bin/env python3
"""
Advanced recovery methods for the original trained model files.
"""

import pickle
import os
import shutil
import tempfile

def try_recovery_methods(filename):
    """Try multiple recovery methods for corrupted pickle files."""
    
    print(f"\n{'='*60}")
    print(f"RECOVERING {filename}")
    print(f"{'='*60}")
    
    if not os.path.exists(filename):
        print(f"✗ File {filename} does not exist")
        return False
    
    file_size = os.path.getsize(filename)
    print(f"File size: {file_size:,} bytes")
    
    # Method 1: Check first few bytes
    try:
        with open(filename, 'rb') as f:
            first_bytes = f.read(50)
        print(f"First 50 bytes: {first_bytes}")
        
        # Check if it starts with proper pickle protocol
        if first_bytes.startswith(b'\x80'):
            print("✓ File starts with proper pickle protocol")
        else:
            print("✗ File doesn't start with pickle protocol")
            
    except Exception as e:
        print(f"✗ Can't read file: {e}")
        return False
    
    # Method 2: Try direct loading
    print("\nMethod 1: Direct loading...")
    try:
        with open(filename, 'rb') as f:
            obj = pickle.load(f)
        print("✓ Direct loading successful!")
        return True
    except Exception as e:
        print(f"✗ Direct loading failed: {e}")
    
    # Method 3: Try with different encodings
    print("\nMethod 2: Different encodings...")
    encodings = ['latin1', 'utf-8', 'cp1252']
    for encoding in encodings:
        try:
            with open(filename, 'rb') as f:
                data = f.read()
            obj = pickle.loads(data, encoding=encoding)
            print(f"✓ Success with encoding: {encoding}")
            
            # Save recovered file
            recovered_name = f"{filename}.recovered"
            with open(recovered_name, 'wb') as f:
                pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
            print(f"✓ Saved recovered file: {recovered_name}")
            return True
            
        except Exception as e:
            print(f"✗ Encoding {encoding} failed: {e}")
    
    # Method 4: Try removing carriage returns
    print("\nMethod 3: Removing carriage returns...")
    try:
        with open(filename, 'rb') as f:
            data = f.read()
        
        # Remove various line ending issues
        original_len = len(data)
        data_cleaned = data.replace(b'\r\n', b'\n').replace(b'\r', b'')
        
        if len(data_cleaned) != original_len:
            print(f"Removed {original_len - len(data_cleaned)} carriage return characters")
            
            try:
                obj = pickle.loads(data_cleaned)
                print("✓ Success after removing carriage returns!")
                
                # Save recovered file
                recovered_name = f"{filename}.recovered"
                with open(recovered_name, 'wb') as f:
                    pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
                print(f"✓ Saved recovered file: {recovered_name}")
                return True
                
            except Exception as e:
                print(f"✗ Still failed after cleaning: {e}")
        else:
            print("No carriage returns found")
            
    except Exception as e:
        print(f"✗ Cleaning method failed: {e}")
    
    # Method 5: Try reading in chunks to find corruption point
    print("\nMethod 4: Chunk analysis...")
    try:
        with open(filename, 'rb') as f:
            chunk_size = 1024
            chunk_num = 0
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                
                # Look for suspicious patterns
                if b'\r' in chunk:
                    print(f"Found carriage return in chunk {chunk_num} at position {chunk_num * chunk_size}")
                
                chunk_num += 1
                if chunk_num > 10:  # Don't analyze too much
                    break
                    
    except Exception as e:
        print(f"✗ Chunk analysis failed: {e}")
    
    print(f"\n✗ All recovery methods failed for {filename}")
    return False

def main():
    """Try to recover both model files."""
    
    print("PICKLE FILE RECOVERY TOOL")
    print("Attempting to recover your original trained models...")
    
    # Try to recover model.pkl
    model_recovered = try_recovery_methods("model.pkl")
    
    # Try to recover scaler.pkl
    scaler_recovered = try_recovery_methods("scaler.pkl")
    
    print(f"\n{'='*60}")
    print("RECOVERY SUMMARY")
    print(f"{'='*60}")
    print(f"model.pkl: {'✓ RECOVERED' if model_recovered else '✗ FAILED'}")
    print(f"scaler.pkl: {'✓ RECOVERED' if scaler_recovered else '✗ FAILED'}")
    
    if model_recovered or scaler_recovered:
        print("\nRecovered files have been saved with .recovered extension")
        print("You can replace the original files with these recovered versions")
    else:
        print("\n⚠️  RECOVERY FAILED")
        print("Your model files appear to be severely corrupted.")
        print("Recommendations:")
        print("1. Check if you have the files stored elsewhere (different computer, cloud, etc.)")
        print("2. Try transferring the files again using binary mode")
        print("3. If no other copies exist, you'll need to retrain the model")

if __name__ == "__main__":
    main()