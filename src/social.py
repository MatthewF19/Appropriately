def follow_user(conn, follower_id):
    followed_id = input("Enter the following id: ")
    with conn.cursor() as cur:
        # Check if the follow relationship already exists
        cur.execute(
            "SELECT 1 FROM Follow WHERE followerID = %s AND followedID = %s;",
            (follower_id, followed_id)
        )
        exists = cur.fetchone()

        if exists:
            print(f"User {follower_id} is already following user {followed_id}.")
        else:
            cur.execute(
                "INSERT INTO Follow (followerID, followedID) VALUES (%s, %s);",
                (follower_id, followed_id)
            )
            conn.commit()
            print(f"User {follower_id} now follows user {followed_id}.")


def unfollow_user(conn, follower_id):
    followed_id = input("Enter the following id: ")
    with conn.cursor() as cur:
        # Check if the follow relationship exists
        cur.execute(
            "SELECT 1 FROM Follow WHERE followerID = %s AND followedID = %s;",
            (follower_id, followed_id)
        )
        exists = cur.fetchone()

        if not exists:
            print(f"User {follower_id} is not following user {followed_id}.")
        else:
            cur.execute(
                "DELETE FROM Follow WHERE followerID = %s AND followedID = %s;",
                (follower_id, followed_id)
            )
            conn.commit()
            print(f"User {follower_id} has unfollowed user {followed_id}.")


def get_follower_count(conn, user_id):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT COUNT(*) FROM Follow WHERE followedID = %s;",
            (user_id,)
        )
        count = cur.fetchone()[0]
        print(f"User {user_id} has {count} followers.")


def get_following_count(conn, user_id):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT COUNT(*) FROM Follow WHERE followerID = %s;",
            (user_id,)
        )
        count = cur.fetchone()[0]
        print(f"User {user_id} follows {count} users.")