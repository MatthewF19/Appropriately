from datetime import date
from datetime import datetime

from auth import authenticate
from auth import hash_password

def login(conn, curs):
    username = input("username: ")
    password = input("password: ")

    result = authenticate(conn, curs, username, password)

    # if user DNE, register them
    if result is None:
        print("\nuser not recognized! creating account")
        first = input("first name: ")
        last  = input("last name: ")
        email = input("email: ")
        dob   = input("date of birth as YYYY-MM-DD: ")

        # get what the user's id WILL be (for hashing)
        curs.execute("SELECT max(id) FROM users;")
        userid = curs.fetchone()[0]+1

        curs.execute("""
            INSERT INTO users(username, password, creationdate, lastaccessdate, firstname, lastname, email, dob)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""",
            (username, hash_password(userid, password), datetime.now(), datetime.now(), first, last, email, dob))
        conn.commit()

        curs.execute("SELECT id FROM users WHERE username=%s", (username,))
        return curs.fetchone()
    
    # wrong password
    if result == False:
        print("INCORRECT CREDENTIALS")
        return login(conn, curs)

    # user logged in successfully
    curs.execute("UPDATE users SET lastaccessdate=%s WHERE id=%s", (datetime.now(), result)) 
    conn.commit()
    return result
