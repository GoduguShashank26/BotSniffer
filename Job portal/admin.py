from flask import Blueprint, render_template, current_app
from MySQLdb.cursors import DictCursor

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin_dashboard():
    mysql = current_app.extensions['mysql']
    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM sessions")
    active_sessions = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM jobs")
    total_jobs = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM bots")
    total_bots = cur.fetchone()[0]

    cur.close()

    return render_template("admin.html",
                           total_users=total_users,
                           active_sessions=active_sessions,
                           total_jobs=total_jobs,
                           total_bots=total_bots)

@admin_bp.route('/users')
def users_view():
    mysql = current_app.extensions['mysql']
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, email, mobile FROM users")
    rows = cur.fetchall()
    cur.close()

    users = []
    for row in rows:
        users.append({
            'id': row[0],
            'username': row[1],
            'email': row[2],
            'mobile': row[3]
        })

    return render_template("users.html", users=users)

@admin_bp.route('/sessions')
def sessions_view():
    mysql = current_app.extensions['mysql']
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, ip, login_time FROM sessions")
    rows = cur.fetchall()
    cur.close()

    sessions = []
    for row in rows:
        sessions.append({
            'id': row[0],
            'username': row[1],
            'ip': row[2],
            'login_time': row[3]
        })

    return render_template("sessions.html", sessions=sessions)

@admin_bp.route('/jobs')
def jobs_view():
    mysql = current_app.extensions['mysql']
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT a.app_id, u.username, j.title, a.status
        FROM applications a
        JOIN users u ON a.user_id = u.id
        JOIN jobs j ON a.job_id = j.id
    """)
    applications = cur.fetchall()
    cur.close()
    return render_template("jobs.html", applications=applications)

@admin_bp.route('/bots')
def view_bots():
    mysql = current_app.extensions['mysql']
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT bot_id, ip_address, detected_on, action FROM bots_detected ORDER BY detected_on DESC")
    bots = cur.fetchall()
    cur.close()
    return render_template("bots.html", bots=bots)