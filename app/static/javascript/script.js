window.addEventListener('load', function() {
    // Fetch news function
    fetchNews();

    // Event listener for Sign Up, Login, and Predictions tabs
    document.querySelectorAll('.user-actions .tab, .nav-bar .tab').forEach(function(tab) {
        tab.addEventListener('click', function() {
            let page;
            if (tab.classList.contains('sign-up')) {
                page = 'signup';
            } else if (tab.classList.contains('predictions')) {
                page = 'predictions';
            } else if (tab.classList.contains('user-profile-tab')) { // Handle user profile tab
                page = 'user';
            } else if (tab.id === 'playersTab') { // Handle Popular Players tab
                page = 'popular_players';
            } else if (tab.id === 'teamsTab') { // Handle #1 Popular Team tab
                page = 'teams_pages';
            } else {
                page = 'login';
            }
            window.location.href = `/${page}`;
        });
    });

    // Event listener for the Predictions tab specifically within the nav-bar
    const predictionsTab = document.getElementById('predictionsTab');
    if (predictionsTab) {
        predictionsTab.addEventListener('click', function() {
            window.location.href = '/predictions';
        });
    }
});



function fetchNews() {
    // Fetch NBA news from Flask route
    fetch('/news')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch NBA news');
            }
            return response.json();
        })
        .then(data => {
            const newsList = document.getElementById('news-list');
            newsList.innerHTML = ''; // Clear existing news

            // Display each NBA news article
            data.articles.forEach(article => {
                const li = document.createElement('li');
                li.textContent = article.title;
                newsList.appendChild(li);
            });
        })
        .catch(error => console.error('Error fetching NBA news:', error));
}
