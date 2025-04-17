import psycopg2
from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv
import os

from login import login
from collection import create_collection
from collection import delete_collection
from collection import rename_collection
from collection import num_collections
from collection import view_collections
from collection import add_movie
from collection import delete_movie
from search import search_user_by_email
from rate import rate_movie
from social import follow_user
from social import unfollow_user
from social import get_follower_count
from social import get_following_count
from movies import search_movie
from top_movies import top_10_movies_by_rates
from top_movies import top_10_movies_by_watches
from watch import watch
from rate import rate_movie
from top_movies import top5_new_releases
from top_movies import top20_movies_currently
from top_movies import most_popular_followers
from top_movies import watch_history_recs


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
    print("Get follower count:              GFRC")
    print("Get following count:             GFNC")
    print("Get Top 10 Movies by ratings:    T10R")
    print("Get Top 10 Movies by watches:    T10W")
    print("Unfollow user:                   UU")
    print("Get top 5 new releases:          T5N")
    print("Get top 20 movies currently      T20C")
    print("Get movies from followers        PF")
    print("Get movies from watch history    WHR")
    print("Exit:                            Q")


def run_action(conn, curs, userid, action):
    match action.upper():
        case "CC":
            create_collection(conn, curs)
        case "LC":
            view_collections(conn, curs, userid)
        case "NC":
            num_collections(conn, curs)
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
            rate_movie(conn, userid)
        case "PM":
            watch(conn, userid, "movie")
        case "SU":
            search_user_by_email(conn)
        case "FU":
            follow_user(conn, userid)
        case "GFRC":
            get_follower_count(conn, userid)
        case "GFNC":
            get_following_count(conn, userid)
        case "T10R":
            top_10_movies_by_rates(conn)
        case "T10W":
            top_10_movies_by_watches(conn)
        case "UU":
            unfollow_user(conn, userid)
        case "T5N":
            top5_new_releases(curs)
        case "T20C":
            top20_movies_currently(curs)
        case "PF":
            most_popular_followers(curs, userid)
        case "WHR":
            watch_history_recs(curs, userid)
        case "Q":
            # nop
            return "exit"
        case _:
            commands()


def prompt_loop(conn, curs, userid):
    action = input("What would you like to do? ")
    while run_action(conn, curs, userid, action) != "exit":
        action = input("-> ")


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

            prompt_loop(conn, curs, userid)

            conn.close()
    except Exception as e:
        print("Connection failed:", e)


if __name__ == '__main__':
    main()
