// Simple JavaScript for the UI
document.addEventListener('DOMContentLoaded', function() {
  // Anime search functionality
  const animeSearchInput = document.getElementById('anime-search-input');
  const searchInput = document.getElementById('search-input');
  
  // Set up event listeners for search inputs
  animeSearchInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      searchAnime(this.value);
    }
  });
  
  searchInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      searchAnime(this.value);
    }
  });
  
  // Set up navigation links
  document.getElementById('home-link').addEventListener('click', function(e) {
    e.preventDefault();
    // In a full implementation, this would navigate to the home page
  });
  
  document.getElementById('browse-link').addEventListener('click', function(e) {
    e.preventDefault();
    // In a full implementation, this would navigate to the browse page
  });
  
  document.getElementById('recommendations-link').addEventListener('click', function(e) {
    e.preventDefault();
    // In a full implementation, this would navigate to the recommendations page
  });
  
  // Function to search for anime (would connect to backend in a full implementation)
  function searchAnime(query) {
    if (query.trim() === '') return;
    
    // Show loading indicator
    const container = document.getElementById('recommendations-container');
    container.innerHTML = `
      <div class="col-span-full py-4 text-center">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-[#007bff]"></div>
        <p class="text-white mt-2">Finding recommendations for "${query}"...</p>
      </div>
    `;
    
    // Make API call to get recommendations
    fetch('/recommend', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        type: 'anime',
        anime_title: query,
        num_recommendations: 12
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        container.innerHTML = `
          <div class="col-span-full py-4 text-center">
            <p class="text-red-500">Error: ${data.error}</p>
          </div>
        `;
        return;
      }
      
      displayRecommendations(data.recommendations, query);
    })
    .catch(error => {
      container.innerHTML = `
        <div class="col-span-full py-4 text-center">
          <p class="text-red-500">Error: ${error.message}</p>
        </div>
      `;
    });
  }
  
  // Function to display recommendations
  function displayRecommendations(recommendations, query) {
    const container = document.getElementById('recommendations-container');
    
    if (!recommendations || recommendations.length === 0) {
      container.innerHTML = `
        <div class="col-span-full py-4 text-center">
          <p class="text-white">No recommendations found for "${query}".</p>
        </div>
      `;
      return;
    }
    
    let html = `
      <div class="col-span-full py-4">
        <h2 class="text-white text-xl font-bold">Recommendations for "${query}"</h2>
        <p class="text-[#9cabba]">Based on your preferences</p>
      </div>
    `;
    
    recommendations.forEach(anime => {
      // Create a simple placeholder image URL
      const imageUrl = `https://placehold.co/300x400/283039/9cabba?text=${encodeURIComponent(anime.title)}`;
      
      html += `
        <div class="flex flex-col gap-3 pb-3">
          <div
            class="w-full bg-center bg-no-repeat aspect-[3/4] bg-cover rounded-lg"
            style='background-image: url("${imageUrl}");'
          ></div>
          <div>
            <p class="text-white text-base font-medium leading-normal">${anime.title}</p>
            <p class="text-[#9cabba] text-sm font-normal leading-normal">${anime.genres || 'N/A'}</p>
          </div>
        </div>
      `;
    });
    
    container.innerHTML = html;
  }
});