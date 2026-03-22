import pickle
import numpy as np
import os

model_path = 'model.pkl'
scaler_path = 'scaler.pkl'

if not os.path.exists(model_path) or not os.path.exists(scaler_path):
    print(f"Error: model.pkl or scaler.pkl not found in {os.getcwd()}")
    exit(1)

with open(model_path, 'rb') as f:
    model = pickle.load(f)
with open(scaler_path, 'rb') as f:
    scaler = pickle.load(f)

print("Model type:", model.__class__.__name__)
print("Number of features:", model.n_features_in_)
print("Classes:", model.classes_)
if hasattr(model, 'n_estimators'):
    print("Number of estimators:", model.n_estimators)

# Test with all neutral responses
neutral = np.array([3.0] * model.n_features_in_)
scaled = scaler.transform(neutral.reshape(1, -1))
probs = model.predict_proba(scaled)[0]
print("\nAll neutral responses probabilities:")
for cls, prob in zip(model.classes_, probs):
    print(f"  {cls}: {prob*100:.1f}%")

# Test with strong IT/CSE signals
# The user mentioned first 14 features are IT/CSE questions
it_cse = np.array([3.0] * model.n_features_in_)
# Set first 14 features high (IT/CSE questions)
it_cse[:14] = 5.0
scaled_it = scaler.transform(it_cse.reshape(1, -1))
probs_it = model.predict_proba(scaled_it)[0]
print("\nStrong IT/CSE signals probabilities:")
for cls, prob in zip(model.classes_, probs_it):
    print(f"  {cls}: {prob*100:.1f}%")
