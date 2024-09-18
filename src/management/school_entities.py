class Person:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email
    def introduce(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")

class Student(Person):
    def __init__(self, name, age, email, id, registered_courses = []):
        super().__init__(name, age, email)
        self.id = id
        self.registered_courses = registered_courses
        
    def register_course(self, course):
        self.registered_courses.append(course)

class Instructor(Person):
    def __init__(self, name, age, email, id, assigned_courses = []):
        super().__init__(name, age, email)
        self.id = id
        self.assigned_courses = assigned_courses

    def assign_course(self, course):
        self.assigned_courses.append(course)

class Course:
    def __init__(self, id, name, instructor = "TBA", students=[]):
        self.id = id
        self.name = name
        self.instructor = instructor
        self.students = students
    def add_student(self, student):
        self.students.append(student)
    def assign_instructor(self, instructor):
        self.instructor = instructor
    
