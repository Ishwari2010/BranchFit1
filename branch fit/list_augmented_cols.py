import pandas as pd
df = pd.read_csv('balanced_dataset_augmented.csv', nrows=0)
print(f"Total columns: {len(df.columns)}")
for i, col in enumerate(df.columns):
    print(f"{i}: {col}")
