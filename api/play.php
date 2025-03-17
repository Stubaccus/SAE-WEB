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

$required_fields = ["game_id", "game_path", "player", "column"];
foreach ($required_fields as $field) {
    if (!isset($data[$field])) {
        echo json_encode(["error" => 1, "error_message" => "Données manquantes : $field"]);
        exit;
    }
}

$db = new SQLite3("../db/puissance4.db");
$stmt = $db->prepare("SELECT * FROM games WHERE id = :game_id AND game_path = :game_path");
$stmt->bindValue(":game_id", $data["game_id"], SQLITE3_INTEGER);
$stmt->bindValue(":game_path", $data["game_path"], SQLITE3_TEXT);
$result = $stmt->execute();
$game = $result->fetchArray(SQLITE3_ASSOC);

if (!$game) {
    echo json_encode(["error" => 1, "error_message" => "Partie introuvable"]);
    exit;
}
error_log("Plateau avant le coup : " . print_r($board, true));
if ($data["player"] != $game["player_turn"] || $data["private_key"] !== $game["private_key"]) {
    echo json_encode(["error" => 1, "error_message" => "Action non autorisée"]);
    exit;
}

$board = json_decode($game["board"], true);
$column = $data["column"];
if ($column < 0 || $column > 6 || $board[0][$column] != 0) {
    echo json_encode(["error" => 1, "error_message" => "Colonne invalide ou pleine"]);
    exit;
}

for ($row = 5; $row >= 0; $row--) {
    if ($board[$row][$column] == 0) {
        $board[$row][$column] = $data["player"];
        break;
    }
}
error_log("Plateau après le coup : " . print_r($board, true));
function check_winner($board, $player) {
    for ($r = 0; $r < 6; $r++) {
        for ($c = 0; $c < 7; $c++) {
            if ($c + 3 < 7 && $board[$r][$c] == $player && $board[$r][$c+1] == $player && $board[$r][$c+2] == $player && $board[$r][$c+3] == $player) return true;
            if ($r + 3 < 6 && $board[$r][$c] == $player && $board[$r+1][$c] == $player && $board[$r+2][$c] == $player && $board[$r+3][$c] == $player) return true;
            if ($r + 3 < 6 && $c + 3 < 7 && $board[$r][$c] == $player && $board[$r+1][$c+1] == $player && $board[$r+2][$c+2] == $player && $board[$r+3][$c+3] == $player) return true;
            if ($r - 3 >= 0 && $c + 3 < 7 && $board[$r][$c] == $player && $board[$r-1][$c+1] == $player && $board[$r-2][$c+2] == $player && $board[$r-3][$c+3] == $player) return true;
        }
    }
    return false;
}

$winner = check_winner($board, $data["player"]);
$status = $winner ? "over" : "play";
$next_player = $winner ? $data["player"] : ($data["player"] == 1 ? 2 : 1);

$new_private_key = bin2hex(random_bytes(16)); // Générer une nouvelle clé privée pour le joueur suivant

$stmt = $db->prepare("UPDATE games SET board = :board, status = :status, player_turn = :next_player, last_move = :column, private_key = :private_key WHERE id = :game_id");
$stmt->bindValue(":board", json_encode($board), SQLITE3_TEXT);
$stmt->bindValue(":status", $status, SQLITE3_TEXT);
$stmt->bindValue(":next_player", $next_player, SQLITE3_INTEGER);
$stmt->bindValue(":column", $column, SQLITE3_INTEGER);
$stmt->bindValue(":private_key", $new_private_key, SQLITE3_TEXT);
$stmt->bindValue(":game_id", $data["game_id"], SQLITE3_INTEGER);
$stmt->execute();

error_log("Données reçues dans play.php : " . print_r($data, true));
echo json_encode([
    "error" => 0,
    "error_message" => "",
    "game_id" => $game["id"],
    "status" => $status,
    "board" => $board, 
    "player_turn" => $next_player,
    "winner" => $winner ? $data["player"] : null,
    "private_key" => $new_private_key
]);
?>