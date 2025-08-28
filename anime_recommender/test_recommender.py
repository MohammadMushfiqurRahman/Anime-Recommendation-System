import unittest
import pandas as pd
from .recommender import AnimeRecommender


class TestAnimeRecommender(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the recommender for all tests."""
        print("Initializing Anime Recommender for testing...")
        cls.recommender = AnimeRecommender()

    def test_get_recommendations_valid_title(self):
        """Test getting recommendations for a valid anime title."""
        print("Testing recommendations for a valid title...")
        recommendations = self.recommender.get_recommendations(
            "Cowboy Bebop", 5
        )
        self.assertIsInstance(recommendations, pd.DataFrame)
        self.assertEqual(len(recommendations), 5)

    def test_get_recommendations_invalid_title(self):
        """Test getting recommendations for an invalid anime title."""
        print("Testing recommendations for an invalid title...")
        recommendations = self.recommender.get_recommendations(
            "NonExistentAnime", 5
        )
        self.assertIsInstance(recommendations, dict)
        self.assertIn("message", recommendations)

    def test_get_recommendations_by_features(self):
        """Test getting recommendations by features."""
        print("Testing recommendations by features...")
        recommendations = self.recommender.get_recommendations_by_features(
            genres=["action"], themes=["space"], num_recommendations=5
        )
        self.assertIsInstance(recommendations, pd.DataFrame)
        self.assertEqual(len(recommendations), 5)

    def test_get_recommendations_by_features_no_features(self):
        """Test getting recommendations with no features."""
        print("Testing recommendations with no features...")
        recommendations = self.recommender.get_recommendations_by_features(
            num_recommendations=5
        )
        self.assertIsInstance(recommendations, pd.DataFrame)
        self.assertEqual(len(recommendations), 5)

    def test_get_recommendations_num_recommendations(self):
        """Test the number of recommendations returned."""
        print("Testing the number of recommendations...")
        recommendations = self.recommender.get_recommendations("Naruto", 10)
        self.assertIsInstance(recommendations, pd.DataFrame)
        self.assertEqual(len(recommendations), 10)


if __name__ == "__main__":
    unittest.main()
