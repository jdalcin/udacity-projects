#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM matches;")
    connection.commit()
    cursor.close()
    connection.close()


def deletePlayers():
    """Remove all the player records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM players;")
    connection.commit()
    cursor.close()
    connection.close()

def countPlayers():
    """Returns the number of players currently registered."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM players;")
    num_players = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return num_players


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO players (name) VALUES (%s);", (name,)) # protects against sql injection
    connection.commit()
    cursor.close()
    connection.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    connection = connect()
    cursor = connection.cursor()
    # joins table 'players', 'all_player_wins', and 'all_player_matches' to query their rows for the player standings
    query = """
    SELECT 
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
        wins
            DESC;
    """
    cursor.execute(query)
    player_standings = cursor.fetchall()
    cursor.close()
    connection.close()
    return player_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    connection = connect()
    cursor = connection.cursor()
    query = """
    INSERT INTO 
        matches 
            (winner_id, loser_id) 
    VALUES 
        (%s, %s);
    """
    cursor.execute(query, (winner, loser)) # protects against sql injection
    connection.commit()
    cursor.close()
    connection.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    connection = connect()
    cursor = connection.cursor()
    # ranks players based on their wins and queries this ranking
    query = """
    SELECT 
        players.id, 
        name 
    From 
        players,
        all_player_wins
    WHERE
        players.id = all_player_wins.id
    ORDER BY
        wins 
            DESC;
    """
    cursor.execute(query)
    players_ranked = cursor.fetchall()
    swiss_pairings = [];
    # pits players of closest rank against each other
    for i in xrange(0, len(players_ranked), 2):
        swiss_pairings.append(players_ranked[i] + players_ranked[i + 1])
    cursor.close()
    connection.close()
    return swiss_pairings

