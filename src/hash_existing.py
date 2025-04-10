from auth import hash_password

def hash_existing_passwords(conn, curs):
    curs.execute('SELECT id, password FROM users')
    users = curs.fetchall()
    for user in users:
        hashed_pass = hash_password(user[0], user[1])
        curs.execute('UPDATE users SET password=%s WHERE id=%s', (hashed_pass, user[0]))
        conn.commit()