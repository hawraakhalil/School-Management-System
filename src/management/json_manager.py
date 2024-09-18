import json
import os
import re
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from management.school_entities import Student, Instructor, Course

# Defining Methods for Serialization
def save_data_to_json(obj, filename):
    # Path to the 'data' directory
    data_directory = 'src/data'
    
    # Construct the full path to the JSON file inside the 'data' folder
    file_path = os.path.join(data_directory, filename)
    # Create the file if it does not exist
    if not os.path.exists(file_path):
        with open(file_path, 'w') as json_file:
            json.dump({}, json_file)  # Initialize with an empty dictionary

    # Read existing data
    with open(file_path, 'r') as json_file:
        try:
            data = json.load(json_file)
        except json.JSONDecodeError:
            data = {}  # In case the file is empty or invalid

    # Check the type of the object and save the appropriate data
    if isinstance(obj, Student):
        obj_id = obj.id  # Get the student ID
        data[obj_id] = {
            "type": "student",
            "name": obj.name,
            "age": obj.age,
            "email": obj.email,  
            "registered_courses": [course  for course in obj.registered_courses] 
        }
    elif isinstance(obj, Instructor):
        obj_id = obj.id  # Get the instructor ID
        data[obj_id] = {
            "type": "instructor",
            "name": obj.name,
            "age": obj.age,
            "email": obj.email, 
            "assigned_courses": obj.assigned_courses
        }
    elif isinstance(obj, Course):
        obj_id = obj.id  # Get the course ID
        data[obj_id] = {
            "type": "course",
            "name": obj.name,
            "instructor": obj.instructor,
            "students": [student  for student in obj.students] 
        }
    else:
        raise ValueError("Object must be an instance of Student, Instructor, or Course.")

    # Write the updated data back to the file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Loading data from a JSON file
def load_data_from_json(filename):
    # Path to the 'data' directory
    data_directory = 'src/data'
    
    # Construct the full path to the JSON file inside the 'data' folder
    file_path = os.path.join(data_directory, filename)
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

def delete_from_json(entry_id : str, filename : str):
    """
    Deletes an entry from a JSON file.
    
    Parameters:
        entry_id (str): The ID of the entry to be deleted.
        file_path (str): The path to the JSON file to be modified.
    """
    # Path to the 'data' directory
    data_directory = 'src/data'
    
    # Construct the full path to the JSON file inside the 'data' folder
    file_path = os.path.join(data_directory, filename)
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    if entry_id in data:
        # Delete the entry from the loaded data
        del data[entry_id]

        # Save the modified data back to the JSON file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        return True
    else:
        return False

#2. Implementing Data Validation
def is_valid_email(email: str):
    email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(email_regex, email) is not None

def is_valid_age(age: int):
    return age >= 0

def validate_and_add_user(obj):
    if not is_valid_email(obj.email):
        raise ValueError("Invalid email address")
    if not is_valid_age(obj.age):
        raise ValueError("Age must be non-negative")
    if obj.id in load_data_from_json('students.json'):
        raise ValueError(f"Student with ID {obj.id} already exists")
    if obj.id in load_data_from_json('instructors.json'):
        raise ValueError(f"Instructor with ID {obj.id} already exists")

def validate_and_add_course(obj):
    if obj.id in load_data_from_json('courses.json'):
        raise ValueError(f"Course with ID {obj.id} already exists")
    print(f"Adding {obj.name} to the system.")

# Function to create JSON files if they do not exist
def create_json_files():
    # Directory where the JSON files will be stored
    data_directory = 'src/data'

    # Create the directory if it doesn't exist
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    # File names with paths pointing to the data directory
    file_names = [os.path.join(data_directory, 'students.json'), 
                  os.path.join(data_directory, 'instructors.json'), 
                  os.path.join(data_directory, 'courses.json')]

    for file_name in file_names:
        if not os.path.exists(file_name):
            # Create an empty JSON file with an empty dictionary
            with open(file_name, 'w') as file:
                json.dump({}, file)
