import requests

from config import *

def create_valide_game(base_url, game_path) -> int:
    url = base_url + game_path + "create_game.php"
    data = {
        "game_name": "Mordor Valide GAME",
        "game_path": game_path,
        "player1": "Sauron",
        "player1_role": "human",
        "player1_path": game_path,
        "player2": "",
        "player2_role": "",
        "player2_path": ""
    }
    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)

    d = response.json()

    if(d["error"] != 0):
        print(d)
        print(d["error_message"])
        return 0
    # print("[INFO] Partie créée avec succès.")
    return d["game_id"]

def delete_game(base_url, game_path, game_id) -> bool:
    url = base_url + game_path + "delete_game.php"
    data = {"game_id": game_id, "game_path" : game_path}

    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)

    d = response.json()

    if(d["error"] != 0):
        print(f"[ERREUR] {d['error_message']}")
        return False

    # print("[INFO] Partie supprimée avec succès.")
    return True

def join_game(base_url, game_path, game_id) -> bool:
    url = base_url + game_path + "join_game.php"
    data = {
        "game_id": game_id,
        "game_path": game_path,
        "player2": "Gandalf",
        "player2_role": "human",
        "player2_path": game_path
    }
    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)

    d = response.json()

    if(d["error"] != 0):
        print(d["error_message"])
        return False
    
    return True

def get_game(base_url, game_path, game_id, player=0) -> dict:
    if(player == 0):
        player = get_game(base_url, game_path, game_id, 1)["player_turn"]
    url = base_url + game_path + "get_game.php"
    data = {"game_id": game_id, "game_path" : game_path, "player" : player}

    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)

    d = response.json()

    if d["error"] != 0:
        print(f"[ERREUR] {d['error_message']}")
        return False

    return d

def list_all_games(base_url, game_path):
    url = base_url + game_path + "list_games.php"
    data = {
        "status": "all",
        "path": game_path
    }

    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)

    d = response.json()
    return d