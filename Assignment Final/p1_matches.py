# Problem 1

# 1. Who won the final of the 2021 Women's US Open?
def ans_players1(data_tourn, tournament, yr, rnd):
    '''Takes a tournament(string), year(integer) and round(string)
    as arguments and prints the winner for the respective matches.'''

    winners_losers = [(row['Win'], row['Lose'])
                      for row in data_tourn[yr, tournament]
                      if row['Tournament'] == tournament
                      and row['End date'].year == yr
                      and row['Round'] == rnd]

    return winners_losers

# 2. Who played against whom in the 4th Round of the 2018 French Open?

def ans_players2(data_tourn, tournament, yr, rnd):
    '''Takes a tournament(string), year(integer) and round(string)
    as arguments and prints the players for the respective matches.'''

    for pair in ans_players1(data_tourn, tournament, yr, rnd):
        print(pair[0], 'played against', pair[1], 'in', rnd,
        'of the', yr, tournament)

# 3. In which round was Venus Williams eliminated in the 2011 Australian Open?
def rnd_lost(data_tourn, tournament, yr, player):
    '''Takes a tournament(string), year(integer), player who lost (string)
    as arguments and prints the round eliminated for the match.'''

    rndlost = [row['Round'] for row in data_tourn[yr, tournament]
              if row['Tournament'] == tournament
              and row['End date'].year == yr
              and row['Lose'] == player]

    print(player, 'was eliminated in', rndlost[0], 'of the', yr, tournament)

# 4. How many finals has Naomi Osaka played in until now?
def ans_nrounds(data_tourn, player, rnd):
    '''Takes a player (string) and round(string) and prints
    the number of the specified round played by the player across dataset.'''

    matches = [row['Tournament'] for tourn in data_tourn.values() for row in tourn
              if (row['Player 1'] == player or row['Player 2'] == player)
              and row['Round'] == rnd]

    print(player, 'has played in', len(matches), rnd)

# 5. How many times have Venus and Serena Williams played against each other
# and how many of these matches each won?
def ans_pvp(data_tourn, p1, p2):
    '''Takes a player 1 and player 2 and prints the number of matches
    they have played together and number of matches won by each player'''

    matches = [row['Win'] for tourn in data_tourn.values() for row in tourn
              if (row['Player 1'] == p1 and row['Player 2'] == p2) or
              (row['Player 2'] == p1 and row['Player 1'] == p2)]

    p1_win =  matches.count(p1)
    p2_win = matches.count(p2)

    print(p1, 'and', p2, 'played in a total of', p1_win + p2_win,
    'matches together where', p1, 'won', p1_win, 'matches and', p2,
    'won', p2_win, 'matches.')
