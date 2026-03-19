#------ADMIN-------------------------------------------------------------------
def admin_login():
    preset_username = "admin"
    preset_password = "admin123"

    while True:
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()

        if username == preset_username and password == preset_password:
            print("Login successful\n")
            display_menu()  # Call the admin menu after login
            return  # Exit the loop after successful login
        else:
            print("Login unsuccessful. Try again\n")

def display_menu():
    print("Welcome to the Education Management System - Administrator Panel")
    while True:
        print("\n1. Manage User Accounts")
        print("2. Manage Student Records")
        print("3. Manage Course Offerings")
        print("4. Maintain Class Schedule")
        print("5. Generate Reports")
        print("6. Logout")
        choice = input("Enter your choice: ")
        if choice == "1":
            manage_user_accounts()
        elif choice == "2":
            manage_student_records()
        elif choice == "3":
            manage_course_offerings()
        elif choice == "4":
            maintain_class_schedule()
        elif choice == "5":
            generate_reports()
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid choice! Please select a valid option.")


def read_data_from_file(filename):
    try:
        with open(filename, "r") as f:
            data = [line.strip().split(",") for line in f]
        return data
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return []


def write_data_to_file(filename, data, append=False):
    mode = "a" if append else "w"
    try:
        with open(filename, mode) as f:
            for row in data:
                f.write(",".join(row) + "\n")
        return True
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return False
    except PermissionError:
        print(f"Error: You do not have permission to write to {filename}.")
        return False
    except Exception as e:
        print(f"Error writing to {filename}: {e}")
        return False


def manage_user_accounts():
    filename = "user.txt"
    while True:
        print("\n1. Create User Account")
        print("2. Delete User Account")
        print("3. Update User Credentials")
        print("4. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_user_account(filename)
        elif choice == "2":
            delete_user(filename)
        elif choice == "3":
            update_user(filename)
        elif choice == "4":
            break
        else:
            print("Invalid choice! Please select a valid option.")

def generate_teacher_id():
    file_name = "user.txt"
    highest_id = 0  # Start from T1 if no teacher exists

    try:
        with open(file_name, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if parts and parts[0].startswith("T") and parts[0][1:].isdigit():
                    user_id = int(parts[0][1:])  # Extract number after "T"
                    if user_id > highest_id:  # Manually track the highest ID
                        highest_id = user_id

    except FileNotFoundError:
        pass  # No file means no users, start from T1

    return f"T{highest_id + 1}"  # Next ID

def generate_staff_id():
    file_name = "user.txt"
    highest_id = 0  # Start from S1 if no staff exists

    try:
        with open(file_name, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if parts and parts[0].startswith("S") and parts[0][1:].isdigit():
                    user_id = int(parts[0][1:])  # Extract number after "S"
                    if user_id > highest_id:  # Manually track the highest ID
                        highest_id = user_id

    except FileNotFoundError:
        pass  # No file means no users, start from S1

    return f"S{highest_id + 1}"  # Next ID

def create_user_account(filename):
    username = input("Enter username: ")
    password = input("Enter password: ")
    role = input("Enter role (Teacher/Staff): ").strip().lower()

    if not (username and password and role):
        print("Error: All fields are required.")
        return

    users = read_data_from_file(filename)
    if any(user[0] == username for user in users):
        print("Error: Username already exists.")
        return

    # Assign correct ID based on role
    if role == "teacher":
        user_id = generate_teacher_id()
    elif role == "staff":
        user_id = generate_staff_id()
    else:
        print("Error: Invalid role.")
        return

    new_user = [[user_id, username, password, role]]  # Save user with unique ID

    if write_data_to_file(filename, new_user, append=True):
        print(f"User account created successfully with ID {user_id}.")
    else:
        print("Error creating user account.")


def delete_user(filename):
    username = input("Enter username to delete: ")
    users = read_data_from_file(filename)
    updated_users = [user for user in users if user[1] != username]

    if len(users) == len(updated_users):
        print(f"User '{username}' not found.")
    elif write_data_to_file(filename, updated_users):
        print(f"User '{username}' deleted successfully.")
    else:
        print("Error deleting user.")


def update_user(filename):
    username = input("Enter username to update: ")
    new_password = input("Enter new password: ")

    users = read_data_from_file(filename)
    updated = False

    for i, user in enumerate(users):
        if user[1] == username:
            users[i] = [user[0], username, new_password, user[3]]  # Retain existing role
            updated = True
            break

    if not updated:
        print(f"User '{username}' not found.")
    elif write_data_to_file(filename, users, append=False):  # Overwrite file with updates
        print("User credentials updated successfully.")
    else:
        print("Error updating user credentials.")


def manage_student_records():
    filename = "student.txt"
    while True:
        print("\n1. View Student Records")
        print("2. Update Student Details")
        print("3. Add Student Record")
        print("4. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            view_student_records(filename)
        elif choice == "2":
            update_student_details(filename)
        elif choice == "3":
            add_student_record(filename)
        elif choice == "4":
            break
        else:
            print("Invalid choice! Please select a valid option.")

def view_student_records(filename):
    students = read_data_from_file(filename)
    if students:
        for student in students:
            print(",".join(student))
    else:
        print("No student records found.")


def add_student_record(filename):
    user = input("Enter student username: ")
    password = input("Enter student password: ")
    name = input("Enter student name: ")
    age = input("Enter student age: ")
    phone_num = input("Enter student contact number: ")
    emergency_num = input("Enter emergency number: ")

    student_id = generate_student_id()

    if not (user and password and name and age and phone_num and emergency_num):
        print("Error: All fields are required.")
        return

    new_student = [[student_id,user,password,name,age,phone_num,emergency_num]]

    if write_data_to_file(filename, new_student, append=True):
        print(f"User account created successfully with ID {student_id}.")
    else:
        print("Error adding student record.")


def update_student_details(filename):
    student_id = input("Enter student ID to update: ")

    students = read_data_from_file(filename)
    updated = False

    for i, student in enumerate(students):
        if student[0] == student_id:
            user = input(f"Enter new username (current: {student[1]}) or leave blank to current:  ") or student[1]
            password = input(f"Enter new password (current: {student[2]}) or leave blank to current: ") or student[2]
            name = input(f"Enter new name (current: {student[3]}) or leave blank to current: ") or student[3]
            age = input(f"Enter new age (current: {student[4]}) or leave blank to current: ") or student[4]
            phone_num = input(f"Enter new contact number (current: {student[5]}) or leave blank to current: ") or student[5]
            emergency_num = input(f"Enter new emergency number (current: {student[6]}) or leave blank to current: ") or student[6]

            students[i] = [student_id,user,password,name,age,phone_num,emergency_num]
            updated = True
            break

    if not updated:
        print(f"Student with ID '{student_id}' not found.")
    elif write_data_to_file(filename, students):
        print("Student details updated successfully.")
    else:
        print("Error updating student details.")


def manage_course_offerings():
    filename = "courses.txt"
    while True:
        print("\n1. Add Course")
        print("2. Update Course")
        print("3. Delete Course")
        print("4. Assign Instructor")
        print("5. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_course(filename)
        elif choice == "2":
            manage_course(filename)
        elif choice == "3":
            remove_course(filename)
        elif choice == "4":
            assign_instructor(filename)
        elif choice == "5":
            break
        else:
            print("Invalid choice! Please select a valid option.")


def add_course(filename):
    course_name = input("Enter course name: ")
    course_id = input("Enter course id: ")
    course_description = input("Enter course description : ")

    if not (course_name and course_id and course_description):
        print("Error: All fields are required.")
        return

    courses = read_data_from_file(filename)
    if any(course[1] == course_id for course in courses):
        print("Error: Course code already exists.")
        return

    new_course = [[course_name, course_id, course_description]]

    if write_data_to_file(filename, new_course, append=True):
        print("Course added successfully.")
    else:
        print("Error adding course.")


def manage_course(filename):
    course_code = input("Enter course code to update: ")

    courses = read_data_from_file(filename)
    updated = False

    for i, course in enumerate(courses):
        if course[1] == course_code:
            course_name = input(f"Enter new course name (current: {course[0]}): ") or course[0]
            description = input(f"Enter new description (current: {course[2]}): ") or course[2]

            courses[i] = [course_name, course_code, description]
            updated = True
            break

    if not updated:
        print(f"Course with code '{course_code}' not found.")
    elif write_data_to_file(filename, courses):
        print("Course updated successfully.")
    else:
        print("Error updating course.")


def remove_course(filename):
    course_code = input("Enter course code to delete: ")

    courses = read_data_from_file(filename)
    updated_courses = [course for course in courses if course[1] != course_code]

    if len(courses) == len(updated_courses):
        print(f"Course with code '{course_code}' not found.")
    elif write_data_to_file(filename, updated_courses):
        print("Course deleted successfully.")
    else:
        print("Error deleting course.")


def assign_instructor(filename):
    course_code = input("Enter course code: ").strip()
    instructor = input("Enter instructor name: ").strip()

    if not course_code or not instructor:
        print("Error: Course code and instructor name are required.")
        return

    try:
        courses = read_data_from_file(filename)
        if courses is None: # handle cases when file reading failed.
            return

        updated = False

        for i, course in enumerate(courses):  # Iterate courses
            if course[1] == course_code:  # Check code
                if len(course) > 2:
                    courses[i] = course[:3] + [instructor]
                else:
                    courses[i] = course + [instructor]  # Append instructor
                updated = True
                break

        if not updated:
            print(f"Course '{course_code}' not found.")
        elif write_data_to_file(filename, courses):  # Write updated data
            print("Instructor assigned.")
        else:  # Write error
            print("Error assigning instructor.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}") # handle unexpected errors

def maintain_class_schedule():
    while True:
        print("\n1. Generate and view timetable")
        print("2. Update timetable")
        print("3. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            generate_and_view_timetable(CLASS_FILE, TIMETABLE_FILE)
        elif choice == "2":
            update_timetable(CLASS_FILE, TIMETABLE_FILE)
        elif choice == "3":
            break
        else:
            print("Invalid choice! Please select a valid option.")


def generate_and_view_timetable(class_filename, timetable_filename):
    classes = read_data_from_file(class_filename)
    if not classes:
        print("No class records found. Cannot generate timetable.")
        return

    timetable_data = []
    for class_info in classes:
        if len(class_info) >= 3:
            timetable_data.append([class_info[1], class_info[2]])  # class_id, schedule

    if write_data_to_file(timetable_filename, timetable_data):
        print("\nUpdated Timetable:")
        timetable = read_data_from_file(timetable_filename)
        if timetable:
            for entry in timetable:
                print(",".join(entry))
        else:
            print("Timetable generated, but is empty.")
    else:
        print("Error generating timetable.")


def update_timetable(class_filename, timetable_filename):
    class_id = input("Enter the class ID to update: ")
    new_time = input("Enter the new schedule: ")

    timetable = read_data_from_file(timetable_filename)
    if not timetable:
        print("Timetable file not found. Generate it first.")
        return

    timetable_updated = False
    updated_timetable = []
    old_time = None  # Store old schedule for announcement

    for entry in timetable:
        if entry[0] == class_id:
            old_time = entry[1]  # Store old schedule before updating
            updated_timetable.append([class_id, new_time])  # Update schedule
            timetable_updated = True
        else:
            updated_timetable.append(entry)

    if not timetable_updated:
        print(f"Class ID '{class_id}' not found in timetable.")
        return

    if write_data_to_file(timetable_filename, updated_timetable):
        print("Timetable updated successfully.")
    else:
        print("Error updating timetable.")
        return

    classes = read_data_from_file(class_filename)
    if not classes:
        print("Error: Class file not found.")
        return

    updated_classes = []
    for class_info in classes:
        if class_info[1] == class_id:  # Class ID matches
            old_time = old_time or class_info[2]  # Ensure we have old schedule
            class_info[2] = new_time  # Update schedule
            updated_classes.append(class_info)
        else:
            updated_classes.append(class_info)

    if write_data_to_file(class_filename, updated_classes):
        print("Class schedule updated successfully in class file.")
        # Call save_announcement function
        save_announcement(class_id, old_time, new_time, "schedule")
    else:
        print("Error updating class schedule in class file.")


def generate_reports():
    while True:
        print("\n1. Academic Performance Report")
        print("2. Financial Report")
        print("3. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            generate_academic_report()
        elif choice == "2":
            generate_financial_report()
        elif choice == "3":
            break
        else:
            print("Invalid choice! Please select a valid option.")


def generate_academic_report():
    filename = "stu_academic_info.txt"
    try:
        with open(filename, "r", encoding="utf-8") as f:
            print("\n--- Academic Performance Report ---")
            content = f.read()
            print(content)

    except FileNotFoundError:
        print(f"Error: {filename} not found.")


def generate_financial_report():
    filename = "finance.txt"
    try:
        with open(filename, "r") as f:
            print("\n--- Financial Report ---")
            for line in f:
                print(line.strip())
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
#------STUDENT------------------------------------------------------------------------
def student_menu():
    while True:
        print("------------------------")
        print("STUDENT DASHBOARD")
        print("------------------------")
        print(f"1.Student Menu\n2.Exit")
        print("------------------------")
        select1 = int(input("Make a selection from 1~2: "))
        if select1 == 1:
            while True:
                print("------------------------")
                print("STUDENT MENU")
                print("------------------------")
                print("1.Create\n2.Login\n3.Back")
                select2 = int(input("Make a selection from 1 ~ 3: "))
                if select2 == 1:
                    create()
                    break
                elif select2 == 2:
                    login()
                    break
                elif select2 == 3:
                    print("Thank You")
                    break
                else :
                    print("Invalid input")
                    break
        else :
            print("Exit")
            break

def generate_student_id():
    file_name = "student.txt"

    try:
        with open(file_name, "r") as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]  # Remove empty lines

            if lines:
                last_line = lines[-1].split(",")  # Get last student's data

                if last_line[0].startswith("TP") and last_line[0][2:].isdigit():
                    last_id = int(last_line[0][2:])  # Extract numeric part after 'TP'
                else:
                    last_id = 0  # Start from TP1 if format is incorrect
            else:
                last_id = 0  # Start from TP1 if file is empty
    except FileNotFoundError:
        last_id = 0  # Start from TP1 if file does not exist

    return f"TP{last_id + 1}"  #  Starts from TP1

def create():
    print("------------------------")
    print("CREATE NEW ACCOUNT")
    print("------------------------")

    user = input("Enter your username name: ").strip()

    try:
        with open("student.txt", "r") as sFile:
            for line in sFile:
                stored_user = line.strip().split(",")[1]  # Username is now in the second column
                if stored_user == user:
                    print("This username has already been used. Please try another.")
                    return
    except FileNotFoundError:
        print("No existing account file found, creating a new one.")

    student_id = generate_student_id()  # Generate unique ID

    while True:
        password = input("Enter your password: ").strip()
        name = input("Enter your name: ").strip()

        while True:
            try:
                age = int(input("Enter your age: "))
                break
            except ValueError:
                print("Invalid age! Please enter a number.")

        while True:
            try:
                contact = int(input("Enter your contact number: "))
                break
            except ValueError:
                print("Invalid contact number! Please enter a number.")

        while True:
            try:
                emergency = int(input("Enter your emergency number: "))
                break
            except ValueError:
                print("Invalid emergency number! Please enter a number.")

        with open("student.txt", "a") as file:
            file.write(f"{student_id},{user},{password},{name},{age},{contact},{emergency}\n")

        print(f"Account created successfully! Your Student ID is {student_id}")
        break  # Exit loop

def login():
    # Handle student login
    print("------------------------")
    print("STUDENT LOGIN")
    print("------------------------")

    user = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    try:
        # Open student.txt and verify login credentials
        with open("student.txt", "r") as sFile:
            for line in sFile:
                account = line.strip().split(",")
                if account[1] == user and account[2] == password:
                    print(f"Login Successful! Welcome {account[3]} {account[0]}")
                    loginmenu(account)  # Redirect to login menu
                    return

        print("Invalid username or password. Please try again.")

    except FileNotFoundError:
        print("Error: student.txt not found! Please create an account first.")

    except Exception as x:
        print(f"\nAn error occurred: {x}\n")

def loginmenu(account):
    while True:
        # Display student login menu
        print("\n------------------------")
        print("STUDENT LOGIN MENU")
        print("------------------------")
        print(f"Welcome, {account[3]} ({account[0]})!")
        print("1. Student Account Management")
        print("2. Course Enrolment")
        print("3. Course Material")
        print("4. Grades Tracking")
        print("5. Feedback Submission")
        print("6. Logout")
        print("------------------------")

        # Get user selection
        select2 = input("Make your selection from 1 ~ 6: ").strip()

        if select2 == "1":
            student_account(account)
        elif select2 == "2":
            student_course(account)
        elif select2 == "3":
            student_class(account)
        elif select2 == "4":
            student_grades(account)
        elif select2 == "5":
            student_feedback(account)
        elif select2 == "6":
            print("\nLogging out!")
            break
        else:
            print("\nInvalid selection. Please enter within 1 ~ 6")

def student_account(account):
    while True:
        # Display student account management menu
        print("\n------------------------")
        print(f"STUDENT ACCOUNT MANAGEMENT - {account[3]} ({account[0]})")
        print("------------------------")
        print("1. View Profile")
        print("2. Update Details")
        print("3. Back")
        print("------------------------")

        # Get user selection
        select3 = input("Make your selection from 1 ~ 3: ").strip()

        if select3 == "1":
            # Display student profile details
            print("\n------------------------")
            print(f"PROFILE DETAILS - {account[3]} ({account[0]})")
            print("------------------------")
            print(f"Username: {account[1]}")
            print(f"Password: {account[2]}")
            print(f"Name: {account[3]}")
            print(f"Student ID: {account[0]}")
            print(f"Age: {account[4]}")
            print(f"Contact: {account[5]}")
            print(f"Emergency Contact: {account[6]}")
        elif select3 == "2":
            updatedetails(account)  # Call function to update details
        elif select3 == "3":
            print("\nReturning to Login Menu")
            break
        else:
            print("\nIncorrect input")


def updatedetails(account):
    # Allow user to update profile details
    print("\n------------------------")
    print(f"UPDATE PROFILE DETAILS - {account[3]} ({account[0]})")
    print("------------------------")

    # Prompt user for new details, keeping old values if left blank
    new_name = input(f"Enter new name (Leave blank to keep '{account[3]}'): ").strip() or account[3]

    while True:
        new_age = input(f"Enter new age (Leave blank to keep '{account[4]}'): ").strip()
        if new_age == "":
            new_age = account[4]
            break
        if new_age.isdigit():
            new_age = int(new_age)
            break
        else:
            print("Invalid age! Please enter a valid number.")

    while True:
        new_contact = input(f"Enter new contact number (Leave blank to keep '{account[5]}'): ").strip()
        if new_contact == "":
            new_contact = account[5]
            break
        if new_contact.isdigit():
            break
        else:
            print("Invalid contact number! Please enter only digits.")

    while True:
        new_emergency = input(f"Enter new emergency contact (Leave blank to keep '{account[6]}'): ").strip()
        if new_emergency == "":
            new_emergency = account[6]
            break
        if new_emergency.isdigit():
            break
        else:
            print("Invalid emergency contact number! Please enter only digits.")

    # Update account details
    account[3], account[4], account[5], account[6] = new_name, new_age, new_contact, new_emergency

    # Read all student records and update the matching account
    with open("student.txt", "r") as sFile:
        lines = sFile.readlines()

    with open("student.txt", "w") as sFile:
        for line in lines:
            stored_account = line.strip().split(",")
            if stored_account[1] == account[1]:  # Find the matching student record using a unique identifier
                sFile.write(
                    f"{account[0]},{account[1]},{account[2]},{new_name},{new_age},{new_contact},{new_emergency}\n")
            else:
                sFile.write(line)

    print("\nProfile updated successfully!")

def student_course(account):
    while True:
        # Display student class enrolment menu
        print("\n------------------------")
        print(f"STUDENT CLASS ENROLMENT - {account[3]} ({account[0]})")
        print("------------------------")
        print("1. Browse available course")
        print("2. Enrol in classes ")
        print("3. Back")
        print("------------------------")

        # Get user selection
        select4 = input("Make your selection from 1 ~ 3: ")

        if select4 == "1":  # Option to browse available courses
            try:
                # Open course file and display contents
                with open("courses.txt", "r") as scFile:
                    content = scFile.read()
                    print(f"\n{content}")
            except FileNotFoundError:  # Handle missing file error
                print("File does not exist")


        elif select4 == "2":  # Option to enroll in a class

            try:

                # Open class file and read existing data

                with open("stu_academic_info.txt", "r") as sclFile:

                    lines = sclFile.readlines()

                updated_lines = []  # List to store updated class records

                found = False  # Flag to track if student is found

                for line in lines:

                    # Split line into fields

                    stored_student_account = line.strip().split(",")

                    # Check if student exists in the class file

                    if stored_student_account[0] == account[0]:

                        # Prompt user to select a class

                        course_class = input("Which class would you like to enrol? Class 1 or Class 2: ")

                        # Append selected class to student's record

                        updated_line = f"{stored_student_account[0]},{stored_student_account[1]},{stored_student_account[2]},{stored_student_account[3]},{stored_student_account[4]},{stored_student_account[1]}-{course_class}\n"

                        updated_lines.append(updated_line)  # Store updated record

                        print("You have successfully enrolled in your selected class")

                        found = True  # Mark student as found

                    else:

                        updated_lines.append(line)  # Keep other records unchanged

                if not found:  # If student record was not found in the file

                    print("User has not been enrolled to a course yet")

                # Write updated class records back to the file

                with open("stu_academic_info.txt", "w") as sclFile:

                    sclFile.writelines(updated_lines)


            except FileNotFoundError:  # Handle missing class file error

                print("File not found.")


            except Exception as x:

                print(f"\nAn error occurred: {x}\n")

        elif select4 == "3":  # Option to return to login menu
            print(" Returning to Login Menu")
            break

        else:  # Handle invalid selection
            print("Invalid selection. Please enter within 1 ~ 3")

def student_class(account):
    while True:
        # Display class material menu
        print("\n------------------------")
        print(f"STUDENT CLASS MATERIAL - {account[3]} ({account[0]})")
        print("------------------------")
        print("1. View & Download material")
        print("2. Read announcement")
        print("3. Back")
        print("------------------------")

        # Get user selection
        select5 = input("Make your selection from 1 ~ 2: ")

        if select5 == "1":  # Option to view and download materials
            try:
                # Open class file to retrieve student's enrolled class
                with open("stu_academic_info.txt", "r") as sclFile:
                    class_lines = sclFile.readlines()

                student_classes = None  # Variable to store the student's class

                # Search for the student's class in stu_academic_info.txt
                for line in class_lines:
                    stored_student_account = line.strip().split(",")
                    if stored_student_account[0].strip() == account[0].strip():
                        student_classes = stored_student_account[5].strip()
                        break  # Stop searching after finding the student's class

                if student_classes:  # FIXED: Correct variable name
                    # Open material file to check for class materials
                    with open("class.txt", "r") as mFile:
                        material_lines = mFile.readlines()

                    found = False  # Flag to track if materials are found

                    # Search for materials related to the student's class
                    for mline in material_lines:
                        stored_class = mline.strip().split(",")
                        if stored_class[1].strip() == student_classes.strip():
                            print(f"\nMaterials for {student_classes}:")
                            for material in stored_class[2:]:  # Print all materials
                                print(f"- {material.strip()}")
                            found = True  # Mark materials as found

                    if not found:  # If no materials were found for the class
                        print("No materials found for your class")
                else:
                    print("No class found for your account")

            except FileNotFoundError:  # Handle missing file error
                print("Error: One or more files not found")

            except IndexError:  # Handle incorrect file format error
                print("Error: Incorrect file format. Please check stu_academic_info.txt and class.txt")

            except Exception as x:
                print(f"\nAn error occurred: {x}\n")
        elif select5 == "2":
            try:
                with open("announcements.txt", "r") as aFile:
                    read = aFile.readlines()

                    for line in read:
                        data = line.strip().split(",")  # Split the line by commas

                        if len(data) >= 4:  # Ensure there are enough values
                            type_ = data[1]
                            class_id = data[0]
                            old = data[2]
                            new = data[3]

                            print(f"Type: {type_} | Class_ID: {class_id} | Changed from Old: {old} to New: {new}")
                        else:
                            print("Invalid data format in announcements.txt")

            except FileNotFoundError:
                print("File doesn't exist")

            except Exception as x:
                print(f"\nAn error occurred: {x}\n")

        elif select5 == "3":  # Option to return to login menu
            print("Returning to Login Menu")
            break

        else:  # Handle invalid selection
            print("\nInvalid selection. Please enter within 1 ~ 2")

def student_grades(account):
    while True:
        # Display menu for tracking student grades
        print("\n------------------------")
        print(f"STUDENT ACADEMIC INFORMATION - {account[3]} ({account[0]})")
        print("------------------------")
        print("1. Academic info")
        print("2. Back")
        print("------------------------")

        # Get user selection
        select6 = input("Make your selection 1 ~ 2: ")

        if select6 == "1":
            try:
                # Open grades.txt to retrieve student grades
                with open("stu_academic_info.txt", "r") as sgFile:
                    found = False
                    print(f"\nAcademic info for {account[3]} ({account[0]}):")

                    # Read each line and check if student ID matches
                    for line in sgFile:
                        student_id,course_id,grades,teacher_feedback,attendance,class_id = line.strip().split(",")
                        if student_id == account[0]:
                            print(f"Grade = {grades}\nFeedback = {teacher_feedback}\nAttendance = {attendance}")
                            found = True

                    if not found:
                        print("Student is not registered in academic file")

            except FileNotFoundError:
                print("File does not exist.")  # Handle missing file error

            except Exception as x:
                print(f"\nAn error occurred: {x}\n")

        elif select6 == "2":
            print("\nReturning to Login Menu")
            break

        else:
            print("\nInvalid selection. Please enter within 1 ~ 2")

def student_feedback(account):
    while True:
        # Display menu for submitting feedback
        print("\n------------------------")
        print(f"STUDENT FEEDBACK SUBMISSION - {account[3]} ({account[0]})")
        print("------------------------")
        print("1. Submission")
        print("2. Back")
        print("------------------------")

        # Get user selection
        select7 = input("Make your selection from 1 ~ 2: ").strip()

        if select7 == "1":
            # Get user feedback and save it to studentfeedback.txt
            sfeedback = input("Please enter your feedback: ")
            with open("studentfeedback.txt", "a") as sfFile:
                sfFile.write(f"{sfeedback} - {account[3]} ({account[0]})\n")
                print("\nThank you for your feedback!")
                break  # Exit the loop after submission
        elif select7 == "2":
            print("\nReturning to Login Menu")
            break
        else:
            print("\nInvalid selection. Please enter within 1 ~ 2")

#------TEACHER------------------------------------------------------------------
def tcr_login():
    while True:
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()
        teacher_id = input("Enter your teacher id: ").strip()
        match = False

        try:
            with open("user.txt", "r") as tcr_file:
                for line in tcr_file:
                    data = line.strip().split(",")
                    if data[1] == username and data[2] == password and data[0] == teacher_id:
                        match = True
                        break
        except FileNotFoundError:
            print("Error: The file 'user.txt' was not found. Please make sure it exists.\n")
            return  # Exit function if file is missing

        if match:
            print("Login successful\n")
            tcr_menu()  # Call the menu with username
            return  # Exit the login function after successful login
        else:
            print("Login unsuccessful. Try again\n")
            return
#---TeacherMenu--------------------------------------------------------
def tcr_menu():
    while True:  # Keeps looping until user selects Exit (6)
        print('''\n---- Teacher Panel ----
1. Course and Class Management
2. Student Enrolment
3. Grading and Assessment
4. Attendance Tracking
5. Report Generation
6. Exit''')

        try:
            tcr_choice = int(input("Enter your choice: "))

            if tcr_choice == 1:
                course()
            elif tcr_choice == 2:
                student_enrollment()
            elif tcr_choice == 3:
                grade_assess()
            elif tcr_choice == 4:
                attendance()
            elif tcr_choice == 5:
                report()
            elif tcr_choice == 6:
                print("Logging out... Returning to main menu.\n")
                return  # Exits tcr_menu()
            else:
                print("Invalid choice! Please enter a number between 1-6.")

        except ValueError:
            print("Invalid input! Please enter a number.")

#----------Course creation and management---------------------
def course():
    while True:
        print('''\n------ Main Menu ------\n
1. Manage Courses
2. Manage Classes
3. Exit
''')

        option = input("Enter your option: ")

        if option == "1":
            course_menu()
        elif option == "2":
            class_menu()
        elif option == "3":
            return
        else:
            print("Invalid option, please try again.")

def course_menu():
    while True:
        print('''\n------ Manage Courses ------\n
1. Create Course
2. Update Course
3. Delete Course
4. Exit
''')

        option = input("Enter your option: ")

        if option == "1":
            create_course()
        elif option == "2":
            update_course()
        elif option == "3":
            delete_course()
        elif option == "4":
            return
        else:
            print("Invalid option, please try again.")


def create_course():
    print("\n------ Create a Course ------\n")
    course_name = get_non_empty_input("Enter course name: ")
    course_id = get_non_empty_input("Enter course ID: ")
    course_description = get_non_empty_input("Enter a short description about the course: ")

    try:
        with open("courses.txt", "a") as courseFile:
            courseFile.write(course_name + "," + course_id + "," + course_description + "\n")

        print("\nCourse created successfully!\n")

    except FileNotFoundError:
        print("\nError: The file 'course.txt' was not found.\n")
    except Exception as e:
        print(f"\nAn error occurred: {e}\n")


def update_course():
    print('\n------ Update a Course ------\n')
    course_id = input("Enter course ID to update: ")

    updated_lines = []
    course_found = False

    try:
        with open("courses.txt", "r") as courseFile:
            lines = courseFile.readlines()

        for line in lines:
            data = line.strip().split(",")
            if len(data) < 3:  # Ensure the line has enough parts
                continue
            if data[1] == course_id:
                course_found = True
                print('''\n------ What would you like to update? ------\n
1. Course Name
2. Course Description
''')
                option = input("Enter your option (1-2): ")

                if option == "1":
                    data[0] = get_non_empty_input("Enter new course name: ")
                elif option == "2":
                    data[2] = get_non_empty_input("Enter new course description: ")
                else:
                    print("Invalid option")
                    return

                updated_line = ",".join(data) + "\n"
                updated_lines.append(updated_line)
            else:
                updated_lines.append(line)

        if course_found:
            with open("courses.txt", "w") as courseFile:
                courseFile.writelines(updated_lines)
            print("\nCourse updated successfully!\n")
        else:
            print("\nCourse not found.\n")

    except FileNotFoundError:
        print("\nError: The file 'course.txt' was not found.\n")
    except Exception as e:
        print(f"\nAn error occurred: {e}\n")


def delete_course():
    print("\n------ Delete a Course ------\n")
    course_id = input("Enter course ID to delete: ")
    course_found = False
    updated_lines = []

    try:
        with open("courses.txt", "r") as file:
            lines = file.readlines()

        for line in lines:
            data = line.strip().split(',')
            if len(data) < 3:  # Ensure the line has enough parts
                continue
            if data[1] != course_id:
                updated_lines.append(line)
            else:
                course_found = True

        if course_found:
            with open("courses.txt", "w") as file:
                file.writelines(updated_lines)
            print("\nCourse deleted successfully!\n")
        else:
            print("\nCourse not found.\n")

    except FileNotFoundError:
        print("\nError: The file 'course.txt' was not found.\n")
    except Exception as e:
        print(f"\nAn error occurred: {e}\n")


# --------- Class Management --------- #

def class_menu():
    while True:
        print('''\n------ Manage Classes ------\n
1. Create Class
2. Update Class
3. Delete Class
4. Exit
''')

        option = input("Enter your option: ")

        if option == "1":
            create_class()
        elif option == "2":
            update_class()
        elif option == "3":
            delete_class()
        elif option == "4":
            return
        else:
            print("Invalid option, please try again.")


def create_class():
    print("\n------ Create a Class ------\n")
    course_id = input("Enter course ID: ")
    # Check if course ID exists
    course_exists = False
    try:
        with open("courses.txt", "r") as courseFile:
            for line in courseFile:
                data = line.strip().split(",")
                if data[1] == course_id:
                    course_exists = True
                    break
    except FileNotFoundError:
        print("\nError: The file 'course.txt' was not found.\n")
        return
    except Exception as e:
        print(f"\nAn error occurred while checking course ID: {e}\n")
        return

    if not course_exists:
        print("\nError: Course ID not found. Please enter a valid course ID.\n")
        return
    class_id = get_non_empty_input("Enter class ID (e.g., CS101-1): ")
    class_schedule = get_non_empty_input("Enter class schedule: ")
    classroom = get_non_empty_input("Enter classroom: ")
    lesson_plan = get_non_empty_input("Enter lesson plan: ")
    assignments = get_non_empty_input("Enter assignment: ")
    instructor = get_non_empty_input("Enter instructor: ")
    try:
        with open("class.txt", "a") as classFile:
            classFile.write(f"{course_id},{class_id},{class_schedule},{classroom},{lesson_plan},{assignments},{instructor}\n")

        print("\nClass created successfully!\n")
    except FileNotFoundError:
        print("\nError: The file 'class.txt' was not found.\n")
    except Exception as e:
        print(f"\nAn error occurred: {e}\n")


def update_class():
    print("\n------ Update a Class ------\n")
    class_id = input("Enter class ID to update: ")

    updated_lines = []
    class_found = False

    try:
        with open("class.txt", "r") as classFile:
            lines = classFile.readlines()

        for line in lines:
            data = line.strip().split(",")
            if len(data) < 5:  # Ensure the line has enough parts
                continue
            if data[1] == class_id:
                class_found = True
                print('''\n------ What would you like to update? ------\n
1. Schedule
2. Classroom
3. Lesson Plan
4. Assignment
5. instructor
''')
                option = input("Enter your option (1-5): ")

                if option == "1":
                    old_schedule = data[2]
                    new_schedule = get_non_empty_input("Enter new schedule: ")
                    data[2] = new_schedule
                    save_announcement(class_id, old_schedule, new_schedule, "schedule")
                elif option == "2":
                    old_classroom = data[3]
                    new_classroom = get_non_empty_input("Enter new classroom: ")
                    data[3] = new_classroom
                    save_announcement(class_id, old_classroom, new_classroom, "classroom")
                elif option == "3":
                    data[4] = get_non_empty_input("Enter new lesson plan : ")
                elif option == "4":
                    data[5] = get_non_empty_input("Enter new assignment : ")
                elif option == "5":
                    data[6] = get_non_empty_input("Enter new instructor : ")
                else:
                    print("Invalid option")
                    return

                updated_line = ",".join(data) + "\n"
                updated_lines.append(updated_line)
            else:
                updated_lines.append(line)

        if class_found:
            with open("class.txt", "w") as classFile:
                classFile.writelines(updated_lines)
            print("\nClass updated successfully!\n")
        else:
            print("\nClass not found.\n")

    except FileNotFoundError:
        print("\nError: The file 'class.txt' was not found.\n")
    except Exception as e:
        print(f"\nAn error occurred: {e}\n")


def delete_class():
    print("\n------ Delete a Class ------\n")
    class_id = input("Enter class ID to delete: ")
    class_found = False
    updated_lines = []

    try:
        with open("class.txt", "r") as file:
            lines = file.readlines()

        for line in lines:
            data = line.strip().split(',')

            # Ensure the line has enough data before accessing index 1
            if len(data) < 5:
                continue  # Skip empty or malformed lines

            if data[1] != class_id:
                updated_lines.append(line)
            else:
                class_found = True

        if class_found:
            with open("class.txt", "w") as file:
                file.writelines(updated_lines)
            print("\nClass deleted successfully!\n")
        else:
            print("\nClass not found.\n")

    except FileNotFoundError:
        print("\nError: The file 'class.txt' was not found.\n")
    except Exception as e:
        print(f"\nAn error occurred: {e}\n")
#-----Student enrollment-------------------------------------
def student_enrollment():
    while True:
        print('''------Student Enrollment------

    1.Enroll student
    2.Remove student
    3.Exit
    ''')
        try:
            option = int(input("Enter your option (1-3) : "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 3.")
            continue

        if option == 1:
            tcr_name = input("Enter your name: ")
            student_id = input("Enter student id: ")
            course_id = input("Enter course id: ")

            # Check if the instructor is teaching the course
            is_teaching = False
            try:
                with open("courses.txt", "r") as course_file:
                    for course_line in course_file:
                        course_data = course_line.strip().split(",")
                        if course_data[1] == course_id and course_data[-1] == tcr_name:
                            is_teaching = True
                            break
            except FileNotFoundError:
                print("\nError: The file 'courses.txt' was not found.\n")
                continue
            except Exception as e:
                print(f"\nAn error occurred while checking courses: {e}\n")
                continue

            if not is_teaching:
                print("Sorry, you can only enroll and remove students from the courses you are teaching.")
                continue

            student_found = False
            try:
                with open("student.txt", "r") as stuFile:
                    for line in stuFile:
                        data = line.strip().split(",")
                        if data[0] == student_id:
                            student_found = True
                            break

                if student_found:
                    try:
                        with open("stu_academic_info.txt", "r") as file:
                            lines = file.readlines()

                        student_found = False
                        updated_lines = []  # Use a list to hold the lines

                        for line in lines:
                            data = line.strip().split(",")
                            if data[0] == student_id:  # Check if this is the correct student ID
                                student_found = True
                                data[1] = course_id  # Put feedback into data[3]
                                line = ",".join(data) + "\n"  # Put the line together separating the data with ","
                            updated_lines.append(line)

                        if student_found:
                            with open("stu_academic_info.txt", "w") as file:
                                file.writelines(updated_lines)  # Write to file
                            print("\nStudent enrolled successfully!\n")
                        else:
                            print("\nData for this student ID doesn't exist.\n")

                    except FileNotFoundError:
                        print("\nFile not found. Please enroll the student first.\n")  # More appropriate message
                    except Exception as e:
                        print(f"\nAn error occurred: {e}\n")

            except FileNotFoundError:
                print("\nFile not found. Please enroll the student first.\n")
            except Exception as e:
                print(f"\nAn error occurred: {e}\n")

        elif option == 2:
            tcr_name = input("Enter your name : ")
            student_id = input("Enter student id to remove: ")
            course_id = input("Enter course id: ")

            # Check if the instructor is teaching the course
            is_teaching = False
            try:
                with open("courses.txt", "r") as course_file:
                    for course_line in course_file:
                        course_data = course_line.strip().split(",")
                        if course_data[1] == course_id and course_data[-1] == tcr_name:
                            is_teaching = True
                            break
            except FileNotFoundError:
                print("\nError: The file 'courses.txt' was not found.\n")
                continue
            except Exception as e:
                print(f"\nAn error occurred while checking courses: {e}\n")
                continue

            if not is_teaching:
                print("Sorry, you can only enroll and remove students from the courses you are teaching.")
                continue

            try:
                with open("stu_academic_info.txt", "r") as file:
                    lines = file.readlines()

                with open("stu_academic_info.txt", "w") as file:
                    removed = False
                    for line in lines:
                        data = line.strip().split(",")
                        if data[0] != student_id or data[1] != course_id:
                            file.write(line)
                        else:
                            removed = True
                    if removed:
                        print("Student removed successfully.")
                    else:
                        print("Student ID or Course ID not found in academic info.")
            except FileNotFoundError:
                print("\nError: The file 'stu_academic_info.txt' was not found.\n")
            except Exception as e:
                print(f"\nAn error occurred while removing student: {e}\n")

        elif option == 3:
            break
        else:
            print("Invalid option. Please enter a number between 1 and 3.")
#-----Grading and assessment---------------------------------
def grade_assess():
    while True:
        print('''------Grading and Assessment------

1. Grade exams and assignments 
2. Provide feedback
3. Exit''')
        option = input("Enter your option (1-3): ")

        if option == "1":
            stu_id = input("Enter student ID: ")
            exam_grade = input("Enter student's exam grade (A, B, C, D, F): ").upper()
            assignment_grade = input("Enter student's assignment grade (A, B, C, D, F): ").upper()

            try:
                exam_weightage = float(input("Enter exam weightage percentage: "))
                assignment_weightage = float(input("Enter assignment weightage percentage: "))
            except ValueError:
                print("\nError: Invalid input for weightage. Please enter a number.\n")
                continue

            exam_gpa = grade_to_gpa(exam_grade)
            assignment_gpa = grade_to_gpa(assignment_grade)

            if exam_weightage + assignment_weightage != 100:
                print("\nError: Weightages must sum up to 100%.\n")
                continue

            final_gpa = (exam_gpa * (exam_weightage / 100)) + (assignment_gpa * (assignment_weightage / 100))

            try:
                student_found = False
                with open("stu_academic_info.txt", "r") as file:
                    lines = file.readlines()

                for i in range(len(lines)): # Go through the lines using index
                    data = lines[i].strip().split(",")
                    if data[0] == stu_id:
                        student_found = True
                        data[2] = f"{final_gpa:.2f}"  # Replace N/A with the GPA
                        lines[i] = ",".join(data) + "\n"  # Update new line with GPA
                        break

                if student_found:
                    with open("stu_academic_info.txt", "w") as file:
                        file.writelines(lines)
                    print("\nGrades recorded successfully!\n")

                else:
                    print("Student ID not found.")

            except FileNotFoundError:
                print("\nError: The file 'stu_academic_info.txt' does not exist.\n")
            except Exception as e:
                print(f"\nAn error occurred: {e}\n")

        elif option=="2":
            add_feedback()

        elif option=="3":
            return

        else:
            print("Option not available")


def grade_to_gpa(letter_grade):
    gpa_scale = {"A+": 4.0, "A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}
    return gpa_scale.get(letter_grade, "Invalid Grade")


def add_feedback():
        stu_id = input("Enter student ID: ")
        feedback = get_non_empty_input("Enter feedback to student: ")

        try:
            # Read the existing file
            with open("stu_academic_info.txt", "r") as file:
                lines = file.readlines()

            student_found = False
            updated_lines = []  # Use a list to hold the lines

            for line in lines:
                data = line.strip().split(",")
                if data[0] == stu_id:  # Check if this is the correct student ID
                    student_found = True
                    data[3] = feedback  # put feedback into data[3]
                    line = ",".join(data) + "\n"  # Put the line together seperating the data with ","
                updated_lines.append(line)

            if student_found:
                with open("stu_academic_info.txt", "w") as file:
                    file.writelines(updated_lines)  # write to file
                print("\nFeedback added successfully!\n")
            else:
                print("\nData for this student ID doesn't exist.\n")

        except FileNotFoundError:
            print("\nFile not found. Please enroll the student first.\n")  # More appropriate message
        except Exception as e:
            print(f"\nAn error occurred: {e}\n")

#-----Attendance tracking------------------------------------
def attendance():
    while True:
        print('''\n------ Attendance ------\n
1. Record attendance
2. Monitor attendance
3. Exit''')
        option = input("Enter your option (1-3): ")

        if option == "1":
            student_id = input("Enter student id: ")

            try:
                total_class = int(input("Total number of classes: "))
                class_att = int(input("Enter how many days student attended the classes: "))
                total_event = int(input("Total number of events: "))
                event_att = int(input("Enter how many days student attended the events: "))

                total_att = round(((class_att + event_att) / (total_event + total_class)) * 100, 2)
            except ValueError:
                print("\nError: Invalid input. Please enter a number.\n")
                continue

            try:
                with open("stu_academic_info.txt", "r") as file:
                    lines = file.readlines()

                student_found = False
                updated_lines = []

                for line in lines:
                    data = line.strip().split(",")
                    if data[0] == student_id:  # Check if this is the correct student ID
                        student_found = True
                        data[4] = f"{total_att:.2f}%"  # Store attendance in data[4]
                        line = ",".join(data) + "\n"  # Reconstruct the line

                    updated_lines.append(line)

                if student_found:
                    with open("stu_academic_info.txt", "w") as file:
                        file.writelines(updated_lines)
                    print("\nAttendance updated successfully!\n")
                else:
                    print("\nData for this student ID doesn't exist.\n")

            except FileNotFoundError:
                print("\nFile not found. Please enroll the student first.\n")  # Corrected message
            except Exception as e:
                print(f"\nAn error occurred: {e}\n")

        elif option == "2":
            try:
                with open("stu_academic_info.txt", "r") as stuFile:
                    lines = stuFile.readlines()

                print("\nAttendance Report:")
                if not lines:
                    print("No attendance records found.")
                    continue  # Go back to the menu

                for line in lines:
                    data = line.strip().split(",")
                    student_id = data[0]
                    try:
                        attendance_percent = float(data[4].replace("%", ""))  # Get attendance from data[4] and convert
                        if attendance_percent < 80:
                            print(f"{student_id}'s attendance is {attendance_percent:.2f}% which is below 80%")
                        else:
                            print(f"{student_id}'s attendance is {attendance_percent:.2f}% which is above 80%")
                    except IndexError:
                         print(f"No attendance info found for {student_id}")
                    except ValueError:
                        print(f"Invalid attendance format for {student_id}")


            except FileNotFoundError:
                print("No attendance file found. Please record attendance first.")
            except Exception as e:
                print(f"\nAn error occurred: {e}\n")

        elif option == "3":
            print("Exiting Attendance...")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 3.")


#-----Report Generation--------------------------------------
def report():
    print("\n------ Report Generation ------\n")

    try:
        with open("stu_academic_info.txt", "r") as stuFile:
            data = stuFile.readlines()

            for line in data:
                data = line.strip().split(",")
                if len(data) == 6:  # Ensure correct number of fields
                    print(f"Student ID: {data[0]},Course ID: {data[1]},Grade: {data[2]},Feedback: {data[3]},Attendance: {data[4]},Class: {data[5]}\n")
                else:
                    print(f"Error: Incorrect format in line: {line}")
    except FileNotFoundError:
        print("\nError: The file 'stu_academic_info.txt' does not exist.\n")
    except Exception as e:
        print(f"\nAn error occurred: {e}\n")

def save_announcement(class_id, old_value, new_value, update_type):
    try:
        with open("announcements.txt", "a") as annFile:
            annFile.write(f"{class_id},{update_type},{old_value},{new_value}\n")
    except FileNotFoundError:
        # Create the file if it doesn't exist
        try:
            with open("announcements.txt", "w") as annFile:
                annFile.write(f"{class_id},{update_type},{old_value},{new_value}\n")
        except Exception as create_error:
            print(f"Error creating announcement file: {create_error}")
    except Exception as e:
        print(f"Error saving announcement: {e}")

def get_non_empty_input(data):
#The extra spaces between words remain because .strip() only removes spaces at the start and end.
    while True:
        user_input = input(data).strip()  # Take input and remove empty spaces
        if user_input:  # If user_input=False means the string is empty
            return user_input  # If input is not empty return the valid input and exit the function
        print("Error: Input cannot be empty. Please try again.")

#------STAFF-------------------------------------------------------------------------------------
# File paths
STUDENT_FILE = "student.txt"
STUDENT_ACADEMIC = "stu_academic_info.txt"
TIMETABLE_FILE = "timetable.txt"
RESOURCES_FILE = "resources.txt"
EVENTS_FILE = "events.txt"
COMMUNICATION_FILE = "communication.txt"
CLASS_FILE = "class.txt"

# Function to remove an entry from a file
def remove_entry(file_path, entry_type):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"No {entry_type} records found.")
        return

    if not lines:
        print(f"No {entry_type} found.")
        return

    print(f"\n{entry_type} List:")
    for i, line in enumerate(lines, 1):
        print(f"{i}. {line.strip()}")

    try:
        choice = int(input(f"Enter the number of the {entry_type} to remove: "))
        if 1 <= choice <= len(lines):
            del lines[choice - 1]
            with open(file_path, "w") as file:
                file.writelines(lines)
            print(f"{entry_type} removed successfully.")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")

# Function to manage student records
def student_management():
    print("1.register student\n2.transfer student\n3.remove student\n4.exit")

    choice = int(input("Enter your option : "))

    if choice == 1:
        with open(STUDENT_FILE, "r") as file:
            lines = file.readlines()

        existing_students = set()
        try:
            with open(STUDENT_ACADEMIC, "r") as stuFile:
                for line in stuFile:
                    existing_students.add(line.split(",")[0])  # Store existing student IDs
        except FileNotFoundError:
            pass  # If the file doesn't exist, continue

        with open(STUDENT_ACADEMIC, "a") as stuFile:
            for line in lines:
                data = line.strip().split(",")
                stu_id = data[0]

                if stu_id not in existing_students:  # Avoid duplicate student records
                    new_data = stu_id + "," + "N/A,N/A,N/A,N/A,N/A\n"
                    stuFile.write(new_data)

        print("\nStudents registered successfully.")

    elif choice == 2:
        stu_id = input("Enter student ID to transfer: ").strip()
        course_id = input("Enter new course ID: ").strip()

        student_found = False
        updated_lines = []

        try:
            with open(STUDENT_ACADEMIC, "r") as file:
                lines = file.readlines()

            for line in lines:
                data = line.strip().split(",")

                if data[0] == stu_id:
                    student_found = True
                    data[1] = course_id  # Update only the course ID
                    updated_lines.append(",".join(data) + "\n")
                else:
                    updated_lines.append(line)

            if student_found:
                with open(STUDENT_ACADEMIC, "w") as file:
                    file.writelines(updated_lines)
                print("\nStudent transferred successfully.")
            else:
                print("\nStudent ID not found.")

        except FileNotFoundError:
            print("\nError: Student academic file not found.")

    elif choice == 3:
        stu_id = input("Enter student to remove: ")
        stu_found = False
        updated_lines = []

        try:
            with open(STUDENT_ACADEMIC, "r") as file:
                lines = file.readlines()

            for line in lines:
                data = line.strip().split(',')

                # Ensure the line has enough data before accessing index 1
                if len(data) < 6:
                    continue  # Skip empty or malformed lines

                if data[0] != stu_id:
                    updated_lines.append(line)
                else:
                    stu_found = True

            if stu_found:
                with open(STUDENT_ACADEMIC, "w") as file:
                    file.writelines(updated_lines)
                print("\nStudent removed successfully!\n")
            else:
                print("\nStudent ID not found.\n")

        except FileNotFoundError:
            print("\nError: The file 'stu_academic_info.txt' was not found.\n")
        except Exception as e:
            print(f"\nAn error occurred: {e}\n")

# Function to manage timetable
def timetable_management():
    while True:
        print('''\n1. Generate and view timetable
2. Update timetable
3. Exit''')
        choice = int(input("Enter your option: "))

        if choice == 1:
            try:
                with open(CLASS_FILE, 'r') as file:
                    lines = file.readlines()

                with open(TIMETABLE_FILE, "w") as tFile:
                    for line in lines:
                        data = line.strip().split(",")

                        if len(data) < 3:  # Ensure there's enough data
                            continue

                        new_data = data[1] + "," + data[2]  # class_id, schedule
                        tFile.write(new_data + "\n")

                print("\nUpdated Timetable:")
                with open(TIMETABLE_FILE, 'r') as tFile:
                    print(tFile.read())
            except FileNotFoundError:
                print("class or timetable file not found")
            except Exception as e:
                print(f"an error occured {e}")

        elif choice == 2:
            # Update timetable entry
            class_id = input("Enter the class ID to update: ").strip()
            new_time = input("Enter the new schedule: ").strip()

            timetable_updated = False
            updated_timetable = []
            updated_class = []

            # Updating the timetable file
            try:
                with open(TIMETABLE_FILE, "r") as tFile:
                    lines = tFile.readlines()

                for line in lines:
                    class_data = line.strip().split(",")

                    if class_data[0] == class_id:
                        updated_timetable.append(f"{class_id},{new_time}\n")  # Update schedule
                        timetable_updated = True
                    else:
                        updated_timetable.append(line)

                if timetable_updated:
                    with open(TIMETABLE_FILE, "w") as tFile:
                        tFile.writelines(updated_timetable)

                    print("\nTimetable updated successfully.")

                else:
                    print("\nClass ID not found in timetable.")

            except FileNotFoundError:
                print("\nTimetable file not found. Generate it first.")
            except Exception as e:
                print(f"An error occurred: {e}")

            # Updating the class file to reflect the new schedule
            try:
                with open(CLASS_FILE, "r") as cFile:
                    class_lines = cFile.readlines()

                for line in class_lines:
                    class_data = line.strip().split(",")

                    if class_data[1] == class_id:  # Class ID matches
                        old_schedule_class = class_data[2]
                        class_data[2] = new_time  # Update schedule
                        updated_class.append(",".join(class_data) + "\n")
                        save_announcement(class_id, old_schedule_class, new_time, "schedule")

                    else:
                        updated_class.append(line)

                with open(CLASS_FILE, "w") as cFile:
                    cFile.writelines(updated_class)

                print("\nClass schedule updated successfully in class file.")

            except FileNotFoundError:
                print("\nError: Class file not found.")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == 3:
            break

        else:
            print("Invalid option")
# Function to allocate resources
def resource_allocation():
    while True:
        print("\n1. Add Resource\n2. Remove Resource\n3. View Resources\n4. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            resource = input("Enter resource (e.g., Projector, Computer): ")
            with open(RESOURCES_FILE, "a") as file:
                file.write(resource + "\n")
            print("Resource added successfully.")

        elif choice == "2":
            remove_entry(RESOURCES_FILE, "Resource")

        elif choice == "3":
            try:
                with open(RESOURCES_FILE, "r") as file:
                    print("\nAvailable Resources:")
                    for line in file:
                        print(line.strip())
            except FileNotFoundError:
                print("No resources found.")

        elif choice == "4":
            break

# Function to manage events
def event_management():
    while True:
        print("\n1. Add Event\n2. Remove Event\n3. View Events\n4. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            event = input("Enter event details (e.g., Seminar - March 5th): ")
            with open(EVENTS_FILE, "a") as file:
                file.write(event + "\n")
            print("Event added successfully.")

        elif choice == "2":
            remove_entry(EVENTS_FILE, "Event")

        elif choice == "3":
            try:
                with open(EVENTS_FILE, "r") as file:
                    print("\nScheduled Events:")
                    for line in file:
                        print(line.strip())
            except FileNotFoundError:
                print("No events found.")

        elif choice == "4":
            break

# Function to manage communication
def communication():
    while True:
        print("\n1. Send Message\n2. Remove Message\n3. View Messages\n4. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            message = input("Enter message for students/parents/faculty: ")
            with open(COMMUNICATION_FILE, "a") as file:
                file.write(message + "\n")
            print("Message sent successfully.")

        elif choice == "2":
            remove_entry(COMMUNICATION_FILE, "Message")

        elif choice == "3":
            try:
                with open(COMMUNICATION_FILE, "r") as file:
                    print("\nMessages:")
                    for line in file:
                        print(line.strip())
            except FileNotFoundError:
                print("No messages found.")

        elif choice == "4":
            break

def staff_menu():
    while True:
        print("\n--- Staff Management System ---")
        print("1. Manage Student Records")
        print("2. Timetable Management")
        print("3. Resource Allocation")
        print("4. Event Management")
        print("5. Communication")
        print("6. Exit")

        option = input("Enter your choice: ")

        if option == "1":
            student_management()
        elif option == "2":
            timetable_management()
        elif option == "3":
            resource_allocation()
        elif option == "4":
            event_management()
        elif option == "5":
            communication()
        elif option == "6":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def staff_login():
    while True:
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()
        staff_id = input("Enter your staff_id: ").strip()
        match = False

        with open("user.txt", "r") as tcr_file:
            for line in tcr_file:
                data = line.strip().split(",")
                if data[1] == username  and data[2] == password and data[0] == staff_id:
                    match = True
                    break

        if match:
            print("Login successful\n")
            staff_menu()  # Call the menu with username
            return  # Exit the login function after successful login
        else:
            print("Login unsuccessful. Try again\n")

#------MAIN MENU-------------------------------------------------------------------------------
def main():
    while True:
        print('''---------MENU---------

1. Administrator
2. Student
3. Staff
4. Teacher
    ''')

        try:
            menu = int(input("Enter your selection: "))
            if menu == 1:
                admin_login()
            elif menu == 2:
                student_menu()
            elif menu == 3:
                staff_login()
            elif menu == 4:
                tcr_login()
            else:
                print("Invalid selection or functionality not implemented.")
        except ValueError:
            print("Please enter a valid number")

main()