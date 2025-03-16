import requests
from utils import *


def test_delete_game_1(base_url, game_path, game_id) -> bool:
    print(f"\t[DELETE GAME] TEST #1 : VALIDE")

    url = base_url + game_path + "delete_game.php"
    data = {"game_id": game_id, "game_path" : game_path}

    response = requests.post(url, data=data)
    d = response.json()

    if(DEBUG):
        print(response.text)

    if(d["error"] != 0):
        print(f"[ERREUR] {d['error_message']}")
        return False

    return True

def test_delete_game_2(base_url, game_path, game_id) -> bool:
    print(f"\t[DELETE GAME] TEST #2 : PAS DE POST")

    url = base_url + game_path + "delete_game.php"
    data = {"game_id": game_id, "game_path" : game_path}

    response = requests.get(url)

    if(DEBUG):
        print(response.text)
        
    d = response.json()

    if(d["error"] == 0):
        print("[ERREUR] Aucune erreur détectée alors qu'on a pas utilisé POST !")
        return False

    return True

def test_delete_game_3(base_url, game_path, game_id) -> bool:
    print(f"\t[DELETE GAME] TEST #3 : PAS DE game_path")

    url = base_url + game_path + "delete_game.php"
    data = {"game_id": game_id}

    response = requests.post(url, json=data)

    if(DEBUG):
        print(response.text)

    d = response.json()


    if(d["error"] == 0):
        print("[ERREUR] Aucune erreur détectée alors qu'une donnée est manquante !")
        return False

    return True

def test_delete_game_4(base_url, game_path) -> bool:
    print("\t[DELETE GAME] TEST #4 : PAS DE game_id")

    url = base_url + game_path + "delete_game.php"
    data = {"game_path" : game_path}

    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)
        
    d = response.json()


    if d["error"] == 0:
        print("[ERREUR] Aucune erreur détectée alors qu'aucun game_id n'a été fourni !")
        return False

    return True

def test_delete_game_5(base_url, game_path, game_id) -> bool:
    print(f"\t[DELETE GAME] TEST #5 : INVALIDE game_id")

    url = base_url + game_path + "delete_game.php"
    data = {"game_id": -5, "game_path" : game_path}

    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)

    d = response.json()

    if d["error"] == 0:
        print("[ERREUR] Aucune erreur détectée alors que le game_id est incorrect !")
        return False

    return True


def test_delete_games(base_url, game_path):
    print("[DELETE GAME] TEST START")
    game_id = create_valide_game(base_url, game_path)
    res = (test_delete_game_1(base_url, game_path, game_id)
        and test_delete_game_2(base_url, game_path, game_id)
        and test_delete_game_3(base_url, game_path, game_id)
        and test_delete_game_4(base_url, game_path)
        and test_delete_game_5(base_url, game_path, game_id))
    
    if(res):
        print("[DELETE GAME] OK!")
    else:
        print("[DELETE GAME] FAIL!")

if __name__ == "__main__":
    print(BASE_URL)
    print(GAME_PATH)
    print(BASE_URL + GAME_PATH + "delete_game.php")
    test_delete_games(BASE_URL, GAME_PATH)