import psycopg2
import random
from faker import Faker
from datetime import datetime, timedelta
from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv
import os

fake = Faker()

# ----------------------------
# DATA GENERATION FUNCTIONS
# ----------------------------

def generate_movies(num):
    movies = []
    start_id = 10000
    for i in range(num):
        movie_id = start_id + i
        title = fake.sentence(nb_words=3).rstrip('.')
        length = random.randint(80, 180)
        MPAA = random.choice(['G', 'PG', 'PG-13', 'R', 'X', 'NR'])
        movies.append((movie_id, title, length, MPAA))
    return movies

def generate_platforms():
    platform_list = [
        'Netflix', 'Hulu', 'DisneyPlus', 'Peacock', 'Max', 'Amazon Prime Video',
        'Apple TV+', 'Paramount+', 'HBO Max', 'Discovery+', 'Crunchyroll', 'BritBox',
        'YouTube Premium', 'Starz', 'Showtime', 'AMC+', 'Sling TV', 'Tubi', 'Pluto TV'
    ]
    platforms = []
    start_id = 10000
    for name in platform_list:
        platforms.append((start_id, name))
        start_id += 1
    return platforms

def generate_releases(movies, platforms):
    releases = []
    for movie in movies:
        movie_id = movie[0]
        platform_id = random.choice(platforms)[0]
        release_date = fake.date_between(start_date='-30y', end_date='today')
        releases.append((movie_id, platform_id, release_date))
    return releases

def generate_genres():
    genre_list = [
        'Action', 'Comedy', 'Drama', 'Horror', 'Romcom', 'Anime', 'Documentary',
        'Sci-Fi', 'Thriller', 'Adventure', 'Crime', 'Mystery', 'Fantasy'
    ]
    genres = []
    start_id = 10000
    for g in genre_list:
        genres.append((start_id, g))
        start_id += 1
    return genres

def generate_genre_of(movies, genres):
    genre_of = []
    for movie in movies:
        movie_id = movie[0]
        genre_id = random.choice(genres)[0]
        genre_of.append((movie_id, genre_id))
    return genre_of

def generate_studios(num):
    studios = []
    start_id = 10000
    for i in range(num):
        name = fake.company()
        address = fake.address().replace('\n', ', ')
        studios.append((start_id, name, address))
        start_id += 1
    return studios

def generate_movie_made_in_studio(movies, studios):
    mms = []
    for movie in movies:
        movie_id = movie[0]
        studio_id = random.choice(studios)[0]
        mms.append((movie_id, studio_id))
    return mms

def generate_persons(num):
    persons = []
    start_id = 10000
    for i in range(num):
        first = fake.first_name()
        last = fake.last_name()
        dob = fake.date_of_birth(minimum_age=20, maximum_age=80)
        persons.append((start_id, first, last, dob))
        start_id += 1
    return persons

def generate_acts_in(movies, persons):
    acts_in = []
    for movie in movies:
        movie_id = movie[0]
        person_id = random.choice(persons)[0]
        character = fake.first_name()
        acts_in.append((person_id, movie_id, character))
    return acts_in

def generate_directs(movies, persons):
    directs = []
    for movie in movies:
        movie_id = movie[0]
        person_id = random.choice(persons)[0]
        directs.append((movie_id, person_id))
    return directs

def generate_users(num):
    users = []
    start_id = 10000
    fake.unique.clear()
    for i in range(num):
        username_val = fake.unique.user_name()
        password_val = fake.password()
        creation = fake.date_time_between(start_date='-5y', end_date='now')
        last_access = creation + timedelta(days=random.randint(0, 1000))
        first = fake.first_name()
        last = fake.last_name()
        email = fake.unique.email()
        dob = fake.date_of_birth(minimum_age=18, maximum_age=80)
        users.append((start_id, username_val, password_val,
                      creation.strftime('%Y-%m-%d %H:%M:%S'),
                      last_access.strftime('%Y-%m-%d %H:%M:%S'),
                      first, last, email, dob))
        start_id += 1
    return users

def generate_rates(users, movies, num):
    rates = []
    for i in range(num):
        user_id = random.choice(users)[0]
        movie_id = random.choice(movies)[0]
        rating = round(random.uniform(0, 5), 1)
        rates.append((user_id, movie_id, rating))
    return rates

def generate_watches(users, movies, num):
    watches = []
    for i in range(num):
        start_dt = fake.date_time_this_decade()
        user_id = random.choice(users)[0]
        movie_id = random.choice(movies)[0]
        end_dt = start_dt + timedelta(minutes=random.randint(80, 200))
        watches.append((start_dt.strftime('%Y-%m-%d %H:%M:%S'),
                        user_id, movie_id,
                        end_dt.strftime('%Y-%m-%d %H:%M:%S')))
    return watches

def generate_follows(users, num):
    follows = set()
    while len(follows) < num:
        follower = random.choice(users)[0]
        followed = random.choice(users)[0]
        if follower != followed:
            follows.add((follower, followed))
    return list(follows)

def generate_collections(users, num):
    collections = []
    start_id = 10000
    for i in range(num):
        user_id = random.choice(users)[0]
        name = fake.word().capitalize() + " Collection"
        collections.append((start_id, user_id, name))
        start_id += 1
    return collections

def generate_has_movie(collections, movies, num):
    has_movie = []
    for i in range(num):
        collection_id = random.choice(collections)[0]
        movie_id = random.choice(movies)[0]
        has_movie.append((collection_id, movie_id))
    return has_movie

def filter_valid_users(conn, users):
    """ Fetch valid user IDs from the database """
    with conn.cursor() as cur:
        cur.execute('SELECT "id" FROM Users')
        valid_user_ids = {row[0] for row in cur.fetchall()}  # Convert result to a set
    return [user for user in users if user[0] in valid_user_ids]  # Keep only valid users


# ----------------------------
# DATABASE INSERTION FUNCTIONS
# ----------------------------
def batch_insert(conn, query, data, table_name):
    with conn.cursor() as cur:
        cur.executemany(query, data)
    conn.commit()
    print(f"Inserted {len(data)} rows into {table_name}")

# ----------------------------
# MAIN FUNCTION
# ----------------------------
def main():
    # Configuration: adjust numbers as needed
    num_movies = 6000
    num_studios = 6000
    num_persons = 6000
    num_users = 6000
    num_rates = 6000
    num_watches = 6000
    num_follows = 6000
    num_collections = 3000
    num_has_movie = 6000

    # Generate data for each table
    movies = generate_movies(num_movies)
    platforms = generate_platforms()
    releases = generate_releases(movies, platforms)
    genres = generate_genres()
    genre_of = generate_genre_of(movies, genres)
    studios = generate_studios(num_studios)
    movie_made_in_studio = generate_movie_made_in_studio(movies, studios)
    persons = generate_persons(num_persons)
    acts_in = generate_acts_in(movies, persons)
    directs = generate_directs(movies, persons)
    users = generate_users(num_users)
    rates = generate_rates(users, movies, num_rates)
    watches = generate_watches(users, movies, num_watches)
    follows = generate_follows(users, num_follows)
    collections = generate_collections(users, num_collections)
    has_movie = generate_has_movie(collections, movies, num_has_movie)

    # Print generated counts for verification
    print("Generated data counts:")
    print("Movies:", len(movies))
    print("Platforms:", len(platforms))
    print("Releases:", len(releases))
    print("Genres:", len(genres))
    print("Genre_of:", len(genre_of))
    print("Studios:", len(studios))
    print("Movie_made_in_studio:", len(movie_made_in_studio))
    print("Persons:", len(persons))
    print("Acts_in:", len(acts_in))
    print("Directs:", len(directs))
    print("Users:", len(users))
    print("Rates:", len(rates))
    print("Watches:", len(watches))
    print("Follows:", len(follows))
    print("Collections:", len(collections))
    print("Has_movie:", len(has_movie))

    load_dotenv()
    ssh_username = os.getenv('USERNAME')
    ssh_password = os.getenv('PASSWORD')
    dbName = "p32001_34"

    try:
        with SSHTunnelForwarder(
            ('starbug.cs.rit.edu', 22),
            ssh_username=ssh_username,
            ssh_password=ssh_password,
            remote_bind_address=('127.0.0.1', 5432),
            allow_agent=False
        ) as server:
            server.start()
            print("SSH tunnel established")

            params = {
                'database': dbName,
                'user': ssh_username,
                'password': ssh_password,
                'host': 'localhost',
                'port': server.local_bind_port
            }
            conn = psycopg2.connect(**params)
            print("Database connection established")

            # Insert data using upsert to avoid duplicates
            batch_insert(conn,
                'INSERT INTO Movie ("id", "title", "length", "mpaa") VALUES (%s, %s, %s, %s) ON CONFLICT ("id") DO NOTHING',
                movies, "Movie")
            batch_insert(conn,
                'INSERT INTO Platform ("id", "name") VALUES (%s, %s) ON CONFLICT ("id") DO NOTHING',
                platforms, "Platform")
            batch_insert(conn,
                'INSERT INTO Release ("movieid", "platformid", "release_date") VALUES (%s, %s, %s) ON CONFLICT DO NOTHING',
                releases, "Release")
            batch_insert(conn,
                'INSERT INTO Genre ("id", "name") VALUES (%s, %s) ON CONFLICT ("id") DO NOTHING',
                genres, "Genre")
            batch_insert(conn,
                'INSERT INTO Genre_of ("movieid", "genreid") VALUES (%s, %s) ON CONFLICT DO NOTHING',
                genre_of, "Genre_of")
            batch_insert(conn,
                'INSERT INTO Studio ("id", "name", "address") VALUES (%s, %s, %s) ON CONFLICT ("id") DO NOTHING',
                studios, "Studio")
            batch_insert(conn,
                'INSERT INTO Movie_made_in_studio ("movie_id", "studio_id") VALUES (%s, %s) ON CONFLICT DO NOTHING',
                movie_made_in_studio, "Movie_made_in_studio")
            batch_insert(conn,
                'INSERT INTO Person ("id", "first_name", "last_name", "dob") VALUES (%s, %s, %s, %s) ON CONFLICT ("id") DO NOTHING',
                persons, "Person")
            batch_insert(conn,
                'INSERT INTO Acts_in ("personid", "movieid", "character") VALUES (%s, %s, %s) ON CONFLICT DO NOTHING',
                acts_in, "Acts_in")
            batch_insert(conn,
                'INSERT INTO Directs ("movie_id", "person_id") VALUES (%s, %s) ON CONFLICT DO NOTHING',
                directs, "Directs")
            batch_insert(conn,
                         'INSERT INTO Users ("id", "username", "password", "creationdate", "lastaccessdate", "firstname", "lastname", "email", "dob") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING',
                         users, "Users")

            users = filter_valid_users(conn, users)

            rates = generate_rates(users, movies, num_rates)

            batch_insert(conn,
                'INSERT INTO Rates ("userid", "movieid", "rating") VALUES (%s, %s, %s) ON CONFLICT DO NOTHING',
                rates, "Rates")
            batch_insert(conn,
                'INSERT INTO Watches ("startdate", "userid", "movieid", "enddate") VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING',
                watches, "Watches")
            batch_insert(conn,
                'INSERT INTO Follow ("followerid", "followedid") VALUES (%s, %s) ON CONFLICT DO NOTHING',
                follows, "Follow")
            # batch_insert(conn,
            #     'INSERT INTO Collection ("id", "user_id", "name") VALUES (%s, %s, %s) ON CONFLICT ("id") DO NOTHING',
            #     collections, "Collection")
            batch_insert(conn,
                'INSERT INTO Has_movie ("collectionid", "movieid") VALUES (%s, %s) ON CONFLICT DO NOTHING',
                has_movie, "Has_movie")

            conn.close()
            print("Data loading complete.")
    except Exception as e:
        print("Connection failed:", e)

if __name__ == '__main__':
    main()