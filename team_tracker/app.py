from flask import Flask, render_template, redirect, request
import sqlite3

app = Flask(__name__)

# DATABASE CONNECTION

def get_db():

    conn = sqlite3.connect("team.db")
    conn.row_factory = sqlite3.Row

    return conn


# CREATE DATABASE

def create_table():

    conn = get_db()

    conn.execute("""

    CREATE TABLE IF NOT EXISTS team(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        role TEXT,

        department TEXT,

        available INTEGER

    )

    """)

    count = conn.execute(
        "SELECT COUNT(*) FROM team"
    ).fetchone()[0]

    if count == 0:

        members = [

            ("Vatsal Seladiya","Full Stack Developer","Development",1),
            ("Rahul Patel","Frontend Developer","Development",0),
            ("Priya Shah","UI UX Designer","Design",1),
            ("Aman Verma","Python Developer","Backend",1),
            ("Neha Sharma","QA Tester","Testing",0),
            ("Krishna Patel","Database Engineer","Database",1),
            ("Yash Mehta","Backend Developer","Backend",0),
            ("Riya Joshi","Project Manager","Management",1),
            ("Arjun Patel","React Developer","Development",1),
            ("Karan Shah","Backend Engineer","Backend",0),
            ("Nisha Patel","UI Designer","Design",1),
            ("Harsh Mehta","DevOps Engineer","DevOps",1),
            ("Parth Shah","Python Developer","Backend",0),
            ("Meet Patel","Software Engineer","Development",1),
            ("Jay Patel","Flutter Developer","Mobile",1),
            ("Riddhi Shah","QA Engineer","Testing",0),
            ("Dhruv Patel","System Analyst","Management",1),
            ("Khushi Patel","HR Manager","HR",1),
            ("Manan Shah","Cloud Engineer","Cloud",0),
            ("Yug Patel","Data Analyst","Analytics",1),
            ("Dev Patel","Java Developer","Development",1),
            ("Smit Shah","Web Designer","Design",0),
            ("Tirth Patel","Database Admin","Database",1),
            ("Het Patel","ML Engineer","AI/ML",1),
            ("Vraj Shah","Security Engineer","Security",0),
            ("Aryan Patel","Network Engineer","Network",1),
            ("Mihir Shah","Product Manager","Management",1),
            ("Jenil Patel","Support Engineer","Support",0),
            ("Bhavya Shah","Software Tester","Testing",1),
            ("Anjali Patel","Business Analyst","Analytics",1)

        ]

        conn.executemany(

            """

            INSERT INTO team
            (name, role, department, available)

            VALUES (?, ?, ?, ?)

            """,

            members

        )

    conn.commit()
    conn.close()


create_table()


@app.route('/')
def home():

    conn = get_db()

    users = conn.execute(
        "SELECT * FROM team"
    ).fetchall()

    total = len(users)

    available = sum(
        user["available"]
        for user in users
    )

    unavailable = total - available

    percentage = round(
        (available / total) * 100
    )

    conn.close()

    return render_template(

        "index.html",

        users=users,

        total=total,

        available=available,

        unavailable=unavailable,

        percentage=percentage

    )


@app.route('/toggle/<int:id>', methods=['POST'])
def toggle(id):

    conn = get_db()

    user = conn.execute(

        """

        SELECT available

        FROM team

        WHERE id=?

        """,

        (id,)

    ).fetchone()

    new_status = 0 if user["available"] else 1

    conn.execute(

        """

        UPDATE team

        SET available=?

        WHERE id=?

        """,

        (new_status, id)

    )

    conn.commit()

    conn.close()

    return redirect('/')


if __name__ == "__main__":

    app.run(debug=True)