import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

class AnimeRecommender:
    def __init__(self, data_path='anime_recommender/processed_anime_data.csv'):
        """Initialize the recommender system with processed data"""
        print("Loading processed data...")
        self.df = pd.read_csv(data_path)
        print(f"Loaded {len(self.df)} anime entries")
        
        # Create indices for fast lookup
        self.indices = pd.Series(self.df.index, index=self.df['title']).drop_duplicates()
        
        # Create the similarity matrix
        print("Creating similarity matrix...")
        self.cosine_sim = self._create_similarity_matrix()
        print("Recommender system initialized!")
    
    def _create_similarity_matrix(self):
        """Create a cosine similarity matrix based on combined features"""
        tfidf = TfidfVectorizer(stop_words='english', max_features=10000)
        tfidf_matrix = tfidf.fit_transform(self.df['combined_features'])
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        return cosine_sim
    
    def get_recommendations(self, title, num_recommendations=10):
        """Get anime recommendations based on title"""
        # Check if the anime exists in our dataset
        if title not in self.indices:
            # Try to find similar titles
            similar_titles = [t for t in self.indices.index if title.lower() in t.lower()]
            if similar_titles:
                print(f"Exact title '{title}' not found. Did you mean one of these?")
                for i, t in enumerate(similar_titles[:5]):
                    print(f"{i+1}. {t}")
                return pd.DataFrame()
            else:
                print(f"Anime '{title}' not found in the dataset.")
                return pd.DataFrame()
        
        # Get the index of the anime that matches the title
        idx = self.indices[title]
        
        # Get the pairwise similarity scores of all anime with that anime
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        
        # Sort the anime based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get the scores of the most similar anime (excluding the anime itself)
        sim_scores = sim_scores[1:num_recommendations+1]
        
        # Get the anime indices
        anime_indices = [i[0] for i in sim_scores]
        
        # Return the top most similar anime
        recommendations = self.df[['title', 'genres', 'themes', 'demographics']].iloc[anime_indices].copy()
        recommendations['similarity_score'] = [i[1] for i in sim_scores]
        
        return recommendations.reset_index(drop=True)
    
    def get_recommendations_by_features(self, genres=None, themes=None, demographics=None, num_recommendations=10):
        """Get anime recommendations based on specific features"""
        # Create a filter string based on provided features
        filter_string = ""
        if genres:
            filter_string += " ".join(genres) + " "
        if themes:
            filter_string += " ".join(themes) + " "
        if demographics:
            filter_string += " ".join(demographics) + " "
        
        if not filter_string.strip():
            print("Please provide at least one feature (genres, themes, or demographics)")
            return pd.DataFrame()
        
        # Create a temporary TF-IDF vector for the filter string
        tfidf = TfidfVectorizer(stop_words='english', max_features=10000)
        tfidf_matrix = tfidf.fit_transform(self.df['combined_features'])
        
        # Transform the filter string
        filter_vector = tfidf.transform([filter_string])
        
        # Calculate similarity scores
        sim_scores = cosine_similarity(filter_vector, tfidf_matrix).flatten()
        
        # Get indices of top recommendations
        top_indices = sim_scores.argsort()[::-1][:num_recommendations]
        
        # Return recommendations
        recommendations = self.df[['title', 'genres', 'themes', 'demographics']].iloc[top_indices].copy()
        recommendations['similarity_score'] = sim_scores[top_indices]
        
        return recommendations.reset_index(drop=True)

def main():
    # Initialize the recommender system
    recommender = AnimeRecommender()
    
    # Example usage
    print("\n" + "="*50)
    print("ANIME RECOMMENDATION SYSTEM")
    print("="*50)
    
    # Get recommendations for a specific anime
    print("\nRecommendations for 'Cowboy Bebop':")
    recommendations = recommender.get_recommendations('Cowboy Bebop', 5)
    if not recommendations.empty:
        for i, row in recommendations.iterrows():
            print(f"{i+1}. {row['title']}")
            print(f"   Genres: {row['genres']}")
            print(f"   Similarity Score: {row['similarity_score']:.4f}")
            print()
    
    # Get recommendations based on features
    print("\nRecommendations for 'Action' anime with 'Space' theme:")
    recommendations = recommender.get_recommendations_by_features(
        genres=['action'], 
        themes=['space'], 
        num_recommendations=5
    )
    if not recommendations.empty:
        for i, row in recommendations.iterrows():
            print(f"{i+1}. {row['title']}")
            print(f"   Genres: {row['genres']}")
            print(f"   Themes: {row['themes']}")
            print(f"   Similarity Score: {row['similarity_score']:.4f}")
            print()

if __name__ == "__main__":
    main()