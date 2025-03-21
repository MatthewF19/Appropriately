def search_user_by_email(conn):
    email_query = input("Enter email address: ")
    with conn.cursor() as cur:
        query = """
            SELECT * FROM Users
            WHERE email ILIKE %s; --ILIKE for case-insensitive search and wildcard % to match any characters.
        """
        search_pattern = f"%{email_query}%"
        cur.execute(query, (search_pattern,))
        results = cur.fetchall()
    return results