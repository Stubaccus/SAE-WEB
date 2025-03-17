let currentGameId = null;
let currentPlayer = null;
let privateKey = null;


document.addEventListener('DOMContentLoaded', () => {
    currentGameId = localStorage.getItem('currentGameId');
    currentPlayer = localStorage.getItem('currentPlayer');
    privateKey = localStorage.getItem('privateKey');

    if (!currentGameId || !currentPlayer || !privateKey) {
        alert("Aucune partie en cours. Veuillez créer ou rejoindre une partie.");
        window.location.href = 'index.html';
        return;
    }

    startGameRefresh();
});

async function playMove(column) {
    // if (!privateKey) {
    //     alert("Erreur d'authentification !");
    //     return;
    // }
    
    try {
        const response = await fetch('../api/play.php', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                game_id: currentGameId,
                game_path: '/api/',
                player: parseInt(currentPlayer),
                column: column
            })
        });
        console.log("Données envoyées à play.php :", {
            game_id: currentGameId,
            game_path: '/api/',
            player: currentPlayer,
            column: column
        });
        
        const data = await response.json();
        
        // if (data.error !== 1) {
        //     alert(data.error_message);
        // } else {
            // privateKey = data.private_key;
            // localStorage.setItem('privateKey', privateKey);
            await updateGameState();
        // }
    } catch (error) {
        console.error('Erreur lors du jeu:', error);
        alert("Erreur lors du jeu. Vérifiez la console pour plus de détails.");
    }
}

async function updateGameState() {
    try {
        const requestData = {
            game_id: currentGameId,
            game_path: '/api/',
            player: currentPlayer
        };
        console.log("Données envoyées à get_game.php :", requestData);

        const response = await fetch('../api/get_game.php', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(requestData)
        });
        
        const data = await response.json();
        console.log("Réponse de get_game.php :", data); // Affichez la réponse

        if (data.error) {
            alert(data.error_message);
            return;
        }
        
        renderBoard(data.board);
        updateGameControls(data);
        
        if (data.status === 'over') {
            clearInterval(refreshInterval);
            alert(data.winner ? `Joueur ${data.winner} a gagné !` : 'victoire !');
        }
    } catch (error) {
        console.error('Erreur lors de la mise à jour du jeu:', error);
    }
}

function renderBoard(board) {
    const boardDiv = document.getElementById('board');
    if (!boardDiv) {
        console.error("L'élément 'board' est introuvable dans le DOM.");
        return;
    }

    // Vide le plateau avant de le remplir
    boardDiv.innerHTML = '';

    if (typeof board === 'string') {
        board = JSON.parse(board);
    }

    const columnSelector = document.createElement('div');
    columnSelector.className = 'column-selector';
    
    for (let c = 0; c < 7; c++) {
        var btn = document.createElement('button');
        console.log(btn);
        btn.className = 'column-btn';
        btn.textContent = c + 1; // Affiche le numéro de la colonne
        (function(columnIndex) {
            btn.addEventListener("click", function (event) {
                console.log("testons");
                playMove(columnIndex);
            });
        })(c); // Associe la fonction playMove au clic
        columnSelector.appendChild(btn);
    }
    
    boardDiv.appendChild(columnSelector);

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

function updateGameControls(data) {
    const buttons = document.querySelectorAll('.column-btn');
    const isPlayerTurn = (data.player_turn == currentPlayer);
    
    buttons.forEach(btn => {
        btn.disabled = !isPlayerTurn || data.status !== 'play';
    });
}

let refreshInterval;
function startGameRefresh() {
    refreshInterval = setInterval(updateGameState, 1500);
}