import sqlite3
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# -------------------------
# DATABASE INITIALIZATION
# -------------------------
def init_db():

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sap_id TEXT,
        name TEXT,
        roll_no TEXT,
        branch TEXT,
        marks REAL
    )
    """)

    conn.commit()
    conn.close()

init_db()


# -------------------------
# ADD STUDENT FUNCTION
# -------------------------
def add_student(sap, name, roll, branch, marks):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students (sap_id,name,roll_no,branch,marks) VALUES (?,?,?,?,?)",
        (sap, name, roll, branch, marks)
    )

    conn.commit()
    conn.close()


# -------------------------
# GET STUDENTS FUNCTION
# -------------------------
def get_students():

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT sap_id,name,roll_no,branch,marks FROM students")

    students = cursor.fetchall()

    conn.close()

    return students


# -------------------------
# BEAUTIFUL HTML UI
# -------------------------
html = """

<!DOCTYPE html>
<html>

<head>

<title>Student Database</title>

<style>

body{
font-family:Arial;
background:linear-gradient(135deg,#667eea,#764ba2);
margin:0;
padding:0;
color:white;
}

.container{
width:700px;
margin:auto;
margin-top:40px;
background:white;
color:black;
padding:30px;
border-radius:10px;
box-shadow:0 10px 25px rgba(0,0,0,0.3);
}

h1{
text-align:center;
}

input{
width:100%;
padding:10px;
margin-top:10px;
border-radius:6px;
border:1px solid #ccc;
}

button{
margin-top:15px;
padding:10px 20px;
border:none;
background:#764ba2;
color:white;
border-radius:6px;
cursor:pointer;
}

button:hover{
background:#667eea;
}

table{
width:100%;
margin-top:20px;
border-collapse:collapse;
}

th,td{
padding:10px;
border:1px solid #ccc;
text-align:center;
}

th{
background:#764ba2;
color:white;
}

</style>

</head>

<body>

<div class="container">

<h1>Student Management System</h1>

<form method="POST" action="/add">

<input name="sap_id" placeholder="SAP ID" required>

<input name="name" placeholder="Student Name" required>

<input name="roll_no" placeholder="Roll Number" required>

<input name="branch" placeholder="Branch" required>

<input name="marks" placeholder="Marks" required>

<button type="submit">Add Student</button>

</form>

<h2>Student Records</h2>

<table>

<tr>
<th>SAP ID</th>
<th>Name</th>
<th>Roll</th>
<th>Branch</th>
<th>Marks</th>
</tr>

{% for s in students %}

<tr>
<td>{{s[0]}}</td>
<td>{{s[1]}}</td>
<td>{{s[2]}}</td>
<td>{{s[3]}}</td>
<td>{{s[4]}}</td>
</tr>

{% endfor %}

</table>

</div>

</body>

</html>

"""


# -------------------------
# HOME ROUTE
# -------------------------
@app.route("/")
def home():

    students = get_students()

    return render_template_string(html, students=students)


# -------------------------
# ADD ROUTE
# -------------------------
@app.route("/add", methods=["POST"])
def add():

    sap = request.form["sap_id"]
    name = request.form["name"]
    roll = request.form["roll_no"]
    branch = request.form["branch"]
    marks = request.form["marks"]

    add_student(sap, name, roll, branch, marks)

    return redirect("/")


# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    app.run()