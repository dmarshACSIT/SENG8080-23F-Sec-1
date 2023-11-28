import sqlite3,json

# Connection SQLite database
conn = sqlite3.connect('property_ownership.db')
cursor = conn.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS property_table (
    id INTEGER PRIMARY KEY,
    type TEXT,
    geometry_type TEXT,
    geometry_coordinates_0 REAL,
    geometry_coordinates_1 REAL,
    properties_OBJECTID INTEGER,
    properties_PROPERTY_UNIT_ID INTEGER,
    properties_CIVIC_NO INTEGER,
    properties_STREET TEXT,
    properties_UNIT TEXT,
    properties_OWNERNAME TEXT,
    properties_GlobalID TEXT
)
"""
cursor.execute(create_table_query)

#JSON data
json_file_path = "property_ownership.json"

#reading data from json file
with open(json_file_path, "r") as json_file:
    data = json.load(json_file)

#extracting data
features = data.get("features", [])

# Looping through
for feature in features:
    properties = feature.get("properties", {})
    geometry = feature.get("geometry", {})

    insert_data_query = """
    INSERT INTO property_table (type, geometry_type, geometry_coordinates_0, geometry_coordinates_1, properties_OBJECTID, properties_PROPERTY_UNIT_ID, properties_CIVIC_NO, properties_STREET, properties_UNIT, properties_OWNERNAME, properties_GlobalID)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    values = (
        feature.get("type"),
        geometry.get("type"),
        geometry.get("coordinates")[0] if "coordinates" in geometry else None,
        geometry.get("coordinates")[1] if "coordinates" in geometry else None,
        properties.get("OBJECTID"),
        properties.get("PROPERTY_UNIT_ID"),
        properties.get("CIVIC_NO"),
        properties.get("STREET"),
        properties.get("UNIT"),
        properties.get("OWNERNAME"),
        properties.get("GlobalID")
    )

    cursor.execute(insert_data_query, values)

conn.commit()
conn.close()
