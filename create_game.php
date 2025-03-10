<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

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

$required_fields = ["game_name", "game_path", "player1", "player1_role", "player1_path"];
foreach ($required_fields as $field) {
    if (!isset($data[$field])) {
        echo json_encode(["error" => 1, "error_message" => "Données manquantes : $field"]);
        exit;
    }
}

$player2 = $data["player2"] ?? "";
$player2_role = $data["player2_role"] ?? "";
$player2_path = $data["player2_path"] ?? "";
$status = ($player2 !== "") ? "play" : "waiting";

function generatePrivateKey() {
    return bin2hex(random_bytes(16));
}
$private_key_p1 = generatePrivateKey();
$private_key_p2 = generatePrivateKey();

$db = new SQLite3("puissance4.db");
$empty_board = json_encode(array_fill(0, 6, array_fill(0, 7, 0)));

$stmt = $db->prepare("INSERT INTO games (name, game_path, player1, player1_role, player1_path, player2, player2_role, player2_path, board, status, player_turn) VALUES (:name, :game_path, :player1, :player1_role, :player1_path, :player2, :player2_role, :player2_path, :board, :status, 1)");

$stmt->bindValue(":name", $data["game_name"], SQLITE3_TEXT);
$stmt->bindValue(":game_path", $data["game_path"], SQLITE3_TEXT);
$stmt->bindValue(":player1", $data["player1"], SQLITE3_TEXT);
$stmt->bindValue(":player1_role", $data["player1_role"], SQLITE3_TEXT);
$stmt->bindValue(":player1_path", $data["player1_path"], SQLITE3_TEXT);
$stmt->bindValue(":player2", $player2, SQLITE3_TEXT);
$stmt->bindValue(":player2_role", $player2_role, SQLITE3_TEXT);
$stmt->bindValue(":player2_path", $player2_path, SQLITE3_TEXT);
$stmt->bindValue(":board", $empty_board, SQLITE3_TEXT);
$stmt->bindValue(":status", $status, SQLITE3_TEXT);

if (!$stmt->execute()) {
    echo json_encode(["error" => 1, "error_message" => "Erreur lors de la création de la partie"]);
    exit;
}

$game_id = $db->lastInsertRowID();
$stmt = $db->prepare("INSERT INTO players (game_id, player_name, private_key) VALUES (:game_id, :player1, :private_key_p1), (:game_id, :player2, :private_key_p2)");
$stmt->bindValue(":game_id", $game_id, SQLITE3_INTEGER);
$stmt->bindValue(":player1", $data["player1"], SQLITE3_TEXT);
$stmt->bindValue(":private_key_p1", $private_key_p1, SQLITE3_TEXT);
$stmt->bindValue(":player2", $player2, SQLITE3_TEXT);
$stmt->bindValue(":private_key_p2", $private_key_p2, SQLITE3_TEXT);
$stmt->execute();

echo json_encode([
    "error" => 0,
    "game_id" => $game_id,
    "game_name" => $data["game_name"],
    "game_path" => $data["game_path"],
    "status" => $status,
    "board" => json_decode($empty_board),
    "player1" => $data["player1"],
    "player1_role" => $data["player1_role"],
    "player1_path" => $data["player1_path"],
    "player2" => $player2,
    "player2_role" => $player2_role,
    "player2_path" => $player2_path,
    "player_turn" => 1
]);
?>
