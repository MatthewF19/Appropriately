def search_movie(conn):

    action = input("How would you like to search by?\n")

    while (action != "Q"):
        if action in ("title", "date", "member", "studio", "genre"):
            results = movie(conn, action)
            if results:
                print("Here are the results:")
                for result in results:
                    print(result)
            else:
                print("No results found.")
        else:
            print("Invalid input. Please try again.")


#incompleted
def search_by(conn, type):
    search = input("search by? ")

def movie(conn, type):
    search = input("input: ")

    with conn.cursor() as curs:
        query = f"""
        SELECT m.title, p.first_name, p.last_name, b.first_name, b.last_name, length, m.mpaa, r.rating
        FROM movie m 
        LEFT JOIN acts_in a on m.id = a.movieid
        LEFT JOIN directs d on m.id = d.movie_id
        LEFT JOIN person b on d.person_id = b.id
        LEFT JOIN person p on a.personid = p.id
        LEFT JOIN rates r on m.id = r.movieid
        WHERE {type} ILIKE %s
        ORDER BY m.title
"""
        curs.execute(query, (f"%{search}%",))
        results = curs.fetchall()
    return results
