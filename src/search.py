def search_user_by_email(conn):
    email_query = input("Enter email address: ")
    with conn.cursor() as cur:
        query = """
            SELECT * FROM Users
            WHERE email ILIKE %s;
        """
        cur.execute(query, (email_query,))
        results = cur.fetchall()
        print(f"found user with username: {results[0][1]}")
    return results