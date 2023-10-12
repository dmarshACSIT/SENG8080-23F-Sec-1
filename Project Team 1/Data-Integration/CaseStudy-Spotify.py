import pandas as pd
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import mysql.connector

# Spotify Credentials
CLIENT_ID = "91106b1989144f538ad4fbe1827a96d7"
CLIENT_SECRET = "469e4a0d56d74349b11edfc726ed4596"

def create_spotify_client():
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_audio_features(sp, track_uri):
    return sp.audio_features(track_uri)

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

def search_tracks_by_year(sp, year):
    search_query = f"year:{year}"
    results = sp.search(q=search_query, type="track")
    return results

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


def connect_to_database(host, user, password, database):
    return mysql.connector.connect(host=host, user=user, password=password, database=database)

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

def insert_audio_features_data(connection, audio_features_df, year):
    insert_query = """
    INSERT INTO audio_features (
        track_name, artist_name, acousticness, danceability, energy,
        instrumentalness, liveness, loudness, speechiness, tempo, valence, year
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor = connection.cursor()
    for index, row in audio_features_df.iterrows():
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

if __name__ == "__main__":
    main()
