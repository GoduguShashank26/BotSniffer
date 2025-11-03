from flask import Blueprint, render_template, session, redirect, url_for, request, current_app
from utils import log_clickstream

user_bp = Blueprint('user', __name__)

@user_bp.route('/content')
def content():
    if 'username' not in session or session.get('role') != 'user':
        return redirect(url_for('auth.login'))

    log_clickstream('content')

    mysql = current_app.extensions['mysql']
    cur = mysql.connection.cursor()

    cur.execute("SELECT id, title FROM jobs")
    jobs = cur.fetchall()

    cur.execute("SELECT id, name FROM companies")
    companies = cur.fetchall()

    cur.close()

    username = session.get('username')
    return render_template('content.html', username=username, jobs=jobs, companies=companies)

@user_bp.route('/job/<int:job_id>')
def job_detail(job_id):
    if 'username' not in session or session.get('role') != 'user':
        return redirect(url_for('auth.login'))

    log_clickstream(f'job_detail_{job_id}')

    mysql = current_app.extensions['mysql']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
    job = cur.fetchone()
    cur.close()

    if job:
        return render_template('job_detail.html', job=job)
    else:
        return "Job not found", 404

@user_bp.route('/company/<name>')
def company_detail(name):
    if 'username' not in session or session.get('role') != 'user':
        return redirect(url_for('auth.login'))

    log_clickstream(f'company_detail_{name}')

    mysql = current_app.extensions['mysql']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM companies WHERE LOWER(name) = %s", (name.lower(),))
    company = cur.fetchone()
    cur.close()

    if company:
        return render_template('company_detail.html', company=company)
    else:
        return "Company not found", 404