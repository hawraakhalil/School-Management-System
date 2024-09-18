import tkinter as tk
from tkinter import ttk
from src.management.school_entities import Student, Instructor, Course
from src.management.json_manager import *

# Create files to store data
create_json_files()

def load_data():
    """Load data from JSON files for students, instructors, and courses.

    Loads the student, instructor, and course data from their respective JSON files
    ('students.json', 'instructors.json', 'courses.json') into global dictionaries.
    This function assumes the JSON files exist and contain valid data.
    
    Global variables:
        students (dict): Dictionary of student data loaded from 'students.json'.
        instructors (dict): Dictionary of instructor data loaded from 'instructors.json'.
        courses (dict): Dictionary of course data loaded from 'courses.json'.
    """
    global students, instructors, courses
    students = load_data_from_json('students.json')
    instructors = load_data_from_json('instructors.json')
    courses = load_data_from_json('courses.json')

def populate_listboxes():
    """Populate listboxes with students, instructors, and courses.

    Clears any existing entries from the listboxes and populates them
    with the respective data of students, instructors, and courses from the
    loaded data dictionaries.
    
    Raises:
        KeyError: If any required keys are missing in the loaded data.
    """
    # Populate students listbox
    student_listbox.delete(0, tk.END)  # Clear the listbox first
    load_data()
    for id, student_details in students.items():
        student_listbox.insert(tk.END, f"{student_details['name']} (ID: {id})")

    # Populate instructors listbox
    instructor_listbox.delete(0, tk.END)  # Clear the listbox first
    for id, instructor_details in instructors.items():
        instructor_listbox.insert(tk.END, f"{instructor_details['name']} (ID: {id})")

    # Populate courses listbox
    course_listbox.delete(0, tk.END)  # Clear the listbox first
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
    """Clear all entry fields in the Students tab.

    This function clears the entries for student name, age, email, and ID
    fields in the Students tab, resetting them to their default state.
    """
    student_name_entry.delete(0, tk.END)
    student_age_entry.delete(0, tk.END)
    student_email_entry.delete(0, tk.END)
    student_id_entry.delete(0, tk.END)

def add_student():
    """Add a new student based on user input.

    Retrieves the student details (name, age, email, ID) entered in the Students tab,
    validates the input, creates a new Student object, saves it to the JSON file,
    and updates the student listbox.

    Raises:
        ValueError: If invalid data is entered or required fields are missing.
    """
    name = student_name_entry.get()
    age = student_age_entry.get()
    email = student_email_entry.get()
    student_id = student_id_entry.get()

    if not name or not age or not email or not student_id:
        message_label.config(text="Error: All fields must be filled out.", fg="red")
        return

    student = Student(name=name, age=int(age), email=email, id=student_id)

    try:
        validate_and_add_user(student)
        save_data_to_json(student, 'students.json')
        student_listbox.insert(tk.END, f"{student.name} (ID: {student.id})")
        message_label.config(text="Student added successfully!", fg="green")
        clear_student_entries()
    except ValueError as e:
        message_label.config(text=f"Error: {e}", fg="red")

def register_course():
    """Register a student for a course.

    Fetches the student and course information from the corresponding entries,
    verifies their existence in the JSON files, and registers the student for
    the selected course.

    Raises:
        KeyError: If the student or course ID does not exist in the respective data.
    """
    student_id = student_register_id_entry.get()
    course_id = course_combobox.get()

    students_data = load_data_from_json('students.json')
    courses_data = load_data_from_json('courses.json')

    if student_id not in students_data:
        message_label.showerror("Error", "Student ID not found.")
        return
    if course_id not in courses_data:
        message_label.showerror("Error", "Course not found.")
        return

    student = Student(name=students_data[student_id]['name'],
                      age=students_data[student_id]['age'],
                      email=students_data[student_id]["email"], id=student_id)
    course = Course(name=courses_data[course_id]['name'], id=course_id,
                    instructor=courses_data[course_id]['instructor'],
                    students=courses_data[course_id]['students'])

    student.register_course(course_id)
    course.add_student(student_id)

    save_data_to_json(student, 'students.json')
    save_data_to_json(course, 'courses.json')

    message_label.config(text=f"Student {student_id} registered for course {course_id} successfully!", fg="green")

def delete_student():
    """Delete the selected student from the system.

    Deletes a student based on their selection from the student listbox.
    Removes the student from the 'students.json' file and updates the listbox.
    
    Raises:
        KeyError: If the selected student does not exist in the data.
    """
    selected = student_listbox.curselection()
    if not selected:
        message_label.config(text="Error: No student selected.", fg="red")
        return

    student_id = student_listbox.get(selected).split(" (ID: ")[-1][:-1]
    
    if delete_from_json(student_id, 'students.json'):
        populate_listboxes()
        load_data()
        message_label.config(text=f"Student {student_id} deleted successfully!", fg="green")
    else:
        message_label.config(text="Error: Student ID not found in the records.", fg="red")

def edit_student():
    """Edit the selected student's details.

    Populates the student form with the currently selected student's details
    for editing, allowing modifications to be made and saved.
    """
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
    """Save the changes made to the student's details.

    Updates the student's information in the 'students.json' file and refreshes
    the listbox with the updated data.
    
    Args:
        student_id (str): The ID of the student whose details are being updated.
    
    Raises:
        ValueError: If any of the required fields are empty or the student ID is changed.
    """
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

    student = Student(name=name, age=int(age), email=email, id=student_id)
    save_data_to_json(student, 'students.json')
    load_data()
    populate_listboxes()
    clear_student_entries()
    message_label.config(text=f"Student {student_id} updated successfully!", fg="green")

# GUI Layout for Students Tab
# ---------------------------
# Add the "Add Student" label and its associated entry fields.
tk.Label(students_frame, text="Add Student").grid(row=0, column=0, columnspan=2, pady=10)
tk.Label(students_frame, text="Student Name:").grid(row=1, column=0)
tk.Label(students_frame, text="Student Age:").grid(row=2, column=0)
tk.Label(students_frame, text="Student Email:").grid(row=3, column=0)
tk.Label(students_frame, text="Student ID:").grid(row=4, column=0)

# Create entry fields for student information input.
student_name_entry = tk.Entry(students_frame)
student_age_entry = tk.Entry(students_frame)
student_email_entry = tk.Entry(students_frame)
student_id_entry = tk.Entry(students_frame)

# Arrange the entry fields on the grid layout.
student_name_entry.grid(row=1, column=1)
student_age_entry.grid(row=2, column=1)
student_email_entry.grid(row=3, column=1)
student_id_entry.grid(row=4, column=1)


# Add a button to submit the student details and call the add_student() function.
tk.Button(students_frame, text="Add Student", command=add_student).grid(row=5, column=1, pady=5)

# Create a listbox to display added students.
student_listbox = tk.Listbox(students_frame, width=50)
student_listbox.grid(row=6, column=0, columnspan=2, pady=10)

# Add labels and fields for student course registration.
tk.Label(students_frame, text="Register Course for Student (ID)").grid(row=7, column=0, padx=5, pady=5)
student_register_id_entry = tk.Entry(students_frame)
student_register_id_entry.grid(row=8, column=0, padx=5, pady=5)

tk.Label(students_frame, text="Select Course").grid(row=7, column=1, padx=5, pady=5)

# Create a dropdown (combobox) to list available courses for registration.
courses_data = load_data_from_json('courses.json')
course_combobox = ttk.Combobox(students_frame, values=list(courses_data.keys()))
course_combobox.grid(row=8, column=1, padx=5, pady=5)

# Add a button to register the selected course for the student.
tk.Button(students_frame, text="Register Course", command=register_course).grid(row=8, column=2, pady=5)

# Add buttons for editing and deleting selected students from the list.
tk.Button(students_frame, text="Edit Student", command=edit_student).grid(row=5, column=2, pady=5)
tk.Button(students_frame, text="Delete Student", command=delete_student).grid(row=5, column=3, pady=5)

# -------------------------------------------
# Functions for Instructors Tab
# -------------------------------------------

def clear_instructor_entries():
    """Clear all entry fields in the Instructors tab.

    This function clears the entries for instructor name, age, email, 
    and ID fields in the Instructors tab, resetting them to their default state.
    """
    instructor_name_entry.delete(0, tk.END)
    instructor_age_entry.delete(0, tk.END)
    instructor_email_entry.delete(0, tk.END)
    instructor_id_entry.delete(0, tk.END)

def add_instructor():
    """Add a new instructor based on user input.

    Retrieves the instructor details (name, age, email, ID) entered in the 
    Instructors tab, validates the input, creates a new Instructor object, 
    saves it to the JSON file, and updates the instructor listbox.

    Raises:
        ValueError: If invalid data is entered or required fields are missing.
    """
    name = instructor_name_entry.get()
    age = instructor_age_entry.get()
    email = instructor_email_entry.get()
    instructor_id = instructor_id_entry.get()

    if not name or not age or not email or not instructor_id:
        message_label.config(text="Error: All fields must be filled out.", fg="red")
        return

    instructor = Instructor(name=name, age=int(age), email=email, id=instructor_id)

    try:
        validate_and_add_user(instructor)
        save_data_to_json(instructor, 'instructors.json')
        instructor_listbox.insert(tk.END, f"{instructor.name} (ID: {instructor.id})")
        message_label.config(text="Instructor added successfully!", fg="green")
        clear_instructor_entries()
    except ValueError as e:
        message_label.config(text=f"Error: {e}", fg="red")

def delete_instructor():
    """Delete the selected instructor from the system.

    Deletes an instructor based on their selection from the instructor listbox.
    Removes the instructor from the 'instructors.json' file and updates the listbox.

    Raises:
        KeyError: If the selected instructor does not exist in the data.
    """
    selected = instructor_listbox.curselection()
    if not selected:
        message_label.config(text="Error: No instructor selected.", fg="red")
        return

    instructor_id = instructor_listbox.get(selected).split(" (ID: ")[-1][:-1]
    
    if delete_from_json(instructor_id, 'instructors.json'):
        populate_listboxes()
        load_data()
        message_label.config(text=f"Instructor {instructor_id} deleted successfully!", fg="green")
    else:
        message_label.config(text="Error: Instructor ID not found in the records.", fg="red")

def edit_instructor():
    """Edit the selected instructor's details.

    Populates the instructor form with the currently selected instructor's details
    for editing, allowing modifications to be made and saved.
    """
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
    """Save the changes made to the instructor's details.

    Updates the instructor's information in the 'instructors.json' file and refreshes
    the listbox with the updated data.
    
    Args:
        instructor_id (str): The ID of the instructor whose details are being updated.
    
    Raises:
        ValueError: If any of the required fields are empty or the instructor ID is changed.
    """
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

    instructor = Instructor(name=name, age=int(age), email=email, id=instructor_id)
    save_data_to_json(instructor, 'instructors.json')
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

instructor_listbox = tk.Listbox(instructors_frame, width = 50)
instructor_listbox.grid(row=6, column=0, columnspan=2, pady=10)

tk.Button(instructors_frame, text="Edit Instructor", command=edit_instructor).grid(row=5, column=2, pady=5)
tk.Button(instructors_frame, text="Delete Instructor", command=delete_instructor).grid(row=5, column=3, pady=5)

# -------------------------------------------
# Functions for Courses Tab
# -------------------------------------------

def clear_course_entries():
    course_name_entry.delete(0, tk.END)
    course_id_entry.delete(0, tk.END)
    course_instructor_entry.delete(0, tk.END)

# Add a new course
def add_course():
    name = course_name_entry.get()
    course_id = course_id_entry.get()
    instructor_id = course_instructor_entry.get()

    if not name or not course_id:
        message_label.config(text="Error: All fields must be filled out.", fg="red")
        return
    

    # Create a Course object
    course = Course(name=name, id=course_id)

    try:
        validate_and_add_course(course)

        # Save data to a JSON file
        save_data_to_json(course, 'courses.json')

        # Update listbox and message label
        course_listbox.insert(tk.END, f"{course.name} (ID: {course.id})")
        message_label.config(text="Course added successfully!", fg="green")
        clear_course_entries()

    except ValueError as e:
        message_label.config(text=f"Error: {e}", fg="red")

def assign_instructor():
    course_id = assign_instructor_id_entry.get()
    instructor_id = instructor_combobox.get()
    
    instructor_data = load_data_from_json('instructors.json')
    courses_data = load_data_from_json('courses.json')

    if instructor_id not in instructor_data:
        message_label.showerror("Error", "Instructor not found.")
        return
    if course_id not in courses_data:
        message_label.showerror("Error", "Course ID not found.")
        return
    
    instructor = Instructor(name=instructor_data[instructor_id]['name'], age=instructor_data[instructor_id]['age'], email=instructor_data[instructor_id]["email"], id=instructor_id)
    course = Course(name=courses_data[course_id]['name'], id=course_id, instructor=courses_data[course_id]['instructor'], students=courses_data[course_id]['students'])
    
    # Register student to the course
    instructor.assign_course(course_id)
    course.assign_instructor(instructor_id)

    save_data_to_json(instructor, 'instructors.json')
    save_data_to_json(course, 'courses.json')
    
    message_label.config(text=f"Instructor {instructor_id} assigned for course {course_id} successfully!", fg="green")

def delete_course():
    selected = course_listbox.curselection()
    if not selected:
        message_label.config(text="Error: No instructor selected.", fg="red")
        return

    course_id = course_listbox.get(selected).split(" (ID: ")[-1][:-1]
    
    # Use delete_from_json function
    if delete_from_json(course_id, 'courses.json'):
        populate_listboxes()
        load_data()
        message_label.config(text=f"Course {course_id} deleted successfully!", fg="green")
    else:
        message_label.config(text="Error: Course ID not found in the records.", fg="red")

# Function to edit a course
def edit_course():
    selected = course_listbox.curselection()
    if not selected:
        message_label.config(text="Error: No course selected.", fg="red")
        return

    course_id = course_listbox.get(selected).split(" (ID: ")[-1][:-1]
    course_details = courses[course_id]

    # Fill the entry fields with the current course's details for editing
    course_name_entry.delete(0, tk.END)
    course_name_entry.insert(tk.END, course_details['name'])
    course_instructor_entry.delete(0, tk.END)
    course_instructor_entry.insert(tk.END, course_details['instructor'])
    course_id_entry.delete(0, tk.END)
    course_id_entry.insert(tk.END, course_id)

    # Update the button to save edited course
    tk.Button(courses_frame, text="Save Changes", command=lambda: save_course_changes(course_id)).grid(row=4, column=4, pady=5)

def save_course_changes(course_id):
    name = course_name_entry.get()
    id = course_id_entry.get()
    instructor = course_instructor_entry.get()

    if not name or not id:
        message_label.config(text="Error: All fields must be filled out.", fg="red")
        return

    if id != course_id:
        message_label.config(text="Error: course ID cannot be changed.", fg="red")
        return
    
    # Update the student's information
    course = Course(name=name, id=course_id, instructor = instructor)

    save_data_to_json(course, 'courses.json')
    load_data()
    populate_listboxes()
    clear_course_entries()
    message_label.config(text=f"course {course_id} updated successfully!", fg="green")

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

course_listbox = tk.Listbox(courses_frame, width = 50)
course_listbox.grid(row=5, column=0, columnspan=2, pady=10)


tk.Label(courses_frame, text="Assign Instructor for Course (ID)").grid(row=7, column=0, padx=5, pady=5)
assign_instructor_id_entry = tk.Entry(courses_frame)
assign_instructor_id_entry.grid(row=8, column=0, padx=5, pady=5)

tk.Label(courses_frame, text="Select Instructor").grid(row=7, column=1, padx=5, pady=5)

# Dropdown for courses
instructors_data = load_data_from_json('instructors.json')
instructor_combobox = ttk.Combobox(courses_frame, values=list(instructors_data.keys()))
instructor_combobox.grid(row=8, column=1, padx=5, pady=5)

tk.Button(courses_frame, text="Assign Instructor", command=assign_instructor).grid(row=8, column=2, pady=5)

tk.Button(courses_frame, text="Edit Course", command=edit_course).grid(row=4, column=2, pady=5)
tk.Button(courses_frame, text="Delete Course", command=delete_course).grid(row=4, column=3, pady=5)

# -------------------------------------------
# Functions for Search Tab
# -------------------------------------------

def clear_search_entries():
    student_search_entry.delete(0, tk.END)
    instructor_search_entry.delete(0, tk.END)
    courses_search_entry.delete(0, tk.END)

# Search Objects

def perform_search(type):
    if student_search_entry.get():
        search_term = student_search_entry.get().lower()
    elif instructor_search_entry.get(): 
        search_term = instructor_search_entry.get().lower()
    elif courses_search_entry.get():
        search_term = courses_search_entry.get().lower()
    else:
        message_label.config(text="Please enter an ID.", fg="red")
        return

    if type == "student":
        data = load_data_from_json('students.json')
    elif type == "instructor":
        data = load_data_from_json('instructors.json')
    elif type == "course":
        data = load_data_from_json('courses.json')

    result_listbox.delete(0, tk.END) 
    clear_search_entries()
    match_found = False

    for item_id, info in data.items():
        if search_term == item_id:
            match_found = True
            # Format the student information in a readable way
            if type == "student":
                result_listbox.insert(tk.END, f"Name: {info['name']}")
                result_listbox.insert(tk.END, f"ID: {item_id}")
                result_listbox.insert(tk.END, f"Age: {info['age']}")
                result_listbox.insert(tk.END, f"Email: {info['email']}")
                result_listbox.insert(tk.END, f"Registered Courses: {', '.join(info['registered_courses']) if info['registered_courses'] else 'None'}")
            elif type == "instructor":
                result_listbox.insert(tk.END, f"Name: {info['name']}")
                result_listbox.insert(tk.END, f"ID: {item_id}")
                result_listbox.insert(tk.END, f"Age: {info['age']}")
                result_listbox.insert(tk.END, f"Email: {info['email']}")
                result_listbox.insert(tk.END, f"Assigned Courses: {', '.join(info['assigned_courses']) if info['assigned_courses'] else 'None'}")
            elif type == "course":
                result_listbox.insert(tk.END, f"Course Name: {info['name']}")
                result_listbox.insert(tk.END, f"ID: {item_id}")
                result_listbox.insert(tk.END, f"Instructor: {info['instructor']}")
                result_listbox.insert(tk.END, f"Students: {', '.join(info['students']) if info['students'] else 'None'}")

    if not match_found:
        message_label.config(text=f"No matching {type} found.", fg="orange")
    else:
        message_label.config(text=f"Matching {type} found.", fg="green")

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


result_listbox = tk.Listbox(search_frame, width = 50)
result_listbox.grid(row=9, column=0, columnspan=2, pady=10)

# -------------------------------------------

# Status Message Label
message_label = tk.Label(root, text="", fg="green")
message_label.grid(row=1, column=0, padx=5, pady=5)

# Start the GUI event loop
populate_listboxes()
root.mainloop()
