from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="host.docker.internal",
    user="root",
    password="",
    database="studentdb"
)

cursor = db.cursor()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add_student():

    name = request.form['name']
    age = request.form['age']
    course = request.form['course']

    query = """
    INSERT INTO students(name, age, course)
    VALUES(%s, %s, %s)
    """

    values = (name, age, course)

    cursor.execute(query, values)
    db.commit()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete_student(id):

    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    db.commit()

    return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update_student(id):

    name = request.form['name']
    age = request.form['age']
    course = request.form['course']

    query = """
    UPDATE students
    SET name=%s, age=%s, course=%s
    WHERE id=%s
    """

    values = (name, age, course, id)

    cursor.execute(query, values)
    db.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)