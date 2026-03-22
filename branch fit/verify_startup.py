import os
import sys
import pandas as pd
import pickle
import json
from pymongo import MongoClient
from dotenv import load_dotenv

# Set UTF-8 encoding for output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

load_dotenv()

def test_startup():
    print("TEST 1 - App Startup Verification")
    print("-" * 30)
    
    # Check dataset
    try:
        df = pd.read_csv('balanced_dataset_augmented.csv')
        all_questions = list(df.columns[1:])
        print(f"✅ Dataset loaded: {len(df)} rows")
        print(f"✅ Questions loaded: {len(all_questions)}")
    except Exception as e:
        print(f"❌ Dataset error: {e}")

    # Check model and scaler
    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        print(f"✅ Model loaded correctly: {model.__class__.__name__}")
        print(f"✅ Features model expects: {model.n_features_in_}")
        print(f"✅ Features scaler expects: {scaler.n_features_in_}")
    except Exception as e:
        print(f"❌ Model/Scaler error: {e}")

    # Check MongoDB
    try:
        client = MongoClient(os.getenv('MONGO_URI'), serverSelectionTimeoutMS=2000)
        client.server_info()
        print("✅ MongoDB connection successful")
    except Exception as e:
        print(f"❌ MongoDB error: {e}")

if __name__ == "__main__":
    test_startup()
