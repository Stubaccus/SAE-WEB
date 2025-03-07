<?php
function sendRequest($url, $data) {
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    $response = curl_exec($ch);
    curl_close($ch);
    return json_decode($response, true);
}

$baseUrl = "http://localhost/puissance4/"; // Remplace par ton URL locale

// 1. Tester la création d'une partie
echo "Test: create_game.php\n";
$createResponse = sendRequest($baseUrl . "create_game.php", [
    "game_name" => "TestGame",
    "game_path" => "server1",
    "player1" => "Alice",
    "player1_role" => "human",
    "player1_path" => "server1",
    "player2" => "",
    "player2_role" => "",
    "player2_path" => ""
]);
if (isset($createResponse["error"]) && $createResponse["error"] !== 0) {
    echo "Erreur lors de la création : " . $createResponse["error_message"] . "\n";
    exit;
}

print_r($createResponse);
$game_id = $createResponse["game_id"] ?? null;

if (!$game_id) exit("Erreur: Impossible de créer la partie\n");

// 2. Tester l'inscription d'un joueur
echo "\nTest: join_game.php\n";
$joinResponse = sendRequest($baseUrl . "join_game.php", [
    "game_id" => $game_id,
    "game_path" => "server1",
    "player2" => "Bob",
    "player2_role" => "human",
    "player2_path" => "server2"
]);
print_r($joinResponse);

// 3. Récupérer les parties disponibles
echo "\nTest: list_games.php\n";
$listResponse = sendRequest($baseUrl . "list_games.php", ["status" => "all", "path" => "server1"]);
print_r($listResponse);

// 4. Récupérer les détails d'une partie
echo "\nTest: get_game.php\n";
$getResponse = sendRequest($baseUrl . "get_game.php", ["game_id" => $game_id, "game_path" => "server1", "player" => 1]);
print_r($getResponse);

// 5. Jouer un coup
echo "\nTest: play.php\n";
$playResponse = sendRequest($baseUrl . "play.php", [
    "game_id" => $game_id,
    "game_path" => "server1",
    "player" => 1,
    "column" => 3,
    "private_key" => "@C2D24#2"
]);
print_r($playResponse);

// 6. Supprimer la partie
echo "\nTest: delete_game.php\n";
$deleteResponse = sendRequest($baseUrl . "delete_game.php", ["game_id" => $game_id, "game_path" => "server1"]);
print_r($deleteResponse);
?>
