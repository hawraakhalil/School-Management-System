from PyQt5.QtWidgets import *
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from management.school_entities import Student, Instructor, Course
from management.json_manager import *

# Create files to store data
create_json_files()

class SchoolManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main window properties
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 800, 600)

        # Main widget and layout
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Initialize tabs
        self.students_tab = QWidget()
        self.instructors_tab = QWidget()
        self.courses_tab = QWidget()
        self.search_tab = QWidget()

        # Add tabs to the tab widget
        self.tabs.addTab(self.students_tab, "Students")
        self.tabs.addTab(self.instructors_tab, "Instructors")
        self.tabs.addTab(self.courses_tab, "Courses")
        self.tabs.addTab(self.search_tab, "Search")

        # Initialize the content of each tab
        self.init_students_tab()
        self.init_instructors_tab()
        self.init_courses_tab()
        self.init_search_tab()

        # Status message label
        self.message_label = QLabel("")
        main_layout.addWidget(self.message_label)

        # Load initial data and populate listboxes
        self.load_data()
        self.populate_listboxes()

    def load_data(self):
        self.students = load_data_from_json('students.json')
        self.instructors = load_data_from_json('instructors.json')
        self.courses = load_data_from_json('courses.json')

    def populate_listboxes(self):
        # Populate students listbox
        self.student_listbox.clear()
        self.load_data()
        for id, student_details in self.students.items():
            self.student_listbox.addItem(f"{student_details['name']} (ID: {id})")

        # Populate instructors listbox
        self.instructor_listbox.clear()
        for id, instructor_details in self.instructors.items():
            self.instructor_listbox.addItem(f"{instructor_details['name']} (ID: {id})")

        # Populate courses listbox
        self.course_listbox.clear()
        for id, course_details in self.courses.items():
            self.course_listbox.addItem(f"{course_details['name']} (ID: {id})")

    def init_students_tab(self):
        layout = QVBoxLayout()
        self.students_tab.setLayout(layout)

        # Input fields
        self.student_name_entry = QLineEdit()
        self.student_age_entry = QLineEdit()
        self.student_email_entry = QLineEdit()
        self.student_id_entry = QLineEdit()

        layout.addWidget(QLabel("Add Student"))
        layout.addWidget(QLabel("Student Name:"))
        layout.addWidget(self.student_name_entry)
        layout.addWidget(QLabel("Student Age:"))
        layout.addWidget(self.student_age_entry)
        layout.addWidget(QLabel("Student Email:"))
        layout.addWidget(self.student_email_entry)
        layout.addWidget(QLabel("Student ID:"))
        layout.addWidget(self.student_id_entry)

        # Buttons
        add_student_btn = QPushButton("Add Student")
        add_student_btn.clicked.connect(self.add_student)
        layout.addWidget(add_student_btn)

        self.student_listbox = QListWidget()
        layout.addWidget(self.student_listbox)

        edit_student_btn = QPushButton("Edit Student")
        edit_student_btn.clicked.connect(self.edit_student)
        layout.addWidget(edit_student_btn)

        delete_student_btn = QPushButton("Delete Student")
        delete_student_btn.clicked.connect(self.delete_student)
        layout.addWidget(delete_student_btn)

    def add_student(self):
        name = self.student_name_entry.text()
        age = self.student_age_entry.text()
        email = self.student_email_entry.text()
        student_id = self.student_id_entry.text()

        if not name or not age or not email or not student_id:
            self.message_label.setText("Error: All fields must be filled out.")
            return

        # Create a Student object
        student = Student(name=name, age=int(age), email=email, id=student_id)

        try:
            validate_and_add_user(student)

            # Save data to a JSON file
            save_data_to_json(student, 'students.json')

            # Update listbox and message label
            self.student_listbox.addItem(f"{student.name} (ID: {student.id})")
            self.message_label.setText("Student added successfully!")
            self.clear_student_entries()

        except ValueError as e:
            self.message_label.setText(f"Error: {e}")

    def clear_student_entries(self):
        self.student_name_entry.clear()
        self.student_age_entry.clear()
        self.student_email_entry.clear()
        self.student_id_entry.clear()

    def delete_student(self):
        selected = self.student_listbox.currentItem()
        if not selected:
            self.message_label.setText("Error: No student selected.")
            return

        student_id = selected.text().split(" (ID: ")[-1][:-1]

        # Use delete_from_json function
        if delete_from_json(student_id, 'students.json'):
            self.populate_listboxes()
            self.message_label.setText(f"Student {student_id} deleted successfully!")
        else:
            self.message_label.setText("Error: Student ID not found in the records.")

    def edit_student(self):
        selected = self.student_listbox.currentItem()
        if not selected:
            self.message_label.setText("Error: No student selected.")
            return

        student_id = selected.text().split(" (ID: ")[-1][:-1]
        student_details = self.students[student_id]

        # Fill the entry fields with the current student's details for editing
        self.student_name_entry.setText(student_details['name'])
        self.student_age_entry.setText(str(student_details['age']))
        self.student_email_entry.setText(student_details['email'])
        self.student_id_entry.setText(student_id)

        save_changes_btn = QPushButton("Save Changes")
        save_changes_btn.clicked.connect(lambda: self.save_student_changes(student_id))
        self.students_tab.layout().addWidget(save_changes_btn)

    def save_student_changes(self, student_id):
        name = self.student_name_entry.text()
        age = self.student_age_entry.text()
        email = self.student_email_entry.text()
        id = self.student_id_entry.text()

        if not name or not age or not email or not id:
            self.message_label.setText("Error: All fields must be filled out.")
            return

        if id != student_id:
            self.message_label.setText("Error: Student ID cannot be changed.")
            return

        # Update the student's information
        student = Student(name=name, age=int(age), email=email, id=student_id)

        save_data_to_json(student, 'students.json')
        self.load_data()
        self.populate_listboxes()
        self.clear_student_entries()
        self.message_label.setText(f"Student {student_id} updated successfully!")

    def init_instructors_tab(self):
        # Initialize Instructors Tab
        layout = QVBoxLayout()
        self.instructors_tab.setLayout(layout)

        self.instructor_name_entry = QLineEdit()
        self.instructor_age_entry = QLineEdit()
        self.instructor_email_entry = QLineEdit()
        self.instructor_id_entry = QLineEdit()

        layout.addWidget(QLabel("Add Instructor"))
        layout.addWidget(QLabel("Instructor Name:"))
        layout.addWidget(self.instructor_name_entry)
        layout.addWidget(QLabel("Instructor Age:"))
        layout.addWidget(self.instructor_age_entry)
        layout.addWidget(QLabel("Instructor Email:"))
        layout.addWidget(self.instructor_email_entry)
        layout.addWidget(QLabel("Instructor ID:"))
        layout.addWidget(self.instructor_id_entry)

        add_instructor_btn = QPushButton("Add Instructor")
        add_instructor_btn.clicked.connect(self.add_instructor)
        layout.addWidget(add_instructor_btn)

        self.instructor_listbox = QListWidget()
        layout.addWidget(self.instructor_listbox)

        edit_instructor_btn = QPushButton("Edit Instructor")
        edit_instructor_btn.clicked.connect(self.edit_instructor)
        layout.addWidget(edit_instructor_btn)

        delete_instructor_btn = QPushButton("Delete Instructor")
        delete_instructor_btn.clicked.connect(self.delete_instructor)
        layout.addWidget(delete_instructor_btn)

    def add_instructor(self):
        name = self.instructor_name_entry.text()
        age = self.instructor_age_entry.text()
        email = self.instructor_email_entry.text()
        instructor_id = self.instructor_id_entry.text()

        if not name or not age or not email or not instructor_id:
            self.message_label.setText("Error: All fields must be filled out.")
            return

        # Create an Instructor object
        instructor = Instructor(name=name, age=int(age), email=email, id=instructor_id)

        try:
            validate_and_add_user(instructor)

            # Save data to a JSON file
            save_data_to_json(instructor, 'instructors.json')

            # Update listbox and message label
            self.instructor_listbox.addItem(f"{instructor.name} (ID: {instructor.id})")
            self.message_label.setText("Instructor added successfully!")
            self.clear_instructor_entries()

        except ValueError as e:
            self.message_label.setText(f"Error: {e}")

    def clear_instructor_entries(self):
        self.instructor_name_entry.clear()
        self.instructor_age_entry.clear()
        self.instructor_email_entry.clear()
        self.instructor_id_entry.clear()

    def delete_instructor(self):
        selected = self.instructor_listbox.currentItem()
        if not selected:
            self.message_label.setText("Error: No instructor selected.")
            return

        instructor_id = selected.text().split(" (ID: ")[-1][:-1]

        # Use delete_from_json function
        if delete_from_json(instructor_id, 'instructors.json'):
            self.populate_listboxes()
            self.message_label.setText(f"Instructor {instructor_id} deleted successfully!")
        else:
            self.message_label.setText("Error: Instructor ID not found in the records.")

    def edit_instructor(self):
        selected = self.instructor_listbox.currentItem()
        if not selected:
            self.message_label.setText("Error: No instructor selected.")
            return

        instructor_id = selected.text().split(" (ID: ")[-1][:-1]
        instructor_details = self.instructors[instructor_id]

        # Fill the entry fields with the current instructor's details for editing
        self.instructor_name_entry.setText(instructor_details['name'])
        self.instructor_age_entry.setText(str(instructor_details['age']))
        self.instructor_email_entry.setText(instructor_details['email'])
        self.instructor_id_entry.setText(instructor_id)

        save_changes_btn = QPushButton("Save Changes")
        save_changes_btn.clicked.connect(lambda: self.save_instructor_changes(instructor_id))
        self.instructors_tab.layout().addWidget(save_changes_btn)

    def save_instructor_changes(self, instructor_id):
        name = self.instructor_name_entry.text()
        age = self.instructor_age_entry.text()
        email = self.instructor_email_entry.text()
        id = self.instructor_id_entry.text()

        if not name or not age or not email or not id:
            self.message_label.setText("Error: All fields must be filled out.")
            return

        if id != instructor_id:
            self.message_label.setText("Error: Instructor ID cannot be changed.")
            return

        # Update the instructor's information
        instructor = Instructor(name=name, age=int(age), email=email, id=instructor_id)

        save_data_to_json(instructor, 'instructors.json')
        self.load_data()
        self.populate_listboxes()
        self.clear_instructor_entries()
        self.message_label.setText(f"Instructor {instructor_id} updated successfully!")

    def init_courses_tab(self):
        # Initialize Courses Tab
        layout = QVBoxLayout()
        self.courses_tab.setLayout(layout)

        self.course_name_entry = QLineEdit()
        self.course_id_entry = QLineEdit()
        self.course_instructor_entry = QLineEdit()

        layout.addWidget(QLabel("Add Course"))
        layout.addWidget(QLabel("Course Name:"))
        layout.addWidget(self.course_name_entry)
        layout.addWidget(QLabel("Course ID:"))
        layout.addWidget(self.course_id_entry)
        layout.addWidget(QLabel("Instructor ID:"))
        layout.addWidget(self.course_instructor_entry)

        add_course_btn = QPushButton("Add Course")
        add_course_btn.clicked.connect(self.add_course)
        layout.addWidget(add_course_btn)

        self.course_listbox = QListWidget()
        layout.addWidget(self.course_listbox)

        edit_course_btn = QPushButton("Edit Course")
        edit_course_btn.clicked.connect(self.edit_course)
        layout.addWidget(edit_course_btn)

        delete_course_btn = QPushButton("Delete Course")
        delete_course_btn.clicked.connect(self.delete_course)
        layout.addWidget(delete_course_btn)

    def add_course(self):
        name = self.course_name_entry.text()
        course_id = self.course_id_entry.text()
        instructor_id = self.course_instructor_entry.text()

        if not name or not course_id:
            self.message_label.setText("Error: All fields must be filled out.")
            return

        # Create a Course object
        course = Course(name=name, id=course_id)

        try:
            validate_and_add_course(course)

            # Save data to a JSON file
            save_data_to_json(course, 'courses.json')

            # Update listbox and message label
            self.course_listbox.addItem(f"{course.name} (ID: {course.id})")
            self.message_label.setText("Course added successfully!")
            self.clear_course_entries()

        except ValueError as e:
            self.message_label.setText(f"Error: {e}")

    def clear_course_entries(self):
        self.course_name_entry.clear()
        self.course_id_entry.clear()
        self.course_instructor_entry.clear()

    def delete_course(self):
        selected = self.course_listbox.currentItem()
        if not selected:
            self.message_label.setText("Error: No course selected.")
            return

        course_id = selected.text().split(" (ID: ")[-1][:-1]

        # Use delete_from_json function
        if delete_from_json(course_id, 'courses.json'):
            self.populate_listboxes()
            self.message_label.setText(f"Course {course_id} deleted successfully!")
        else:
            self.message_label.setText("Error: Course ID not found in the records.")

    def edit_course(self):
        selected = self.course_listbox.currentItem()
        if not selected:
            self.message_label.setText("Error: No course selected.")
            return

        course_id = selected.text().split(" (ID: ")[-1][:-1]
        course_details = self.courses[course_id]

        # Fill the entry fields with the current course's details for editing
        self.course_name_entry.setText(course_details['name'])
        self.course_instructor_entry.setText(course_details['instructor'])
        self.course_id_entry.setText(course_id)

        save_changes_btn = QPushButton("Save Changes")
        save_changes_btn.clicked.connect(lambda: self.save_course_changes(course_id))
        self.courses_tab.layout().addWidget(save_changes_btn)

    def save_course_changes(self, course_id):
        name = self.course_name_entry.text()
        id = self.course_id_entry.text()
        instructor = self.course_instructor_entry.text()

        if not name or not id:
            self.message_label.setText("Error: All fields must be filled out.")
            return

        if id != course_id:
            self.message_label.setText("Error: Course ID cannot be changed.")
            return

        # Update the course's information
        course = Course(name=name, id=course_id, instructor=instructor)

        save_data_to_json(course, 'courses.json')
        self.load_data()
        self.populate_listboxes()
        self.clear_course_entries()
        self.message_label.setText(f"Course {course_id} updated successfully!")

    def init_search_tab(self):
        # Initialize Search Tab
        layout = QVBoxLayout()
        self.search_tab.setLayout(layout)

        self.student_search_entry = QLineEdit()
        self.instructor_search_entry = QLineEdit()
        self.courses_search_entry = QLineEdit()

        layout.addWidget(QLabel("Search Students"))
        layout.addWidget(QLabel("Search by ID:"))
        layout.addWidget(self.student_search_entry)

        search_student_btn = QPushButton("Search Student")
        search_student_btn.clicked.connect(lambda: self.perform_search("student"))
        layout.addWidget(search_student_btn)

        layout.addWidget(QLabel("Search Instructors"))
        layout.addWidget(QLabel("Search by ID:"))
        layout.addWidget(self.instructor_search_entry)

        search_instructor_btn = QPushButton("Search Instructor")
        search_instructor_btn.clicked.connect(lambda: self.perform_search("instructor"))
        layout.addWidget(search_instructor_btn)

        layout.addWidget(QLabel("Search Courses"))
        layout.addWidget(QLabel("Search by ID:"))
        layout.addWidget(self.courses_search_entry)

        search_course_btn = QPushButton("Search Course")
        search_course_btn.clicked.connect(lambda: self.perform_search("course"))
        layout.addWidget(search_course_btn)

        self.result_listbox = QListWidget()
        layout.addWidget(self.result_listbox)

    def perform_search(self, type):
        if self.student_search_entry.text():
            search_term = self.student_search_entry.text().lower()
        elif self.instructor_search_entry.text():
            search_term = self.instructor_search_entry.text().lower()
        elif self.courses_search_entry.text():
            search_term = self.courses_search_entry.text().lower()
        else:
            self.message_label.setText("Please enter an ID.")
            return

        if type == "student":
            data = load_data_from_json('students.json')
        elif type == "instructor":
            data = load_data_from_json('instructors.json')
        elif type == "course":
            data = load_data_from_json('courses.json')

        self.result_listbox.clear()
        match_found = False

        for item_id, info in data.items():
            if search_term == item_id:
                match_found = True
                # Format the information in a readable way
                if type == "student":
                    self.result_listbox.addItem(f"Name: {info['name']}")
                    self.result_listbox.addItem(f"ID: {item_id}")
                    self.result_listbox.addItem(f"Age: {info['age']}")
                    self.result_listbox.addItem(f"Email: {info['email']}")
                    self.result_listbox.addItem(f"Registered Courses: {', '.join(info['registered_courses']) if info['registered_courses'] else 'None'}")
                elif type == "instructor":
                    self.result_listbox.addItem(f"Name: {info['name']}")
                    self.result_listbox.addItem(f"ID: {item_id}")
                    self.result_listbox.addItem(f"Age: {info['age']}")
                    self.result_listbox.addItem(f"Email: {info['email']}")
                    self.result_listbox.addItem(f"Assigned Courses: {', '.join(info['assigned_courses']) if info['assigned_courses'] else 'None'}")
                elif type == "course":
                    self.result_listbox.addItem(f"Course Name: {info['name']}")
                    self.result_listbox.addItem(f"ID: {item_id}")
                    self.result_listbox.addItem(f"Instructor: {info['instructor']}")
                    self.result_listbox.addItem(f"Students: {', '.join(info['students']) if info['students'] else 'None'}")

        if not match_found:
            self.message_label.setText(f"No matching {type} found.")
        else:
            self.message_label.setText(f"Matching {type} found.")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = SchoolManagementSystem()
    window.show()
    sys.exit(app.exec_())
