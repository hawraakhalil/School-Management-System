import sqlite3
import os
import sys

# Function to create the database and tables
def create_database():
        # Ensure the 'database' directory exists
    database_dir = 'src/database'
    if not os.path.exists(database_dir):
        os.makedirs(database_dir)
    
    # Path to the SQLite database inside the 'database' directory
    db_path = os.path.join(database_dir, 'school_management.db')

    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create Students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL
        )
    ''')

    # Create Instructors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Instructors (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL
        )
    ''')

    # Create Courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Courses (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            instructor_id TEXT,
            FOREIGN KEY (instructor_id) REFERENCES Instructors (id)
        )
    ''')

    # Create Registrations table (Join table)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Registrations (
            student_id TEXT,
            course_id TEXT,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES Students (id),
            FOREIGN KEY (course_id) REFERENCES Courses (id)
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Call the function to create the database and tables
create_database()

# -------------------------------------------
# CRUD operations for students
# -------------------------------------------

# Connect to the SQLite database
def connect_db():
    db_path = os.path.join('src/database', 'school_management.db')
    return sqlite3.connect(db_path)

# Create a new student
def create_student(student):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Students (id, name, age, email) VALUES (?, ?, ?, ?)
    ''', (student.id, student.name, student.age, student.email))
    conn.commit()
    conn.close()

# Read all students
def read_students():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Students')
    students = cursor.fetchall()
    conn.close()
    return students

# Update a student
def update_student(student):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Students SET name = ?, age = ?, email = ? WHERE id = ?
    ''', (student.name, student.age, student.email, student.id))
    conn.commit()
    conn.close()

# Delete a student
def delete_student(student_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Students WHERE id = ?', (student_id,))
    conn.commit()
    conn.close()

# -------------------------------------------
# CRUD operations for instructors
# -------------------------------------------

# Create a new instructor
def create_instructor(instructor):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Instructors (id, name, age, email) VALUES (?, ?, ?, ?)
    ''', (instructor.id, instructor.name, instructor.age, instructor.email))
    conn.commit()
    conn.close()

# Read all instructors
def read_instructors():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Instructors')
    instructors = cursor.fetchall()
    conn.close()
    return instructors

# Update an instructor
def update_instructor(instructor):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Instructors SET name = ?, age = ?, email = ? WHERE id = ?
    ''', (instructor.name, instructor.age, instructor.email, instructor.id))
    conn.commit()
    conn.close()

# Delete an instructor
def delete_instructor(instructor_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Instructors WHERE id = ?', (instructor_id,))
    conn.commit()
    conn.close()

# -------------------------------------------
# CRUD operations for courses
# -------------------------------------------

# Create a new instructor
def create_course(course):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Courses (id, name, instructor_id) VALUES (?, ?, ?)
    ''', (course.id, course.name, course.instructor))
    conn.commit()
    conn.close()

# Read all instructors
def read_course():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Courses')
    courses = cursor.fetchall()
    conn.close()
    return courses

# Update a student
def update_course(course):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Courses SET name = ?, instructor = ? WHERE id = ?
    ''', (course.name, course.instructr, course.id))
    conn.commit()
    conn.close()

# Delete a student
def delete_course(course_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Coruses WHERE id = ?', (course_id,))
    conn.commit()
    conn.close()
    