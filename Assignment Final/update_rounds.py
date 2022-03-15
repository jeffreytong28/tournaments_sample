# Create function to correct round numbers for round robin tournaments and
# replace round values.
def update_rounds(data_tourn):
    '''Corrects the round in the overall data list with the right round
    for round robin tournaments. Replaces round numbers in data list in place
    with respective round terms (e.g. Finals, Semifinals, Quarterfinals,
    Round n)'''

    # Create list/dictionary to store round numbers per match and maximum round per
    # tournament
    rounds = [[row['Round_n'] for row in tourn] for tourn in data_tourn.values()]
    maxrnd = dict(zip(data_tourn.keys(), list(map(max, rounds))))

    # Create dictionary of round robin tournaments and their years as given.
    roundrobin = {'Sony Ericsson Championships': range(2007, 2016),
                  'Commonwealth Bank Tournament of Champions': range(2009, 2010),
                  'Qatar Airways Tournament of Champions Sofia': range(2012, 2013),
                  'Garanti Koza WTA Tournament of Champions': range(2013, 2015),
                  'BNP Paribas WTA Finals': range(2016, 2019),
                  'WTA Elite Trophy': range(2015, 2020),
                  'WTA Finals': range(2019, 2022)}

    for key, tourn in data_tourn.items():
        for row in tourn:

    # For tournaments with Round Robins, set the maximum round as 'Finals',
    # followed by 'Semifinals' and remaining as'Round Robin'
            cur_rnd = row['Round_n']
            if (row['Tournament'] in roundrobin.keys() and
            row['End date'].year in roundrobin[row['Tournament']]):
                if cur_rnd == maxrnd[key]:
                    row['Round'] = 'Finals'
                    row['Round_n'] = 3
                elif cur_rnd == maxrnd[key] - 1:
                    row['Round'] = 'Semifinals'
                    row['Round_n'] = 2
                else:
                    row['Round'] = 'Round Robin'
                    row['Round_n'] = 1

    # For non-round robins, assign finals, semifinals, quarterfinals
    # respectively
            elif cur_rnd == maxrnd[key]:
                row['Round'] = 'Finals'
            elif cur_rnd == (maxrnd[key] - 1):
                row['Round'] = 'Semifinals'
            elif cur_rnd == (maxrnd[key] - 2):
                row['Round'] = 'Quarterfinals'
            else:
                row['Round'] = 'Round ' + str(row['Round_n'])

    # Check if there is more than one finals match in a tournament.
    # If so, assume the two matches prior to the last match entry
    # in the tournament (by order) as the semifinals and third place match.
    for index, tourn in enumerate(rounds):
        if tourn.count(max(tourn)) == 2:
            data_tourn[key][-2]['Round'] = 'Semifinals'
        if tourn.count(max(tourn)) == 3:
            data_tourn[key][-2]['Round'] = 'Semifinals'
            data_tourn[key][-3]['Round'] = 'Third Place'

    return data_tourn
