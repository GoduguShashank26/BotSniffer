from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from bot_utils import detect_bot
from flask import request

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def welcome():
    return render_template('welcome.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email_id')
        mobile = request.form.get('mobile_number')
        password = request.form.get('password')

        print(f"Form Data: {full_name}, {email}, {mobile}, {password}")

        hashed_password = generate_password_hash(password)
        mysql = current_app.extensions['mysql']
        cursor = mysql.connection.cursor()

        try:
            cursor.execute("INSERT INTO users (username, email, mobile, password, role) VALUES (%s, %s, %s, %s, %s)",
                           (full_name, email, mobile, hashed_password, 'user'))
            mysql.connection.commit()
            print("User registered successfully")
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            print(f"Error during registration: {e}")
            mysql.connection.rollback()
            flash(f'Registration failed: {e}', 'danger')
            return render_template('register.html')
        finally:
            cursor.close()

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form.get('username')
        password_input = request.form.get('password')

        if not login_input or not password_input:
            flash("Please enter both username/email and password.", 'danger')
            return render_template('login.html')

        mysql = current_app.extensions['mysql']
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM users WHERE email = %s OR username = %s", (login_input, login_input))
        user = cur.fetchone()

        if user and check_password_hash(user[4], password_input):
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[5]

            ip = request.remote_addr
            login_time = datetime.now()

            cur.execute("INSERT INTO sessions (user_id, username, ip, login_time) VALUES (%s, %s, %s, %s)",
                        (user[0], user[1], ip, login_time))
            mysql.connection.commit()

            status = detect_bot(user[0], ip)

            bot_id = f"bot_{user[0]}_{int(datetime.utcnow().timestamp())}"

            cur.execute("INSERT INTO bots (bot_id, user_id, ip, status, detected_time) VALUES (%s, %s, %s, %s, %s)",
                        (bot_id, user[0], ip, status, login_time))
            mysql.connection.commit()

            cur.close()
            return redirect('/admin' if user[5] == 'admin' else '/content')

        flash("Invalid credentials", 'danger')
        cur.close()

    return render_template('login.html')