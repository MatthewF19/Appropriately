def follow_user(conn, follower_id, followed_id):
    with conn.cursor() as cur:
        query = """
            INSERT INTO Follow (followerID, followedID)
            VALUES (%s, %s)
            ON CONFLICT (followerID, followedID) DO NOTHING;
        """
        cur.execute(query, (follower_id, followed_id))
    conn.commit()
    print(f"User {follower_id} now follows user {followed_id}.")


def unfollow_user(conn, follower_id, followed_id):
    with conn.cursor() as cur:
        query = "DELETE FROM Follow WHERE followerID = %s AND followedID = %s;"
        cur.execute(query, (follower_id, followed_id))
    conn.commit()
    print(f"User {follower_id} has unfollowed user {followed_id}.")
