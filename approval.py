import pandas as pd
import requests

# Load data from the API response
url = "https://www.politico.eu/wp-json/politico/v1/poll-of-polls/GB-leadership-approval"
data = requests.get(url).json()

# Extract relevant data
polls = pd.DataFrame(data['polls'])
trends = pd.DataFrame(data['trends']['kalmanSmooth'])

# Combine trends data
trends_parties = pd.DataFrame(trends['parties'].tolist())
full_trends = pd.concat([trends, trends_parties], axis=1).drop(columns=['parties'])

starmer = full_trends[['date','approve_starmer','disapprove_starmer']]
starmer['date'] = pd.to_datetime(starmer['date'])
starmer = starmer.set_index('date')

starmer = starmer.loc['2024-07-12':]
starmer.columns = ['Approve','Disapprove']
starmer


output_path = "approval-rating-UK.csv"
starmer.to_csv(output_path)

# Fetch JSON data
url = "https://www.politico.eu/wp-json/politico/v1/poll-of-polls/GB-parliament"
data = requests.get(url).json()

# Extract 'polls' and 'trends' data
polls = pd.DataFrame(data['polls'])
trends = pd.DataFrame(data['trends']['kalmanSmooth'])

# Combine 'polls' with its 'parties' data
polls_parties = pd.DataFrame(polls['parties'].tolist())  # Extract nested data as DataFrame
full_polls = pd.concat([polls, polls_parties], axis=1).drop(polls.columns[1], axis=1)

# Pivot longer (melt) to reshape the data
working_polls = full_polls.melt(
    id_vars=[col for col in full_polls.columns if col not in ["Con", "ChUK"]],
    value_vars=["Con", "ChUK"],
    var_name="parties",
    value_name="value"
)

# Combine 'trends' with its 'parties' data
trends_parties = pd.DataFrame(trends['parties'].tolist())
full_trends = pd.concat([trends, trends_parties], axis=1).drop(trends.columns[1], axis=1)
full_trends['date'] = pd.to_datetime(full_trends['date'])
full_trends = full_trends.set_index('date')
last_trends = full_trends.loc['2024-07-12':]
last_trends.columns = ['Conservative','Labour', 'Lib Dem', 'UKIP', 'Green', 'SNP', 'Plaid','Reform','ChangeUK']
last_trends.to_csv('uk-polls.csv')
all_trends = full_trends.loc['2018-01-01':]
all_trends.columns = ['Conservatives','Labour', 'Lib Dem', 'UKIP', 'Green', 'SNP', 'Plaid','Reform','ChangeUK']
all_trends.to_csv('uk-polls-all.csv')
