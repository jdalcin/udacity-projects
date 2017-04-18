-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- DATABASE

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

-- TABLES

-- table representing tournament players
CREATE TABLE players (
	id SERIAL PRIMARY KEY,
	name TEXT);

-- table representing match outcomes
CREATE TABLE matches (
	id SERIAL PRIMARY KEY,
	winner_id INTEGER REFERENCES players (id),
	loser_id INTEGER REFERENCES players (id));

--VIEWS

-- view representing player wins but includes null data values (players that do not have win values because they have yet to win a game)
CREATE VIEW 
	player_wins 
AS SELECT 
	winner_id,
	count(*) AS wins -- counts all the times a player has won a match
FROM
	matches
GROUP BY
	winner_id;

-- view which assigns all players the number of times in which they won a game
-- replaces any null data value from the player_losses view with value 0
CREATE VIEW
	all_player_wins
AS SELECT
	players.id,
	coalesce(wins, 0) AS wins
FROM
		players
	LEFT JOIN
		player_wins
	ON 
		players.id = player_wins.winner_id;

-- view representing player losses but includes null data values (players that do not have loss values because they have yet to lose a game)
CREATE VIEW 
	player_losses 
AS SELECT 
	loser_id,
	count(*) AS losses -- counts all the times a player has lost a match
FROM
	matches
GROUP BY
	loser_id;

-- view which assigns all players the number of times in which they lost a game
-- replaces any null data value from the player_losses view with value 0
CREATE VIEW
	all_player_losses
AS SELECT
	players.id,
	coalesce(losses, 0)	AS losses
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
	all_player_wins.id AS player_id,
	(all_player_wins.wins
	+ all_player_losses.losses) AS matches -- adds the players wins and losses to get their total matches played
FROM
	all_player_wins,
	all_player_losses
WHERE
	all_player_wins.id = all_player_losses.id;

--view representing player rankings

CREATE VIEW
	player_rankings
AS SELECT 
	players.id,
	players.name,
	all_player_wins.wins,
	all_player_matches.matches
FROM
	players,
	all_player_wins,
	all_player_matches
WHERE
           all_player_wins.id = all_player_matches.player_id
AND
           players.id = all_player_wins.id
ORDER BY 
	wins DESC;


