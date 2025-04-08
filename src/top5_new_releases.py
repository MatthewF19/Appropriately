from datetime import datetime

#returns the top 5 movies released in the current calendar month based on rating
def top5_new_releases(conn, curs):
    now = datetime.now()
    month = now.strftime('%m')
    month = "0" + str(int(month) - 1)
    year = now.strftime('%Y')
    result = top5_releases_by_month(conn, curs, month, year)
    for i, (title, rating) in enumerate(result):
        print(f"#{i+1}: {title} -- {float(rating)}/5")


def top5_releases_by_month(conn, curs, month, year):
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
