import pandas as pd
from recommender import AnimeRecommender

def test_recommender():
    """Test the anime recommender system"""
    print("Initializing Anime Recommender System...")
    recommender = AnimeRecommender()
    
    print("\n" + "="*60)
    print("TESTING ANIME RECOMMENDATION SYSTEM")
    print("="*60)
    
    # Test 1: Get recommendations for a specific anime
    print("\nTest 1: Recommendations for 'Cowboy Bebop'")
    print("-" * 40)
    recommendations = recommender.get_recommendations('Cowboy Bebop', 5)
    if not recommendations.empty:
        print(f"Found {len(recommendations)} recommendations:")
        for i, row in recommendations.iterrows():
            print(f"  {i+1}. {row['title']} (Score: {row['similarity_score']:.4f})")
    else:
        print("No recommendations found.")
    
    # Test 2: Get recommendations for another anime
    print("\nTest 2: Recommendations for 'Naruto'")
    print("-" * 40)
    recommendations = recommender.get_recommendations('Naruto', 5)
    if not recommendations.empty:
        print(f"Found {len(recommendations)} recommendations:")
        for i, row in recommendations.iterrows():
            print(f"  {i+1}. {row['title']} (Score: {row['similarity_score']:.4f})")
    else:
        print("No recommendations found.")
    
    # Test 3: Get recommendations by features
    print("\nTest 3: Action anime with Adventure theme")
    print("-" * 40)
    recommendations = recommender.get_recommendations_by_features(
        genres=['action'], 
        themes=['adventure'], 
        num_recommendations=5
    )
    if not recommendations.empty:
        print(f"Found {len(recommendations)} recommendations:")
        for i, row in recommendations.iterrows():
            print(f"  {i+1}. {row['title']} (Score: {row['similarity_score']:.4f})")
            print(f"     Genres: {row['genres']}")
            print(f"     Themes: {row['themes']}")
    else:
        print("No recommendations found.")
    
    # Test 4: Get recommendations by demographics
    print("\nTest 4: Shounen demographic anime")
    print("-" * 40)
    recommendations = recommender.get_recommendations_by_features(
        demographics=['shounen'], 
        num_recommendations=5
    )
    if not recommendations.empty:
        print(f"Found {len(recommendations)} recommendations:")
        for i, row in recommendations.iterrows():
            print(f"  {i+1}. {row['title']} (Score: {row['similarity_score']:.4f})")
            print(f"     Demographics: {row['demographics']}")
    else:
        print("No recommendations found.")
    
    # Test 5: Test with non-existent anime
    print("\nTest 5: Non-existent anime 'NonExistentAnime'")
    print("-" * 40)
    recommendations = recommender.get_recommendations('NonExistentAnime', 5)
    
    print("\n" + "="*60)
    print("TESTING COMPLETED")
    print("="*60)

if __name__ == "__main__":
    test_recommender()