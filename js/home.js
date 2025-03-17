document.addEventListener('DOMContentLoaded', () => {
    refreshGameList();
    setInterval(refreshGameList, 5000);
});

async function refreshGameList() {
    try {
        const response = await fetch('../api/list_games.php', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                status: "waiting", 
                path: '/api/'
            })
        });
        
        const data = await response.json();
        console.log("Réponse de list_games.php :", data);

        const list = document.getElementById('games_list');
        if (!list) {
            console.error("L'élément 'games_list' est introuvable dans le DOM.");
            return;
        }

        list.innerHTML = '';
        
        if (data.games && data.games.length > 0) {
            data.games.forEach(game => {
                const li = document.createElement('li');
                li.innerHTML = `${game.game_name} (${game.player1}) - `;
                const btn = document.createElement('button');
                btn.textContent = 'Rejoindre';
                btn.onclick = () => joinGame(game.game_id);
                li.appendChild(btn);
                list.appendChild(li);
            });
        } else {
            list.innerHTML = '<li>Aucune partie disponible</li>';
        }
    } catch (error) {
        console.error('Erreur lors de la récupération de la liste des parties:', error);
    }
}

async function joinGame(gameId) {
    const playerName = prompt("Entrez votre nom:");
    if (!playerName) {
        alert("Vous devez entrer un nom pour rejoindre une partie.");
        return;
    }
    
    try {
        const response = await fetch('../api/join_game.php', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                game_id: gameId, 
                game_path: '/api/',
                player2: playerName,
                player2_role: "human", 
                player2_path: '/api/' 
            })
        });
        
        const responseText = await response.text();
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = JSON.parse(responseText);
        
        if (data.error) {
            alert(data.error_message);
            return;
        }
        
        localStorage.setItem('currentGameId', gameId);
        localStorage.setItem('currentPlayer', 2);
        localStorage.setItem('privateKey', data.private_key);

        window.location.href = 'game.html';
    } catch (error) {
        console.error('Erreur lors de la jonction à la partie:', error);
        alert("Erreur lors de la jonction à la partie. Vérifiez la console pour plus de détails.");
    }
}