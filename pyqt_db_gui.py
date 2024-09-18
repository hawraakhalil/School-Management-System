from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QListWidget, QTabWidget
)
import sys
from src.database.database import create_student, read_students, update_student, delete_student, create_instructor, read_instructors, update_instructor, delete_instructor, create_course, read_course, update_course, delete_course
from src.management.school_entities import Student, Instructor, Course

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
        self.populate_listboxes()

    def populate_listboxes(self):
        # Populate students listbox
        self.student_listbox.clear()
        students = read_students()
        for student in students:
            self.student_listbox.addItem(f"{student[1]} (ID: {student[0]})")  # student[1]: name, student[0]: id

        # Populate instructors listbox
        self.instructor_listbox.clear()
        instructors = read_instructors()
        for instructor in instructors:
            self.instructor_listbox.addItem(f"{instructor[1]} (ID: {instructor[0]})")  # instructor[1]: name, instructor[0]: id

        # Populate courses listbox
        self.course_listbox.clear()
        courses = read_course()
        for course in courses:
            self.course_listbox.addItem(f"{course[1]} (ID: {course[0]})")  # course[1]: name, course[0]: id

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
        student = Student(name, int(age), email, student_id)

        try:
            create_student(student)

            # Update listbox and message label
            self.populate_listboxes()
            self.message_label.setText("Student added successfully!")
            self.clear_student_entries()

        except Exception as e:
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

        try:
            delete_student(student_id)
            self.populate_listboxes()
            self.message_label.setText(f"Student {student_id} deleted successfully!")
        except Exception as e:
            self.message_label.setText(f"Error: {e}")

    def edit_student(self):
        selected = self.student_listbox.currentItem()
        if not selected:
            self.message_label.setText("Error: No student selected.")
            return

        student_id = selected.text().split(" (ID: ")[-1][:-1]
        students = read_students()
        student_details = next((student for student in students if student[0] == student_id), None)

        if student_details:
            self.student_name_entry.setText(student_details[1])
            self.student_age_entry.setText(str(student_details[2]))
            self.student_email_entry.setText(student_details[3])
            self.student_id_entry.setText(student_details[0])

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
        student = Student(name, int(age), email, student_id)

        try:
            update_student(student)
            self.populate_listboxes()
            self.clear_student_entries()
            self.message_label.setText(f"Student {student_id} updated successfully!")
        except Exception as e:
            self.message_label.setText(f"Error: {e}")

    def init_instructors_tab(self):
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
        instructor = Instructor(name, int(age), email, instructor_id)

        try:
            create_instructor(instructor)

            # Update listbox and message label
            self.populate_listboxes()
            self.message_label.setText("Instructor added successfully!")
            self.clear_instructor_entries()

        except Exception as e:
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

        try:
            delete_instructor(instructor_id)
            self.populate_listboxes()
            self.message_label.setText(f"Instructor {instructor_id} deleted successfully!")
        except Exception as e:
            self.message_label.setText(f"Error: {e}")

    def edit_instructor(self):
        selected = self.instructor_listbox.currentItem()
        if not selected:
            self.message_label.setText("Error: No instructor selected.")
            return

        instructor_id = selected.text().split(" (ID: ")[-1][:-1]
        instructors = read_instructors()
        instructor_details = next((instructor for instructor in instructors if instructor[0] == instructor_id), None)

        if instructor_details:
            self.instructor_name_entry.setText(instructor_details[1])
            self.instructor_age_entry.setText(str(instructor_details[2]))
            self.instructor_email_entry.setText(instructor_details[3])
            self.instructor_id_entry.setText(instructor_details[0])

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
        instructor = Instructor(id = instructor_id, name = name, age = int(age), email = email )

        try:
            update_instructor(instructor)
            self.populate_listboxes()
            self.clear_instructor_entries()
            self.message_label.setText(f"Instructor {instructor_id} updated successfully!")
        except Exception as e:
            self.message_label.setText(f"Error: {e}")

    def init_courses_tab(self):
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
        course = Course(course_id, name, instructor_id)

        try:
            create_course(course)

            # Update listbox and message label
            self.populate_listboxes()
            self.message_label.setText("Course added successfully!")
            self.clear_course_entries()

        except Exception as e:
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

        try:
            delete_course(course_id)
            self.populate_listboxes()
            self.message_label.setText(f"Course {course_id} deleted successfully!")
        except Exception as e:
            self.message_label.setText(f"Error: {e}")

    def edit_course(self):
        selected = self.course_listbox.currentItem()
        if not selected:
            self.message_label.setText("Error: No course selected.")
            return

        course_id = selected.text().split(" (ID: ")[-1][:-1]
        courses = read_course()
        course_details = next((course for course in courses if course[0] == course_id), None)

        if course_details:
            self.course_name_entry.setText(course_details[1])
            self.course_instructor_entry.setText(course_details[2])
            self.course_id_entry.setText(course_details[0])

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
        course = Course(course_id, name, instructor)

        try:
            update_course(course)
            self.populate_listboxes()
            self.clear_course_entries()
            self.message_label.setText(f"Course {course_id} updated successfully!")
        except Exception as e:
            self.message_label.setText(f"Error: {e}")

    def init_search_tab(self):
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
        search_term = None
        if self.student_search_entry.text():
            search_term = self.student_search_entry.text()
        elif self.instructor_search_entry.text():
            search_term = self.instructor_search_entry.text()
        elif self.courses_search_entry.text():
            search_term = self.courses_search_entry.text()
        else:
            self.message_label.setText("Please enter an ID.")
            return

        if type == "student":
            data = read_students()
        elif type == "instructor":
            data = read_instructors()
        elif type == "course":
            data = read_course()

        self.result_listbox.clear()
        match_found = False

        for item in data:
            if search_term == item[0]:  # item[0] is the ID
                match_found = True
                # Format the information in a readable way
                if type == "student":
                    self.result_listbox.addItem(f"Name: {item[1]}")
                    self.result_listbox.addItem(f"ID: {item[0]}")
                    self.result_listbox.addItem(f"Age: {item[2]}")
                    self.result_listbox.addItem(f"Email: {item[3]}")
                elif type == "instructor":
                    self.result_listbox.addItem(f"Name: {item[1]}")
                    self.result_listbox.addItem(f"ID: {item[0]}")
                    self.result_listbox.addItem(f"Age: {item[2]}")
                    self.result_listbox.addItem(f"Email: {item[3]}")
                elif type == "course":
                    self.result_listbox.addItem(f"Course Name: {item[1]}")
                    self.result_listbox.addItem(f"ID: {item[0]}")
                    self.result_listbox.addItem(f"Instructor: {item[2]}")

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
