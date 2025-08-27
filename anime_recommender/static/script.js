// Function to display recommendations
function displayRecommendations(recommendations, query) {
  console.log("Displaying recommendations for:", query);
  console.log("Recommendations:", recommendations);
  
  const container = document.getElementById('recommendations-container');
  const errorContainer = document.getElementById('error-container');
  errorContainer.innerHTML = ''; // Clear previous errors
  
  if (!recommendations || recommendations.length === 0) {
    container.innerHTML = `
      <div class="col-span-full py-4 text-center">
        <p class="text-white">No recommendations found for "${query}".</p>
        <p class="text-[#9cabba] text-sm mt-2">Try searching for a different anime or browse by category.</p>
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

// Function to handle API errors
function handleApiError(error) {
  console.error("API Error:", error);
  const errorContainer = document.getElementById('error-container');
  errorContainer.innerHTML = `<p class="text-red-500">Error: ${error.message || 'An unknown error occurred.'}</p>`;
  const recommendationsContainer = document.getElementById('recommendations-container');
  recommendationsContainer.innerHTML = ''; // Clear recommendations
}

// Function to load initial recommendations
function loadInitialRecommendations() {
  console.log("Loading initial recommendations");
  
  const container = document.getElementById('recommendations-container');
  container.innerHTML = `
    <div class="col-span-full py-4 text-center">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-[#007bff]"></div>
      <p class="text-white mt-2">Loading recommendations...</p>
    </div>
  `;
  
  fetch('/recommend', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      type: 'features',
      genres: ['action'],
      num_recommendations: 12
    })
  })
  .then(response => {
    if (!response.ok) {
      return response.json().then(err => { throw new Error(err.error || response.statusText) });
    }
    return response.json();
  })
  .then(data => {
    displayRecommendations(data.recommendations, 'Action');
  })
  .catch(error => {
    handleApiError(error);
  });
}

// Simple JavaScript for the UI
document.addEventListener('DOMContentLoaded', function() {
  console.log("DOM loaded");

  // Initialize autocomplete
  const autocomplete = new Autocomplete(document.querySelector('#anime-search-input'), {
    data: [],
    onSelectItem: ({label, value}) => {
      searchAnime(value);
    }
  });

  fetch('/anime_list')
    .then(response => response.json())
    .then(data => {
      const animeTitles = data.anime_titles.map(title => ({ label: title, value: title }));
      autocomplete.setData(animeTitles);
    });
  
  // Anime search functionality
  const animeSearchInput = document.getElementById('anime-search-input');
  const searchInput = document.getElementById('search-input');
  
  // Set up event listeners for search inputs
  animeSearchInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      console.log("Searching for anime:", this.value);
      searchAnime(this.value);
    }
  });
  
  searchInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      console.log("Searching for anime:", this.value);
      searchAnime(this.value);
    }
  });
  
  // Set up navigation links
  document.getElementById('home-link').addEventListener('click', function(e) {
    e.preventDefault();
    console.log("Home link clicked");
  });
  
  document.getElementById('browse-link').addEventListener('click', function(e) {
    e.preventDefault();
    console.log("Browse link clicked");
  });
  
  document.getElementById('recommendations-link').addEventListener('click', function(e) {
    e.preventDefault();
    console.log("Recommendations link clicked");
    loadInitialRecommendations();
  });
  
  // Set up category filter buttons
  const categoryButtons = document.querySelectorAll('[data-category]');
  categoryButtons.forEach(button => {
    button.addEventListener('click', function() {
      const category = this.getAttribute('data-category');
      console.log("Filtering by category:", category);
      filterByCategory(category);
    });
  });
  
  // Set up apply filters button
  document.getElementById('apply-filters-btn').addEventListener('click', function() {
    const genre = document.getElementById('genre-filter').value;
    const theme = document.getElementById('theme-filter').value;
    const demographic = document.getElementById('demographic-filter').value;
    
    console.log("Applying filters:", {genre, theme, demographic});
    
    let filterString = '';
    if (genre) filterString += genre + ' ';
    if (theme) filterString += theme + ' ';
    if (demographic) filterString += demographic;
    
    if (!genre && !theme && !demographic) {
      filterString = 'All';
    }
    
    filterByFeatures(genre, theme, demographic, filterString.trim() || 'All');
  });

  // Set up surprise me button
  document.getElementById('surprise-me-btn').addEventListener('click', function() {
    surpriseMe();
  });
  
  // Function to search for anime
  function searchAnime(query) {
    if (query.trim() === '') return;
    
    console.log("Searching for anime:", query);
    
    const container = document.getElementById('recommendations-container');
    container.innerHTML = `
      <div class="col-span-full py-4 text-center">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-[#007bff]"></div>
        <p class="text-white mt-2">Finding recommendations for "${query}"...</p>
      </div>
    `;
    
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
    .then(response => {
      if (!response.ok) {
        return response.json().then(err => { throw new Error(err.error || response.statusText) });
      }
      return response.json();
    })
    .then(data => {
      displayRecommendations(data.recommendations, query);
    })
    .catch(error => {
      handleApiError(error);
    });
  }
  
  // Function to filter by category
  function filterByCategory(category) {
    console.log("Filtering by category:", category);
    
    categoryButtons.forEach(button => {
      button.classList.remove('bg-[#007bff]');
    });
    
    event.target.closest('[data-category]').classList.add('bg-[#007bff]');
    
    const container = document.getElementById('recommendations-container');
    container.innerHTML = `
      <div class="col-span-full py-4 text-center">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-[#007bff]"></div>
        <p class="text-white mt-2">Finding ${category} anime...</p>
      </div>
    `;
    
    fetch('/recommend', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        type: 'features',
        genres: category === 'All' ? [] : [category.toLowerCase()],
        num_recommendations: 12
      })
    })
    .then(response => {
      if (!response.ok) {
        return response.json().then(err => { throw new Error(err.error || response.statusText) });
      }
      return response.json();
    })
    .then(data => {
      displayRecommendations(data.recommendations, category);
    })
    .catch(error => {
      handleApiError(error);
    });
  }
  
  // Function to filter by features
  function filterByFeatures(genre, theme, demographic, filterString) {
    console.log("Filtering by features:", {genre, theme, demographic, filterString});
    
    const container = document.getElementById('recommendations-container');
    container.innerHTML = `
      <div class="col-span-full py-4 text-center">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-[#007bff]"></div>
        <p class="text-white mt-2">Finding anime with filters: ${filterString}...</p>
      </div>
    `;
    
    const genres = genre ? [genre] : [];
    const themes = theme ? [theme] : [];
    const demographics = demographic ? [demographic] : [];
    
    fetch('/recommend', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        type: 'features',
        genres: genres,
        themes: themes,
        demographics: demographics,
        num_recommendations: 12
      })
    })
    .then(response => {
      if (!response.ok) {
        return response.json().then(err => { throw new Error(err.error || response.statusText) });
      }
      return response.json();
    })
    .then(data => {
      displayRecommendations(data.recommendations, filterString);
    })
    .catch(error => {
      handleApiError(error);
    });
  }
  
  // Function to get a surprise recommendation
  function surpriseMe() {
    console.log("Getting a surprise recommendation");
    
    const container = document.getElementById('recommendations-container');
    container.innerHTML = `
      <div class="col-span-full py-4 text-center">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-[#007bff]"></div>
        <p class="text-white mt-2">Finding a surprise anime...</p>
      </div>
    `;
    
    fetch('/surprise')
    .then(response => {
      if (!response.ok) {
        return response.json().then(err => { throw new Error(err.error || response.statusText) });
      }
      return response.json();
    })
    .then(data => {
      displayRecommendations(data.recommendations, 'Surprise Recommendation');
    })
    .catch(error => {
      handleApiError(error);
    });
  }

  // Load initial recommendations
  loadInitialRecommendations();
});