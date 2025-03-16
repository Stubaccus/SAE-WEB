import requests
from utils import *

def test_create_game_2(base_url, game_path) -> bool:
    print("\t[CREATE GAME] TEST #2 : VALIDE")
    url = base_url + game_path + "create_game.php"
    data = {
        "game_name": "Mordor",
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
        print(d["error_message"])
        return False

    l = ["game_name", "game_path", "player1", "player1_role", "player1_path", "player2", "player2_path", "player2_role"]
    for i in l:
        if(d[i] != data[i]):
            print(f'{i} different : {d[i]} != {data[i]}')
            return False
    delete_game(base_url, game_path, d["game_id"])
    return True

def test_create_game_4(base_url, game_path) -> bool:
    print("\t[CREATE GAME] TEST #4 : VALIDE + player2_role")
    url = base_url + game_path + "create_game.php"
    data = {
        "game_name": "Mordor",
        "game_path": game_path,
        "player1": "Sauron",
        "player1_role": "human",
        "player1_path": game_path,
        "player2": "",
        "player2_role": "AI",
        "player2_path": ""
    }
    response = requests.post(url, data=data)
    
    if(DEBUG):
        print(response.text)
    
    d = response.json()



    if(d["error"] != 0):
        print(d["error_message"])
        return False

    l = ["game_name", "game_path", "player1", "player1_role", "player1_path", "player2", "player2_path", "player2_role"]
    for i in l:
        if(d[i] != data[i]):
            print(f'{i} different : {d[i]} != {data[i]}')
            return False
    delete_game(base_url, game_path, d["game_id"])
    return True

def test_create_game_5(base_url, game_path) -> bool:
    print("\t[CREATE GAME] TEST #5 : INVALIDE player2_role")
    url = base_url + game_path + "create_game.php"
    data = {
        "game_name": "Mordor",
        "game_path": game_path,
        "player1": "Sauron",
        "player1_role": "human",
        "player1_path": game_path,
        "player2": "",
        "player2_role": "Un truc",
        "player2_path": ""
    }
    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)

    d = response.json()

    

    if(d["error"] == 0):
        print("[ERREUR] Aucune erreur détectée alors que player2_role est invalide !")
        return False

    return True

def test_create_game_3(base_url, game_path) -> bool:
    print("\t[CREATE GAME] TEST #3 : MANQUE DE DONNEE")
    url = base_url + game_path + "create_game.php"
    data = {
        "game_name": "Mordor",
        "game_path": game_path,
        "player1": "Sauron",
        "player1_role": "human",
        "player1_path": game_path,
        "player2": "",
        "player2_role": ""
    }
    response = requests.post(url, data=data)

    if(DEBUG):
        print(response.text)
    
    d = response.json()



    if(d["error"] == 0):
        print("[ERREUR] Aucune erreur détectée alors qu'une donnée est manquante !")
        return False

    return True

def test_create_game_1(base_url, game_path) -> bool:
    print("\t[CREATE GAME] TEST #1 : PAS DE POST")
    url = base_url + game_path + "create_game.php"
    data = {
        "game_name": "Mordor",
        "game_path": game_path,
        "player1": "Sauron",
        "player1_role": "human",
        "player1_path": game_path,
        "player2": "",
        "player2_role": ""
    }
    response = requests.get(url)

    if(DEBUG):
        print(response.text)
    
    d = response.json()



    if(d["error"] == 0):
        print("[ERREUR] Aucune erreur détectée alors qu'on a pas utilisé POST !")
        return False

    return True


def test_create_games(base_url, game_path):
    print("[CREATE GAME] TEST START")
    res = (test_create_game_1(base_url, game_path)
       and test_create_game_2(base_url, game_path)
       and test_create_game_3(base_url, game_path)
       and test_create_game_4(base_url, game_path)
       and test_create_game_5(base_url, game_path))
    
    if(res):
        print("[CREATE GAME] OK!")
    else:
        print("[CREATE GAME] FAIL!")

if __name__ == "__main__":
    print(BASE_URL)
    print(GAME_PATH)
    print(BASE_URL + GAME_PATH + "create_game.php")
    test_create_games(BASE_URL, GAME_PATH)