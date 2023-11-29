import requests
import pymongo
import json
import pandas as pd
import os

# Define your Bing Maps API key
bing_maps_key = "AhW5_RFhg-QzrA95-uhpppal-B-eWgwCocRhhlmnB_ZYJniwj3cgHICbv3dXGn6F"

# Define the parameters for the API request
mapArea = "37,-105,45,-94"  # Replace with the desired map area
severities = "1,2,3"  # Replace with desired severities
incidentTypes = ""  # Replace with desired incident types

# Define the URL for the Bing Maps Traffic Incidents API
url = f"http://dev.virtualearth.net/REST/v1/Traffic/Incidents/{mapArea}/?severity={severities}&type={incidentTypes}&key={bing_maps_key}"

# Make an API request to Bing Maps Traffic Incidents API
response = requests.get(url)

if response.status_code == 200:
    api_data = response.json()

    # Extract and transform the data as needed
    extracted_data = []
    resource_set = api_data.get("resourceSets", [])[0]
    for resource in resource_set.get("resources", []):
        extracted_data.append({
            "point": resource.get("point", {}),
            "description": resource.get("description"),
            "start": resource.get("start"),
            "end": resource.get("end"),
            "incidentId": resource.get("incidentId"),
            "lastModified": resource.get("lastModified"),
            "roadClosed": resource.get("roadClosed"),
            "severity": resource.get("severity"),
            "severityScore": resource.get("severityScore"),
            "toPoint": resource.get("toPoint", {}),
            "type": resource.get("type"),
            "verified": resource.get("verified"),
            "isEndTimeBackfilled": resource.get("isEndTimeBackfilled"),
            "title": resource.get("title"),
            "alertCCodes": resource.get("alertCCodes", []),
            "eventList": resource.get("eventList", []),
            "icon": resource.get("icon"),
            "isJamcident": resource.get("isJamcident"),
        })


    # Destination directory for CSV export
    export_directory = "Project Team 3/traffic_prediction_project/datasets"

    # Create the directory if it doesn't exist
    if not os.path.exists(export_directory):
        os.makedirs(export_directory)

    # Destination file for CSV export
    csv_file = os.path.join(export_directory, "traffic_incident_data.csv")

    # Set up a MongoDB connection
    client = pymongo.MongoClient("mongodb://localhost:27017/")  
    db = client["traffic"]  
    collection = db["traffic_incidents"]  
    
    # Insert data into MongoDB
    collection.insert_many(extracted_data)
    print("Data inserted successfully in Mongo DB!")


    # Retrieve data from the collection
    data = list(collection.find())

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)

    # Export the data to a CSV file
    df.to_csv(csv_file, index=False)

    client.close()
else:
    print("Failed to fetch data from the API.")
