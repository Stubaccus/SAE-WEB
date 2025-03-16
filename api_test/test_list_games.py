import requests
from utils import *

def test_list_games_1(base_url, game_path) -> bool:
    print("\t[LIST GAMES] TEST #1 : VALIDE ALL")
    game_id = create_valide_game(base_url, game_path)
    url = base_url + game_path + "list_games.php"
    data = {
        "status": "all",
        "path": game_path
    }

    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)

    d = response.json()


    delete_game(base_url, game_path, game_id)
    if("error" in d and d["error"] != 0):
        print(f"[ERREUR] {d['error_message']}")
        return False

    if not any(game["game_id"] == game_id for game in d["games"]):
        print("[ERREUR] La partie créée n'est pas présente dans la liste.")
        return False

    return True

def test_list_games_2(base_url, game_path) -> bool:
    print("\t[LIST GAMES] TEST #2 : VALIDE waiting")
    game_id = create_valide_game(base_url, game_path)
    url = base_url + game_path + "list_games.php"
    data = {
        "status": "waiting",
        "path": game_path
    }

    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)

    d = response.json()

    delete_game(base_url, game_path, game_id)

    if("error" in d and d["error"] != 0):
        print(f"[ERREUR] {d['error_message']}")
        return False

    if not any(game["game_id"] == game_id for game in d["games"]):
        print("[ERREUR] La partie créée n'est pas trouvée alors qu'elle est en attente.")
        return False

    return True

def test_list_games_3(base_url, game_path) -> bool:
    print("\t[LIST GAMES] TEST #3 : VALIDE play")
    game_id = create_valide_game(base_url, game_path)
    if not join_game(base_url, game_path, game_id):
        print("[ERREUR] Impossible de rejoindre la partie pour le test.")
        return False

    url = base_url + game_path + "list_games.php"
    data = {
        "status": "play",
        "path": game_path
    }

    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)
        
    d = response.json()


    delete_game(base_url, game_path, game_id)
    if "error" in d and d["error"] != 0:
        print(f"[ERREUR] {d['error_message']}")
        return False

    if not any(game["game_id"] == game_id for game in d["games"]):
        print("[ERREUR] La partie n'est pas listée alors qu'elle est en cours.")
        return False

    return True

def test_list_games_4(base_url, game_path) -> bool:
    print("\t[LIST GAMES] TEST #4 : DONNEE MANQUANTE")

    url = base_url + game_path + "list_games.php"
    data = {
        "path": game_path
    }

    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)

    d = response.json()


    if "error" not in d or d["error"] == 0:
        print("[ERREUR] Aucune erreur détectée alors que le status est manquant !")
        return False

    return True

def test_list_games_5(base_url, game_path) -> bool:
    print("\t[LIST GAMES] TEST #5 : PAS DE POST")

    url = base_url + game_path + "list_games.php"
    response = requests.get(url)

    if(DEBUG):
        print(response.text)

    d = response.json()


    if "error" not in d or d["error"] == 0:
        print("[ERREUR] Aucune erreur détectée alors qu'on a pas utilisé POST !")
        return False

    return True

def test_list_games_6(base_url, game_path) -> bool:
    print("\t[LIST GAMES] TEST #6 : INVALIDE status")

    url = base_url + game_path + "list_games.php"
    data = {
        "status": "Aragorn",
        "path": game_path
    }

    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)
        
    d = response.json()


    if "error" not in d or d["error"] == 0:
        print("[ERREUR] Aucune erreur détectée alors que le status est invalide !")
        return False

    return True

def test_list_games(base_url, game_path):
    print("[LIST GAMES] TEST START")

    res = (test_list_games_1(base_url, game_path)
           and test_list_games_2(base_url, game_path)
           and test_list_games_3(base_url, game_path)
           and test_list_games_4(base_url, game_path)
           and test_list_games_5(base_url, game_path)
           and test_list_games_6(base_url, game_path))

    if res:
        print("[LIST GAMES] OK!")
    else:
        print("[LIST GAMES] FAIL!")


if __name__ == "__main__":
    print(BASE_URL)
    print(GAME_PATH)
    print(BASE_URL + GAME_PATH + "list_games.php")
    test_list_games(BASE_URL, GAME_PATH)