let currentGameId = null;
let currentPlayer = null;
let privateKey = null;
let isLocalServerMaster = true;

// Création d'une partie
async function createGame() {
    const gameName = document.getElementById('game_name').value;
    const playerName = prompt("Entrez votre nom:");
    
    try {
        const response = await fetch('/api/create_game.php', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                game_name: gameName,
                game_path: window.location.pathname,
                player1: playerName,
                player1_role: "human",
                player1_path: window.location.pathname
            })
        });
        
        // Vérification du contenu de la réponse
        const responseText = await response.text();
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = JSON.parse(responseText);
        
        if (data.error) {
            alert(data.error_message);
            return;
        }
        
        currentGameId = data.game_id;
        currentPlayer = 1;
        privateKey = data.private_key;
        showGameBoard();
        startGameRefresh();
    } catch (error) {
        console.error('Erreur création de partie:', error);
        alert("Erreur lors de la création de la partie. Vérifiez la console pour plus de détails.");
    }
}

// Rejoindre une partie
async function joinGame(gameId) {
    const playerName = prompt("Entrez votre nom:");
    
    try {
        const response = await fetch('/api/join_game.php', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                game_id: gameId,
                game_path: window.location.pathname,
                player2: playerName,
                player2_role: "human",
                player2_path: window.location.pathname
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
        
        currentGameId = gameId;
        currentPlayer = 2;
        privateKey = data.private_key;
        showGameBoard();
        startGameRefresh();
    } catch (error) {
        console.error('Erreur rejoindre partie:', error);
        alert("Erreur lors de la jonction à la partie. Vérifiez la console pour plus de détails.");
    }
}

// Jouer un coup
async function playMove(column) {
    if (!privateKey) {
        alert("Erreur d'authentification !");
        return;
    }
    
    try {
        const response = await fetch('/api/play.php', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                game_id: currentGameId,
                game_path: window.location.pathname,
                player: currentPlayer,
                column: column,
                private_key: privateKey
            })
        });
        
        const responseText = await response.text();
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = JSON.parse(responseText);
        
        if (data.error) {
            alert(data.error_message);
        } else {
            privateKey = data.private_key;
            await updateGameState();
            refreshGameList();
        }
    } catch (error) {
        console.error('Erreur jeu:', error);
        alert("Erreur lors du jeu. Vérifiez la console pour plus de détails.");
    }
}

// Rafraîchir la liste des parties
async function refreshGameList() {
    try {
        const response = await fetch('/api/list_games.php', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                status: "waiting",
                path: window.location.pathname
            })
        });
        
        const data = await response.json();
        const list = document.getElementById('games_list');
        list.innerHTML = '';
        
        data.games.forEach(game => {
            const li = document.createElement('li');
            li.innerHTML = `${game.game_name} (${game.player1}) - `;
            const btn = document.createElement('button');
            btn.textContent = 'Rejoindre';
            btn.onclick = () => joinGame(game.game_id);
            li.appendChild(btn);
            list.appendChild(li);
        });
    } catch (error) {
        console.error('Erreur liste parties:', error);
    }
}

// Affichage du plateau
function showGameBoard() {
    document.getElementById('game_board').style.display = 'block';
    document.querySelector('h1').scrollIntoView();
    updateGameState();
    refreshGameList();
}

// Rafraîchissement automatique
let refreshInterval;
function startGameRefresh() {
    refreshInterval = setInterval(updateGameState, 5000);
}

// Mise à jour de l'état du jeu
async function updateGameState() {
    try {
        const response = await fetch('/api/get_game.php', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                game_id: currentGameId,
                game_path: window.location.pathname,
                player: currentPlayer
            })
        });
        
        const data = await response.json();
        if (data.error) {
            alert(data.error_message);
            return;
        }
        
        renderBoard(data.board);
        updateGameControls(data);
        
        // Gestion fin de partie
        if (data.status === 'over') {
            clearInterval(refreshInterval);
            alert(data.winner ? `Joueur ${data.winner} a gagné !` : 'Match nul !');
        }
    } catch (error) {
        console.error('Erreur mise à jour:', error);
    }
}

// Rendu du plateau
function renderBoard(board) {
    const boardDiv = document.getElementById('board');
    boardDiv.innerHTML = '';

    // Conversion si nécessaire
    if (typeof board === 'string') board = JSON.parse(board);

    // Sélecteur de colonnes
    const columnSelector = document.createElement('div');
    columnSelector.className = 'column-selector';
    
    for (let c = 0; c < 7; c++) {
        const btn = document.createElement('button');
        btn.className = 'column-btn';
        btn.textContent = c + 1;
        btn.onclick = () => playMove(c);
        columnSelector.appendChild(btn);
    }
    
    boardDiv.appendChild(columnSelector);

    // Grille de jeu
    const grid = document.createElement('div');
    grid.className = 'grid';

    for (let r = 0; r < 6; r++) {
        const rowDiv = document.createElement('div');
        rowDiv.className = 'row';

        for (let c = 0; c < 7; c++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            if (board[r][c] === 1) cell.classList.add('player1');
            if (board[r][c] === 2) cell.classList.add('player2');
            rowDiv.appendChild(cell);
        }

        grid.appendChild(rowDiv);
    }

    boardDiv.appendChild(grid);
}

// Contrôles de jeu
function updateGameControls(data) {
    const buttons = document.querySelectorAll('.column-btn');
    const isPlayerTurn = (data.player_turn === currentPlayer);
    
    buttons.forEach(btn => {
        btn.disabled = !isPlayerTurn || data.status !== 'play';
    });
}


// Liste des parties
async function refreshGameList() {
    try {
        const response = await fetch('/api/list_games.php', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                status: "waiting",
                path: window.location.pathname
            })
        });
        
        const data = await response.json();
        const list = document.getElementById('games_list');
        list.innerHTML = '';
        
        data.games.forEach(game => {
            const li = document.createElement('li');
            li.innerHTML = `${game.game_name} (${game.player1}) - `;
            const btn = document.createElement('button');
            btn.textContent = 'Rejoindre';
            btn.onclick = () => joinGame(game.game_id);
            li.appendChild(btn);
            list.appendChild(li);
        });
    } catch (error) {
        console.error('Erreur liste parties:', error);
    }
}

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    refreshGameList();
    setInterval(refreshGameList, 5000);
});