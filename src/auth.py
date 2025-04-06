import hashlib

def hash_password(userid, password):
    salted = str(userid) + password
    return hashlib.sha3_256(salted.encode()).hexdigest()

def authenticate(conn, curs, username, password):
    curs.execute('SELECT id, password FROM users WHERE username=%s', 
                 (username,))
    user = curs.fetchone()

    if user is None:                               return None # THIS IS NOT STUPID I HAVE TO ERROR CHECK
    elif user[1] != hash_password(user[0], password): return False # wrong password
    else:                                          return user[0] # user logged in