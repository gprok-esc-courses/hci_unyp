from flask import Flask, render_template, request, redirect
import sqlite3 

app = Flask(__name__)

# Create the database, if not already there
conn = sqlite3.connect('projects.db')
cursor = conn.cursor()
cursor.execute("""
               CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
               )
               """)
cursor.execute("""
               CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    user_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
               )
               """)



@app.route('/')
def home():
    return "HOME"


@app.route('/users')
def users():
    db = sqlite3.connect('projects.db')
    cursor = db.cursor()
    all_users = cursor.execute("SELECT * FROM users").fetchall()
    return render_template('users.html', users=all_users)


@app.route('/projects/all')
def projects_all():
    db = sqlite3.connect('projects.db')
    cursor = db.cursor()
    all_projects = cursor.execute("SELECT * FROM projects p INNER JOIN users u ON p.user_id=u.id").fetchall()
    return render_template('projects.html', projects=all_projects)


@app.route('/projects/user/<int:uid>')
def projects_user(uid):
    db = sqlite3.connect('projects.db')
    cursor = db.cursor()
    user = cursor.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    if not user:
        return render_template('error.html', error_message='User not found')
    projects = cursor.execute("SELECT * FROM projects WHERE user_id=?", (uid,)).fetchall()
    return render_template('projects_user.html', user=user, projects=projects)


@app.route('/add/project', methods=[ 'GET', 'POST' ])
def add_project():
    if request.method == 'POST':
        data = request.form
        db = sqlite3.connect('projects.db')
        cursor = db.cursor()
        user = cursor.execute("SELECT * FROM users WHERE id=?", (data['user_id'],)).fetchone()
        if not user:
            return render_template('error.html', error_message='User not found')
        cursor.execute("INSERT INTO projects (name, user_id) VALUES (?, ?)", (data['project_name'], data['user_id']))
        db.commit()
        db.close()
        return redirect('/projects/all')
    else:
        return render_template('add_project.html')


if __name__ == '__main__':
    app.run(debug=True)


