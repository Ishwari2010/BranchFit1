import pandas as pd
import json

# Setup keywords exactly as in app.py
keywords = {
    'computer_eng': ['hardware', 'circuits', 'electronic', 'digital', 'components'],
    'extc': ['signals', 'communication', 'transmission', 'frequency', 'networks'],
    'electrical': ['electrical', 'voltage', 'current', 'power', 'electricity'],
    'it_cse': ['software', 'code', 'database', 'programming', 'apps'],
    'mechanical': ['mechanical', 'machines', 'motion', 'forces', 'materials']
}

df = pd.read_csv('balanced_dataset_augmented.csv')
all_questions = list(df.columns[1:])

category_map = {
    'computer_eng': [],
    'extc': [],
    'electrical': [],
    'it_cse': [],
    'mechanical': []
}

for i, question in enumerate(all_questions):
    question_lower = question.lower()
    for category, category_keywords in keywords.items():
        if any(keyword in question_lower for keyword in category_keywords):
            category_map[category].append(i)

with open('mapping.json', 'w') as f:
    json.dump(category_map, f, indent=2)

print("Mapping saved to mapping.json")
