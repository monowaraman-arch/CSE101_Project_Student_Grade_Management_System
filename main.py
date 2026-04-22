# Load all student data once at the beginning
def load_from_file(filename):
    students = []

    try:
        infile = open(filename, "r")
        for line in infile:
                parts = line.strip().split("#") # parts = ["2321123", " Aman", " 21.0 24.0"]

                if len(parts) != 3:
                    continue

                student_id = parts[0].strip()
                student_name = parts[1].strip()
                grades_part = parts[2].strip()

                try:
                    if grades_part == "":
                        grades = []
                    else:
                        grades = list(map(float, grades_part.split()))
                except ValueError:
                    print("Invalid grade format:", line)
                    continue

                student = {
                    "id": student_id,
                    "name": student_name,
                    "grades": grades
                }

                students.append(student)

    except FileNotFoundError:
        print("Error: File not found.")

    return students

students = load_from_file("students.txt") #


# Option 1: This function displays grade information for all students
def display_all_students(students):
    # If there are no students in the list
    if len(students) == 0:
        print("No student records found.")
        input("Press Enter key to continue . . .")
        return

    # Find the maximum number of tests among all students
    max_tests = 0
    for student in students:
        if len(student["grades"]) > max_tests:
            max_tests = len(student["grades"])

    # Print header
    print(f"\n{'StudentID':<12}{'Student Name':<22}", end="")

    # Print test headings
    for i in range(max_tests):
        print(f"{'Test' + str(i + 1):<8}", end="")
    print()

    # Print all student data
    for student in students:
        print(f"{student['id']:<12}{student['name']:<22}", end="")

        for grade in student["grades"]:
            print(f"{grade:<8}", end="")
        print()

    # Wait for Enter before returning to the menu
    input("\nPress Enter key to continue . . .")


# Option 2: This function displays grade information for one particular student
def display_one_student(students):
    # Ask the user which student's information they want to see.
    student_id = input("Enter studentID: ")

    # We will use this variable to remember whether we found the student.
    student_found = False

    # Go through the student list one by one.
    for student in students:
        # Check whether the current student's ID matches the ID entered by the user.
        if student["id"] == student_id:
            student_found = True

            # Print the heading for the table first.
            print(f"\n{'StudentID':<12}{'Student Name':<22}", end="")

            # Print one test title for each grade the student has.
            # Example: if the student has 3 grades, we print Test1, Test2, Test3.
            for i in range(len(student["grades"])):
                print(f"{'Test' + str(i + 1):<8}", end="")
            print()

            # Print the student's ID and name on the same row.
            print(f"{student['id']:<12}{student['name']:<22}", end="")

            # Print all grades for that student.
            for grade in student["grades"]:
                print(f"{grade:<8}", end="")
            print()

            # We found the correct student, so no need to keep checking.
            break

    # If no matching student was found after checking the whole list,
    # show an error message.
    if student_found == False:
        print("Error: Invalid student ID")

    # Pause so the user can read the result before returning to the menu.
    input("\nPress Enter key to continue . . .")


# Option 3: This function displays the average grade of all students
def display_all_averages(students):
    # Check whether there is at least one test grade in the whole list
    has_any_test = False
    for student in students:
        if len(student["grades"]) > 0:
            has_any_test = True
            break

    # If no student has any test grade
    if has_any_test == False:
        print("No test grades available.")
        input("Press Enter key to continue . . .")
        return

    # Print table header
    print("\nStudentID   Student Name   Average")

    # Print each student's average
    for student in students:
        if len(student["grades"]) == 0:
            # If a particular student has no grades yet
            print(f'{student["id"]}   {student["name"]}   No tests')
        else:
            # Average = sum of grades / number of grades
            average = sum(student["grades"]) / len(student["grades"])

            # .1f means show 1 digit after decimal point
            print(f'{student["id"]}   {student["name"]}   {average:.1f}')

    # Wait for Enter before returning to menu
    input("\nPress Enter key to continue . . .")


# Option 4: This function modifies one quiz grade for one particular student
def modify_student_grade(students):
    # Read student ID from the user
    student_id = input("Please enter studentID: ")

    # Search for the student first
    found_student = None
    for student in students:
        if student["id"] == student_id:
            found_student = student
            break

    # If student ID is not found
    if found_student is None:
        print("Error: Invalid student ID")
        input("Press Enter key to continue . . .")
        return

    # If the student has no quiz grades yet
    if len(found_student["grades"]) == 0:
        print("Error: This student has no quiz grades yet")
        input("Press Enter key to continue . . .")
        return

    # Read quiz number
    quiz_number = int(input("Please enter quiz number to modify: "))

    # Check whether quiz number is valid
    # Example: if there are 3 grades, valid quiz numbers are 1, 2, 3
    if quiz_number < 1 or quiz_number > len(found_student["grades"]):
        print("Error: Invalid quiz number")
        input("Press Enter key to continue . . .")
        return

    # Read new quiz grade
    new_grade = float(input(f"Please enter new quiz {quiz_number} grade: "))

    # Check whether grade is valid
    if new_grade < 0 or new_grade > 100:
        print("Error: Invalid grade")
        input("Press Enter key to continue . . .")
        return

    # Print student data before modification
    print("\nBefore grade modification:" )
    print(found_student["id"], found_student["name"], end=" ")
    for grade in found_student["grades"]:
        print(grade, end=" ")
    print()

    # Modify the selected quiz grade
    # quiz_number - 1 is used because list index starts from 0
    found_student["grades"][quiz_number - 1] = new_grade

    # Print student data after modification
    print("After grade modification:", end=" ")
    print(found_student["id"], found_student["name"], end=" ")
    for grade in found_student["grades"]:
        print(grade, end=" ")
    print()

    # Wait before returning to the menu
    input("Press Enter key to continue . . .")


# Option 5: This function adds the next test grade for all students
def add_test_grades_for_all_students(students):
    # Check if there are no students
    if len(students) == 0:
        print("Error: No student records found.")
        input("Press Enter key to continue . . .")
        return

    # Find the current maximum number of tests
    # The next test number will be max + 1
    max_tests = 0
    for student in students:
        if len(student["grades"]) > max_tests:
            max_tests = len(student["grades"])

    next_test_number = max_tests + 1

    print(f"\nPlease enter test grades for Test#{next_test_number}")

    # Read one new grade for each student
    for student in students:
        while True:
            try:
                grade = float(input(f'Please enter grade for student : {student["id"]}\n'))

                # Check if the grade is valid
                if grade < 0 or grade > 100:
                    print("Error: Invalid grade")
                else:
                    # Add the new grade to that student's grades list
                    student["grades"].append(grade)
                    break

            except ValueError:
                print("Error: Invalid grade")

    input("Press Enter key to continue . . .")


# Option 6: This function adds a new student to the students list
def add_new_student(students):
    # Read the new student ID
    new_id = input("Please enter new studentID: ")

    # Check if the same ID already exists
    for student in students:
        if student["id"] == new_id:
            print("Error: Student ID already exists")
            input("Press Enter key to continue . . .")
            return

    # Read the new student name
    new_name = input("Please enter student name: ").strip()

    # Ask how many quiz grades will be entered for this new student
    try:
        number_of_quizzes = int(input("Please enter number of quizzes: "))
    except ValueError:
        print("Error: Invalid number of quizzes")
        input("Press Enter key to continue . . .")
        return

    # Number of quizzes cannot be negative
    if number_of_quizzes < 0:
        print("Error: Invalid number of quizzes")
        input("Press Enter key to continue . . .")
        return

    # Read all quiz grades one by one
    new_grades = []

    for i in range(number_of_quizzes):
        while True:
            try:
                grade = float(input(f"Please enter quiz {i + 1} grade: "))

                # Grade must be between 0 and 100
                if grade < 0 or grade > 100:
                    print("Error: Invalid grade")
                else:
                    new_grades.append(grade)
                    break

            except ValueError:
                print("Error: Invalid grade")

    # Create the new student dictionary
    new_student = {
        "id": new_id,
        "name": new_name,
        "grades": new_grades
    }

    # Add the new student to the list
    students.append(new_student)

    print("New student added successfully.")
    input("Press Enter key to continue . . .")


# Option 7: This function deletes a student by student ID
def delete_student(students):
    # Read student ID to delete
    student_id = input("Please enter studentID to delete: ").strip()

    # Search for the student using index
    for index in range(len(students)):
        if students[index]["id"] == student_id:
            # Delete the matched student from the list
            del students[index]
            print("Student deleted successfully.")
            input("Press Enter key to continue . . .")
            return

    # If loop finishes, student ID was not found
    print("Error: Invalid student ID")
    input("Press Enter key to continue . . .")


# Option 8: Save function: This function saves all student data to the same file format
def save_to_file(students):
    with open("students.txt", "w") as file:
        for student in students:
            # Convert the grades list into one space-separated string
            grades_text = " ".join(map(str, student["grades"]))

            # Write data in the same required format:
            # ID# Name# grade1 grade2 grade3
            file.write(f'{student["id"]}# {student["name"]}# {grades_text}\n')



# Part 3: Main menu loop
while True:
    print("\n--------------- MENU ----------------")
    print("1. Display Grade Info for all students")
    print("2. Display Grade Info for a particular student")
    print("3. Display tests average for all students")
    print("4. Modify a particular test grade for a particular student")
    print("5. Add test grades for a particular test for all students")
    print("6. Add a new Student")
    print("7. Delete a student")
    print("8. Save and Exit")

    choice = input("Please select your choice: ")

    if choice == "1":
        display_all_students(students)

    elif choice == "2":
        display_one_student(students)

    elif choice == "3":
        display_all_averages(students)

    elif choice == "4":
        modify_student_grade(students)

    elif choice == "5":
        add_test_grades_for_all_students(students)


    elif choice == "6":
        add_new_student(students)


    elif choice == "7":
        delete_student(students)

    elif choice == "8":
        save_to_file(students)
        print("Data saved. Exiting program.")
        break

    else:
        print("Error: Invalid choice")
        input("Press Enter key to continue . . .")
