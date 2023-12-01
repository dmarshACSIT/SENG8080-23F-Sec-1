import pyodbc
import json

def insert_data(api_response):
    # Define the connection parameters
    server = 'your_server_name'
    database = 'your_database_name'
    conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

    try:
        # Establish a connection
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Extract data from the API response
        data = json.loads(api_response)
        jobs = data['SearchResult']['SearchResultItems']

        # Insert data into the table
        for job in jobs:
            cursor.execute("""
                INSERT INTO job_data (
                    PositionFormattedDescription, UserArea, DepartmentName, PositionURI,
                    PositionTitle, JobCategory, OrganizationName, PositionLocation,
                    PositionRemuneration, JobGrade, PositionStartDate, ApplicationCloseDate,
                    PositionLocationDisplay, ApplyURI, SubAgency, QualificationSummary,
                    PositionOfferingType, PositionSchedule, PublicationStartDate, PositionID,
                    PositionEndDate
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job['MatchedObjectDescriptor']['PositionFormattedDescription'],
                json.dumps(job['UserArea']),
                job['MatchedObjectDescriptor']['DepartmentName'],
                job['MatchedObjectDescriptor']['PositionURI'],
                job['MatchedObjectDescriptor']['PositionTitle'],
                job['MatchedObjectDescriptor']['JobCategory'][0]['Name'] if job['MatchedObjectDescriptor']['JobCategory'] else None,
                job['MatchedObjectDescriptor']['OrganizationName'],
                json.dumps(job['MatchedObjectDescriptor']['PositionLocation']),
                json.dumps(job['MatchedObjectDescriptor']['PositionRemuneration']),
                job['MatchedObjectDescriptor']['JobGrade'][0]['Code'] if job['MatchedObjectDescriptor']['JobGrade'] else None,
                job['MatchedObjectDescriptor']['PositionStartDate'],
                job['MatchedObjectDescriptor']['ApplicationCloseDate'],
                job['MatchedObjectDescriptor']['PositionLocationDisplay'],
                job['MatchedObjectDescriptor']['ApplyURI'][0] if job['MatchedObjectDescriptor']['ApplyURI'] else None,
                job['MatchedObjectDescriptor']['OrganizationName'],
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

    finally:
        # Close the connection
        if conn:
            conn.close()

# Replace 'your_server_name' and 'your_database_name' with your MSSQL Server details
api_response = '''...'''  # Replace with your actual API response
insert_data(api_response)
