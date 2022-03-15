# Problem 4
from collections import Counter

def get_ranks_wbw(data_period):
    '''Takes a data dictionary and gets players' scores across all tournaments
    from data. Returns a dictionary with players as keys and overall points and
    rank for the period as values.'''

    #Create lists of players, identify losers and count number of matches lost
    p1 = [row['Player 1'] for row in data_period]
    p2 = [row['Player 2'] for row in data_period]
    n_players = len(set(p1 + p2))
    losers = [row['Lose'] for row in data_period]

    # Initialise counter dictionary of players with number of matches lost and
    # update lost count
    n_lost = Counter({name: 0 for name in p1 + p2})
    n_lost.update(Counter(losers))

    # Initialise dictionary of player points with point of 1/n and share
    scores = {name: 1/n_players for name in p1 + p2}

    # Initialise iteration count
    i = 0

    # For each iteration, each loser divides current score by number of matches
    # lost and passes share to winner.
    while i < 10:
        for row in data_period:
            # Check if a player (winner for match) has lost in a tournament.
            # If not, pass their score to themselves.
            if n_lost[row['Win']] == 0:
                scores[row['Win']] += scores[row['Win']]

            # Otherwise proceed to update scores for loser and winner
            else:
                scores[row['Lose']] -= scores[row['Lose']]/n_lost[row['Lose']]
                scores[row['Win']] += scores[row['Lose']]/n_lost[row['Lose']]

        # Rescale score of each player by multiplying it by 0.85 and adding
        # 0.15/n
        for score in scores.values():
            score = score*0.85 + 0.15/n_players

        i += 1

    # Sort scores dictionary in descending order of scores in period
    ranks = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranks


def ranks_wbw(data_tourn, startyr, endyr):
    '''Takes a starting year and ending year (integers) that defines period for
    which to apply get_ranks_wbw to obtain scores of players. Returns a
    dictionary with players as keys and overall points and rank for the period
    as values. Ranks exclude players who did not play within the specified period.'''

    # Get subset of match data based on input period
    data_period = [row for key, tourn in data_tourn.items()
                   for row in tourn
                   if key[0] in range(startyr, endyr + 1)]

    return get_ranks_wbw(data_period)

# Create function to print outputs
def print_wbw(data_tourn, startyr, endyr, n):
    '''Takes startyear, endyear, number of ranks to print and prints results
    of ranks_wbw players and rankings.'''

    ranks_wbw_period = list(ranks_wbw(data_tourn, startyr, endyr))

    print('From', startyr, 'to', endyr, 'the top', n, 'are:')
    for i in range(1, n + 1):
        print('Rank', i, ': ', ranks_wbw_period[i-1][0] + ',',
               ranks_wbw_period[i-1][1], 'points')
