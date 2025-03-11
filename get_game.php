<?php
header("Content-Type: application/json");

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(["error" => 1, "error_message" => "Méthode non autorisée"]);
    exit;
}

$data_raw = file_get_contents("php://input");
$data = json_decode($data_raw, true);

if (!$data) {
    echo json_encode(["error" => 1, "error_message" => "JSON invalide"]);
    exit;
}

$required_fields = ["game_id", "game_path", "player"];
foreach ($required_fields as $field) {
    if (!isset($data[$field])) {
        echo json_encode(["error" => 1, "error_message" => "Données manquantes : $field"]);
        exit;
    }
}

$db = new SQLite3("puissance4.db");
$stmt = $db->prepare("SELECT * FROM games WHERE id = :game_id AND game_path = :game_path");
$stmt->bindValue(":game_id", $data["game_id"], SQLITE3_INTEGER);
$stmt->bindValue(":game_path", $data["game_path"], SQLITE3_TEXT);
$result = $stmt->execute();
$game = $result->fetchArray(SQLITE3_ASSOC);
$private_key = ($data["player"] == $game["player_turn"]) ? $game["private_key"] : null;

if (!$game) {
    echo json_encode(["error" => 1, "error_message" => "Partie introuvable"]);
    exit;
}

$last_move = isset($game["last_move"]) ? $game["last_move"] : null;

error_log("Game ID: " . $game["id"] . " - Player: " . $data["player"] . " - Private Key: " . json_encode($game["private_key"]));

echo json_encode([
    "error" => 0,
    "game_id" => $game["id"],
    "game_name" => $game["name"],
    "game_path" => $game["game_path"],
    "status" => $game["status"],
    "board" => json_decode($game["board"], true),
    "player1" => $game["player1"],
    "player1_role" => $game["player1_role"],
    "player1_path" => $game["player1_path"],
    "player2" => $game["player2"],
    "player2_role" => $game["player2_role"],
    "player2_path" => $game["player2_path"],
    "player_turn" => $game["player_turn"],
    "last_move" => $last_move,
    "private_key" => $private_key
]);
?>
