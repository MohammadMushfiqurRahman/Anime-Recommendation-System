import pandas as pd
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
import os

class CollaborativeRecommender:
    def __init__(self, rating_path='rating_complete.csv', anime_path='anime.csv'):
        self.rating_path = rating_path
        self.anime_path = anime_path
        self.model_path = 'anime_recommender/collaborative_model.pkl'
        self.algo = None
        self.df_anime = None
        self.data = None

        self._load_data()
        self._train_model()

    def _load_data(self):
        """Load the datasets"""
        print("Loading collaborative filtering data...")
        df_rating = pd.read_csv(self.rating_path)
        self.df_anime = pd.read_csv(self.anime_path)

        # The Reader class is used to parse a file containing ratings.
        # We need to define the rating scale.
        reader = Reader(rating_scale=(1, 10))

        # The columns must correspond to user id, item id and ratings (in that order).
        self.data = Dataset.load_from_df(df_rating[['user_id', 'anime_id', 'rating']], reader)
        print("Collaborative filtering data loaded.")

    def _train_model(self):
        """Train the SVD model and save it"""
        if os.path.exists(self.model_path):
            print("Loading existing collaborative model...")
            self.algo = self.load_model(self.model_path)
            print("Collaborative model loaded.")
        else:
            print("Training collaborative model...")
            # We'll use the famous SVD algorithm.
            self.algo = SVD()

            # Train the algorithm on the whole dataset, and wait for it to finish.
            trainset = self.data.build_full_trainset()
            self.algo.fit(trainset)

            # Save the trained model
            self.save_model(self.algo, self.model_path)
            print(f"Collaborative model trained and saved to {self.model_path}")

    def get_recommendations(self, user_id, num_recommendations=10):
        """Get anime recommendations for a given user"""
        # Get a list of all anime ids
        all_anime_ids = self.df_anime['anime_id'].unique()

        # Get a list of anime the user has already rated
        rated_anime_ids = self.data.df[self.data.df['user_id'] == user_id]['anime_id'].unique()

        # Get a list of anime to predict ratings for
        anime_to_predict_ids = [anime_id for anime_id in all_anime_ids if anime_id not in rated_anime_ids]

        # Predict ratings for the anime the user has not seen
        predictions = [self.algo.predict(user_id, anime_id) for anime_id in anime_to_predict_ids]

        # Sort the predictions by estimated rating
        predictions.sort(key=lambda x: x.est, reverse=True)

        # Get the top N recommendations
        top_n_predictions = predictions[:num_recommendations]

        # Get the anime ids of the top N recommendations
        top_n_anime_ids = [pred.iid for pred in top_n_predictions]

        # Get the anime titles and other info
        recommendations = self.df_anime[self.df_anime['anime_id'].isin(top_n_anime_ids)]

        return recommendations

    def save_model(self, model, file_name):
        """Save the model to a file"""
        from surprise.dump import dump
        dump(file_name, algo=model)

    def load_model(self, file_name):
        """Load the model from a file"""
        from surprise.dump import load
        _, model = load(file_name)
        return model

if __name__ == '__main__':
    # This is for testing purposes
    recommender = CollaborativeRecommender()
    recommendations = recommender.get_recommendations(user_id=1, num_recommendations=10)
    print("Recommendations for user 1:")
    print(recommendations)
