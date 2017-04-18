-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- table represeniting tournament players
CREATE TABLE
	players (
		id SERIAL PRIMARY KEY,
		name TEXT);

-- table representing match outcomes
CREATE TABLE 
	matches (
		id SERIAL PRIMARY KEY,
		winner_id INTEGER 
			REFERENCES 
				players (id),
		loser_id INTEGER 
			REFERENCES 
				players (id));

-- view representing player wins but includes nulls
CREATE VIEW 
	player_wins 
AS SELECT 
	winner_id,
	count(*)  -- counts all the times a player has won a match
		AS wins 
FROM
	matches
GROUP BY
	winner_id;

-- same as player_wins view but nulls are replaced by 0
CREATE VIEW
	all_player_wins
AS SELECT
	players.id,
	coalesce(wins, 0)
		AS wins
FROM
		players
	LEFT JOIN
		player_wins
	ON 
		players.id = player_wins.winner_id;

-- view representing player losses but includes nulls
CREATE VIEW 
	player_losses 
AS SELECT 
	loser_id,
	count(*) -- counts all the times a player has lost a match
		AS losses 
FROM
	matches
GROUP BY
	loser_id;

-- same as player_losses views but nulls are replaced by 0 
CREATE VIEW
	all_player_losses
AS SELECT
	players.id,
	coalesce(losses, 0)	
		AS losses
FROM
		players
	LEFT JOIN
		player_losses
	ON 
		players.id = player_losses.loser_id;

-- view representing the total matches that a player has completed
CREATE VIEW
	all_player_matches
AS SELECT
	all_player_wins.id
		AS player_id,
	all_player_wins.wins
	+ all_player_losses.losses -- adds the players wins and losses to get their total matches played
		AS matches
	FROM
			all_player_wins
		JOIN
			all_player_losses
		ON 
			all_player_wins.id = all_player_losses.id;



