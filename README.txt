------Music School Management System (MSMS)-----

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
