from datetime import date
from datetime import datetime

def login(conn, curs):
    username = input("username: ")
    password = input("password: ")

    curs.execute("SELECT * FROM users WHERE username = %s", (username,))
    result = curs.fetchone()

    # if user DNE, register them
    if result is None:
        print("\nuser not recognized! creating account")
        first = input("first name: ")
        last  = input("last name: ")
        email = input("email: ")
        dob   = input("date of birth as YYYY-MM-DD: ")

        curs.execute("""
            INSERT INTO users(username, password, creationdate, lastaccessdate, firstname, lastname, email, dob)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""",
            (username, password, date.today(), datetime.now(), first, last, email, dob))
        conn.commit()

        curs.execute("SELECT id FROM users WHERE username=%s", (username,))
        return curs.fetchone()[0]
    
    # user already exists
    if password == result[2]:
        curs.execute("UPDATE users SET lastaccessdate=%s WHERE id=%s", (datetime.now(), result[0])) 
        conn.commit()
        return result[0]

    # wrong password
    print("INCORRECT USERNAME")
    # try again
    return login(conn, curs)
