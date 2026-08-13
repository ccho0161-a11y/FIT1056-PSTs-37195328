------Music School Management System (MSMS)-----

PST 1: In-Memory System
Purpose:
    An application run by Python which helps in managing students and teachers at the music school.
    PST1 is an in-memory prototype, so every time the program ends the data input will be lost.

How to run:
    1. Preferably have Python 3.14.6 installed (Python 3 is also acceptable)
    2. Run the file "MSMS.py"
    3. Interact with the menu in the terminal 

Features:
    Data models:
        > The "Student" class stores their ID, name and enrolled instruments 
        > The "Teacher" class stores their ID, name and instrument speciality.
    Core helper functions:
        > "add_teacher" allows for the addition of teachers and their information into the data base
        > "list_students" and "list_teachers" respectively print out the students/teachers in the database and their information
        > "find_students" searches for students by name from letters input by the user
        > "find_teachers" searches for teachers by name or speciality matching the letter input from the user
    Front desk functions:
        > "front_desk_register" adds new students to the existing list of students
        > "front_desk_enrol" adds existing students to another instrument course
        > "front_desk_lookup" allows the user to search for students and teachers in the database (combines "find_students" and "find_teachers")
    Main menu: allows the user to add, search for and enrol students as well as adding and searching for teachers. Lists of all students and teachers can be printed.

How to test:
    1. Register the first (new) student
    2. Try to enrol a student using a valid ID then an invalid ID
    3. Search for a student (by name) or teacher (by name or speciality)
    4. List all the existing students
    5. List all the existing teachers (2 sample teachers "Dr. Keys" and "Ms. Fret" are preset)
    6. Press "q" to exit the program

Design choices/assumptions
    > The assignation of IDs are automated and does not allow the user to create one for a student or teacher
    > When searching for a student or teacher the term entered is not case sensitive and can match single letters or parts of a name
    > Invalid IDs when enrolling provides an error message instead of crashing the program 

=========================================================================================================================================================================================

PST2: Persistence System
Purpose:
    An improved application from PST1 to pst2_main.py which replaces the in-memory system (data is lost once application is closed) with a msms.json file providing permanent storage.
    It retains features allowing for CRUD (creating, reading, updating and deleting) while adding new features such as student check_in and a printable student card.

How to run:
    1. Preferably have Python 3.14.6 installed (Python 3 is also acceptable)
    2. Run the file "pst2_main.py"
    3. Interact with the menu in the terminal 

Features:
    Persistence application:
        > "load_data" obtains the existing data in the JSON file when the application is run
        > "save_data" adds any data from the running of the application into the same JSON file so it can also be accessed next time the program is run
    CRUD functions:
        > "add_teacher" and "add_student" allows for the addition for the names of new teachers/students as well as their specialities/classes respectively
        > "update_teacher" and "update_student" allows for the updating of their information such as names or specialities/classes respectively
        > "remove_teacher" and "remove_student" allows for deleting teachers/students along with their data from the system
    Receptionist features:
        > "check_in" allows the user to record students' attendance of their classes
        > "print_student_card" creates a formatted text file with the student's information
    Main menu: provides the main user interface that loads the data from JSON upon startup and automatically saves any changes made after any change as well as upon exiting the program

How to test:
    1. Run the "pst2_main.py" file and add student(s) and teacher(s)
    2. Check the student into their class
    3. Print their student card and open the created .txt file
    4. Update the student's and teacher's details
    5. Remove the student
    6. Quit and restart the program to confirm the correct data was saved from msms.json

Design choices/assumptions:
    > Added "add_student" and a menu option corresponding to it, allowing the rest of the functions to work as the initial data stores are empty
    > "update_teacher" and "update_student" use **fields so not all fields must be changed at once and can preserve previous entries if unchanged
    > "check_in" ensures there is a student that exists under the ID before allowing them to be checked in 
    > "update_student" was given a menu option so their data can be edited easily like the teachers' data
    > The assignation of IDs are automated and does not allow the user to create one for a student or teacher