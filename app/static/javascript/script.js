window.addEventListener('load', function() {
    // Fetch news function
    fetchNews();

    // Event listener for tabs in both user-actions and nav-bar
    document.querySelectorAll('.user-actions .user-tab, .nav-bar .nav-tab').forEach(function(tab) {
        tab.addEventListener('click', function() {
            let page;
            if (tab.id === 'signupTab') {
                page = 'signup';
            } else if (tab.id === 'loginTab') {
                page = 'login';
            } else if (tab.id === 'user-profile-tab') {
                page = 'user';
            } else if (tab.id === 'predictionsTab') {
                page = 'predictions';
            } else if (tab.id === 'playersTab') {
                page = 'popular_players';
            } else if (tab.id === 'teamsTab') {
                page = 'teams_pages';
            } else {
                page = ''; // Default to empty for no specific page matches
            }
            // Redirect based on the determined page
            if (page) {
                window.location.href = `/${page}`;
            }
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

function fetchPlayers() {
    // Fetch NBA players from Flask route
    fetch('/nba-players')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch NBA players');
            }
            return response.json();
        })
        .then(data => {
            const playersContainer = document.getElementById('players-container');
            playersContainer.innerHTML = ''; // Clear existing players

            // Display each NBA player
            data.api.players.forEach(player => {
                const playerDiv = document.createElement('div');
                playerDiv.classList.add('player-info');
                playerDiv.innerHTML = `
                    <h3>${player.firstname} ${player.lastname}</h3>
                    <p>Team Affiliation: ${player.affiliation}</p>
                    <p>Birth Date: ${player.birth.date}</p>
                    <p>Country: ${player.birth.country}</p>
                    <p>College: ${player.college}</p>
                    <p>Position: ${player.pos}</p>
                    <p>Height: ${player.height.feets}'${player.height.inches}" (${player.height.meters}m)</p>
                    <p>Weight: ${player.weight.pounds} lbs (${player.weight.kilograms} kg)</p>
                    <p>Jersey Number: ${player.jersey}</p>
                    <p>NBA Pro Seasons: ${player.nba.pro}</p>
                `;
                playersContainer.appendChild(playerDiv);
            });
        })
        .catch(error => console.error('Error fetching NBA players:', error));
}
