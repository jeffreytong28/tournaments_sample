from itertools import groupby
from collections import Counter

# Create function to get the counts of number of matches played per player
# in each tournament.
def get_match_counts(data):
    '''Groups data by tournament and year to obtain a list of players. Returns
    a data dictionary grouped by tournament and year, as well as a list
    of dictionaries, each with the match count per player within the tournament.'''

    # Group data to obtain matches ordered by end date year and create
    # dictionary data_year
    year_group = groupby(data, key = lambda row: (row['End date'].year, row['Tournament']))
    data_tourn = {key: list(val) for key, val in year_group}

    # Create dictionary of all players including duplicates, grouped by tournament
    keys = ['Player 1', 'Player 2']
    players = {i: [row[key] for key in keys for row in tourn]
              for i, tourn in data_tourn.items()}

    # Create list of player match counts per tournament
    match_counts = dict(zip(players.keys(), map(Counter, players.values())))
    return data_tourn, match_counts

# Create function to get round numbers for each match.

def get_rounds(data_tourn, match_counts):
    '''Takes list of list of dictionaries representing all tournaments and
    matches and updates rounds value for each match based on the frequency of
    match counts by player. Returns updated tournament data.'''

    for key, tourn in data_tourn.items():
        rnd = 1 # Initialise round counter as 1
        while rnd <= max(match_counts[key].values()):

            # Begin to assign the round value incrementally for each match based
            # on number of matches played by any of the two players in each match
            # (e.g. if a match has a player with match count of 1, the match is
            # assigned a value of round 1). Continue assigning incrementally by
            # match count until all rounds values have been assigned.
            for row in tourn:
                if row['Round_n'] == 0:
                    if (match_counts[key][row['Player 1']] == rnd or
                        match_counts[key][row['Player 2']] == rnd):
                        row['Round_n'] = rnd
            rnd += 1
    return data_tourn
