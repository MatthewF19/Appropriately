def rate_movie(conn, user_id):
    movie_name = input("Enter the movie name: ")

    with conn.cursor() as cursor:
        cursor.execute(
            'SELECT "id", "title" FROM Movie WHERE "title" ILIKE %s ORDER BY "title" ASC LIMIT 1',
            (f"%{movie_name}%",)
        )
        result = cursor.fetchone()
    if not result:
        print("No movies found with that name")
        return
    movie_id, title = result
    rating = int(input("Enter your rating: "))
    if not (0 <= rating <= 5):
        raise ValueError("Rating must be between 0 and 5")

    with conn.cursor() as cursor:
        query = """
        INSERT INTO rates (userID, movieID, rating)
        VALUES (%s, %s, %s)
        ON CONFLICT (userID, movieID) DO UPDATE SET rating = excluded.rating;"""
        cursor.execute(query, (user_id, movie_id, rating))
        conn.commit()

    print(f"User {user_id} rated movie {movie_id} with {rating} stars.")