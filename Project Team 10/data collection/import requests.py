import requests,json

#API endpoint URL
api_url = 'https://services1.arcgis.com/qAo1OsXi67t7XgmS/arcgis/rest/services/Property_Ownership_Public/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson'
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    #print(data)
    with open('property_ownership.json', 'w') as json_file:
          json.dump(data, json_file, indent=4)

else:
    print(f"Error: Unable to fetch data from the API. Status code: {response.status_code}")

