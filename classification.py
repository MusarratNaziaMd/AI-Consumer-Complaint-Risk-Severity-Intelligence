import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import os

# -------------------------
# Configuration
# -------------------------
INPUT_FILE = 'data/processed_complaints.csv'  # output from sentiment/severity step
OUTPUT_DIR = 'data/classification_chunks'
CHUNK_SIZE = 50000  # number of rows per chunk
MAX_FEATURES = 3000  # TF-IDF max features

# Make sure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load full dataset
print("Loading dataset...")
df = pd.read_csv(INPUT_FILE)
print(f"Total rows: {len(df)}")

# Drop rows with empty complaint text or missing labels
df = df.dropna(subset=['Consumer complaint narrative', 'Product'])

# -------------------------
# Split dataset into manageable chunks
# -------------------------
num_chunks = (len(df) // CHUNK_SIZE) + 1
print(f"Processing in {num_chunks} chunks of up to {CHUNK_SIZE} rows each...")

for i in range(num_chunks):
    start_idx = i * CHUNK_SIZE
    end_idx = min((i + 1) * CHUNK_SIZE, len(df))
    chunk = df.iloc[start_idx:end_idx].copy()
    print(f"\nProcessing chunk {i+1}/{num_chunks} | Rows: {len(chunk)}")

    # -------------------------
    # Prepare text & labels
    # -------------------------
    X = chunk['Consumer complaint narrative'].astype(str)
    y = chunk['Product'].astype(str)

    # Split into train/test (optional, for evaluation)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # -------------------------
    # Vectorization
    # -------------------------
    print("Vectorizing text with TF-IDF...")
    vectorizer = TfidfVectorizer(max_features=MAX_FEATURES)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    print("Vectorization done!")

    # -------------------------
    # Train classifier
    # -------------------------
    print("Training Logistic Regression model...")
    clf = LogisticRegression(max_iter=500)
    clf.fit(X_train_vec, y_train)
    print("Model training complete!")

    # -------------------------
    # Predict and evaluate
    # -------------------------
    y_pred = clf.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    print(f"Chunk {i+1} accuracy: {acc:.4f}")

    # Optional: detailed report
    # print(classification_report(y_test, y_pred))

    # -------------------------
    # Apply model to full chunk and save
    # -------------------------
    print("Classifying full chunk...")
    chunk_vec = vectorizer.transform(chunk['Consumer complaint narrative'].astype(str))
    chunk['Predicted_Product'] = clf.predict(chunk_vec)

    # Save chunk results
    output_file = os.path.join(OUTPUT_DIR, f'classified_chunk_{i+1}.csv')
    chunk.to_csv(output_file, index=False)
    print(f"Chunk {i+1} saved to {output_file}")

print("\nAll chunks processed successfully!")
