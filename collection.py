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
