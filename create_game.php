<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

header("Content-Type: application/json");

// Vérifie que la méthode est bien POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(["error" => 1, "error_message" => "Méthode non autorisée"]);
    exit;
}

// Récupération et log des données brutes
$data_raw = file_get_contents("php://input");
file_put_contents("debug.log", "Données brutes reçues : " . $data_raw . "\n", FILE_APPEND);

// Vérification si JSON est valide
$data = json_decode($data_raw, true);
if (!$data) {
    echo json_encode(["error" => 1, "error_message" => "JSON invalide"]);
    exit;
}

// Vérification des champs obligatoires
$required_fields = ["game_name", "game_path", "player1", "player1_role", "player1_path", "player2", "player2_role", "player2_path"];
foreach ($required_fields as $field) {
    if (!isset($data[$field])) {
        echo json_encode(["error" => 1, "error_message" => "Données manquantes : $field"]);
        exit;
    }
}

// Initialisation de la base de données
$db = new SQLite3("puissance4.db");

// Génération d'un plateau vide
$empty_board = json_encode([
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0]
]);

// Préparation de l'insertion dans la base de données
$stmt = $db->prepare("
    INSERT INTO games (name, game_path, player1, player1_role, player1_path, player2, player2_role, player2_path, board, status, player_turn) 
    VALUES (:name, :game_path, :player1, :player1_role, :player1_path, :player2, :player2_role, :player2_path, :board, 'waiting', 1)
");

$stmt->bindValue(":name", $data["game_name"], SQLITE3_TEXT);
$stmt->bindValue(":game_path", $data["game_path"], SQLITE3_TEXT);
$stmt->bindValue(":player1", $data["player1"], SQLITE3_TEXT);
$stmt->bindValue(":player1_role", $data["player1_role"], SQLITE3_TEXT);
$stmt->bindValue(":player1_path", $data["player1_path"], SQLITE3_TEXT);
$stmt->bindValue(":player2", $data["player2"], SQLITE3_TEXT);
$stmt->bindValue(":player2_role", $data["player2_role"], SQLITE3_TEXT);
$stmt->bindValue(":player2_path", $data["player2_path"], SQLITE3_TEXT);
$stmt->bindValue(":board", $empty_board, SQLITE3_TEXT);

$result = $stmt->execute();

// Vérification de l'insertion en base
if ($result) {
    $game_id = $db->lastInsertRowID();
    echo json_encode([
        "error" => 0,
        "game_id" => $game_id,
        "game_name" => $data["game_name"],
        "game_path" => $data["game_path"],
        "status" => "waiting",
        "board" => json_decode($empty_board),
        "player1" => $data["player1"],
        "player1_role" => $data["player1_role"],
        "player1_path" => $data["player1_path"],
        "player2" => $data["player2"],
        "player2_role" => $data["player2_role"],
        "player2_path" => $data["player2_path"],
        "player_turn" => 1,
        "private_key" => null
    ]);
} else {
    echo json_encode(["error" => 1, "error_message" => "Erreur lors de la création de la partie"]);
}
?>
