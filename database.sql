CREATE TABLE IF NOT EXISTS games(                                                                                                          
    id INTEGER PRIMARY KEY AUTOINCREMENT,                                                                                                   -- id unique de la partie
    name TEXT NOT NULL,                                                                                                                     -- nom de la partie 
    game_path TEXT,
    status TEXT CHECK(status IN ('waiting', 'play', 'over')) DEFAULT 'waiting',                                                             -- statue de la partie
    player1 TEXT NOT NULL,                                                                                                                  -- nom du joueur 1
    player1_role TEXT CHECK(player1_role IN ('human', 'AI')) NOT NULL,                                                                      -- role du joueur 1
    player1_path TEXT,
    player2 TEXT,                                                                                                                           -- nom du joueur 2
    player2_role TEXT CHECK(player2_role IN ('human', 'AI')),                                                                               -- role du joueur 2
    player2_path TEXT,
    board TEXT NOT NULL DEFAULT '[ [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0] ]',  -- plateau de jeu
    player_turn INTEGER DEFAULT 1 ,                                                                                                          -- tour du joueur
    last_move INTEGER
);

CREATE TABLE IF NOT EXISTS moves (                                                                                                          -- table des mouvements (la ou sont stocké les coups joué)
    id INTEGER PRIMARY KEY AUTOINCREMENT,                                                                                                   -- id unique du mouvement
    game_id INTEGER,                                                                                                                        -- id de la partie en cours 
    player INTEGER,                                                                                                                         -- id du joueur ayant joué
    column INTEGER,                                                                                                                         -- colonne ou a mis un pion
    FOREIGN KEY (game_id) REFERENCES games(id)                                                                                              -- lien avec la table games 
);


CREATE TABLE IF NOT EXISTS players (                                                                                                        -- table des joueurs
    id INTEGER PRIMARY KEY AUTOINCREMENT,                                                                                                   -- id unique du joueur
    game_id INTEGER,                                                                                                                        -- id de la partie en cours
    player_name TEXT,                                                                                                                       -- nom du joueur
    private_key TEXT,                                                                                                                       -- clé privée du joueur
    FOREIGN KEY (game_id) REFERENCES games(id)                                                                                              -- lien avec la table games
);