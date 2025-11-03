from flask import request, session, current_app

def log_clickstream(page_visited):
    if 'user_id' not in session:
        return

    user_id = session['user_id']
    ip_address = request.remote_addr

    mysql = current_app.extensions['mysql']
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO clickstream (user_id, page_visited, ip_address) VALUES (%s, %s, %s)",
        (user_id, page_visited, ip_address)
    )
    mysql.connection.commit()
    cur.close()