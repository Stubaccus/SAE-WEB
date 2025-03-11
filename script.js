let currentGameId = null;
let currentPlayer = null;
let privateKey = null;
let isLocalServerMaster = true; // À adapter selon la configuration

// Création d'une partie
async function createGame() {
    const gameName = document.getElementById('game_name').value;
    const playerName = prompt("Entrez votre nom:");
    
    const response = await fetch('create_game.php', {
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
    
    const data = await response.json();
    if (data.error) {
        alert(data.error_message);
        return;
    }
    
    currentGameId = data.game_id;
    currentPlayer = 1;
    privateKey = data.private_key;
    showGameBoard();
    startGameRefresh();
}

// Rejoindre une partie
async function joinGame(gameId) {
    const playerName = prompt("Entrez votre nom:");
    
    const response = await fetch('join_game.php', {
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
    
    const data = await response.json();
    if (data.error) {
        alert(data.error_message);
        return;
    }
    
    currentGameId = gameId;
    currentPlayer = 2;
    showGameBoard();
    startGameRefresh();
}

// Affichage du plateau
function showGameBoard() {
    document.getElementById('game_board').style.display = 'block';
    document.querySelector('h1').scrollIntoView();
    updateGameState();
    
    // Force le rafraîchissement immédiat
    refreshGameList();
    updateGameState();
}

// Rafraîchissement automatique
let refreshInterval;
function startGameRefresh() {
    refreshInterval = setInterval(updateGameState, 5000);
}

// Mise à jour de l'état du jeu
async function updateGameState() {
    const response = await fetch('get_game.php', {
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
}

// Rendu du plateau
function renderBoard(board) {
    const boardDiv = document.getElementById('board');
    boardDiv.innerHTML = '';
    
    // Création des colonnes cliquables
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
    
    // Création des cellules
    for (let r = 0; r < 6; r++) {
        for (let c = 0; c < 7; c++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            if (board[r][c] === 1) cell.classList.add('player1');
            if (board[r][c] === 2) cell.classList.add('player2');
            boardDiv.appendChild(cell);
        }
    }
}

// Jouer un coup
async function playMove(column) {
    const response = await fetch('play.php', {
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
    
    const data = await response.json();
    if (data.error) {
        alert(data.error_message);
    } else {
        privateKey = data.private_key;
        updateGameState();
    }
}

// Liste des parties
async function refreshGameList() {
    const response = await fetch('list_games.php', {
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
}

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    refreshGameList();
    setInterval(refreshGameList, 5000);
});