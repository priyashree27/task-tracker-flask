from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# ------------------- DATABASE SETUP -------------------
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT DEFAULT 'pending'
        )
    """)
    conn.commit()
    conn.close()

# Initialize database when app starts
init_db()


# ------------------- ROUTES -------------------

@app.route("/")
def home():
    return render_template("index.html")


# ----------- API: Get All Tasks -------------
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    conn.close()

    tasks = [{"id": r[0], "title": r[1], "status": r[2]} for r in rows]
    return jsonify(tasks)


# ----------- API: Add Task -------------
@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.json
    title = data.get("title", "")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Task added successfully"}), 201


# ----------- API: Update Task Status -------------
@app.route("/api/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    data = request.json
    status = data.get("status")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET status=? WHERE id=?", (status, id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Task updated successfully"})


# ----------- API: Delete Task -------------
@app.route("/api/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Task deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
