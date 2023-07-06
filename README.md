# fantasy-football-predictor

Utilized ridge regression to predict fantasy football players' next year PPG based on NFL data from 2013-2022. Data was obtained from https://www.pro-football-reference.com/. This model currently supports QBs, RBs, and WRs. A ridge regression was used to account for multicollinearity between predictors (e.g. receptions is positively correlated with recieving yards), as well as to balance the high-dimensionality of the data. The model considers in-game statistics on a per-game basis from previous seasons, as well as the player's age.

Assumptions made for training data:
- Player played at least 10 games in the previous year (to remove injuries as outliers)
- PPG thresholds were made for each position, as the use-case for this model is for fantasy football, where low-scoring players should not play a major role in the model as the experience higher volatility in PPG change

Future considerations:
- Incorporate more in-game factors into the model (snap count, target share, etc.)
- Include team-related changes (player is on a better/worse team than they were last year, offseason changes to current team such as FA additions, etc.)
- Include rookies in predictions (using draft position, college stats, etc.)

The current ridge regression model showed ~0.25 R^2 value for each position, as well as the model predicting 50% of the test dataset within 15% of the actual PPG. However, this could be due to the relatively tame nature of the model.

File information:
- functions.py: includes function to calculate PPR score as well as extract and clean player data
- model.py: builds and evaluates model
