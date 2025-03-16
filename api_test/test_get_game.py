import requests
from utils import *


def test_get_game_1(base_url, game_path, game_id) -> bool:
    print(f"\t[GET GAME] TEST #1 : VALIDE")

    url = base_url + game_path + "get_game.php"
    data = {"game_id": game_id, "game_path" : game_path, "player" : 2}

    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)

    d = response.json()


    if d["error"] != 0:
        print(f"[ERREUR] {d['error_message']}")
        return False

    expected_values = {
        "game_id": game_id,
        "game_name": "Mordor Valide GAME",
        "game_path" : game_path,
        "status": "waiting",
        "player1": "Sauron",
        "player1_role": "human",
        "player1_path": game_path,
        "player2": "Gandalf",
        "player2_role": "human",
        "player2_path": game_path,
        "player_turn" : 1,
        "private_key" : ""
    }

    l = ["game_name", "game_path", "player1", "player1_role", "player1_path", "player2", "player2_path", "player2_role"]
    
    for i in l:
        if d[i] != expected_values[i]:
            print(f'{i} différent : {d[i]} != {expected_values[i]}')
            return False
        
    if("last_move" not in d):
        print(d)
        print("[ERREUR] LAST_MOVE Absent !")
        return False

    return True

def test_get_game_6(base_url, game_path, game_id) -> bool:
    print(f"\t[GET GAME] TEST #6 : VALIDE + private_key test")

    url = base_url + game_path + "get_game.php"
    data = {"game_id": game_id, "game_path" : game_path, "player" : 1}

    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)

    d = response.json()


    if(d["error"] != 0):
        print(f"[ERREUR] {d['error_message']}")
        return False

    expected_values = {
        "game_id": game_id,
        "game_name": "Mordor Valide GAME",
        "game_path" : game_path,
        "status": "waiting",
        "player1": "Sauron",
        "player1_role": "human",
        "player1_path": game_path,
        "player2": "Gandalf",
        "player2_role": "human",
        "player2_path": game_path,
        "player_turn" : 1
    }

    l = ["game_name", "game_path", "player1", "player1_role", "player1_path", "player2", "player2_path", "player2_role"]
    
    for i in l:
        if d[i] != expected_values[i]:
            print(f'{i} différent : {d[i]} != {expected_values[i]}')
            return False

    if(d["private_key"] is None or len(d["private_key"]) == 0):
        print(d)
        print("[ERREUR] private_key non générée !")
        return False
    
    if("last_move" not in d):
        print(d)
        print("[ERREUR] LAST_MOVE Absent !")
        return False

    return True

def test_get_game_2(base_url, game_path, game_id) -> bool:
    print(f"\t[GET GAME] TEST #2 : INVALIDE game_id")

    url = base_url + game_path + "get_game.php"
    data = {"game_id": -2, "game_path" : game_path, "player" : 2}

    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)

    d = response.json()


    if(d["error"] == 0):
        print(f"[ERREUR] La partie n'existe pas, mais aucune erreur détectée !")
        return False

    return True

def test_get_game_3(base_url, game_path, game_id) -> bool:
    print(f"\t[GET GAME] TEST #3 : PAS DE POST")

    url = base_url + game_path + "get_game.php"

    response = requests.get(url)

    if(DEBUG):
        print(response.text)


    d = response.json()

    if(d["error"] == 0):
        print(f"[ERREUR] Aucune erreur détectée alors qu'on a pas utilisé POST !")
        return False

    return True

def test_get_game_4(base_url, game_path, game_id) -> bool:
    print(f"\t[GET GAME] TEST #4 : DONNEE MANQUANTE")

    url = base_url + game_path + "get_game.php"
    data = {"game_path" : game_path, "player" : 2}

    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)


    d = response.json()


    if(d["error"] == 0):
        print(f"[ERREUR] Aucune erreur détectée alors qu'une donnée est manquante !")
        return False

    return True

def test_get_game_5(base_url, game_path, game_id) -> bool:
    print(f"\t[GET GAME] TEST #5 : INVALIDE player")
    url = base_url + game_path + "get_game.php"
    data = {"game_id": game_id, "game_path" : game_path, "player" : 6}

    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)
        
    d = response.json()

    if(d["error"] == 0):
        print(f"[ERREUR] Aucune erreur détectée alors que l'indice du joueur n'est pas bon !")
        return True

    return True



def test_get_games(base_url, game_path):
    """ Lancer tous les tests pour get_game """
    print("[GET GAME] TEST START")
    game_id = create_valide_game(base_url, game_path)
    join_game(base_url, game_path, game_id)
    
    res = (test_get_game_1(base_url, game_path, game_id)
           and test_get_game_2(base_url, game_path, game_id)
           and test_get_game_3(base_url, game_path, game_id)
           and test_get_game_4(base_url, game_path, game_id)
        #    and test_get_game_5(base_url, game_id)
           and test_get_game_6(base_url, game_path, game_id))
    
    delete_game(base_url, game_path, game_id)

    if(res):
        print("[GET GAME] OK!")
    else:
        print("[GET GAME] FAIL!")

if __name__ == "__main__":
    print(BASE_URL)
    print(GAME_PATH)
    print(BASE_URL + GAME_PATH + "get_game.php")
    test_get_games(BASE_URL, GAME_PATH)
