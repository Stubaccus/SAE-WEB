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

$required_fields = ["game_id", "game_path", "player2", "player2_role", "player2_path"];
foreach ($required_fields as $field) {
    if (!isset($data[$field])) {
        echo json_encode(["error" => 1, "error_message" => "Données manquantes : $field"]);
        exit;
    }
}

$db = new SQLite3("puissance4.db");

$stmt = $db->prepare("SELECT * FROM games WHERE id = :game_id");
$stmt->bindValue(":game_id", $data["game_id"], SQLITE3_INTEGER);
$result = $stmt->execute();
$game = $result->fetchArray(SQLITE3_ASSOC);

if (!$game) {
    echo json_encode(["error" => 1, "error_message" => "Partie introuvable"]);
    exit;
}

if ($game["status"] !== "waiting") {
    echo json_encode(["error" => 1, "error_message" => "La partie a déjà commencé"]);
    exit;
}

$stmt = $db->prepare("UPDATE games SET player2 = :player2, player2_role = :player2_role, player2_path = :player2_path, status = 'play' WHERE id = :game_id");
$stmt->bindValue(":player2", $data["player2"], SQLITE3_TEXT);
$stmt->bindValue(":player2_role", $data["player2_role"], SQLITE3_TEXT);
$stmt->bindValue(":player2_path", $data["player2_path"], SQLITE3_TEXT);
$stmt->bindValue(":game_id", $data["game_id"], SQLITE3_INTEGER);
$result = $stmt->execute();

if ($result) {
    echo json_encode([
        "error" => 0,
        "game_id" => $data["game_id"],
        "status" => "play",
        "board" => json_decode($game["board"]),
        "player1" => $game["player1"],
        "player1_role" => $game["player1_role"],
        "player1_path" => $game["player1_path"],
        "player2" => $data["player2"],
        "player2_role" => $data["player2_role"],
        "player2_path" => $data["player2_path"],
        "player_turn" => $game["player_turn"]
    ]);
} else {
    echo json_encode(["error" => 1, "error_message" => "Erreur lors de la mise à jour de la partie"]);
}
?>
