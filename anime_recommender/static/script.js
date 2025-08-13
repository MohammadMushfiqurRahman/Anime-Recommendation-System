// Tab switching functionality
document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            
            // Remove active class from all buttons and panes
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));
            
            // Add active class to clicked button and corresponding pane
            this.classList.add('active');
            document.getElementById(`${tabId}-tab`).classList.add('active');
        });
    });
    
    // Anime recommendation button
    document.getElementById('anime-recommend-btn').addEventListener('click', getAnimeRecommendations);
    
    // Features recommendation button
    document.getElementById('features-recommend-btn').addEventListener('click', getFeatureRecommendations);
    
    // Anime title input with suggestions
    const animeTitleInput = document.getElementById('anime-title');
    animeTitleInput.addEventListener('input', showAnimeSuggestions);
    
    // Load anime titles for suggestions
    loadAnimeTitles();
});

// Global variable to store anime titles
let animeTitles = [];

// Load anime titles for autocomplete suggestions
async function loadAnimeTitles() {
    try {
        const response = await fetch('/anime_list');
        const data = await response.json();
        animeTitles = data.anime_titles || [];
    } catch (error) {
        console.error('Error loading anime titles:', error);
    }
}

// Show anime title suggestions
function showAnimeSuggestions() {
    const input = this.value.toLowerCase();
    const suggestionsContainer = document.getElementById('anime-suggestions');
    
    // Clear previous suggestions
    suggestionsContainer.innerHTML = '';
    
    if (input.length < 2) {
        suggestionsContainer.style.display = 'none';
        return;
    }
    
    // Filter titles based on input
    const filteredTitles = animeTitles.filter(title => 
        title.toLowerCase().includes(input)
    ).slice(0, 10); // Limit to 10 suggestions
    
    if (filteredTitles.length > 0) {
        suggestionsContainer.style.display = 'block';
        
        filteredTitles.forEach(title => {
            const suggestionItem = document.createElement('div');
            suggestionItem.className = 'suggestion-item';
            suggestionItem.textContent = title;
            suggestionItem.addEventListener('click', function() {
                document.getElementById('anime-title').value = title;
                suggestionsContainer.style.display = 'none';
            });
            suggestionsContainer.appendChild(suggestionItem);
        });
    } else {
        suggestionsContainer.style.display = 'none';
    }
}

// Get anime-based recommendations
async function getAnimeRecommendations() {
    const animeTitle = document.getElementById('anime-title').value.trim();
    const numRecommendations = document.getElementById('anime-num-recs').value;
    
    if (!animeTitle) {
        alert('Please enter an anime title');
        return;
    }
    
    // Show loading indicator
    showLoading();
    
    try {
        const response = await fetch('/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                type: 'anime',
                anime_title: animeTitle,
                num_recommendations: parseInt(numRecommendations)
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayRecommendations(data.recommendations);
        } else {
            showError(data.error || 'An error occurred');
        }
    } catch (error) {
        showError('Network error: ' + error.message);
    }
}

// Get feature-based recommendations
async function getFeatureRecommendations() {
    const genres = document.getElementById('genres').value.trim();
    const themes = document.getElementById('themes').value.trim();
    const demographics = document.getElementById('demographics').value;
    const numRecommendations = document.getElementById('features-num-recs').value;
    
    // Convert comma-separated strings to arrays
    const genresArray = genres ? genres.split(',').map(item => item.trim()).filter(item => item) : [];
    const themesArray = themes ? themes.split(',').map(item => item.trim()).filter(item => item) : [];
    const demographicsArray = demographics ? [demographics] : [];
    
    // Show loading indicator
    showLoading();
    
    try {
        const response = await fetch('/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                type: 'features',
                genres: genresArray,
                themes: themesArray,
                demographics: demographicsArray,
                num_recommendations: parseInt(numRecommendations)
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayRecommendations(data.recommendations);
        } else {
            showError(data.error || 'An error occurred');
        }
    } catch (error) {
        showError('Network error: ' + error.message);
    }
}

// Show loading indicator
function showLoading() {
    const resultsContainer = document.getElementById('results');
    resultsContainer.style.display = 'block';
    resultsContainer.innerHTML = `
        <h2>Recommendations</h2>
        <div class="loading">
            <div class="spinner"></div>
            <p>Finding the best anime recommendations for you...</p>
        </div>
    `;
}

// Display recommendations
function displayRecommendations(recommendations) {
    const resultsContainer = document.getElementById('results');
    resultsContainer.style.display = 'block';
    
    if (!recommendations || recommendations.length === 0) {
        resultsContainer.innerHTML = `
            <h2>Recommendations</h2>
            <p>No recommendations found. Please try a different anime title or features.</p>
        `;
        return;
    }
    
    let recommendationsHTML = '<h2>Recommendations</h2>';
    
    recommendations.forEach((anime, index) => {
        recommendationsHTML += `
            <div class="anime-card">
                <h3>${index + 1}. ${anime.title}</h3>
                <div class="anime-info">
                    <strong>Genres:</strong> ${anime.genres || 'N/A'}
                </div>
                <div class="anime-info">
                    <strong>Themes:</strong> ${anime.themes || 'N/A'}
                </div>
                <div class="anime-info">
                    <strong>Demographics:</strong> ${anime.demographics || 'N/A'}
                </div>
                <div class="anime-info similarity-score">
                    <strong>Similarity Score:</strong> ${anime.similarity_score.toFixed(4)}
                </div>
            </div>
        `;
    });
    
    resultsContainer.innerHTML = recommendationsHTML;
}

// Show error message
function showError(message) {
    const resultsContainer = document.getElementById('results');
    resultsContainer.style.display = 'block';
    resultsContainer.innerHTML = `
        <h2>Recommendations</h2>
        <div class="error">
            <p>Error: ${message}</p>
        </div>
    `;
}