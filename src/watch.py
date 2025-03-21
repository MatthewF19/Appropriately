from datetime import datetime

def watch(conn, userid, type):

    while type != "Q":
        if type == "collection":
            query = """
            SELECT m.title, m.id
            FROM movie m 
            LEFT JOIN has_movie hm ON m.id=hm.movieid
            LEFT JOIN collection c ON hm.collectionid=c.id
            WHERE c.name ILIKE %s

            """

            name = input("Type collection name:\n")
            with conn.cursor() as curs:
                curs.execute(query, (name,))
                results = curs.fetchall()

                for row in results:
                    mov = row[0]
                    start = datetime.now()
                    type = input(f"Now playing {mov}, press N for next movie, "
                          "or S to quit collection\n")

                    end = datetime.now()
                    curs.execute("""
                        INSERT INTO watches(startdate, userid, movieid, enddate) 
                        VALUES(%s, %s, %s, %s)""",
                        (start, userid, row[1], end))
                    conn.commit()
                    if type.upper() == "N":
                        continue
                    elif type.upper() == "Q":
                        type = input("Finished early, type movie or "
                              "collection to watch more, or "
                              "type Q to quit\n")
                        break
                type = input("End of Collection, type movie or "
                             "collection to watch more, or "
                             "type Q to quit\n")


        elif type == "movie":

            query = """
            SELECT title, id
            FROM movie
            WHERE title ILIKE %s
            """

            name = input("Type movie name:\n")
            with conn.cursor() as curs:
                curs.execute(query, (name,))
                results = curs.fetchone()

                start = datetime.now()
                type = input(f"Now playing {name}, type movie or "
                             f"collection to watch more, or "
                             f"type Q to quit\n")

                end = datetime.now()
                curs.execute("""
                                        INSERT INTO watches(startdate, userid, movieid, enddate) 
                                        VALUES(%s, %s, %s, %s)""",
                             (start, userid, results[1], end))
                conn.commit()
        else:
            "Type movie or collection to watch, or type Q to quit"

