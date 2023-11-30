import csv
import os
import mysql.connector
import configparser
from datetime import datetime

def load_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    datasetPath = config['DatasetPaths']['extractPath']
    fpath = os.path.abspath(datasetPath)
    print(fpath)

    db_config = {
        'host': config['dbconnection']['host'],
        'user': config['dbconnection']['user'],
        'password': config['dbconnection']['password'],
        'database': config['dbconnection']['database']
    }

    return fpath, db_config

def init_conn(db_config):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    return conn, cursor

def extract_and_save_to_csv(conn, cursor, csv_filename):
    
    
    print("in here")
    with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
        print("here")
        csv_writer = csv.writer(csvfile)

        # Write the header
        csv_writer.writerow(['id','name', 'rating', 'genre', 'year', 'released', 'score', 'votes',
                             'director', 'writer', 'star', 'country', 'budget', 'gross', 'company', 'runtime'])

        # Execute the SELECT query
        query = "SELECT * FROM movies;"
        cursor.execute(query)

        # Fetch all rows from the result
        rows = cursor.fetchall()
        # Write each row to the CSV file
        csv_writer.writerows(rows)

def main():
    config_file = 'appConfig.ini'
    
    # Load configuration and initialize database connection
    fpath, db_config = load_config(config_file)
    conn, cursor = init_conn(db_config)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    csv_filename = f'{fpath}\\movies_data_{timestamp}.csv'
    print(csv_filename)
    try:
        print("In try")
        # Extract data from the database and save to CSV
        extract_and_save_to_csv(conn, cursor, csv_filename)
        
        print(f'Data extracted and saved to {csv_filename}')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        # Close the database connection
        conn.close()

if __name__ == "__main__":
    main()
