# School Management System

This School Management System is a Python-based project designed to manage students, instructors, and courses efficiently. The system is implemented using three different graphical user interfaces (GUIs) with varied data storage methods, providing flexibility in managing and storing data.

## Features

All four versions of the system include the following features:
- **Student Management**: Add, edit, delete student records.
- **Instructor Management**: Add, edit, delete instructor records.
- **Course Management**: Add, edit, delete course records.
- **Instructor Assignment**: Assign instructors to specific courses.
- **Course Registration**: Register students for courses.
- **Search Functionality**: Search for students, instructors, and courses.
  
### Available GUIs

1. **Tkinter JSON-Based GUI (`tkinter_json_gui`)**
   - Implements the user interface using Tkinter.
   - Data is stored in and loaded from JSON files.

2. **Tkinter Database-Based GUI (`tkinter_db_gui`)**
   - Implements the user interface using Tkinter.
   - Utilizes SQLite3 database for data persistence.
   - Implements full CRUD (Create, Read, Update, Delete) operations with database management.

2. **PyQt JSON-Based GUI (`pyqt_json_gui`)**
   - Implements the user interface using PyQt.
   - Data is stored in and loaded from JSON files.

3. **PyQt Database-Based GUI (`pyqt_db_gui`)**
   - Implements the user interface using PyQt.
   - Utilizes SQLite3 database for data persistence.
   - Implements full CRUD (Create, Read, Update, Delete) operations with database management.

## Installation

### Prerequisites
- Python 3.x
- Required Python libraries: 
  - Tkinter (for `tkinter_json_gui` and `tkinter_db_gui`)
  - PyQt5 (for `pyqt_json_gui` and `pyqt_db_gui`)
  - SQLite3 (for `pyqt_db_gui` and `tkinter_db_gui`)

### Installation Instructions
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/school-management-system.git
   cd school-management-system```
2. Install the required Python packages:
   ```bash
   pip install pyqt5```

## Usage

### Running the Tkinter JSON-Based GUI (`tkinter_json_gui`)
To run the Tkinter version:
   ```bash
   python tkinter_json_gui.py
 ```
### Running the Tkinter Database-Based GUI (`tkinter_db_gui`)
To run the Tkinter version:
   ```bash
   python tkinter_db_gui.py
 ```
### Running the PyQt JSON-Based GUI (pyqt_json_gui)
To run the PyQt version that uses JSON for data storage: ana jon
   ```bash
   python pyqt_json_gui.py
```
### Running the PyQt Database-Based GUI (pyqt_db_gui)
To run the Tkinter version:
   ```bash
   python pyqt_db_gui.py
```
## Data Storage

- **JSON-Based GUIs**: Data is stored locally in JSON files. Ensure that you have read and write access to the working directory.
- **Database-Based GUI**: The SQLite3 database is used for data persistence, ensuring robust data management and efficient querying.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

