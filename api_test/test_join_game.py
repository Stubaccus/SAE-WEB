import requests

from utils import *


def test_join_game_1(base_url, game_path, game_id) -> bool:
    print("\t[JOIN GAME] TEST #1 : VALIDE")
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


    if d["error"] != 0:
        print(d["error_message"])
        return False

    l = ["game_id", "status", "player2", "player2_role", "player2_path"]
    expected_values = {
        "game_id": game_id,
        "status": "play",
        "player2": data["player2"],
        "player2_role": data["player2_role"],
        "player2_path": data["player2_path"]
    }

    for i in l:
        if d[i] != expected_values[i]:
            print(f'{i} différent : {d[i]} != {expected_values[i]}')
            return False
    return True

def test_join_game_2(base_url, game_path) -> bool:
    print("\t[JOIN GAME] TEST #2 : PARTIE INEXISTANTE")
    url = base_url + game_path + "join_game.php"
    data = {
        "game_id": 99999,
        "game_path": game_path,
        "player2": "Gollum",
        "player2_role": "human",
        "player2_path": game_path
    }
    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)

    d = response.json()

    if d["error"] == 0:
        print("[ERREUR] La partie n'existe pas, mais aucune erreur détectée !")
        return False

    return True

def test_join_game_3(base_url, game_path, game_id) -> bool:
    print("\t[JOIN GAME] TEST #3 : PARTIE COMPLETE")
    url = base_url + game_path + "join_game.php"
    data = {
        "game_id": game_id,
        "game_path": game_path,
        "player2": "Aragorn",
        "player2_role": "human",
        "player2_path": game_path
    }
    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)

    d = response.json()

    if d["error"] == 0:
        print("[ERREUR] La partie a déjà un joueur 2, mais aucune erreur détectée !")
        return False

    return True

def test_join_game_4(base_url, game_path) -> bool:
    print("\t[JOIN GAME] TEST #4 : PAS DE POST")
    url = base_url + game_path + "join_game.php"
    response = requests.get(url)

    if(DEBUG):
        print(response.text)
        
    d = response.json()

    if d["error"] == 0:
        print("[ERREUR] Pas d'erreur détectée alors qu'on n'a pas envoyé de POST !")
        return False

    return True


def test_join_games(base_url, game_path):
    print("[JOIN GAME] TEST START")
    game_id = create_valide_game(base_url, game_path)
    res = (test_join_game_1(base_url, game_path, game_id)
        and test_join_game_2(base_url, game_path)
        and test_join_game_3(base_url, game_path, game_id)
        and test_join_game_4(base_url, game_path))
    
    delete_game(base_url, game_path, game_id)
    if(res):
        print("[JOIN GAME] OK!")
    else:
        print("[JOIN GAME] FAIL!")


if __name__ == "__main__":
    print(BASE_URL)
    print(GAME_PATH)
    print(BASE_URL + GAME_PATH + "join_game.php")
    test_join_games(BASE_URL, GAME_PATH)
