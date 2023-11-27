import configparser
import csv
import os
import mysql.connector
import traceback
from datetime import datetime



def load_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    datasetPath = config['DatasetPaths']['movieDataset']
    fpath = os.path.abspath(datasetPath)

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

   
def read_csv(file_path):
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        data.append(header)
        for row in reader:
            data.append(row)
    return data
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False
    
def clean_currency(value):
    # Convert currency values to integers (remove dollar signs, commas, etc.)
    if value:
        return int(''.join(filter(str.isdigit, value)))
    else:
        return None
    
def clean_text(value):
    # Convert text to lowercase and remove leading/trailing whitespaces
    return value.lower().strip() if value else None

def format_date(value):
    # Convert date string to MySQL date format
    # Modify based on the actual date format in your dataset
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return None

def clean_data(row):
    # Example data cleaning steps, modify as needed
    if any(value is None or value == '' for value in row.values()):
        # Skip rows with missing values
        return None

    row['year'] = int(row['year']) if row['year'].isdigit() else None
    row['score'] = float(row['score']) if is_float(row['score']) else None
    row['votes'] = int(row['votes']) if is_integer(row['votes']) else None
    row['budget'] = clean_currency(row['budget'])
    row['gross'] = clean_currency(row['gross'])
    
    # Cleaning text data
    row['name'] = clean_text(row['name'])
    row['director'] = clean_text(row['director'])
    row['writer'] = clean_text(row['writer'])
    row['star'] = clean_text(row['star'])
    row['company'] = clean_text(row['company'])
    
    # Date formatting
    row['released'] = format_date(row['released'])

    # Add more cleaning steps as needed

    return row

def drop_missing_values(data):
    # Drop rows with missing values
    cleaned_data = [clean_data(row) for row in data if clean_data(row) is not None]
    return cleaned_data

def insertDb(csv_file_path,cursor,conn):
    
    with open(csv_file_path, 'r',encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = [row for row in csv_reader]
        cleaned_data = drop_missing_values(data)

        
        for row in cleaned_data:
            cleaned_row = clean_data(row)
            print(cleaned_row)
            insert_query = """
            INSERT INTO movies (name, rating, genre, year, released, score, votes, director, writer, star, country, budget, gross, company, runtime)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (
                cleaned_row['name'], cleaned_row['rating'], cleaned_row['genre'], cleaned_row['year'],
                cleaned_row['released'].split(" ")[0], cleaned_row['score'], cleaned_row['votes'],
                cleaned_row['director'], cleaned_row['writer'], cleaned_row['star'], cleaned_row['country'],
                cleaned_row['budget'], cleaned_row['gross'], cleaned_row['company'], cleaned_row['runtime']
            ))
        conn.commit()

    cursor.close()
    conn.close()



def main():
    try:
        config_file = 'appConfig.ini'
        fpath, db_config = load_config(config_file)
        #csv_data = read_csv(fpath)
        conn,cursor = init_conn(db_config)
        insertDb(fpath,cursor,conn)
         
    except Exception as e:
        print(f"An error occurred: {e}")
        print(traceback.print_exc())

if __name__ == "__main__":
    main()

