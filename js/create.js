document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('create-game-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const gameName = document.getElementById('game-name').value;
        const playerName = document.getElementById('player-name').value;
        const player1Role = document.getElementById('player1-role').value;
        const player2Type = document.getElementById('player2-type').value;
        const targetApi = document.getElementById('target-api').value;

        try {
            const response = await fetch('../api/create_game.php', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    game_name: gameName,
                    game_path: 'api/',
                    player1: playerName,
                    player1_role: player1Role,
                    player1_path: 'api/',
                    player2: "",
                    player2_role: player2Type,
                    player2_path: ""
                })
            });
            
            const responseText = await response.text();
            console.log("test: " + response);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = JSON.parse(responseText);
            
            if (data.error) {
                alert(data.error_message);
                return;
            }
            
            localStorage.setItem('currentGameId', data.game_id);
            localStorage.setItem('currentPlayer', 1); // Joueur 1
            localStorage.setItem('privateKey', data.private_key);

            window.location.href = 'game.html';
        } catch (error) {
            console.error('Erreur création de partie:', error);
            alert("Erreur lors de la création de la partie. Vérifiez la console pour plus de détails.");
        }
    });
});