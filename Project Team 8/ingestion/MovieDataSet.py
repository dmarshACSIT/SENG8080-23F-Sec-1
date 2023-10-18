import configparser
import csv
import os
import mysql.connector
import traceback


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


def insertDb(csv_file_path,cursor,conn):
    
    with open(csv_file_path, 'r',encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            print(
                row['name'], row['rating'], row['genre'], row['year'], row['released'].split(" ")[0], 
                row['score'], row['votes'], row['director'], row['writer'], row['star'], 
                row['country'], row['budget'], row['gross'], row['company'], row['runtime']
            )
            insert_query = """
            INSERT INTO movies (name, rating, genre, year, released, score, votes, director, writer, star, country, budget, gross, company, runtime)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (
                row['name'], row['rating'], row['genre'], row['year'], row['released'].split(" ")[0], 
                row['score'], row['votes'], row['director'], row['writer'], row['star'], 
                row['country'], row['budget'], row['gross'], row['company'], row['runtime']
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

