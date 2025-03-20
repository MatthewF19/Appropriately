import psycopg2
from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv
from rate import rate_movie
import os

from login import login
from collection import create_collection
from collection import delete_collection
from collection import rename_collection
from search import search_user_by_email
from rate import rate_movie
from social import follow_user
from social import unfollow_user

def commands():
    print("Create a collection:             CC")
    print("List all collections:            LC")
    print("Play collection:                 PC")
    print("Add movie to collection:         AC")
    print("Remove movie from collection:    RMC")
    print("Rename collection:               RNC")
    print("Delete collection:               DC")
    print("Search for a movie:              SM")
    print("Rate a movie:                    RM")
    print("Play movie:                      PM")
    print("Search for user:                 SU")
    print("Follow user:                     FU")
    print("Unfollow user:                   UU")
    print("Exit:                            Q")

def main():
    # load sensitive info
    load_dotenv()
    username = os.getenv('RIT_USERNAME')
    password = os.getenv('RIT_PASSWORD')
    db_name = "p32001_34"

    try:
        with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                                ssh_username=username,
                                ssh_password=password,
                                remote_bind_address=('127.0.0.1', 5432)) as server:
            server.start()
            print("SSH tunnel established")
            params = {
                'database': db_name,
                'user': username,
                'password': password,
                'host': 'localhost',
                'port': server.local_bind_port
            }

            conn = psycopg2.connect(**params)
            curs = conn.cursor()
            print("Database connection established")

            userid = login(conn, curs)

            action = input("What do you want to do?\n-> ")
            while(action != "Q"):
                match action:
                    case "CC":
                        create_collection(conn, curs, userid)
                    case "LC":
                        # (not merged into main yet)
                        # view_collections(conn, curs, userid) 
                        print("NOT IMPLEMENTED")
                    case "PC":
                        print("NOT IMPLEMENTED")
                    case "AC":
                        # (not merged into main yet)
                        # add_movie(conn, curs, userid)
                        print("NOT IMPLEMENTED")
                    case "RMC":
                        # (not merged into main yet)
                        # delete_movie(conn, curs, userid)
                        print("NOT IMPLEMENTED")
                    case "RNC":
                        rename_collection(conn, curs, userid)
                    case "DC":
                        delete_collection(conn, curs, userid)
                    case "SM":
                        print("NOT IMPLEMENTED")
                    case "RM":
                        # TODO make fn prompt for movieid/rating
                        rate_movie(conn, userid, movieid, rating)
                    case "PM":
                        print("NOT IMPLEMENTED")
                    case "SU":
                        # TODO make fn prompt for email
                        search_user_by_email(conn, email)
                    case "FU":
                        # TODO make fn prompt for ids
                        follow_user(conn, frid, fdid)
                    case "UU":
                        unfollow_user(conn, frid, fdid)
                    case "Q":
                        # nop
                        print("", end="") 
                    case _: 
                        commands()

            conn.close()
    except Exception as e:
        print("Connection failed:", e)


if __name__ == '__main__':
    main()
