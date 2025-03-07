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

$required_fields = ["game_id", "game_path"];
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

if (!$game) {
    echo json_encode(["error" => 1, "error_message" => "Partie introuvable"]);
    exit;
}

$stmt = $db->prepare("DELETE FROM games WHERE id = :game_id");
$stmt->bindValue(":game_id", $data["game_id"], SQLITE3_INTEGER);
$result = $stmt->execute();

if ($result) {
    echo json_encode(["error" => 0, "error_message" => "Partie supprimée avec succès"]);
} else {
    echo json_encode(["error" => 1, "error_message" => "Erreur lors de la suppression de la partie"]);
}
?>
