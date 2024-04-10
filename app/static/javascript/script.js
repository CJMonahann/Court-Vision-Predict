window.addEventListener('load', function() {
    fetchNews();
});

function fetchNews() {
    // Fetch news from Flask route instead of News API
    fetch('/news')
    .then(response => response.json())
    .then(data => {
        const newsList = document.getElementById('news-list');

        // Clear existing news
        newsList.innerHTML = '';

        // Display each news item
        data.articles.forEach(article => {
            const li = document.createElement('li');
            li.textContent = article.title;
            newsList.appendChild(li);
        });
    })
    .catch(error => console.error('Error fetching news:', error));
}

// Event listener for Sign Up and Login tabs
document.querySelectorAll('.user-actions .tab').forEach(function(tab) {
    tab.addEventListener('click', function() {
        // Redirect to the corresponding page
        const page = tab.classList.contains('sign-up') ? 'signup.html' : 'login.html';
        window.location.href = '/' + page;
    });
});
