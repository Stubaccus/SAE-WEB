# SAE-WEB
Projet sae web

les tests a faire dans le terminal pour test l'api:
# CREATE_GAME

curl -X POST http://localhost:8000/create_game.php -H "Content-Type: application/json" -d '{
  "game_name": "TestGame",
  "game_path": "server1",
  "player1": "Alice",
  "player1_role": "human",
  "player1_path": "server1"
}'

# LIST_GAMES

curl -X POST http://localhost:8000/list_games.php -H "Content-Type: application/json" -d '{
  "status": "all",
  "path": "server1"
}'

# JOIN_GAME

curl -X POST http://localhost:8000/join_game.php -H "Content-Type: application/json" -d '{
  "game_id": 1,
  "game_path": "server1",
  "player2": "Bob",
  "player2_role": "human",
  "player2_path": "server2"
}'


# GET_GAME

curl -X POST http://localhost:8000/get_game.php -H "Content-Type: application/json" -d '{
  "game_id": 1,
  "game_path": "server1",
  "player": 1
}'

# PLAY

curl -X POST http://localhost:8000/play.php -H "Content-Type: application/json" -d '{
  "game_id": 1,
  "game_path": "server1",
  "player": 1,
  "column": 3,
  "private_key": "6912ca3fdced11e537598b4d472a9e88"
}'


# DELETE_GAME

curl -X POST http://localhost:8000/delete_game.php -H "Content-Type: application/json" -d '{
  "game_id": 1,
  "game_path": "server1"
}'
