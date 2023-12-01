"""This program does the trend analysis on musical attributes for an artist over a time

    by establishing API connection to Spotify data source

    Fetch the track data based on year

    Stores the data in MySQL DB
   """
import pandas as pd
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import mysql.connector

# Spotify Credentials
CLIENT_ID = "91106b1989144f538ad4fbe1827a96d7"
CLIENT_SECRET = "469e4a0d56d74349b11edfc726ed4596"

# Establish API connection using Spotify Credentials
def create_spotify_client():
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Returns the audio features from the returned API response
def get_audio_features(sp, track_uri):
    return sp.audio_features(track_uri)

# Creates the track dataframe from the returned API response
def create_track_dataframe(track_features):
    if track_features:
        track_name = track_features.get('name', 'Unknown')
        artist_name = track_features.get('artists', [{'name': 'Unknown'}])[0]['name']
        df = pd.DataFrame({
            'Track Name': [track_name],
            'Artist Name': [artist_name],
            'Acousticness': [track_features['acousticness']],
            'Danceability': [track_features['danceability']],
            'Energy': [track_features['energy']],
            'Instrumentalness': [track_features['instrumentalness']],
            'Liveness': [track_features['liveness']],
            'Loudness': [track_features['loudness']],
            'Speechiness': [track_features['speechiness']],
            'Tempo': [track_features['tempo']],
            'Valence': [track_features['valence']]
        })
        return df
    else:
        return None

# Search API Request based on year
def search_tracks_by_year(sp, year):
    search_query = f"year:{year}"
    results = sp.search(q=search_query, type="track", limit=50)
    return results

# Creates the track dataframe from the returned API response
def create_audio_features_dataframe(results, sp):
    audio_features_df = pd.DataFrame(columns=[
        'Track Name', 'Artist Name', 'Acousticness', 'Danceability',
        'Energy', 'Instrumentalness', 'Liveness', 'Loudness',
        'Speechiness', 'Tempo', 'Valence'
    ])

    # Iterate through the search results and retrieve audio features for each track
    for track in results['tracks']['items']:
        # Get the Spotify URI of the track
        track_uri = track['uri']

        # Get audio features for the track
        audio_features = sp.audio_features(track_uri)

        if audio_features:
            # Extract relevant audio features from the first item in the list (assuming one track)
            track_features = audio_features[0]

            # Create a DataFrame with the current track's audio features
            if track_features is not None:
                current_track_df = pd.DataFrame({
                    'Track Name': [track['name']],
                    'Artist Name': [track['artists'][0]['name']],
                    'Acousticness': [track_features['acousticness']],
                    'Danceability': [track_features['danceability']],
                    'Energy': [track_features['energy']],
                    'Instrumentalness': [track_features['instrumentalness']],
                    'Liveness': [track_features['liveness']],
                    'Loudness': [track_features['loudness']],
                    'Speechiness': [track_features['speechiness']],
                    'Tempo': [track_features['tempo']],
                    'Valence': [track_features['valence']]
                })

            # Concatenate the current track's DataFrame to the main audio_features_df
            audio_features_df = pd.concat([audio_features_df, current_track_df], ignore_index=True)

        # Display the dataset
        print(audio_features_df)
    
    return audio_features_df

# Establish MySQL DB Connection
def connect_to_database(host, user, password, database):
    return mysql.connector.connect(host=host, user=user, password=password, database=database)

# Create audio_feature DB table if it does not exists
def create_audio_features_table(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS audio_features (
        id INT AUTO_INCREMENT PRIMARY KEY,
        track_name VARCHAR(255),
        artist_name VARCHAR(255),
        acousticness FLOAT,
        danceability FLOAT,
        energy FLOAT,
        instrumentalness FLOAT,
        liveness FLOAT,
        loudness FLOAT,
        speechiness FLOAT,
        tempo FLOAT,
        valence FLOAT,
        year INT
    )
    """
    cursor = connection.cursor()
    cursor.execute(create_table_query)

def clean_data_for_insertion(audio_features_df):
    # Perform data cleaning and validation steps here
  
    # Handling Missing Values
    audio_features_df.fillna(0, inplace=True)  # Replace missing values with 0 (assuming appropriate for numeric fields)
    
    # Ensure data types are correct
    audio_features_df['Track Name'] = audio_features_df['Track Name'].astype(str)
    audio_features_df['Artist Name'] = audio_features_df['Artist Name'].astype(str)
    audio_features_df['Acousticness'] = audio_features_df['Acousticness'].astype(float)
    audio_features_df['Danceability'] = audio_features_df['Danceability'].astype(float)
    audio_features_df['Energy'] = audio_features_df['Energy'].astype(float)
    audio_features_df['Instrumentalness'] = audio_features_df['Instrumentalness'].astype(float)
    audio_features_df['Liveness'] = audio_features_df['Liveness'].astype(float)
    audio_features_df['Speechiness'] = audio_features_df['Speechiness'].astype(float)
    audio_features_df['Tempo'] = audio_features_df['Tempo'].astype(float)
    audio_features_df['Valence'] = audio_features_df['Valence'].astype(float)
    
    # Data validation
    audio_features_df['Acousticness'] = audio_features_df['Acousticness'].apply(lambda x: min(max(0, x), 1))
    audio_features_df['Danceability'] = audio_features_df['Danceability'].apply(lambda x: min(max(0, x), 1))
    audio_features_df['Energy'] = audio_features_df['Energy'].apply(lambda x: min(max(0, x), 1))
    audio_features_df['Instrumentalness'] = audio_features_df['Instrumentalness'].apply(lambda x: min(max(0, x), 1))
    audio_features_df['Liveness'] = audio_features_df['Liveness'].apply(lambda x: min(max(0, x), 1))
    audio_features_df['Speechiness'] = audio_features_df['Speechiness'].apply(lambda x: min(max(0, x), 1))
    audio_features_df['Valence'] = audio_features_df['Valence'].apply(lambda x: min(max(0, x), 1))
    audio_features_df['Tempo'] = audio_features_df['Tempo'].apply(lambda x: min(max(0, x), 300))  # Limit tempo between 0 and 300 BPM
    
    return audio_features_df

# Inserting the audio feature data into the DB table
def insert_audio_features_data(connection, audio_features_df, year):
    clean_audio_features_df = clean_data_for_insertion(audio_features_df)
    insert_query = """
    INSERT INTO audio_features (
        track_name, artist_name, acousticness, danceability, energy,
        instrumentalness, liveness, loudness, speechiness, tempo, valence, year
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor = connection.cursor()
    for index, row in clean_audio_features_df.iterrows():
        values = (
            row['Track Name'],
            row['Artist Name'],
            row['Acousticness'],
            row['Danceability'],
            row['Energy'],
            row['Instrumentalness'],
            row['Liveness'],
            row['Loudness'],
            row['Speechiness'],
            row['Tempo'],
            row['Valence'],
            year
        )
        cursor.execute(insert_query, values)
    connection.commit()

# Main implementation method
def main():
    sp = create_spotify_client()
 
    host = 'localhost'
    user = 'root'
    password = 'password'
    database = 'case_study_spotify_db'
    connection = connect_to_database(host, user, password, database)
    create_audio_features_table(connection)

    year = '2021'
    results_2021 = search_tracks_by_year(sp, year)
    audio_features_df = create_audio_features_dataframe(results_2021, sp)
    insert_audio_features_data(connection, audio_features_df, year)

    year = '2022'
    results_2022 = search_tracks_by_year(sp, year)
    audio_features_df = create_audio_features_dataframe(results_2022, sp)
    insert_audio_features_data(connection, audio_features_df, year)
    connection.close()

# Main Initial Execution
if __name__ == "__main__":
    main()
