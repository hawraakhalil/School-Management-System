import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from src.database.database import create_student, read_students, update_student, delete_student, create_instructor, read_instructors, update_instructor, delete_instructor, create_course, read_course, update_course, delete_course, get_student_courses, get_instructor_courses, get_course_students, register_student_to_course, connect_db, get_student_courses, get_instructor_courses, get_course_students, register_student_to_course
from src.management.school_entities import Student, Instructor, Course

# -------------------------------------------
# Functions for Setup
# -------------------------------------------

def load_data():
    """
    Load student, instructor, and course data from the database.
    """
    global students, instructors, courses
    students = {}
    instructors = {}
    courses = {}

    # Load students
    student_records = read_students()
    for id, name, age, email in student_records:
        students[id] = {'name': name, 'age': age, 'email': email}
        # Get registered courses for student
        registered_courses = get_student_courses(id)
        students[id]['registered_courses'] = registered_courses

    # Load instructors
    instructor_records = read_instructors()
    for id, name, age, email in instructor_records:
        instructors[id] = {'name': name, 'age': age, 'email': email}
        # Get assigned courses for instructor
        assigned_courses = get_instructor_courses(id)
        instructors[id]['assigned_courses'] = assigned_courses

    # Load courses
    course_records = read_course()
    for id, name, instructor_id in course_records:
        courses[id] = {'name': name, 'instructor_id': instructor_id}
        # Get students enrolled in course
        enrolled_students = get_course_students(id)
        courses[id]['students'] = enrolled_students

def populate_listboxes():
    """
    Populate listboxes with students, instructors, and courses.
    """
    # Populate students listbox
    student_listbox.delete(0, tk.END)
    load_data()
    for id, student_details in students.items():
        student_listbox.insert(tk.END, f"{student_details['name']} (ID: {id})")

    # Populate instructors listbox
    instructor_listbox.delete(0, tk.END)
    for id, instructor_details in instructors.items():
        instructor_listbox.insert(tk.END, f"{instructor_details['name']} (ID: {id})")

    # Populate courses listbox
    course_listbox.delete(0, tk.END)
    for id, course_details in courses.items():
        course_listbox.insert(tk.END, f"{course_details['name']} (ID: {id})")

# Tkinter GUI Setup
root = tk.Tk()
root.title("School Management System")
root.geometry("800x600")

# Load initial data
load_data()

# Create Notebook (tabs)
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

# Configure grid to expand with window resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create frames for each tab
students_frame = ttk.Frame(notebook)
instructors_frame = ttk.Frame(notebook)
courses_frame = ttk.Frame(notebook)
search_frame = ttk.Frame(notebook)

# Add frames to notebook
notebook.add(students_frame, text="Students")
notebook.add(instructors_frame, text="Instructors")
notebook.add(courses_frame, text="Courses")
notebook.add(search_frame, text="Search")

# -------------------------------------------
# Functions for Students Tab
# -------------------------------------------

def clear_student_entries():
    student_name_entry.delete(0, tk.END)
    student_age_entry.delete(0, tk.END)
    student_email_entry.delete(0, tk.END)
    student_id_entry.delete(0, tk.END)

def add_student():
    name = student_name_entry.get()
    age = student_age_entry.get()
    email = student_email_entry.get()
    student_id = student_id_entry.get()

    if not name or not age or not email or not student_id:
        message_label.config(text="Error: All fields must be filled out.", fg="red")
        return

    student = Student(id=student_id, name=name, age=int(age), email=email)

    try:
        create_student(student)
        student_listbox.insert(tk.END, f"{student.name} (ID: {student.id})")
        message_label.config(text="Student added successfully!", fg="green")
        clear_student_entries()
    except sqlite3.IntegrityError:
        message_label.config(text="Error: Student ID already exists.", fg="red")

def delete_student_gui():
    selected = student_listbox.curselection()
    if not selected:
        message_label.config(text="Error: No student selected.", fg="red")
        return

    student_id = student_listbox.get(selected).split(" (ID: ")[-1][:-1]

    try:
        delete_student(student_id)
        populate_listboxes()
        load_data()
        message_label.config(text=f"Student {student_id} deleted successfully!", fg="green")
    except Exception as e:
        message_label.config(text="Error: Student ID not found in the records.", fg="red")

def edit_student():
    selected = student_listbox.curselection()
    if not selected:
        message_label.config(text="Error: No student selected.", fg="red")
        return

    student_id = student_listbox.get(selected).split(" (ID: ")[-1][:-1]
    student_details = students[student_id]

    student_name_entry.delete(0, tk.END)
    student_name_entry.insert(tk.END, student_details['name'])
    student_age_entry.delete(0, tk.END)
    student_age_entry.insert(tk.END, student_details['age'])
    student_email_entry.delete(0, tk.END)
    student_email_entry.insert(tk.END, student_details['email'])
    student_id_entry.delete(0, tk.END)
    student_id_entry.insert(tk.END, student_id)

    tk.Button(students_frame, text="Save Changes", command=lambda: save_student_changes(student_id)).grid(row=5, column=4, pady=5)

def save_student_changes(student_id):
    name = student_name_entry.get()
    age = student_age_entry.get()
    email = student_email_entry.get()
    id = student_id_entry.get()

    if not name or not age or not email or not id:
        message_label.config(text="Error: All fields must be filled out.", fg="red")
        return

    if id != student_id:
        message_label.config(text="Error: Student ID cannot be changed.", fg="red")
        return

    student = Student(id=student_id, name=name, age=int(age), email=email)
    update_student(student)
    load_data()
    populate_listboxes()
    clear_student_entries()
    message_label.config(text=f"Student {student_id} updated successfully!", fg="green")

def register_course():
    student_id = student_register_id_entry.get()
    course_id = course_combobox.get()

    if not student_id or not course_id:
        message_label.config(text="Error: Please enter Student ID and select a course.", fg="red")
        return

    # Check if student and course exist
    if student_id not in students:
        message_label.config(text="Error: Student ID not found.", fg="red")
        return
    if course_id not in courses:
        message_label.config(text="Error: Course ID not found.", fg="red")
        return

    try:
        register_student_to_course(student_id, course_id)
        message_label.config(text=f"Student {student_id} registered for course {course_id} successfully!", fg="green")
    except sqlite3.IntegrityError:
        message_label.config(text="Error: Student is already registered for this course.", fg="red")

    load_data()

# GUI Layout for Students Tab
tk.Label(students_frame, text="Add Student").grid(row=0, column=0, columnspan=2, pady=10)
tk.Label(students_frame, text="Student Name:").grid(row=1, column=0)
tk.Label(students_frame, text="Student Age:").grid(row=2, column=0)
tk.Label(students_frame, text="Student Email:").grid(row=3, column=0)
tk.Label(students_frame, text="Student ID:").grid(row=4, column=0)

student_name_entry = tk.Entry(students_frame)
student_age_entry = tk.Entry(students_frame)
student_email_entry = tk.Entry(students_frame)
student_id_entry = tk.Entry(students_frame)

student_name_entry.grid(row=1, column=1)
student_age_entry.grid(row=2, column=1)
student_email_entry.grid(row=3, column=1)
student_id_entry.grid(row=4, column=1)

tk.Button(students_frame, text="Add Student", command=add_student).grid(row=5, column=1, pady=5)

student_listbox = tk.Listbox(students_frame, width=50)
student_listbox.grid(row=6, column=0, columnspan=2, pady=10)

tk.Label(students_frame, text="Register Course for Student (ID)").grid(row=7, column=0, padx=5, pady=5)
student_register_id_entry = tk.Entry(students_frame)
student_register_id_entry.grid(row=8, column=0, padx=5, pady=5)

tk.Label(students_frame, text="Select Course").grid(row=7, column=1, padx=5, pady=5)

# Create a dropdown (combobox) to list available courses for registration.
course_combobox = ttk.Combobox(students_frame, values=list(courses.keys()))
course_combobox.grid(row=8, column=1, padx=5, pady=5)

tk.Button(students_frame, text="Register Course", command=register_course).grid(row=8, column=2, pady=5)

tk.Button(students_frame, text="Edit Student", command=edit_student).grid(row=5, column=2, pady=5)
tk.Button(students_frame, text="Delete Student", command=delete_student_gui).grid(row=5, column=3, pady=5)

# -------------------------------------------
# Functions for Instructors Tab
# -------------------------------------------

def clear_instructor_entries():
    instructor_name_entry.delete(0, tk.END)
    instructor_age_entry.delete(0, tk.END)
    instructor_email_entry.delete(0, tk.END)
    instructor_id_entry.delete(0, tk.END)

def add_instructor():
    name = instructor_name_entry.get()
    age = instructor_age_entry.get()
    email = instructor_email_entry.get()
    instructor_id = instructor_id_entry.get()

    if not name or not age or not email or not instructor_id:
        message_label.config(text="Error: All fields must be filled out.", fg="red")
        return

    instructor = Instructor(id=instructor_id, name=name, age=int(age), email=email)

    try:
        create_instructor(instructor)
        instructor_listbox.insert(tk.END, f"{instructor.name} (ID: {instructor.id})")
        message_label.config(text="Instructor added successfully!", fg="green")
        clear_instructor_entries()
    except sqlite3.IntegrityError:
        message_label.config(text="Error: Instructor ID already exists.", fg="red")

def delete_instructor_gui():
    selected = instructor_listbox.curselection()
    if not selected:
        message_label.config(text="Error: No instructor selected.", fg="red")
        return

    instructor_id = instructor_listbox.get(selected).split(" (ID: ")[-1][:-1]

    try:
        delete_instructor(instructor_id)
        populate_listboxes()
        load_data()
        message_label.config(text=f"Instructor {instructor_id} deleted successfully!", fg="green")
    except Exception as e:
        message_label.config(text="Error: Instructor ID not found in the records.", fg="red")

def edit_instructor():
    selected = instructor_listbox.curselection()
    if not selected:
        message_label.config(text="Error: No instructor selected.", fg="red")
        return

    instructor_id = instructor_listbox.get(selected).split(" (ID: ")[-1][:-1]
    instructor_details = instructors[instructor_id]

    instructor_name_entry.delete(0, tk.END)
    instructor_name_entry.insert(tk.END, instructor_details['name'])
    instructor_age_entry.delete(0, tk.END)
    instructor_age_entry.insert(tk.END, instructor_details['age'])
    instructor_email_entry.delete(0, tk.END)
    instructor_email_entry.insert(tk.END, instructor_details['email'])
    instructor_id_entry.delete(0, tk.END)
    instructor_id_entry.insert(tk.END, instructor_id)

    tk.Button(instructors_frame, text="Save Changes", command=lambda: save_instructor_changes(instructor_id)).grid(row=5, column=4, pady=5)

def save_instructor_changes(instructor_id):
    name = instructor_name_entry.get()
    age = instructor_age_entry.get()
    email = instructor_email_entry.get()
    id = instructor_id_entry.get()

    if not name or not age or not email or not id:
        message_label.config(text="Error: All fields must be filled out.", fg="red")
        return

    if id != instructor_id:
        message_label.config(text="Error: Instructor ID cannot be changed.", fg="red")
        return

    instructor = Instructor(id=instructor_id, name=name, age=int(age), email=email)
    update_instructor(instructor)
    load_data()
    populate_listboxes()
    clear_instructor_entries()
    message_label.config(text=f"Instructor {instructor_id} updated successfully!", fg="green")

# GUI Layout for Instructors Tab
tk.Label(instructors_frame, text="Add Instructor").grid(row=0, column=0, columnspan=2, pady=10)
tk.Label(instructors_frame, text="Instructor Name:").grid(row=1, column=0)
tk.Label(instructors_frame, text="Instructor Age:").grid(row=2, column=0)
tk.Label(instructors_frame, text="Instructor Email:").grid(row=3, column=0)
tk.Label(instructors_frame, text="Instructor ID:").grid(row=4, column=0)

instructor_name_entry = tk.Entry(instructors_frame)
instructor_age_entry = tk.Entry(instructors_frame)
instructor_email_entry = tk.Entry(instructors_frame)
instructor_id_entry = tk.Entry(instructors_frame)

instructor_name_entry.grid(row=1, column=1)
instructor_age_entry.grid(row=2, column=1)
instructor_email_entry.grid(row=3, column=1)
instructor_id_entry.grid(row=4, column=1)

tk.Button(instructors_frame, text="Add Instructor", command=add_instructor).grid(row=5, column=1, pady=5)

instructor_listbox = tk.Listbox(instructors_frame, width=50)
instructor_listbox.grid(row=6, column=0, columnspan=2, pady=10)

tk.Button(instructors_frame, text="Edit Instructor", command=edit_instructor).grid(row=5, column=2, pady=5)
tk.Button(instructors_frame, text="Delete Instructor", command=delete_instructor_gui).grid(row=5, column=3, pady=5)

# -------------------------------------------
# Functions for Courses Tab
# -------------------------------------------

def clear_course_entries():
    course_name_entry.delete(0, tk.END)
    course_id_entry.delete(0, tk.END)
    course_instructor_entry.delete(0, tk.END)

def add_course():
    name = course_name_entry.get()
    course_id = course_id_entry.get()
    instructor_id = course_instructor_entry.get()

    if not name or not course_id:
        message_label.config(text="Error: All fields must be filled out.", fg="red")
        return

    if instructor_id and instructor_id not in instructors:
        message_label.config(text="Error: Instructor ID not found.", fg="red")
        return

    course = Course(id=course_id, name=name, instructor_id=instructor_id)

    try:
        create_course(course)
        course_listbox.insert(tk.END, f"{course.name} (ID: {course.id})")
        message_label.config(text="Course added successfully!", fg="green")
        clear_course_entries()
    except sqlite3.IntegrityError:
        message_label.config(text="Error: Course ID already exists.", fg="red")

def delete_course_gui():
    selected = course_listbox.curselection()
    if not selected:
        message_label.config(text="Error: No course selected.", fg="red")
        return

    course_id = course_listbox.get(selected).split(" (ID: ")[-1][:-1]

    try:
        delete_course(course_id)
        populate_listboxes()
        load_data()
        message_label.config(text=f"Course {course_id} deleted successfully!", fg="green")
    except Exception as e:
        message_label.config(text="Error: Course ID not found in the records.", fg="red")

def edit_course():
    selected = course_listbox.curselection()
    if not selected:
        message_label.config(text="Error: No course selected.", fg="red")
        return

    course_id = course_listbox.get(selected).split(" (ID: ")[-1][:-1]
    course_details = courses[course_id]

    course_name_entry.delete(0, tk.END)
    course_name_entry.insert(tk.END, course_details['name'])
    course_instructor_entry.delete(0, tk.END)
    course_instructor_entry.insert(tk.END, course_details['instructor_id'] or '')
    course_id_entry.delete(0, tk.END)
    course_id_entry.insert(tk.END, course_id)

    tk.Button(courses_frame, text="Save Changes", command=lambda: save_course_changes(course_id)).grid(row=4, column=4, pady=5)

def save_course_changes(course_id):
    name = course_name_entry.get()
    id = course_id_entry.get()
    instructor_id = course_instructor_entry.get()

    if not name or not id:
        message_label.config(text="Error: All fields must be filled out.", fg="red")
        return

    if id != course_id:
        message_label.config(text="Error: Course ID cannot be changed.", fg="red")
        return

    if instructor_id and instructor_id not in instructors:
        message_label.config(text="Error: Instructor ID not found.", fg="red")
        return

    course = Course(id=course_id, name=name, instructor_id=instructor_id)
    update_course(course)
    load_data()
    populate_listboxes()
    clear_course_entries()
    message_label.config(text=f"Course {course_id} updated successfully!", fg="green")

def assign_instructor():
    course_id = assign_instructor_id_entry.get()
    instructor_id = instructor_combobox.get()

    if not course_id or not instructor_id:
        message_label.config(text="Error: Please enter Course ID and select an instructor.", fg="red")
        return

    if course_id not in courses:
        message_label.config(text="Error: Course ID not found.", fg="red")
        return
    if instructor_id not in instructors:
        message_label.config(text="Error: Instructor ID not found.", fg="red")
        return

    # Update course's instructor_id
    course = courses[course_id]
    course_obj = Course(id=course_id, name=course['name'], instructor_id=instructor_id)
    update_course(course_obj)
    message_label.config(text=f"Instructor {instructor_id} assigned to course {course_id} successfully!", fg="green")
    load_data()
    populate_listboxes()

# GUI Layout for Courses Tab
tk.Label(courses_frame, text="Add Course").grid(row=0, column=0, columnspan=2, pady=10)
tk.Label(courses_frame, text="Course Name:").grid(row=1, column=0)
tk.Label(courses_frame, text="Course ID:").grid(row=2, column=0)
tk.Label(courses_frame, text="Instructor ID:").grid(row=3, column=0)

course_name_entry = tk.Entry(courses_frame)
course_id_entry = tk.Entry(courses_frame)
course_instructor_entry = tk.Entry(courses_frame)

course_name_entry.grid(row=1, column=1)
course_id_entry.grid(row=2, column=1)
course_instructor_entry.grid(row=3, column=1)

tk.Button(courses_frame, text="Add Course", command=add_course).grid(row=4, column=1, pady=5)

course_listbox = tk.Listbox(courses_frame, width=50)
course_listbox.grid(row=5, column=0, columnspan=2, pady=10)

tk.Label(courses_frame, text="Assign Instructor for Course (ID)").grid(row=7, column=0, padx=5, pady=5)
assign_instructor_id_entry = tk.Entry(courses_frame)
assign_instructor_id_entry.grid(row=8, column=0, padx=5, pady=5)

tk.Label(courses_frame, text="Select Instructor").grid(row=7, column=1, padx=5, pady=5)

instructor_combobox = ttk.Combobox(courses_frame, values=list(instructors.keys()))
instructor_combobox.grid(row=8, column=1, padx=5, pady=5)

tk.Button(courses_frame, text="Assign Instructor", command=assign_instructor).grid(row=8, column=2, pady=5)

tk.Button(courses_frame, text="Edit Course", command=edit_course).grid(row=4, column=2, pady=5)
tk.Button(courses_frame, text="Delete Course", command=delete_course_gui).grid(row=4, column=3, pady=5)

# -------------------------------------------
# Functions for Search Tab
# -------------------------------------------

def clear_search_entries():
    student_search_entry.delete(0, tk.END)
    instructor_search_entry.delete(0, tk.END)
    courses_search_entry.delete(0, tk.END)

def perform_search(type):
    search_term = ''
    if type == 'student':
        search_term = student_search_entry.get().strip()
    elif type == 'instructor':
        search_term = instructor_search_entry.get().strip()
    elif type == 'course':
        search_term = courses_search_entry.get().strip()

    if not search_term:
        message_label.config(text="Please enter an ID.", fg="red")
        return

    result_listbox.delete(0, tk.END)
    clear_search_entries()

    if type == 'student':
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Students WHERE id = ?', (search_term,))
        student = cursor.fetchone()
        conn.close()
        if student:
            id, name, age, email = student
            registered_courses = get_student_courses(id)
            result_listbox.insert(tk.END, f"Name: {name}")
            result_listbox.insert(tk.END, f"ID: {id}")
            result_listbox.insert(tk.END, f"Age: {age}")
            result_listbox.insert(tk.END, f"Email: {email}")
            result_listbox.insert(tk.END, f"Registered Courses: {', '.join(registered_courses) if registered_courses else 'None'}")
            message_label.config(text=f"Matching {type} found.", fg="green")
        else:
            message_label.config(text=f"No matching {type} found.", fg="orange")
    elif type == 'instructor':
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Instructors WHERE id = ?', (search_term,))
        instructor = cursor.fetchone()
        conn.close()
        if instructor:
            id, name, age, email = instructor
            assigned_courses = get_instructor_courses(id)
            result_listbox.insert(tk.END, f"Name: {name}")
            result_listbox.insert(tk.END, f"ID: {id}")
            result_listbox.insert(tk.END, f"Age: {age}")
            result_listbox.insert(tk.END, f"Email: {email}")
            result_listbox.insert(tk.END, f"Assigned Courses: {', '.join(assigned_courses) if assigned_courses else 'None'}")
            message_label.config(text=f"Matching {type} found.", fg="green")
        else:
            message_label.config(text=f"No matching {type} found.", fg="orange")
    elif type == 'course':
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Courses WHERE id = ?', (search_term,))
        course = cursor.fetchone()
        conn.close()
        if course:
            id, name, instructor_id = course
            enrolled_students = get_course_students(id)
            result_listbox.insert(tk.END, f"Course Name: {name}")
            result_listbox.insert(tk.END, f"ID: {id}")
            result_listbox.insert(tk.END, f"Instructor: {instructor_id if instructor_id else 'None'}")
            result_listbox.insert(tk.END, f"Students: {', '.join(enrolled_students) if enrolled_students else 'None'}")
            message_label.config(text=f"Matching {type} found.", fg="green")
        else:
            message_label.config(text=f"No matching {type} found.", fg="orange")

# GUI Layout for Search Tab
tk.Label(search_frame, text="Search Students").grid(row=0, column=0, columnspan=2, pady=10)
tk.Label(search_frame, text="Search by ID:").grid(row=1, column=0)
tk.Label(search_frame, text="Search Instructors").grid(row=3, column=0, columnspan=2, pady=10)
tk.Label(search_frame, text="Search by ID:").grid(row=4, column=0)
tk.Label(search_frame, text="Search Courses").grid(row=6, column=0, columnspan=2, pady=10)
tk.Label(search_frame, text="Search by ID:").grid(row=7, column=0)

student_search_entry = tk.Entry(search_frame)
student_search_entry.grid(row=1, column=1)
instructor_search_entry = tk.Entry(search_frame)
instructor_search_entry.grid(row=4, column=1)
courses_search_entry = tk.Entry(search_frame)
courses_search_entry.grid(row=7, column=1)

tk.Button(search_frame, text="Search Student", command=lambda: perform_search("student")).grid(row=2, column=1, pady=5)
tk.Button(search_frame, text="Search Instructor", command=lambda: perform_search("instructor")).grid(row=5, column=1, pady=5)
tk.Button(search_frame, text="Search Course", command=lambda: perform_search("course")).grid(row=8, column=1, pady=5)

result_listbox = tk.Listbox(search_frame, width=50)
result_listbox.grid(row=9, column=0, columnspan=2, pady=10)

# -------------------------------------------

# Status Message Label
message_label = tk.Label(root, text="", fg="green")
message_label.grid(row=1, column=0, padx=5, pady=5)

# Start the GUI event loop
populate_listboxes()
root.mainloop()
