def rate_movie(conn, user_id):
    movie_id = input("Enter your movie ID: ")
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