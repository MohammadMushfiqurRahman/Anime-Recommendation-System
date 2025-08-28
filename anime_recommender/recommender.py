import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import os
from annoy import AnnoyIndex

warnings.filterwarnings("ignore")


class AnimeRecommender:
    def __init__(self, data_path="anime_recommender/processed_anime_data.feather"):
        """Initialize the recommender system with processed data"""
        print("Loading processed data...")
        self.df = pd.read_feather(data_path)
        print(f"Loaded {len(self.df)} anime entries")

        # Create indices for fast lookup
        self.indices = pd.Series(
            self.df.index, index=self.df["title"]
        ).drop_duplicates()

        # Initialize TF-IDF vectorizer
        print("Initializing TF-IDF vectorizer...")
        self.tfidf = TfidfVectorizer(stop_words="english", max_features=10000)
        self.tfidf_matrix = self.tfidf.fit_transform(
            self.df["combined_features"]
        )

        # Initialize Annoy index
        self.annoy_index = None
        self.build_annoy_index()

        print("Recommender system initialized!")

    def build_annoy_index(self, num_trees=50):
        """Build or load the Annoy index for faster similarity search"""
        index_path = "anime_recommender/anime_annoy_index.ann"
        vector_length = self.tfidf_matrix.shape[1]

        if os.path.exists(index_path):
            print("Loading existing Annoy index...")
            self.annoy_index = AnnoyIndex(vector_length, "angular")
            self.annoy_index.load(index_path)
            print("Annoy index loaded.")
        else:
            print("Building Annoy index...")
            self.annoy_index = AnnoyIndex(vector_length, "angular")
            for i, vector in enumerate(self.tfidf_matrix):
                self.annoy_index.add_item(i, vector.toarray()[0])
            self.annoy_index.build(num_trees)
            self.annoy_index.save(index_path)
            print(f"Annoy index built and saved to {index_path}")

    def get_recommendations(self, title, num_recommendations=10):
        """Get anime recommendations based on title"""
        # Check if the anime exists in our dataset
        if title not in self.indices:
            # Try to find similar titles
            similar_titles = [
                t for t in self.indices.index if title.lower() in t.lower()
            ]
            if similar_titles:
                return {
                    "message": (
                        f"Exact title '{title}' not found. "
                        "Did you mean one of these?"
                    ),
                    "suggestions": similar_titles[:5],
                }
            else:
                return {
                    "message": f"Anime '{title}' not found in the dataset."
                }

        # Get the index of the anime that matches the title
        idx = self.indices[title]

        # Get nearest neighbors from Annoy index
        anime_indices = self.annoy_index.get_nns_by_item(
            idx, num_recommendations + 1
        )[1:]

        # Get similarity scores for the recommended items
        sim_scores = cosine_similarity(
            self.tfidf_matrix[idx], self.tfidf_matrix[anime_indices]
        ).flatten()


        # Return the top most similar anime
        recommendations = (
            self.df[
                [
                    "title",
                    "genres",
                    "themes",
                    "demographics",
                    "synopsis",
                    "rating",
                ]
            ]
            .iloc[anime_indices]
            .copy()
        )
        recommendations["similarity_score"] = sim_scores

        # Replace any NaN values with empty strings
        recommendations = recommendations.fillna("")

        return recommendations.reset_index(drop=True)

    def get_surprise_recommendation(self, min_rating=8.0):
        """Get a random highly-rated anime recommendation"""
        # Filter for highly-rated anime
        highly_rated_anime = self.df[self.df["rating"] >= min_rating]

        if highly_rated_anime.empty:
            # If no anime meets the criteria, return a random one
            highly_rated_anime = self.df

        # Get a random anime from the filtered list
        surprise_anime = highly_rated_anime.sample(n=1)

        # Format the output to be consistent with other recommendation methods
        recommendation = surprise_anime[
            ["title", "genres", "themes", "demographics", "synopsis", "rating"]
        ].copy()
        recommendation["similarity_score"] = surprise_anime["rating"]

        return recommendation.reset_index(drop=True)

    def get_recommendations_by_features(
        self,
        genres=None,
        themes=None,
        demographics=None,
        num_recommendations=10,
    ):
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
            # If no features are provided, return top-rated anime
            print("No features provided. Returning top-rated anime.")
            top_rated = self.df.sort_values(by="rating", ascending=False).head(
                num_recommendations
            )
            recommendations = top_rated[
                ["title", "genres", "themes", "demographics"]
            ].copy()
            recommendations["similarity_score"] = top_rated["rating"]
            return recommendations.reset_index(drop=True)

        # Transform the filter string
        filter_vector = self.tfidf.transform([filter_string])

        # Calculate similarity scores
        sim_scores = cosine_similarity(
            filter_vector, self.tfidf_matrix
        ).flatten()

        # Get indices of top recommendations
        top_indices = sim_scores.argsort()[::-1][:num_recommendations]
        top_scores = sim_scores[top_indices]

        # Return recommendations
        recommendations = (
            self.df[["title", "genres", "themes", "demographics"]]
            .iloc[top_indices]
            .copy()
        )
        recommendations["similarity_score"] = top_scores

        # Replace any NaN values with empty strings
        recommendations = recommendations.fillna("")

        return recommendations.reset_index(drop=True)


def main():
    # Initialize the recommender system
    recommender = AnimeRecommender()

    # Example usage
    print("\n" + "=" * 50)
    print("ANIME RECOMMENDATION SYSTEM")
    print("=" * 50)

    # Get recommendations for a specific anime
    print("\nRecommendations for 'Cowboy Bebop':")
    recommendations = recommender.get_recommendations("Cowboy Bebop", 5)
    if not recommendations.empty:
        for i, row in recommendations.iterrows():
            print(f"{i+1}. {row['title']}")
            print(f"   Genres: {row['genres']}")
            print(f"   Similarity Score: {row['similarity_score']:.4f}")
            print()

    # Get recommendations based on features
    print("\nRecommendations for 'Action' anime with 'Space' theme:")
    recommendations = recommender.get_recommendations_by_features(
        genres=["action"], themes=["space"], num_recommendations=5
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
