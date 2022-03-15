# Problem 2
from itertools import groupby
from collections import Counter

def group_data_year(data_tourn):
    '''Takes dictionary (data_tourn) whose keys represent each tournament
    and values representing matches to group them by year. Returns a dictionary
    with years as keys and values as lists of tournaments and stats in a year.'''

    # Group data to obtain matches ordered by year
    year_group = groupby(data_tourn.items(), key = lambda x: x[0][0])

    # Return sorted matches by tournament within each year sublist
    data_year = {yr: list(tourn) for yr, tourn in year_group}

    return data_year


# Function to count number of matches won each year
def ranks_ww(data_year, startyr, endyr):
    '''Takes a starting year and ending year (integers) denoting period for
    which to obtain players who won matches. Retrieves winning players from data
    and counts number of matches won each year. Returns dictionary with players
    and their ranking as keys, and matches won during period specified in argument
    as values. Ranking excludes players that have not won any match in the
    period specified.'''

    # Create dictionary with index as keys and list of winners
    # across matches per year as values.
    player_wins = {yr:[row['Win'] for tourn in val
                   for row in tourn[1]]
                   for yr, val in data_year.items()}

    # Count matches won in period with Counter
    player_wins_period = Counter()
    for yr in range(startyr, endyr + 1):
        player_wins_period.update(player_wins[yr])

    # Sort dictionary in descending order of matches won in period and assign
    # player's index as ranking
    player_wins_period = sorted(player_wins_period.items(),
                                key=lambda x: x[1], reverse=True)
    rank_wins_period = {index + 1:name
                        for index, name in enumerate(player_wins_period)}

    return rank_wins_period

# Create function to print outputs
def print_ww(data_year, startyr, endyr, n):
    '''Takes startyear, endyear, number of ranks to print and prints results
    of ranks_ww players and rankings.'''

    ranks_ww_period = ranks_ww(data_year, startyr, endyr)

    print('From', startyr, 'to', endyr, 'the top', n, 'are:')
    for i in range(1, n + 1):
        print('Rank', i, ': ' + ranks_ww_period[i][0] + ',',
              ranks_ww_period[i][1], 'points')
