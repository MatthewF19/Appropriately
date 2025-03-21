def create_collection(conn, curs, userid):
    print("\nCreating a movie collection!")
    name = input("What would you like to name the collection? ")

    curs.execute("INSERT INTO collection(user_id, name) VALUES(%s, %s)", (userid, name))
    conn.commit()

    print("Collection successfully added!")

    curs.execute("SELECT id FROM collection WHERE user_id=%s AND name=%s", (userid, name))
    return curs.fetchone()[0]


def delete_collection(conn, curs, userid):
    print("\nDeleting a movie collection!")
    name = input("Enter the name of the collection to delete: ")

    curs.execute("SELECT id FROM collection WHERE user_id=%s AND name=%s", (userid, name))
    collection = curs.fetchone()

    if collection is None:
        print("Collection not found!")
        return

    curs.execute("DELETE FROM collection WHERE user_id=%s AND name=%s", (userid, name))
    conn.commit()
    print("Collection deleted successfully!")


def rename_collection(conn, curs, userid):
    print("\nRenaming a movie collection!")
    old_name = input("Enter the current name of the collection you wish to rename: ")

    curs.execute("SELECT id FROM collection WHERE user_id=%s AND name=%s", (userid, old_name))
    collection = curs.fetchone()

    if collection is None:
        print("Collection not found!")
        return

    new_name = input("Enter the name you'd like to rename the collection to: ")

    curs.execute("UPDATE collection SET name=%s WHERE user_id=%s AND name=%s", (new_name, userid, old_name))
    conn.commit()
    print("Collection renamed successfully!")


def view_collections(conn, curs, userid):
    query = """
    SELECT c.name, COUNT(m.id) AS numMovies, COALESCE(SUM(m.length), 0)
    FROM collection c
    LEFT JOIN has_movie hm ON c.id=hm.collectionid
    LEFT JOIN movie m ON hm.movieid=m.id
    WHERE c.user_id=%s
    GROUP BY c.name
    ORDER BY c.name
    """

    curs.execute(query, (userid,))
    collections = curs.fetchall()

    for collection in collections:
        print(collection[0], collection[1], str(collection[2]//60) + ":" + str(collection[2]%60))


def add_movie(conn, curs, userid):
    collection_name = input("Enter the name of the collection you would like to add to: ")
    curs.execute("SELECT id FROM collection WHERE user_id=%s AND name=%s", (userid, collection_name))
    collection = curs.fetchone()
    if collection is None:
        print("Collection not found!")
        return

    movie_name = input("Enter the name of the movie you would like to add to : ")
    curs.execute("SELECT id from movie WHERE title ILIKE %s", (movie_name,))
    movie = curs.fetchone()
    if movie is None:
        print("Movie not found!")
        return

    curs.execute("SELECT movieid FROM has_movie WHERE collectionid=%s AND movieid=%s", (collection, movie))
    check = curs.fetchone()
    if check is None:
        curs.execute("INSERT INTO has_movie(collectionid, movieid) VALUES(%s, %s)", (collection, movie))
        conn.commit()
    else:
        print("Movie already added!")


def delete_movie(conn, curs, userid):
    collection_name = input("Enter the name of the collection you would like to delete from: ")
    curs.execute("SELECT id FROM collection WHERE user_id=%s AND name=%s", (userid, collection_name))
    collection = curs.fetchone()
    if collection is None:
        print("Collection not found!")
        return

    movie_name = input("Enter the name of the movie you would like to remove : ")
    curs.execute("SELECT id from movie WHERE title ILIKE %s", (movie_name,))
    movie = curs.fetchone()
    if movie is None:
        print("Movie not found!")
        return

    curs.execute("SELECT movieid FROM has_movie WHERE collectionid=%s AND movieid=%s", (collection, movie))
    check = curs.fetchone()
    if check is None:
        print("Movie not in collection!")
        return
    curs.execute("DELETE FROM has_movie WHERE collectionid=%s and movieid=%s", (collection, movie))
    conn.commit()
