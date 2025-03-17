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
starmer.to_csv(output_path, index=False)
