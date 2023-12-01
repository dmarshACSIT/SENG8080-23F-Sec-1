import requests
import pandas as pd
import json
import pyodbc
import traceback

# Replace with your API key and email
api_key = '3OTszDGwFM2jGM5+TBfffs0SNeRvOqq9o5w5C/mM4XI='
email = 'rizwiliakathp@gmail.com'

# API endpoint URL
url = 'https://data.usajobs.gov/api/search'

# Initialize an empty DataFrame to store all data
all_data_df = pd.DataFrame()

# Headers for the API request
headers = {
    'Authorization-Key': api_key,
}

# Pagination parameters
page = 100
results_per_page = 100  # You can adjust this value based on your needs


def insert_data(api_response):
    # Define the connection parameters
    server = 'RIZWI'
    database = 'USjob'
    conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

    try:
        # Establish a connection
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Extract data from the API response
        data = api_response
        jobs = data['SearchResult']['SearchResultItems']

        # Insert data into the table


        for job in jobs:

            print(job['MatchedObjectDescriptor']['PositionFormattedDescription'][0]['Label'])
            print(job['MatchedObjectDescriptor']['DepartmentName']                                                                                         )    
            print(job['MatchedObjectDescriptor']['PositionURI'])
            print(job['MatchedObjectDescriptor']['PositionTitle'])
            print(job['MatchedObjectDescriptor']['JobCategory'][0]['Name'] if job['MatchedObjectDescriptor']['JobCategory'] else None)
            print(job['MatchedObjectDescriptor']['OrganizationName'])
            print(job['MatchedObjectDescriptor']['JobGrade'][0]['Code'] if job['MatchedObjectDescriptor']['JobGrade'] else None)
            print(job['MatchedObjectDescriptor']['PositionStartDate'])
            print(job['MatchedObjectDescriptor']['ApplicationCloseDate'])
            print(job['MatchedObjectDescriptor']['PositionLocationDisplay'])
            print(job['MatchedObjectDescriptor']['ApplyURI'][0] if job['MatchedObjectDescriptor']['ApplyURI'] else None)
            print(job['MatchedObjectDescriptor']['QualificationSummary'])
            print(job['MatchedObjectDescriptor']['PositionOfferingType'][0]['Name'] if job['MatchedObjectDescriptor']['PositionOfferingType'] else None)
            print(job['MatchedObjectDescriptor']['PositionSchedule'][0]['Name'] if job['MatchedObjectDescriptor']['PositionSchedule'] else None)
            print(job['MatchedObjectDescriptor']['PublicationStartDate'])
            print(job['MatchedObjectDescriptor']['PositionID'])
            print(job['MatchedObjectDescriptor']['PositionEndDate'])


            cursor.execute("""
    INSERT INTO job_data (
        PositionFormattedDescription, DepartmentName, PositionURI,
        PositionTitle, JobCategory, OrganizationName,
        JobGrade, PositionStartDate, ApplicationCloseDate,
        PositionLocationDisplay, ApplyURI, QualificationSummary,
        PositionOfferingType, PositionSchedule, PublicationStartDate,
        PositionID, PositionEndDate
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""",
(
    job['MatchedObjectDescriptor']['PositionFormattedDescription'][0]['Label'],
    job['MatchedObjectDescriptor']['DepartmentName'],
    job['MatchedObjectDescriptor']['PositionURI'],
    job['MatchedObjectDescriptor']['PositionTitle'],
    job['MatchedObjectDescriptor']['JobCategory'][0]['Name'] if job['MatchedObjectDescriptor']['JobCategory'] else None,
    job['MatchedObjectDescriptor']['OrganizationName'],
    job['MatchedObjectDescriptor']['JobGrade'][0]['Code'] if job['MatchedObjectDescriptor']['JobGrade'] else None,
    job['MatchedObjectDescriptor']['PositionStartDate'],
    job['MatchedObjectDescriptor']['ApplicationCloseDate'],
    job['MatchedObjectDescriptor']['PositionLocationDisplay'],
    job['MatchedObjectDescriptor']['ApplyURI'][0] if job['MatchedObjectDescriptor']['ApplyURI'] else None,
    job['MatchedObjectDescriptor']['QualificationSummary'],
    job['MatchedObjectDescriptor']['PositionOfferingType'][0]['Name'] if job['MatchedObjectDescriptor']['PositionOfferingType'] else None,
    job['MatchedObjectDescriptor']['PositionSchedule'][0]['Name'] if job['MatchedObjectDescriptor']['PositionSchedule'] else None,
    job['MatchedObjectDescriptor']['PublicationStartDate'],
    job['MatchedObjectDescriptor']['PositionID'],
    job['MatchedObjectDescriptor']['PositionEndDate']
))



        # Commit the transaction
        conn.commit()

        print("Data inserted successfully!")

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

    finally:
        # Close the connection
        if conn:
            conn.close()




for i in range(page):
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
        print(type(job_data))
        #print(job_data)

        insert_data(job_data)

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
    

# Split 'MatchedObjectDescriptor' into separate columns
unique_keys = {'PositionFormattedDescription', 'UserArea', 'DepartmentName', 'PositionURI', 'PositionTitle', 'JobCategory',
               'OrganizationName', 'PositionLocation', 'PositionRemuneration', 'JobGrade', 'PositionStartDate',
               'ApplicationCloseDate', 'PositionLocationDisplay', 'ApplyURI', 'SubAgency', 'QualificationSummary',
               'PositionOfferingType', 'PositionSchedule', 'PublicationStartDate', 'PositionID', 'PositionEndDate'}

for key in unique_keys:
    all_data_df[key] = all_data_df['MatchedObjectDescriptor'].apply(lambda x: x.get(key) if isinstance(x, dict) else None)

# Drop the original 'MatchedObjectDescriptor' column
all_data_df.drop('MatchedObjectDescriptor', axis=1, inplace=True)

