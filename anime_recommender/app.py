from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from recommender import AnimeRecommender

app = Flask(__name__)

# Initialize the recommender system
recommender = AnimeRecommender()

@app.route('/')
def index():
    """Main page for the anime recommendation system"""
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    """API endpoint for getting anime recommendations"""
    data = request.get_json()
    
    # Get the recommendation type and parameters
    rec_type = data.get('type', 'anime')
    num_recommendations = int(data.get('num_recommendations', 10))
    
    try:
        if rec_type == 'anime':
            anime_title = data.get('anime_title', '')
            if not anime_title:
                return jsonify({'error': 'Anime title is required'}), 400
            
            recommendations = recommender.get_recommendations(anime_title, num_recommendations)
            
        elif rec_type == 'features':
            genres = data.get('genres', [])
            themes = data.get('themes', [])
            demographics = data.get('demographics', [])
            
            # Convert empty lists to None
            genres = genres if genres else None
            themes = themes if themes else None
            demographics = demographics if demographics else None
            
            recommendations = recommender.get_recommendations_by_features(
                genres=genres,
                themes=themes,
                demographics=demographics,
                num_recommendations=num_recommendations
            )
        else:
            return jsonify({'error': 'Invalid recommendation type'}), 400
        
        # Convert recommendations to JSON-serializable format
        if recommendations.empty:
            return jsonify({'recommendations': []})
        
        # Convert DataFrame to list of dictionaries
        rec_list = []
        for _, row in recommendations.iterrows():
            rec_list.append({
                'title': row['title'],
                'genres': row['genres'],
                'themes': row['themes'],
                'demographics': row['demographics'],
                'similarity_score': float(row['similarity_score'])
            })
        
        return jsonify({'recommendations': rec_list})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/anime_list')
def anime_list():
    """API endpoint for getting a list of all anime titles"""
    try:
        # Get unique anime titles from the dataset
        titles = recommender.df['title'].tolist()
        return jsonify({'anime_titles': titles})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)