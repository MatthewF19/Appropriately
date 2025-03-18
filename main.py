import psycopg2
from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv
from rate import rate_movie
import os

from login import login

def main():
    # load sensitive info
    load_dotenv()
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    dbName = "p32001_34"

    try:
        with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                                ssh_username=username,
                                ssh_password=password,
                                remote_bind_address=('127.0.0.1', 5432)) as server:
            server.start()
            print("SSH tunnel established")
            params = {
                'database': dbName,
                'user': username,
                'password': password,
                'host': 'localhost',
                'port': server.local_bind_port
            }

            conn = psycopg2.connect(**params)
            curs = conn.cursor()
            print("Database connection established")

            userid = login(conn, curs)
            print(userid)

            conn.close()
    except:
        print("Connection failed")

if __name__ == '__main__':
    main()
