from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL connection
db = mysql.connector.connect(
    host="mysql-db",      # MySQL container name
    user="root",
    password="root",
    database="tododb"
)

cursor = db.cursor()

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        task = request.form.get("task")

        sql = "INSERT INTO tasks (task) VALUES (%s)"
        val = (task,)
        cursor.execute(sql, val)
        db.commit()

        return redirect("/")

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    sql = "DELETE FROM tasks WHERE id=%s"
    val = (id,)
    cursor.execute(sql, val)
    db.commit()

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)