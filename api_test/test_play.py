import requests
import json

from utils import *

def test_play_1(base_url, game_path, game_id) -> bool:
    print("\t[PLAY] TEST #1 : VALIDE")
    url = base_url + game_path + "play.php"
    game = get_game(base_url, game_path, game_id, 1)
    data = {
        "game_id": game_id,
        "game_path": game_path,
        "player": 1,
        "column" : 5,
        "private_key": game["private_key"]
    }
    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)

    d = response.json()

    if(d["error"] != 0):
        print(d["error_message"])
        return False
    d["board"] = json.loads(d["board"])
    if(d["board"][5][5] != 1):
        print("[ERREUR] Coup non enregistré correctement sur le plateau.")
        return False

    return True

def test_play_2(base_url, game_path, game_id) -> bool:
    print("\t[PLAY] TEST #2 : INVALIDE HORS TOUR")
    url = base_url + game_path + "play.php"
    game = get_game(base_url, game_path, game_id, 1)
    data = {
        "game_id": game_id,
        "game_path": game_path,
        "player": (game["player_turn"]&1)+1,
        "column" : 5,
        "private_key": game["private_key"]
    }
    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)


    d = response.json()

    if(d["error"] == 0):
        print("[ERREUR] Aucune erreur détectée alors que ce n'est pas au tour du joueur 1 !")
        return False
    
    return True

def test_play_3(base_url, game_path, game_id) -> bool:
    print("\t[PLAY] TEST #3 : INVALIDE PRIVATE KEY")
    url = base_url + game_path + "play.php"
    game = get_game(base_url, game_path, game_id)
    data = {
        "game_id": game_id,
        "game_path": game_path,
        "player": game["player_turn"],
        "column" : 5,
        "private_key": game["private_key"]+"a"
    }
    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)

    d = response.json()

    if(d["error"] == 0):
        print("[ERREUR] Aucune erreur détectée alors que la clé n'est pas valide")
        return False
    
    return True

def test_play_4(base_url, game_path, game_id) -> bool:
    print("\t[PLAY] TEST #4 : INVALIDE Colonne < 0")
    url = base_url + game_path + "play.php"
    game = get_game(base_url, game_path, game_id, 1)
    data = {
        "game_id": game_id,
        "game_path": game_path,
        "player": game["player_turn"],
        "column" : -1,
        "private_key": game["private_key"]
    }
    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)

    d = response.json()


    if(d["error"] == 0):
        print("[ERREUR] Aucune erreur détectée alors que la colonne est incorrecte.")
        return False
    
    return True

def test_play_5(base_url, game_path, game_id) -> bool:
    print("\t[PLAY] TEST #5 : INVALIDE Colonne > 7")
    url = base_url+ game_path + "play.php"
    game = get_game(base_url, game_path, game_id)
    data = {
        "game_id": game_id,
        "game_path": game_path,
        "player": game["player_turn"],
        "column" : 8,
        "private_key": game["private_key"]
    }
    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)

    d = response.json()

    if(d["error"] == 0):
        print("[ERREUR] Aucune erreur détectée alors que la colonne est incorrecte !")
        return False
    
    return True

def test_play_6(base_url, game_path) -> bool:
    print("\t[PLAY] TEST #6 : INVALIDE Colonne Pleine")
    game_id = create_valide_game(base_url, game_path)
    join_game(base_url, game_path, game_id)
    url = base_url + game_path + "play.php"
    game = get_game(base_url, game_path, game_id)
    data = {
        "game_id": game_id,
        "game_path": game_path,
        "player": game["player_turn"],
        "column" : 5,
        "private_key": game["private_key"]
    }
    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)


    d = response.json()

    for _ in range(8):
        game = get_game(base_url, game_path, game_id)
        data = {
            "game_id": game_id,
            "game_path": game_path,
            "player": game["player_turn"],
            "column" : 5,
            "private_key": game["private_key"]
        }
        response = requests.post(url, data=data)
        d = response.json()
    delete_game(base_url, game_path, game_id)
    if(d["error"] == 0):
        print("[ERREUR] Aucune erreur détectée alors que la colonne est pleine.")
        print(d["board"])
        return False
    
    return True

def test_play_7(base_url, game_path) -> bool:
    print("\t[PLAY] TEST #7 : VALIDE + winner")
    game_id = create_valide_game(base_url, game_path)
    join_game(base_url, game_path, game_id)
    url = base_url + game_path + "play.php"
    
    d = {}
    for _ in range(7):
        game = get_game(base_url, game_path, game_id)
        column = 0
        if(game["player_turn"] == 1):
            column = 2
        else:
            column = 3
        data = {
            "game_id": game_id,
            "game_path": game_path,
            "player": game["player_turn"],
            "column" : column,
            "private_key": game["private_key"]
        }
        response = requests.post(url, data=data)
        
        if(DEBUG):
            print(response.text)

        d = response.json()
            
        if(d["error"] != 0):
            print(d["error_message"])
            return False
    delete_game(base_url, game_path, game_id)
    if(d["winner"] != 1):
        print("[ERREUR] Vainqueur Incorrect")
        print(d["board"])
        return False
    # print(d)
    return True

def test_play_8(base_url, game_path, game_id) -> bool:
    print("\t[PLAY] TEST #8 : PAS DE POST")
    url = base_url + game_path + "play.php"
    response = requests.get(url)

    if(DEBUG):
        print(response.text)

    d = response.json()

    if(d["error"] == 0):
        print("[ERREUR] Aucune erreur détectée alors qu'on a pas utilisé POST !")
        return False
    
    return True

def test_play_9(base_url, game_path, game_id) -> bool:
    print("\t[PLAY] TEST #9 : DONNEE MANQUANTE")
    url = base_url + game_path + "play.php"
    game = get_game(base_url, game_path, game_id, 1)
    data = {
        "game_path": game_path,
        "player": (game["player_turn"]&1)+1,
        "column" : 5,
        "private_key": game["private_key"]
    }
    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)
        
    d = response.json()

    if(d["error"] == 0):
        print("[ERREUR] Aucune erreur détectée alors que la game_id est manquante !")
        return False
    
    return True

def test_play(base_url, game_path):
    print("[PLAY] TEST START")
    game_id = create_valide_game(base_url, game_path)
    join_game(base_url, game_path, game_id)
    res = (test_play_1(base_url, game_path, game_id)
        and test_play_2(base_url, game_path, game_id)
        and test_play_3(base_url, game_path, game_id)
        and test_play_4(base_url, game_path, game_id)
        and test_play_5(base_url, game_path, game_id)
        and test_play_6(base_url, game_path)
        and test_play_7(base_url, game_path)
        and test_play_8(base_url, game_path, game_id)
        and test_play_9(base_url, game_path, game_id))
    
    delete_game(base_url, game_path, game_id)
    if(res):
        print("[PLAY] OK!")
    else:
        print("[PLAY] FAIL!")


if __name__ == "__main__":
    print(BASE_URL)
    print(GAME_PATH)
    print(BASE_URL + GAME_PATH + "play.php")
    test_play(BASE_URL, GAME_PATH)