from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from functions import nfl

def model(pos: str):
    nfl_data = nfl(pos)
    nfl_pred = nfl_data[nfl_data['Year'] == 2022]
    nfl_data = nfl_data.dropna(subset=['PPG Next Year'])

    # Predictors dependent on position
    if pos == 'QB':
        nfl_mod = nfl_data[nfl_data['Pos'] == 'QB']
        nfl_pred = nfl_pred[nfl_pred['Pos'] == 'QB']
        X = nfl_mod[['Age', 'Cmp', 'PassAtt', 'PassYds', 'PassTD', 'Int', 'RushAtt', 'RushYds', 'RushTD']]
        x_23 = nfl_pred[['Age', 'Cmp', 'PassAtt', 'PassYds', 'PassTD', 'Int', 'RushAtt', 'RushYds', 'RushTD']]
    elif pos == 'RB':
        nfl_mod = nfl_data[nfl_data['Pos'] == 'RB']
        nfl_pred = nfl_pred[nfl_pred['Pos'] == 'RB']
        X = nfl_mod[['Age', 'Tgt', 'Rec', 'RecYds', 'RecTD', 'RushAtt', 'RushYds', 'RushTD']]
        x_23 = nfl_pred[['Age', 'Tgt', 'Rec', 'RecYds', 'RecTD', 'RushAtt', 'RushYds', 'RushTD']]
    elif pos == 'WR':
        nfl_mod = nfl_data[nfl_data['Pos'] == 'WR']
        nfl_pred = nfl_pred[nfl_pred['Pos'] == 'WR']
        X = nfl_mod[['Age', 'Tgt', 'Rec', 'RecYds', 'RecTD']]
        x_23 = nfl_pred[['Age', 'Tgt', 'Rec', 'RecYds', 'RecTD']]
    
    y = nfl_mod['Percent Change']


    # Build model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state=42)
    
    mod = Ridge(alpha=0.1)
    mod.fit(X_train, y_train)
    print('Coefficients:', mod.coef_)
    print('Intercept:', mod.intercept_)

    # Regression analysis
    print('R^2:', mod.score(X, y))
    y_pred = mod.predict(X_test)
    absolute_diff = abs(y_test - y_pred)
    threshold = 15
    within_threshold = (absolute_diff <= threshold)
    num_within_threshold = sum(within_threshold)
    percentage_within_threshold = (num_within_threshold / len(y_test)) * 100
    print(f"Percentage within 15% of prediction: {percentage_within_threshold}%")


    # Make predictions
    predictions = mod.predict(x_23)
    nfl_pred['Predictions'] = predictions
    nfl_pred['Next Year PPG'] = (1 + (predictions/100))*nfl_pred['PPG']
    nfl_pred = nfl_pred.sort_values(by=['Next Year PPG'], ascending=False)
    return print(nfl_pred[['Player', 'Tm', 'PPG', 'Next Year PPG']])

print(model('QB'))
print(model('RB'))
print(model('WR'))
