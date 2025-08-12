import pandas as pd
import numpy as np

# Load a sample of the data to understand its structure
# Since the file is large, we'll read just the first 1000 rows for initial analysis
df_sample = pd.read_csv('65k_anime_data.csv', nrows=1000)

print("Dataset shape:", df_sample.shape)
print("\nColumn names:")
print(df_sample.columns.tolist())

print("\nData types:")
print(df_sample.dtypes)

print("\nFirst few rows:")
print(df_sample.head())

print("\nMissing values:")
print(df_sample.isnull().sum())

print("\nUnique values in categorical columns:")
categorical_columns = ['status', 'rating', 'genres', 'themes', 'demographics']
for col in categorical_columns:
    if col in df_sample.columns:
        print(f"\n{col}:")
        print(df_sample[col].value_counts().head())