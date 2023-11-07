import requests
import pandas as pd
import json

# Replace with your API key and email
api_key = '3OTszDGwFM2jGM5+TBfffs0SNeRvOqq9o5w5C/mM4XI='
email = 'rizwiliakathp@gmail.com'

# API endpoint URL
url = 'https://data.usajobs.gov/api/search'

# Initialize an empty DataFrame to store all data
all_data_df = pd.DataFrame()

# Headers for the API request
headers = {
    'User-Agent': email,
    'Authorization-Key': api_key,
}

# Pagination parameters
page = 1
results_per_page = 100  # You can adjust this value based on your needs

while True:
    # Parameters for the API request
    params = {
        'Page': page,
        'ResultsPerPage': results_per_page,
    }

    # Make the API request to retrieve job announcements
    response = requests.get(url, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        job_data = response.json()

        # Extract job announcements from the response
        announcements = job_data.get('SearchResult', {}).get('SearchResultItems', [])

        if announcements:
            # Convert the data into a DataFrame and append to the existing DataFrame
            all_data_df = pd.concat([all_data_df, pd.DataFrame(announcements)], ignore_index=True)
        else:
            # No more data to retrieve
            break
    else:
        print(f"API request failed with status code {response.status_code}")
        break

    # Increment the page number
    page += 1

# Split 'MatchedObjectDescriptor' into separate columns
unique_keys = {'PositionFormattedDescription', 'UserArea', 'DepartmentName', 'PositionURI', 'PositionTitle', 'JobCategory',
               'OrganizationName', 'PositionLocation', 'PositionRemuneration', 'JobGrade', 'PositionStartDate',
               'ApplicationCloseDate', 'PositionLocationDisplay', 'ApplyURI', 'SubAgency', 'QualificationSummary',
               'PositionOfferingType', 'PositionSchedule', 'PublicationStartDate', 'PositionID', 'PositionEndDate'}

for key in unique_keys:
    all_data_df[key] = all_data_df['MatchedObjectDescriptor'].apply(lambda x: x.get(key) if isinstance(x, dict) else None)

# Drop the original 'MatchedObjectDescriptor' column
all_data_df.drop('MatchedObjectDescriptor', axis=1, inplace=True)

# Print the DataFrame with all data
print(all_data_df)
