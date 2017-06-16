# Tournament Rules

### Function

This code finds the winner of a tournament in a Swiss-ranking system. Ranks players after every round until a winner is found.

### Command Line Instructions

1. psql -f tournament.sql
2. python tournament_test.py

* running step 2 is simply a test case to confirm that the database is working

### Instructions for a General Tournament

1. execute file "tournament.sql" to create "tournament" database (psql -f tournament.sql).

2. alter file tournament_test.py in this manner:
   i. register players by inputting their name into the "registerPlayer" function.
   ii. use "playerStandings" function to obtain player rankings for the current round.
   iii.use "reportMatch" function to input the winner and loser of each match into the database.
   iv. use "swissPairings" function to get new player pairings for the next round.
   v. Repeat steps 4-6 until the tournament has a clearly defined winner (one player has more wins than all the others).

3. run code through command line with "python tournament_test.py".

#### Notes

* all inputs must be inputted within "tournament_test.py".
* instructions for each function are found within "tournament.py".
* "tournament.py" must be run in python 2.7 and "tournament.sql" must be imported into a postgreSQL database before running.
* specific names in this README file are inside the quotes. They are not including the quotes.
