import pandas as pd
import numpy as np

df = pd.read_csv('balanced_dataset_full__1_.csv')
answer_map = {
    "Strongly disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly agree": 5
}
feature_cols = df.columns[1:]
df_numeric = df.copy()
for col in feature_cols:
    df_numeric[col] = df_numeric[col].map(answer_map)

# Group by branch and calculate mean
means = df_numeric.groupby(df.columns[0]).mean()

# Show average score for "it_cse" blocks (first 14) for each branch
print("Average scores for first 14 features (IT/CSE block) per branch:")
for branch in means.index:
    avg = means.loc[branch, feature_cols[:14]].mean()
    print(f"  {branch}: {avg:.2f}")

# Show average score for "Electrical" blocks (cols 39-52) for each branch
print("\nAverage scores for features 39-52 (Electrical block) per branch:")
for branch in means.index:
    avg = means.loc[branch, feature_cols[38:52]].mean()
    print(f"  {branch}: {avg:.2f}")

# Show average score for "EXTC" blocks (cols 53-60) for each branch
print("\nAverage scores for features 53-60 (EXTC block) per branch:")
for branch in means.index:
    avg = means.loc[branch, feature_cols[52:60]].mean()
    print(f"  {branch}: {avg:.2f}")

# Show average score for "Computer Engineering" blocks (cols 
# 15-25) for each branch
print("\nAverage scores for features 15-25 (CompEng block) per branch:")
for branch in means.index:
    avg = means.loc[branch, feature_cols[14:25]].mean()
    print(f"  {branch}: {avg:.2f}")

# Show average score for "Mechanical" blocks (cols 26-38) for each branch
print("\nAverage scores for features 26-38 (Mechanical block) per branch:")
for branch in means.index:
    avg = means.loc[branch, feature_cols[25:38]].mean()
    print(f"  {branch}: {avg:.2f}")

# Check class distribution
print("\nClass distribution:")
print(df[df.columns[0]].value_counts())
