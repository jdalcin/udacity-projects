									Tournament Rules
Function:

This code finds the winner of a tournament in a Swiss-ranking system. Ranks players after every round until a winner is found.

Steps:

1. create Database "tournament" in PostGreSQL. 
2. import file "tournament.sql" into the "tournament" database.
3. register players by inputting their name into the "registerPlayer" function.
4. use "playerStandings" function to obtain player rankings for the current round.
5. use "reportMatch" function to input the winner and loser of each match into the database.
6. use "swissPairings" function to get new player pairings for the next round.
7. Repeat steps 4-6 until the tournament has a clearly defined winner (one player has more wins than all the others).

Notes:

* all inputs must be inputted within "tournament_test.py".
* instructions for each function are found within "tournament.py".
* "tournament.py" must be run in python 2.7 and "tournament.sql" must be imported into a postgreSQL database before running.
* specific names in this README file are inside the quotes. They are not including the quotes. 
