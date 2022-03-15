# Problem 3
from collections import Counter

# Create function to obtain player points in a year
def get_player_pts(year):
    '''Sub-function that takes a dictionary value (list of all tournament stats)
    for a year and returns a dictionary of players' points for the year
    across the tournaments of the year with players as keys and points as values.'''

    # Create list of players
    p1 = [row['Player 1'] for tourn in year for row in tourn[1]]
    p2 = [row['Player 2'] for tourn in year for row in tourn[1]]

    # Initialise dictionary of player points
    pts = {name: 0 for name in p1 + p2}

    for tourn in year:
        for row in tourn[1]:
        # For round-robins, assume that r = 1. Add r for every win to player pts
        # and subtract r from player pts for every loss
            if row['Round'] == 'Round Robin':
                pts[row['Win']] += 1
                pts[row['Lose']] -= 1

        # For non-round robins, assume that elimination round is the nth match
        # played in the tournament. Add r for every win to player pts and
        # subtract 1/r from player pts for every loss
            else:
                pts[row['Win']] += row['Round_n']
                pts[row['Lose']] -= 1/row['Round_n']

    return pts

# Create function to obtain player points for specified period

def ranks_wdl(data_year, startyr, endyr):
    '''Takes a starting year and ending year (integers) denoting period for
    which to obtain points of players. Applies get_player_pts to each year in
    the period and returns a dictionary with players as keys and overall points
    and rank for the period as values. Ranks exclude players who did not play
    within the specified period.'''

    # Obtain player points per year across all years in dataset
    pts_allyears = dict(zip(data_year.keys(),
                            map(get_player_pts, data_year.values())))

    # Total points (sum) across years within input period
    totalpts = Counter()
    for yr in range(startyr, endyr + 1):
        totalpts.update(pts_allyears[yr])

    # Sort dictionary in descending order of points in period and assign
    # index as ranking
    totalpts = sorted(totalpts.items(), key=lambda x: x[1], reverse=True)
    ranks_totalpts = {index + 1:name for index, name in enumerate(totalpts)}

    return ranks_totalpts

# Create function to print outputs
def print_wdl(data_year, startyr, endyr, n):
    '''Takes startyear, endyear, number of ranks to print and prints results of
    ranks_wdl players and rankings.'''

    ranks_wdl_period = ranks_wdl(data_year, startyr, endyr)

    print('From', startyr, 'to', endyr, 'the top', n, 'are:')
    for i in range(1, n + 1):
        print('Rank', i, ': ' + ranks_wdl_period[i][0] + ',',
              ranks_wdl_period[i][1], 'points')
