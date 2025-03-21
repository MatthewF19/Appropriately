def watch(conn):

    type = input("Watch movie or collection?")


    col_query = """
    SELECT m.title
    FROM movie m 
    LEFT JOIN has_movie hm ON m.id=hm.movieid
    LEFT JOIN collection c ON hm.collectionid=c.id
    WHERE collecton LIKE
    
    """
    while type != "Q":
        if type == "collection":
            name = input("Type collection name:\n")
            with conn.cursor() as cursor:
                curs.execute(

        # elif type == "movie":
        #     name = input("Type movie name:\n")

        else:
            "Choose what to watch or type Q to quit"

