#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect(database_name = "tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    database = psycopg2.connect("dbname={}".format(database_name))
    cursor = database.cursor()
    return (database, cursor)

def queryDatabase(query, database_name = "tournament", params = ()):
	"""Queries a database returning a list of rows selected or an empty list if none were selected. 
	Any command executed in the query updates the database.
	params: see cursor class for psycopg2 for an explanation behind the input parameters of the params variable
	"""
	database, cursor = connect(database_name)
	cursor.execute(query, params) # params is a list object
	table_rows = ()
	try:
		table_rows = cursor.fetchall()
	except psycopg2.ProgrammingError:
		table_rows = ()
	database.commit()
	cursor.close()
	database.close()
	return table_rows

def deleteMatches():
    """Remove all the match records from the database."""
    queryDatabase("TRUNCATE TABLE matches;")

def deletePlayers():
    """Remove all the player records from the database.
    This includes match records, if they are dependent on player ids.
    """
    queryDatabase("TRUNCATE TABLE players CASCADE;")
  
def countPlayers():
    """Returns the number of players currently registered."""
    num_players = queryDatabase("SELECT count(*) FROM players;")[0][0]
    print num_players
    return num_players


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    query = """
    INSERT INTO players
    	(name)
    VALUES
    	(%s);
    """
    params = (name,)
    queryDatabase(query, params = params)

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
    player_standings = queryDatabase("SELECT * FROM player_rankings;")
    return player_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    query = """
    INSERT INTO matches 
            (winner_id, 
              loser_id) 
    VALUES 
        (%s, 
         %s);
    """
    params = (winner, loser)
    queryDatabase(query, params = params)
 
 
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
    player_standings = playerStandings() # sorts players based on their wins 
    swiss_pairings = [];
    # pits players of closest rank against each other
    for i in xrange(0, len(player_standings), 2):
        swiss_pairings.append((player_standings[i][0], player_standings[i][1]) + (player_standings[i + 1][0], player_standings[i + 1][1]))
    return swiss_pairings

