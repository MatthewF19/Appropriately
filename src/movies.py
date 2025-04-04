def top_10_movies_by_rates(conn):
    year = int(input("From what year would you like to see the Top 10 movies \n"))
    platform = input("Which platform would you like to focus on \n")
    with conn.cursor() as cur:
        query = """
            SELECT m.id, m.title, AVG(r.rating) AS avg_rating
            FROM Rates r
            JOIN Movie m ON r.movieid = m.id
            JOIN Release rel ON m.id = rel.movieid
            JOIN Platform p ON rel.platformid = p.id
            WHERE EXTRACT(YEAR FROM rel.release_date) >= %s
              AND p.name ILIKE %s
            GROUP BY m.id, m.title
            ORDER BY avg_rating DESC
            LIMIT 10;
        """
        cur.execute(query, (year,f"%{platform}%"))
        results = cur.fetchall()

    print(f"Top 10 movies since {year} on platform matching '{platform}':")
    for row in results:
        print(f"Movie ID: {row[0]}, Title: {row[1]}, Average Rating: {row[2]:.2f}")

def top_10_movies_by_watches(conn):
    year = int(input("From what year would you like to see the Top 10 movies\n"))
    platform = input("Which platform would you like to focus on \n")

    with conn.cursor() as cur:
        query = """
            SELECT m.id, m.title, COUNT(*) AS watch_count
            FROM Watches w
            JOIN Movie m ON w."movieid" = m."id"
            JOIN Release r ON m."id" = r."movieid"
            JOIN Platform p ON r."platformid" = p."id"
            WHERE EXTRACT(YEAR FROM r."release_date") >= %s
              AND p."name" ILIKE %s
            GROUP BY m."id", m."title"
            ORDER BY watch_count DESC
            LIMIT 10;
        """
        cur.execute(query, (year, f"%{platform}%"))
        results = cur.fetchall()

    print(f"Top 10 movies since {year} on platform matching '{platform}' by watch count:")
    for row in results:
        print(f"Movie ID: {row[0]}, Title: {row[1]}, Watch Count: {row[2]}")


def search_movie(conn):

    action = input("How would you like to search by?\n")

    while action != "Q":
        if action in ("title", "date", "actor", "director", "studio", "genre"):
            results = movie(conn, action)
            if results:
                print("Here are the results:")
                for result in results:
                    print("title:", result[0])
                    print("actors:", result[1])
                    print("director:", result[2])
                    print("length:", result[3])
                    print("mpaa rating:", result[4])
                    print("rating:", result[5])
                    print("\n")


                while action != "E":
                    action = input("Type S to sort list, "
                                   "E to exit, or enter another search type.\n")
                    if action == "S":
                        results = sort_by(conn, results, action)
                        for result in results:
                            print("title:", result[0])
                            print("actors:", result[1])
                            print("director:", result[2])
                            print("length:", result[3])
                            print("mpaa rating:", result[4])
                            print("rating:", result[5])
                            print("\n")
                continue

            else:
                action = input("No results found, enter search  "
                               "type again or type Q to quit.\n")
        else:
            action = input("Try title, date, actor, director,"
                           "studio, genre, or Q to quit.\n")

def sort_by(conn, results, type):
    search = input("sort by?\n")
    list = ()
    if search == "title":
        list = sorted(results, key=lambda x: x[0])
    elif search == "studio":
        list = sorted(results, key=lambda x: x[6])
    elif search == "genre":
        list = sorted(results, key=lambda x: x[7])
    elif search == "date":
        list = sorted(results, key=lambda x: x[8])
    else:
        print("Try title, studio, genre, or date to sort by")
    asc = input("ascending(Enter) or descending(D)?")
    if asc == "D":
        return reversed(list)
    else:
        return list


def movie(conn, type):

    search = ""

    if type == "actor" or type == "director":
        if type == "actor":
            type = "p.first_name ILIKE %s AND p.last_name"
        elif type == "director":
            type = "b.first_name ILIKE %s AND b.last_name"
        else:
            print("defaulting to actor")
            type = "p.first_name ILIKE %s AND p.last_name"

        first = input("first name: ")
        last = input("last name: ")

        param = (first, last)

    else:
        if type == "title":
            search = input("title: ")
            type = "m.title"
        if type == "genre":
            search = input("genre: ")
            type = "g.name"
        if type == "date":
            search = input("date (YYYY-MM-DD): ")
            type = "e.release_date"
        if type == "studio":
            search = input("studio: ")
            type = "s.name"

        param = (f"%{search}%",)


    query = f"""
    SELECT m.title, array_agg(p.first_name || ' ' || p.last_name), 
        array_agg(b.first_name || ' ' || b.last_name), length, m.mpaa, r.rating,
        s.name, g.name, e.release_date
        
    FROM movie m 
    LEFT JOIN acts_in a on m.id = a.movieid
    LEFT JOIN directs d on m.id = d.movie_id
    LEFT JOIN person b on d.person_id = b.id
    LEFT JOIN person p on a.personid = p.id
    LEFT JOIN rates r on m.id = r.movieid
    LEFT JOIN genre_of f on m.id = f.movieid
    LEFT JOIN genre g on f.genreid = g.id
    LEFT JOIN movie_made_in_studio i on m.id = i.movie_id
    LEFT JOIN studio s on i.studio_id = s.id
    LEFT JOIN release e on m.id = e.movieid
    WHERE {type} ILIKE %s
    GROUP by m.id, m.title, m.length, m.mpaa, r.rating,
    s.name, g.name, e.release_date
    ORDER BY m.title, e.release_date
    """

    print(param)
    with conn.cursor() as curs:
        curs.execute(query, param)
        return curs.fetchall()
