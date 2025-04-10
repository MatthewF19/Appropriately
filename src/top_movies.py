from datetime import datetime

#returns the top 5 movies released in the current calendar month based on rating
def top5_new_releases(curs):
    now = datetime.now()
    month = now.strftime('%m')
    month = "0" + str(int(month) - 1)
    year = now.strftime('%Y')
    result = top5_releases_by_month(curs, month, year)
    for i, (title, rating) in enumerate(result):
        print(f"#{i+1}: {title} -- {float(rating)}/5")


#returns top 5 movies released in a particular month and year based on rating
def top5_releases_by_month(curs, month, year):
    curs.execute("""
        SELECT m.title, r.avg_rating FROM 
        movie m JOIN (
            SELECT rat.movieid, AVG(rat.rating) AS avg_rating FROM
                rates rat JOIN release rel ON rat.movieid = rel.movieid
                WHERE TO_CHAR(rel.release_date, 'MM') = %s
                AND TO_CHAR(rel.release_date, 'YYYY') = %s
            GROUP BY rat.movieid
            ORDER BY avg_rating DESC
            LIMIT 5
        ) r
        ON m.id = r.movieid
    """, (month, year))
    return curs.fetchall()


#------------------------------------------------------------------------------


# returns the most watched movies in the past 90 days
def top20_movies_currently(curs):
    curs.execute("""
        select title, count(w.movieid) as times_watched
        from movie m
        join watches w
        on m.id = w.movieid
        where w.startdate >= CURRENT_DATE - interval '90 days'
        group by w.movieid, title
        order by times_watched desc
        limit 20
    """)
    for i, (title, times_watched) in enumerate(curs.fetchall()):
        print(f"#{i+1}: {title}")

#------------------------------------------------------------------------------
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

