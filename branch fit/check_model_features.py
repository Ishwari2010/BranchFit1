import pickle
import numpy as np

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

print(f"Model type: {model.__class__.__name__}")
print(f"Number of features model expects: {model.n_features_in_}")
print(f"Number of features scaler expects: {scaler.n_features_in_}")
if hasattr(model, 'classes_'):
    print(f"Classes: {model.classes_}")
