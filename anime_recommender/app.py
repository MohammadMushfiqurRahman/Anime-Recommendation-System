from flask import Flask, render_template, request, jsonify
import pandas as pd
from recommender import AnimeRecommender
from collaborative_recommender import CollaborativeRecommender

app = Flask(__name__)

# Initialize the recommender systems
recommender = AnimeRecommender()
collaborative_recommender = CollaborativeRecommender()


@app.route("/")
def index():
    """Main page for the anime recommendation system"""
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    """API endpoint for getting anime recommendations"""
    data = request.get_json()
    print(f"Received data: {data}")  # Debugging statement

    # Get the recommendation type and parameters
    rec_type = data.get("type", "anime")
    num_recommendations = int(data.get("num_recommendations", 10))

    try:
        if rec_type == "anime":
            anime_title = data.get("anime_title", "")
            if not anime_title:
                return jsonify({"error": "Anime title is required"}), 400

            recommendations = recommender.get_recommendations(
                anime_title, num_recommendations
            )

        elif rec_type == "features":
            genres = data.get("genres", [])
            themes = data.get("themes", [])
            demographics = data.get("demographics", [])

            # Convert empty lists to None
            genres = genres if genres else None
            themes = themes if themes else None
            demographics = demographics if demographics else None

            recommendations = recommender.get_recommendations_by_features(
                genres=genres,
                themes=themes,
                demographics=demographics,
                num_recommendations=num_recommendations,
            )
        else:
            return jsonify({"error": "Invalid recommendation type"}), 400

        print(f"Recommendations: {recommendations}")  # Debugging statement

        # Convert recommendations to JSON-serializable format
        if recommendations.empty:
            return jsonify({"recommendations": []})

        # Convert DataFrame to list of dictionaries
        rec_list = []
        for _, row in recommendations.iterrows():
            rec_list.append(
                {
                    "title": row["title"],
                    "genres": row["genres"] if pd.notna(row["genres"]) else "",
                    "themes": row["themes"] if pd.notna(row["themes"]) else "",
                    "demographics": (
                        row["demographics"]
                        if pd.notna(row["demographics"])
                        else ""
                    ),
                    "similarity_score": (
                        float(row["similarity_score"])
                        if pd.notna(row["similarity_score"])
                        else 0.0
                    ),
                }
            )

        return jsonify({"recommendations": rec_list})

    except Exception as e:
        print(f"Error: {e}")  # Debugging statement
        return jsonify({"error": str(e)}), 500


@app.route("/surprise")
def surprise():
    """API endpoint for getting a surprise anime recommendation"""
    try:
        recommendation = recommender.get_surprise_recommendation()
        rec_list = []
        for _, row in recommendation.iterrows():
            rec_list.append(
                {
                    "title": row["title"],
                    "genres": row["genres"] if pd.notna(row["genres"]) else "",
                    "themes": row["themes"] if pd.notna(row["themes"]) else "",
                    "demographics": (
                        row["demographics"]
                        if pd.notna(row["demographics"])
                        else ""
                    ),
                    "similarity_score": (
                        float(row["similarity_score"])
                        if pd.notna(row["similarity_score"])
                        else 0.0
                    ),
                }
            )
        return jsonify({"recommendations": rec_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/collaborative-recommendations/<int:user_id>")
def collaborative_recommendations(user_id):
    """API endpoint for getting collaborative filtering recommendations"""
    try:
        recommendations = collaborative_recommender.get_recommendations(user_id)
        rec_list = recommendations.to_dict('records')
        return jsonify({"recommendations": rec_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def anime__list():
    """API endpoint for getting a list of all anime titles"""
    try:
        # Get unique anime titles from the dataset
        titles = recommender.df["title"].tolist()
        return jsonify({"anime_titles": titles})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
