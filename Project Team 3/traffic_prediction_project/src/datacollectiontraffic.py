import requests
import pymongo
import json
import pandas as pd
import os
import schedule
import time

import math

def get_bounding_box(center_lat, center_lon, distance_km):
    # Radius of the Earth in kilometers
    earth_radius = 6371.0

    # Convert latitude and longitude from degrees to radians
    center_lat_rad = center_lat * (math.pi / 180.0)
    center_lon_rad = center_lon * (math.pi / 180.0)

    # Calculate the latitude range based on the desired distance
    lat_delta = distance_km / earth_radius * (180.0 / math.pi)

    # Calculate the longitude range based on the desired distance
    lon_delta = distance_km / (earth_radius * abs(math.cos(center_lat_rad))) * (180.0 / math.pi)

    # Calculate the bounding box coordinates
    south_lat = center_lat - lat_delta
    west_lon = center_lon - lon_delta
    north_lat = center_lat + lat_delta
    east_lon = center_lon + lon_delta

    return f"{south_lat},{west_lon},{north_lat},{east_lon}"


def fetch_and_export_traffic_data():
    print("Running data collection code.......")
    # Define your Bing Maps API key
    bing_maps_key = "AhW5_RFhg-QzrA95-uhpppal-B-eWgwCocRhhlmnB_ZYJniwj3cgHICbv3dXGn6F"

    # Define the parameters for the geocoding API request
    location = "Kitchener, Ontario, Canada"
    urlLoc = f"http://dev.virtualearth.net/REST/v1/Locations/{location}?key={bing_maps_key}"

    # Make an API request to Bing Maps for the coordinates of Kitchener
    responseLoc = requests.get(urlLoc)

    if responseLoc.status_code == 200:
        location_data = responseLoc.json()

        # Extract latitude and longitude from the response
        coordinates = location_data["resourceSets"][0]["resources"][0]["point"]["coordinates"]
        kitchener_coordinates = f"{coordinates[0]},{coordinates[1]}"
        kitchener_coordinates = get_bounding_box(coordinates[0],coordinates[1],25)
        
        # Use the obtained coordinates for the traffic incidents query
        mapArea = kitchener_coordinates  # Use these coordinates for the traffic incidents query
        severities = ""  # Replace with desired severities
        incidentTypes = "1,2,3,4,5"  # Replace with desired incident types

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
    else:
        print("Failed to fetch location data from Bing Maps API.")



    # Schedule the job to run every 5 hours
fetch_and_export_traffic_data()
# schedule.every(5).hours.do(fetch_and_export_traffic_data)

#     # Run the job indefinitely
# while True:
#     schedule.run_pending()
    
#     time.sleep(1)

