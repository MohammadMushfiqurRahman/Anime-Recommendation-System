import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def clean_text(text):
    """Clean text data by removing special characters and converting to lowercase"""
    if pd.isna(text):
        return ""
    # Convert to string first to handle any non-string types
    text = str(text)
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z0-9\s,]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

def preprocess_anime_data():
    """Preprocess the anime data for recommendation system"""
    # Load the full dataset
    print("Loading dataset...")
    df = pd.read_csv('65k_anime_data.csv', encoding='utf-8', encoding_errors='ignore')
    print(f"Dataset loaded with {len(df)} rows")
    
    # Select relevant columns for recommendation system
    relevant_columns = ['title', 'genres', 'themes', 'demographics', 'rating', 'synopsis']
    df_processed = df[relevant_columns].copy()
    
    # Handle missing values
    df_processed['genres'] = df_processed['genres'].fillna('')
    df_processed['themes'] = df_processed['themes'].fillna('')
    df_processed['demographics'] = df_processed['demographics'].fillna('')
    df_processed['synopsis'] = df_processed['synopsis'].fillna('')
    
    # Clean text data
    text_columns = ['genres', 'themes', 'demographics', 'synopsis']
    for col in text_columns:
        df_processed[col] = df_processed[col].apply(clean_text)
    
    # Create a combined feature for content-based filtering
    df_processed['combined_features'] = (
        df_processed['genres'] + ' ' + 
        df_processed['themes'] + ' ' + 
        df_processed['demographics'] + ' ' + 
        df_processed['synopsis']
    )
    
    # Remove rows with empty combined features
    df_processed = df_processed[df_processed['combined_features'].str.strip() != '']
    
    print(f"Dataset processed with {len(df_processed)} rows after cleaning")
    return df_processed

def create_similarity_matrix(df):
    """Create a cosine similarity matrix based on combined features"""
    print("Creating TF-IDF matrix...")
    tfidf = TfidfVectorizer(stop_words='english', max_features=10000)
    tfidf_matrix = tfidf.fit_transform(df['combined_features'])
    
    print("Calculating cosine similarity matrix...")
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    print("Similarity matrix created")
    return cosine_sim

if __name__ == "__main__":
    # Preprocess the data
    df_processed = preprocess_anime_data()
    
    # Save processed data
    df_processed.to_csv('anime_recommender/processed_anime_data.csv', index=False, encoding='utf-8')
    print("Processed data saved to 'anime_recommender/processed_anime_data.csv'")