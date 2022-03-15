# Functions to edit and update data
from datetime import datetime

def change_dates(row):
    '''Takes a dictionary representing a match and edits the start and end date
    of the match in place to datetime format. Accounts for tournaments that
    stretch across two years by replacing their end dates with the next date
    in the following year.'''

    # Amend start dates and end dates to datetime format
    dt_start = datetime.strptime(row['Start date'], "%Y-%m-%d")
    dt_end = datetime.strptime(row['End date'], "%Y-%m-%d")

    # For tournaments occuring across two years (typically with end dates
    # 31 Dec in first) year, replace with match end dates of 1 Jan in the
    # following year
    if dt_end.month == 12 and dt_end.day == 31:
        dt_end = dt_end.replace(year = dt_end.year + 1, month = 1, day = 1)
    row['Start date'] = dt_start
    row['End date'] = dt_end

def change_ranks(row):
    '''Takes a dictionary representing a match and edits the ranks of each
    player in place to float type. If ranks are empty, replace them with 0.'''

    # Convert ranks to floats
    row['Rank 1'] = int(float((row['Rank 1']))) if row['Rank 1'] != '' else None
    row['Rank 2'] = int(float((row['Rank 2']))) if row['Rank 2'] != '' else None

def edit_names(row):
    '''Takes a dictionary representing a match and standardises the player names
    if names have not been standardised.'''

    # Dictionary of names found in dataset that are not standardized
    # (not comprehensive)
    p_names = {'Kostanic T. J.':'Kostanic J.', 'Kostanic Tosic J.':'Kostanic J.',
               'Teichmann J.':'Teichmann J.B.', 'Muguruza Blanco G.':'Muguruza G.',
               'Date Krumm K.': 'Date-Krumm K.', 'Date Krumm K. ':'Date-Krumm K.',
               'Xu Y-F.': 'Xu Y.F.', 'Zhang K.L.': 'Zhang K-L.',
               'Dushevina V. ': 'Dushevina V.', 'Lu Jia-Jing': 'Lu Jia Jing',
               'Pous Tio L.':'Pous-Tio L.', 'Pous-T L.':'Pous-Tio L.',
               'Pous-T. L.':'Pous-Tio L.', 'Salerni M.':'Salerni M.E.',
               'Arruabarrena-Vecino L.': 'Arruabarrena L.',
               'Arruabarrena Vecino L.':'Arruabarrena L.',
               'Rezai A. ': 'Rezai A.', 'Schmiedlova A.K.':'Schmiedlova K.',
               'Schmiedlova A.': 'Schmiedlova K.',
               'Cohen Aloro S.':'Cohen-Aloro S.',
               'Cohen A.': 'Cohen-Aloro S.',
               'Garcia Vidagany B.': 'Garcia-Vidagany B.',
               'Badosa Gibert. P.':'Badosa P.',
               'Badosa Gibert P.': 'Badosa P.',
               'Rodionova Ar.':'Rodionova A.', 'Rodionova An.':'Rodionova A.',
               'Stosur S. ': 'Stosur S.', 'Zahlavova Strycova B..':'Zahlavova S.',
               'Zahlavova Strycova B.': 'Zahlavova S.', 'Wickmayer Y. ': 'Wickmayer Y.',
               'Mattek B.': 'Mattek-Sands B.', 'Torro-Flor M.T.': 'Torro Flor M.T.',
               'Czink M.': 'Czink M.', 'Saidkhodj. D.': 'Saidkhodjaeva D.',
               'Bolsova A.': 'Bolsova Zadoinov A.', 'Kerkhove L.': 'Pattinama Kerkhove L.',
               'Soler Espinosa S..':'Soler Espinosa S.',
               'El Allami Zhara F.': 'El Allami Zahra F.',
               'Raducànu E.':'Raducanu E.'}

    # Amend player names to value if they appear above
    if row['Player 1'] in p_names.keys():
        if row['Comment'] == row['Player 1'] + ' Retired':
            row['Comment'] = p_names[row['Player 1']] + ' Retired'
        row['Player 1'] = p_names[row['Player 1']]
    if row['Player 2'] in p_names.keys():
        if row['Comment'] == row['Player 2'] + ' Retired':
            row['Comment'] = p_names[row['Player 2']] + ' Retired'
        row['Player 2'] = p_names[row['Player 2']]

# Create function to determine winner of each round
def get_winner_loser(row):
    '''Takes a dictionary representing a match and inserts key 'round' to initialise
    round as 0. Also inserts keys 'Win' and 'Lose with name of winning or losing
    player respectively.'''

    # Insert two round keys and initialise values as 0.
    row['Round_n'] = 0

    # If player has retired, assign as loser and opposing player as winner and
    # return function.
    if row['Comment'] == row['Player 1'] + ' Retired':
        row['Win'] = row['Player 2']
        row['Lose'] = row['Player 1']
        return
    elif row['Comment'] == row['Player 2'] + ' Retired':
        row['Win'] = row['Player 1']
        row['Lose'] = row['Player 2']
        return

    # If no players have retired, evaluate strings in columns Set 1-3.
    # Positive denotes set is won by player 1. If player 1 has won the match
    # with at least two sets, assign as winner and vice versa.
    else:
        try:
            if(eval(row['Set 1']) > 0 and eval(row['Set 2']) > 0) or (
                eval(row['Set 1']) > 0 and eval(row['Set 3']) > 0) or (
                eval(row['Set 2']) > 0 and eval(row['Set 3']) > 0):
                row['Win'] = row['Player 1']
                row['Lose'] = row['Player 2']
            else:
                row['Win'] = row['Player 2']
                row['Lose'] = row['Player 1']

        except SyntaxError:
            pass


def update_data(row):
    '''Wrapper function that compiles functions for change_startdate,
    change_enddate, get_winner_loser. Returns updated dictionary row.'''

    change_dates(row)
    change_ranks(row)
    edit_names(row)
    get_winner_loser(row)
    return row

def update_all(data):
    '''Applies update_data to each row of the dataset and returns
    updated data.'''

    updated_data = list(map(update_data, data))
    return updated_data
