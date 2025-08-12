import pandas as pd
from recommender import AnimeRecommender

def main():
    """Main interface for the anime recommendation system"""
    print("="*60)
    print("ANIME RECOMMENDATION SYSTEM")
    print("="*60)
    print("Welcome to the Anime Recommendation System!")
    print("This system will help you discover new anime based on your preferences.")
    
    # Initialize the recommender system
    print("\nInitializing recommendation system...")
    recommender = AnimeRecommender()
    
    while True:
        print("\n" + "-"*60)
        print("MAIN MENU")
        print("-"*60)
        print("1. Get recommendations for a specific anime")
        print("2. Get recommendations by genre")
        print("3. Get recommendations by theme")
        print("4. Get recommendations by demographic")
        print("5. Get recommendations by multiple features")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            get_anime_recommendations(recommender)
        elif choice == '2':
            get_genre_recommendations(recommender)
        elif choice == '3':
            get_theme_recommendations(recommender)
        elif choice == '4':
            get_demographic_recommendations(recommender)
        elif choice == '5':
            get_feature_recommendations(recommender)
        elif choice == '6':
            print("\nThank you for using the Anime Recommendation System!")
            print("Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 6.")

def get_anime_recommendations(recommender):
    """Get recommendations for a specific anime"""
    print("\n" + "-"*40)
    print("ANIME-BASED RECOMMENDATIONS")
    print("-"*40)
    
    anime_title = input("Enter the name of an anime you like: ").strip()
    if not anime_title:
        print("No input provided.")
        return
    
    num_recs = input("How many recommendations would you like? (default: 10): ").strip()
    try:
        num_recs = int(num_recs) if num_recs else 10
    except ValueError:
        print("Invalid number. Using default value of 10.")
        num_recs = 10
    
    print(f"\nFinding recommendations for '{anime_title}'...")
    recommendations = recommender.get_recommendations(anime_title, num_recs)
    
    if not recommendations.empty:
        print(f"\nTop {len(recommendations)} recommendations:")
        print("-" * 40)
        for i, row in recommendations.iterrows():
            print(f"{i+1:2d}. {row['title']}")
            if row['genres']:
                print(f"     Genres: {row['genres']}")
            if row['themes']:
                print(f"     Themes: {row['themes']}")
            if row['demographics']:
                print(f"     Demographics: {row['demographics']}")
            print(f"     Similarity Score: {row['similarity_score']:.4f}")
            print()
    else:
        print("No recommendations found.")

def get_genre_recommendations(recommender):
    """Get recommendations by genre"""
    print("\n" + "-"*40)
    print("GENRE-BASED RECOMMENDATIONS")
    print("-"*40)
    
    print("Enter one or more genres (comma-separated):")
    print("Examples: action, comedy, drama, romance, scifi, fantasy, etc.")
    genres_input = input("Genres: ").strip()
    
    if not genres_input:
        print("No genres provided.")
        return
    
    genres = [genre.strip().lower() for genre in genres_input.split(',')]
    
    num_recs = input("How many recommendations would you like? (default: 10): ").strip()
    try:
        num_recs = int(num_recs) if num_recs else 10
    except ValueError:
        print("Invalid number. Using default value of 10.")
        num_recs = 10
    
    print(f"\nFinding recommendations for genres: {', '.join(genres)}...")
    recommendations = recommender.get_recommendations_by_features(
        genres=genres, 
        num_recommendations=num_recs
    )
    
    if not recommendations.empty:
        print(f"\nTop {len(recommendations)} recommendations:")
        print("-" * 40)
        for i, row in recommendations.iterrows():
            print(f"{i+1:2d}. {row['title']}")
            if row['genres']:
                print(f"     Genres: {row['genres']}")
            if row['themes']:
                print(f"     Themes: {row['themes']}")
            if row['demographics']:
                print(f"     Demographics: {row['demographics']}")
            print(f"     Similarity Score: {row['similarity_score']:.4f}")
            print()
    else:
        print("No recommendations found.")

def get_theme_recommendations(recommender):
    """Get recommendations by theme"""
    print("\n" + "-"*40)
    print("THEME-BASED RECOMMENDATIONS")
    print("-"*40)
    
    print("Enter one or more themes (comma-separated):")
    print("Examples: school, space, romance, comedy, etc.")
    themes_input = input("Themes: ").strip()
    
    if not themes_input:
        print("No themes provided.")
        return
    
    themes = [theme.strip().lower() for theme in themes_input.split(',')]
    
    num_recs = input("How many recommendations would you like? (default: 10): ").strip()
    try:
        num_recs = int(num_recs) if num_recs else 10
    except ValueError:
        print("Invalid number. Using default value of 10.")
        num_recs = 10
    
    print(f"\nFinding recommendations for themes: {', '.join(themes)}...")
    recommendations = recommender.get_recommendations_by_features(
        themes=themes, 
        num_recommendations=num_recs
    )
    
    if not recommendations.empty:
        print(f"\nTop {len(recommendations)} recommendations:")
        print("-" * 40)
        for i, row in recommendations.iterrows():
            print(f"{i+1:2d}. {row['title']}")
            if row['genres']:
                print(f"     Genres: {row['genres']}")
            if row['themes']:
                print(f"     Themes: {row['themes']}")
            if row['demographics']:
                print(f"     Demographics: {row['demographics']}")
            print(f"     Similarity Score: {row['similarity_score']:.4f}")
            print()
    else:
        print("No recommendations found.")

def get_demographic_recommendations(recommender):
    """Get recommendations by demographic"""
    print("\n" + "-"*40)
    print("DEMOGRAPHIC-BASED RECOMMENDATIONS")
    print("-"*40)
    
    print("Enter a demographic:")
    print("Examples: shounen, shoujo, seinen, josei, kids")
    demographic = input("Demographic: ").strip().lower()
    
    if not demographic:
        print("No demographic provided.")
        return
    
    num_recs = input("How many recommendations would you like? (default: 10): ").strip()
    try:
        num_recs = int(num_recs) if num_recs else 10
    except ValueError:
        print("Invalid number. Using default value of 10.")
        num_recs = 10
    
    print(f"\nFinding recommendations for demographic: {demographic}...")
    recommendations = recommender.get_recommendations_by_features(
        demographics=[demographic], 
        num_recommendations=num_recs
    )
    
    if not recommendations.empty:
        print(f"\nTop {len(recommendations)} recommendations:")
        print("-" * 40)
        for i, row in recommendations.iterrows():
            print(f"{i+1:2d}. {row['title']}")
            if row['genres']:
                print(f"     Genres: {row['genres']}")
            if row['themes']:
                print(f"     Themes: {row['themes']}")
            if row['demographics']:
                print(f"     Demographics: {row['demographics']}")
            print(f"     Similarity Score: {row['similarity_score']:.4f}")
            print()
    else:
        print("No recommendations found.")

def get_feature_recommendations(recommender):
    """Get recommendations by multiple features"""
    print("\n" + "-"*40)
    print("MULTI-FEATURE RECOMMENDATIONS")
    print("-"*40)
    
    print("Enter genres (comma-separated, or press Enter to skip):")
    genres_input = input("Genres: ").strip()
    genres = [genre.strip().lower() for genre in genres_input.split(',')] if genres_input else None
    
    print("Enter themes (comma-separated, or press Enter to skip):")
    themes_input = input("Themes: ").strip()
    themes = [theme.strip().lower() for theme in themes_input.split(',')] if themes_input else None
    
    print("Enter demographic (or press Enter to skip):")
    demographic = input("Demographic: ").strip().lower() or None
    
    # Check if at least one feature is provided
    if not any([genres, themes, demographic]):
        print("No features provided.")
        return
    
    num_recs = input("How many recommendations would you like? (default: 10): ").strip()
    try:
        num_recs = int(num_recs) if num_recs else 10
    except ValueError:
        print("Invalid number. Using default value of 10.")
        num_recs = 10
    
    print("\nFinding recommendations based on your preferences...")
    recommendations = recommender.get_recommendations_by_features(
        genres=genres,
        themes=themes,
        demographics=[demographic] if demographic else None,
        num_recommendations=num_recs
    )
    
    if not recommendations.empty:
        print(f"\nTop {len(recommendations)} recommendations:")
        print("-" * 40)
        for i, row in recommendations.iterrows():
            print(f"{i+1:2d}. {row['title']}")
            if row['genres']:
                print(f"     Genres: {row['genres']}")
            if row['themes']:
                print(f"     Themes: {row['themes']}")
            if row['demographics']:
                print(f"     Demographics: {row['demographics']}")
            print(f"     Similarity Score: {row['similarity_score']:.4f}")
            print()
    else:
        print("No recommendations found.")

if __name__ == "__main__":
    main()