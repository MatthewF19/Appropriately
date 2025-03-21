import psycopg2
from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv
import os

from login import login
from collection import create_collection
from collection import delete_collection
from collection import rename_collection
from collection import view_collections
from collection import add_movie
from collection import delete_movie
from search import search_user_by_email
from rate import rate_movie
from social import follow_user
from social import unfollow_user
from movies import search_movie
from watch import watch
from rate import rate_movie


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


def prompt(conn, curs, userid):
    action = input("What do you want to do?\n-> ").upper()
    while action != "Q":
        match action:
            case "CC":
                create_collection(conn, curs, userid)
            case "LC":
                view_collections(conn, curs, userid) 
            case "PC":
                watch(conn, userid, "collection")
            case "AC":
                add_movie(conn, curs, userid)
            case "RMC":
                delete_movie(conn, curs, userid)
            case "RNC":
                rename_collection(conn, curs, userid)
            case "DC":
                delete_collection(conn, curs, userid)
            case "SM":
                search_movie(conn)
            case "RM":
                rate_movie(conn)
            case "PM":
                watch(conn, userid, "movie")
            case "SU":
                search_user_by_email(conn)
            case "FU":
                follow_user(conn)
            case "UU":
                unfollow_user(conn)
            case "Q":
                # nop
                print("", end="") 
            case _: 
                commands()
    
        action = input("-> ").upper()


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

            prompt(conn, curs, userid)

            conn.close()
    except Exception as e:
        print("Connection failed:", e)


if __name__ == '__main__':
    main()
