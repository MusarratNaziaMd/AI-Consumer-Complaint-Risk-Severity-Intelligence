import pandas as pd

# Load dataset
df = pd.read_csv('data/complaints.csv')

# Keep essential columns
cols = ['Date received','Product','Issue','Consumer complaint narrative','Company','State']
df = df[cols]

# Drop missing complaints
df = df.dropna(subset=['Consumer complaint narrative'])

# Standardize text
df['Consumer complaint narrative'] = df['Consumer complaint narrative'].str.lower().str.replace(r'[^\w\s]','', regex=True).str.strip()

# Save cleaned data
df.to_csv('data/cleaned_complaints.csv', index=False)
print("Data cleaned and saved.")
