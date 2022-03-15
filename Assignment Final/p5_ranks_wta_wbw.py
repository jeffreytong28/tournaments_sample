# Problem 5
from matplotlib import pyplot as plt
from p4_ranks_wbw import get_ranks_wbw

# The initialisation with 2007 data is not required as the method below draws
# upon the same method in P4 to initialise with 1/n_players.

# Create function to obtain WTA rankings by tournament from 2008
def get_wta_tourn(data_tourn, tournament):
    '''Creates a dictionary of dictionaries of WTA rankings with each dictionary
    representing a tournament storing player:rank.'''

    # For each tournament, insert name:rank into a dictionary if a player name
    # and their rank does not already exist. If rank changes during tournament,
    # first rank will be taken.

    wta_ranks = {}
    for row in data_tourn[tournament]:
        if row['Player 1'] not in wta_ranks.keys():
            wta_ranks[row['Player 1']] = row['Rank 1']
        if row['Player 2'] not in wta_ranks.keys():
            wta_ranks[row['Player 2']] = row['Rank 2']

    return wta_ranks

def tourns_start(data_tourn, year):
    '''Takes a year and creates a dictionary of tournaments and obtain start
    dates of each tournament from that year onwards. For tournaments occuring
    across two years with two different start dates reflected in dataset,
    the later start date is taken.'''
    tourns_start = {key:row['Start date']
                       for key, tourn in data_tourn.items()
                       for row in tourn
                       if key[0] > year - 1}
    return tourns_start



# Function to obtain scatterplot of WTA against WBW rankings
def plot_wta_wbw(data_tourn, tourns_2008_2021):
    '''Obtains WTA and WBW ranks for each tournament from 2008 to 2021 and
    creates a scatter plot of WBW rankings against WTA rankings.'''

    # Function to get wbw ranks of players
    def ranks_wta_wbw_tourn(tournament):
        '''Takes a given tournament year and name and returns the wbw rankings of
        its players at the start of the tournament based on match data in the 52
        weeks before the tournament. Returns a dictionary of tournament unique
        players as keys, and ranks and scores as values.'''

        # Obtain data subset of tournaments completed within 52 weeks before
        # start of tournament
        data_52 = [row for key, val in data_tourn.items()
                   for row in val
                   if (tourns_2008_2021[tournament] - row['End date']).days//7 <= 52 and
                   (tourns_2008_2021[tournament] - row['End date']).days//7 >= 0]

        # Apply get_ranks_wbw on data in previous 52 weeks before tournament to
        # obtain wbw estimates of players before start of tournament
        ranks_wbw = get_ranks_wbw(data_52)

        # Obtain WTA ranks of players at start of tournament
        ranks_wta = get_wta_tourn(data_tourn, tournament)

        # Create dictionary that stores both WTA and WBW ranks for only players
        # who have played in the tournament. Returns players as keys and (WTA, WBW)
        # ranks as values
        ranks_wta_wbw = {player[0]:(get_wta_tourn(data_tourn, tournament)[player[0]], wbw)
                         for wbw, player in enumerate(ranks_wbw)
                         if player[0] in get_wta_tourn(data_tourn, tournament).keys()}

        return ranks_wta_wbw


    # Obtain WTA, WBW ranks for each tournament from 2008 to 2021
    ranks_wta_wbw_2008_2021 = list(map(ranks_wta_wbw_tourn,
                                       tourns_2008_2021.keys()))

    # Plot scatter plot of WTA rankings on x axis and WBW on y axis
    x = [wta_wbw[0] for tourn in ranks_wta_wbw_2008_2021 for wta_wbw in tourn.values()]
    y = [wta_wbw[1] for tourn in ranks_wta_wbw_2008_2021 for wta_wbw in tourn.values()]

    plt.scatter(x, y, s = 5, alpha = 0.3)
    plt.title('Scatter plot of WbW rankings against WTA rankings')
    plt.show()
