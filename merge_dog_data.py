import pandas as pd

# Load both datasets
traits_df = pd.read_csv('dog_breeds_traits.csv')
popularity_df = pd.read_csv('akc_popularity.csv')

# Standardize column names for merging
traits_df['Breed'] = traits_df['Breed'].str.strip().str.lower()
popularity_df['Breed'] = popularity_df['Breed'].str.strip().str.lower()

# Merge datasets on the 'Breed' column
merged_df = pd.merge(traits_df, popularity_df, on='Breed', how='inner')

# Save merged dataset
merged_df.to_csv('merged_dog_data.csv', index=False)

print("✅ Merged dataset saved as 'merged_dog_data.csv'")
