from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('bug.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bugs (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('bug.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM bugs WHERE status = "Open"')
    open_bugs = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM bugs WHERE status = "In Progress"')
    in_progress_bugs = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM bugs WHERE status = "Resolved"')
    resolved_bugs = c.fetchone()[0]
    conn.close()
    return render_template('index.html', open_bugs=open_bugs, in_progress_bugs=in_progress_bugs, resolved_bugs=resolved_bugs)

@app.route('/bugs')
def bugs():
    conn = sqlite3.connect('bug.db')
    c = conn.cursor()
    c.execute('SELECT * FROM bugs')
    bugs = c.fetchall()
    conn.close()
    return render_template('bug_list.html', bugs=bugs)

@app.route('/reports')
def reports():
    conn = sqlite3.connect('bug.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM bugs')
    total_bugs = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM bugs WHERE status = "Open"')
    open_bugs = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM bugs WHERE status = "In Progress"')
    in_progress_bugs = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM bugs WHERE status = "Resolved"')
    resolved_bugs = c.fetchone()[0]
    conn.close()
    return render_template('reports.html', total_bugs=total_bugs, open_bugs=open_bugs,
                           in_progress_bugs=in_progress_bugs, resolved_bugs=resolved_bugs)

@app.route('/add', methods=['POST'])
def add_bug():
    title = request.form['title']
    description = request.form['description']
    priority = request.form['priority']
    status = request.form['status']
    conn = sqlite3.connect('bug.db')
    c = conn.cursor()
    c.execute('INSERT INTO bugs (title, description, priority, status) VALUES (?, ?, ?, ?)',
              (title, description, priority, status))
    conn.commit()
    conn.close()
    return redirect('/bugs')

@app.route('/delete/<int:id>')
def delete_bug(id):
    conn = sqlite3.connect('bug.db')
    c = conn.cursor()
    c.execute('DELETE FROM bugs WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/bugs')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
