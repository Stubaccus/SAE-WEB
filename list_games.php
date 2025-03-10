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

if (!isset($data["status"]) || !isset($data["path"])) {
    echo json_encode(["error" => 1, "error_message" => "Données manquantes"]);
    exit;
}

$status_filter = $data["status"];
$path_filter = $data["path"];

$db = new SQLite3("puissance4.db");

$query = "SELECT id as game_id, status, player1, player1_role, player1_path, player2, player2_role, player2_path, player_turn FROM games WHERE game_path = :game_path";
if ($status_filter !== "all") {
    $query .= " AND status = :status";
}

$stmt = $db->prepare($query);
$stmt->bindValue(":game_path", $path_filter, SQLITE3_TEXT);
if ($status_filter !== "all") {
    $stmt->bindValue(":status", $status_filter, SQLITE3_TEXT);
}

$result = $stmt->execute();

$games = [];
while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
    $games[] = $row;
}

echo json_encode(["games" => $games]);
?>
