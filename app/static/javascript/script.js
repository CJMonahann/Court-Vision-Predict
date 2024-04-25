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

document.addEventListener('DOMContentLoaded', () => {
    const tabsContainer = document.getElementById('tabs-container');
    const teamInfoBox = document.getElementById('team-info-box');

    const teams = [
        { id: 31, name: 'San Antonio Spurs', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/a/a2/San_Antonio_Spurs.svg' },
        { id: 19, name: 'Memphis Grizzlies', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/f/f1/Memphis_Grizzlies.svg' },
        { id: 14, name: 'Houston Rockets', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/2/28/Houston_Rockets.svg' },
        { id: 23, name: 'New Orleans Pelicans', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/0/0d/New_Orleans_Pelicans_logo.svg' },
        { id: 8, name: 'Dallas Mavericks', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/a/a2/Dallas_Mavericks_logo.svg' },
        { id: 11, name: 'Golden State Warriors', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/0/01/Golden_State_Warriors_logo.svg' },
        { id: 30, name: 'Sacramento Kings', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/c/c7/SacramentoKings.svg' },
        { id: 17, name: 'Los Angeles Lakers', logoUrl: 'https://upload.wikimedia.org/wikipedia/commons/3/3c/Los_Angeles_Lakers_logo.svg' },
        { id: 28, name: 'Phoenix Suns', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/d/dc/Phoenix_Suns_logo.svg' },
        { id: 16, name: 'LA Clippers', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/b/bb/Los_Angeles_Clippers_%282015%29.svg' },
        { id: 29, name: 'Portland Trail Blazers', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/2/21/Portland_Trail_Blazers_logo.svg' },
        { id: 40, name: 'Utah Jazz', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/0/04/Utah_Jazz_logo_%282016%29.svg' },
        { id: 9, name: 'Denver Nuggets', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/7/76/Denver_Nuggets.svg' },
        { id: 22, name: 'Minnesota Timberwolves', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/9/9a/Minnesota_Timberwolves_logo.svg' },
        { id: 25, name: 'Oklahoma City Thunder', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/5/5d/Oklahoma_City_Thunder.svg' },
        { id: 41, name: 'Washington Wizards', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/0/02/Washington_Wizards_logo.svg' },
        { id: 5, name: 'Charlotte Hornets', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/c/c4/Charlotte_Hornets_%282014%29.svg' },
        { id: 1, name: 'Atlanta Hawks', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/2/24/Atlanta_Hawks_logo.svg' },
        { id: 20, name: 'Miami Heat', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/f/fb/Miami_Heat_logo.svg' },
        { id: 26, name: 'Orlando Magic', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/1/10/Orlando_Magic_logo.svg' },
        { id: 10, name: 'Detroit Pistons', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/1/1e/Detroit_Pistons_logo.svg' },
        { id: 6, name: 'Chicago Bulls', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/6/67/Chicago_Bulls_logo.svg' },
        { id: 15, name: 'Indiana Pacers', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/1/1b/Indiana_Pacers_logo.svg' },
        { id: 7, name: 'Cleveland Cavaliers', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/4/4b/Cleveland_Cavaliers_logo.svg' },
        { id: 21, name: 'Milwaukee Bucks', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/4/4a/Milwaukee_Bucks_logo.svg' },
        { id: 38, name: 'Toronto Raptors', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/3/36/Toronto_Raptors_logo.svg' },
        { id: 4, name: 'Brooklyn Nets', logoUrl: 'https://upload.wikimedia.org/wikipedia/commons/4/44/Brooklyn_Nets_newlogo.svg' },
        { id: 27, name: 'Philadelphia 76ers', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/0/0e/Philadelphia_76ers_logo.svg' },
        { id: 24, name: 'New York Knicks', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/2/25/New_York_Knicks_logo.svg' },
        { id: 2, name: 'Boston Celtics', logoUrl: 'https://upload.wikimedia.org/wikipedia/en/8/8f/Boston_Celtics.svg' }
    ];    

    teams.forEach(team => {
        const button = document.createElement('button');
        button.textContent = team.name;
        button.addEventListener('click', () => {
            fetchTeamInfo(team.id, team.name, team.logoUrl);
        });
        tabsContainer.appendChild(button);
    });

    // Function to fetch and display team information
    function fetchTeamInfo(teamId, teamName, logoUrl) {
        const url = `https://api-nba-v1.p.rapidapi.com/standings`;
        const querystring = {
            league: 'standard',
            season: '2023',
            team: teamId
        };
        const headers = {
            'X-RapidAPI-Key': '3e1ea378a2msh4dc8e4f48876bd3p19ae7ejsnd145768cd66d',
            'X-RapidAPI-Host': 'api-nba-v1.p.rapidapi.com'
        };

        fetch(`${url}?${new URLSearchParams(querystring)}`, { headers })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`API request failed with status ${response.status}`);
                }
                return response.json();
            })
            .then(teamData => {
                displayTeamInfo(teamName, teamData, logoUrl);
            })
            .catch(error => {
                console.error('Error fetching team data:', error);
                teamInfoBox.textContent = `Error fetching team data: ${error.message}`;
            });
    }

    // Function to display team information including logo
    function displayTeamInfo(teamName, teamData, logoUrl) {
        teamInfoBox.innerHTML = ''; // Clear previous content

        const teamInfo = document.createElement('div');
        teamInfo.classList.add('team-info');

        // Display team logo
        const logoImg = document.createElement('img');
        logoImg.src = logoUrl;
        logoImg.alt = `${teamName} Logo`;
        logoImg.style.width = '100px'; // Adjust size as needed
        teamInfo.appendChild(logoImg);

        // Display other team information
        teamInfo.innerHTML += `
            <h2>${teamName}</h2>
            <p><strong>Conference:</strong> ${teamData.response[0].conference.name}</p>
            <p><strong>Division:</strong> ${teamData.response[0].division.name}</p>
            <p><strong>Wins:</strong> ${teamData.response[0].win.total}</p>
            <p><strong>Losses:</strong> ${teamData.response[0].loss.total}</p>
            <p><strong>Last 10 Games:</strong> ${teamData.response[0].win.lastTen}-${teamData.response[0].loss.lastTen}</p>
            <p><strong>Win Percentage:</strong> ${teamData.response[0].win.percentage}</p>
            <p><strong>Streak:</strong> ${teamData.response[0].streak}</p>
        `;

        teamInfoBox.appendChild(teamInfo);
    }
});
