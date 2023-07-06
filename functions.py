import pandas as pd
import re

# Calculate a PPR (point per reception) PPG (points per game) fantasy score for a player given a year
def score(row):
    data = row
    total = data[7]*0.04 + data[8]*4 - data[9]*2 + data[12] + data[13]*0.1 + data[14]*6 + data[16]*0.1 + data[17]*6
    ppg = total / data[4]
    return ppg

# Create nfl dataframe
def nfl(pos: str):

    # Initialize pass, rec, and rush dataframes
    pass_names = ['Player', 'Tm', 'Age', 'Pos', 'G', 'Cmp', 'PassAtt', 'PassYds', 'PassTD', 'Int', 'Year']
    passing = pd.DataFrame(columns=pass_names)

    rec_names = ['Player', 'Tm', 'Age', 'Pos', 'G', 'Tgt', 'Rec', 'RecYds', 'RecTD', 'Year']
    rec = pd.DataFrame(columns=rec_names)

    rush_names = ['Player', 'Tm', 'Age', 'Pos', 'G', 'RushAtt', 'RushYds', 'RushTD', 'Year']
    rush = pd.DataFrame(columns=rush_names)

    # Import csv files for each year 2018-2022 and append them to respective dataframes
    for i in range(13, 23):

        # Passing
        t1 = pd.read_csv('passing/passing-{0}.csv'.format(i))
        t1['Year'] = pd.Series([2000+i for x in range(len(t1.index))])
        t1['Player'] = t1['Player'].astype(str)
        for index, row in t1.iterrows():
            name = re.sub(r'[*+]+', '', row.Player)
            t1.at[index, 'Player'] = name
        t1 = t1[['Player', 'Tm', 'Age', 'Pos', 'G', 'Cmp', 'Att', 'Yds', 'TD', 'Int', 'Year']]
        new_names = {'Att': 'PassAtt', 'Yds': 'PassYds', 'TD': 'PassTD'}
        t1.rename(columns=new_names, inplace=True)
        passing = pd.concat([passing, t1], ignore_index=True)

        # Recieving
        t2 = pd.read_csv('recieving/recieving-{0}.csv'.format(i))
        t2['Year'] = pd.Series([2000+i for x in range(len(t2.index))])
        t2['Player'] = t2['Player'].astype(str)
        for index, row in t2.iterrows():
            name = re.sub(r'[*+]+', '', row.Player)
            t2.at[index, 'Player'] = name
        t2 = t2[['Player', 'Tm', 'Age', 'Pos', 'G', 'Tgt', 'Rec', 'Yds', 'TD', 'Year']]
        new_names = {'Yds': 'RecYds', 'TD': 'RecTD'}
        t2.rename(columns=new_names, inplace=True)
        rec = pd.concat([rec, t2], ignore_index=True)

        # Rushing
        t3 = pd.read_csv('rushing/rushing-{0}.csv'.format(i))
        t3['Year'] = pd.Series([2000+i for x in range(len(t3.index))])
        t3['Player'] = t3['Player'].astype(str)
        for index, row in t3.iterrows():
            name = re.sub(r'[*+]+', '', row.Player)
            t3.at[index, 'Player'] = name
        t3 = t3[['Player', 'Tm', 'Age', 'Pos', 'G', 'Att', 'Yds', 'TD', 'Year']]
        new_names = {'Att': 'RushAtt', 'Yds': 'RushYds', 'TD': 'RushTD'}
        t3.rename(columns=new_names, inplace=True)
        rush = pd.concat([rush, t3], ignore_index=True)

    # Join all data
    nfl = pd.merge(rec, rush, on=['Player', 'Tm', 'Age', 'Pos', 'G', 'Year'], how='outer').fillna(0)
    nfl = pd.merge(passing, nfl, on=['Player', 'Tm', 'Age', 'Pos', 'G', 'Year'], how='outer').fillna(0)

    # Edge case fixing
    nfl['Year'] = nfl['Year'].astype(int)
    # Ensures that player played a sufficient number of games
    nfl = nfl[nfl['G'] >= 1]

    # Apply fantasy score function to add fantasy score columns
    nfl['PPG'] = nfl.apply(score, axis=1)

    if pos == 'QB':
        nfl = nfl[nfl['PPG'] >= 12]
    elif pos == 'RB':
        nfl = nfl[nfl['PPG'] >= 10]
    elif pos == 'WR':
        nfl = nfl[nfl['PPG'] >= 10]

    # Normalize appropriate columns to per-game basis
    nfl['Cmp'] = nfl['Cmp']/nfl['G']
    nfl['PassAtt'] = nfl['PassAtt']/nfl['G']
    nfl['PassYds'] = nfl['PassYds']/nfl['G']
    nfl['Int'] = nfl['Int']/nfl['G']
    nfl['RushAtt'] = nfl['RushAtt']/nfl['G']
    nfl['RushYds'] = nfl['RushYds']/nfl['G']
    nfl['RushTD'] = nfl['RushTD']/nfl['G']
    nfl['Tgt'] = nfl['Tgt']/nfl['G']
    nfl['Rec'] = nfl['Rec']/nfl['G']
    nfl['RecYds'] = nfl['RecYds']/nfl['G']
    nfl['RecTD'] = nfl['RecTD']/nfl['G']

    # Add columns for future PPG for model
    nfl = nfl.sort_values(by=['Player', 'Year'])
    nfl['PPG Next Year'] = nfl.groupby('Player')['PPG'].shift(-1)
    nfl['PPG Previous Year'] = nfl.groupby('Player')['PPG'].shift(1)
    nfl['Percent Change'] = 100*(nfl['PPG Next Year']-nfl['PPG'])/nfl['PPG']

    return nfl
