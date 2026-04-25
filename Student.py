import csv
import os
import re

STUDENT_FILE = "student.csv"

#Student ID Validation: Exactly 8 digits
def validate_student_id(student_id: str) -> bool:
    return bool(re.fullmatch(r"\d{8}", student_id))

#First Name Validation: Letters only, max 10 charecters
def validate_first_name(name: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z]{1,10}", name))

#CSV Helpers
def load_students() -> list[dict]:
    if not os.path.exists(STUDENT_FILE):
        return []
    with open(STUDENT_FILE, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def save_students(students: list[dict]) -> None:
    fieldnames = ["student_id", "first_name"]
    with open(STUDENT_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)


def find_student(students: list[dict], student_id: str) -> dict | None:
    return next(
        (student for student in students if student["student_id"] == student_id), None
    )

#Add Student
def add_student() -> None:
    students = load_students()

    print("\n---Add Student---")

    #Student ID Validation
    while True:
        student_id = input("Enter Student ID (8 digits) : ").strip()
        if not validate_student_id(student_id):
            print("Invalid Student ID.")
        elif find_student(students, student_id):
            print("Student ID is already registered.")
        else:
            break

    #First Name Validation
    while True:
        first_name = input("Enter First Name: ").strip()
        if not validate_first_name(first_name):
            print("Invalid First Name.")
        else:
            break


    new_student = {
        "student_id": student_id,
        "first_name": first_name,
    }

    students.append(new_student)
    save_students(students)
    print(f"Students '{first_name}' (ID: {student_id}) added successfully.")


#View Students
def view_students() -> None:
    students = load_students()

    if not students:
        print("\nNo Students found.")
        return

    print("\n--- Student List ---")
    print(f"\n{'Student ID':<12}{'First Name'}")
    print("-"*25)
    for student in students:
        print(f"{student['student_id']:<12}{student['first_name']}")
    print(f"\n  Total students: {len(students)}")


#Search Student
def search_students() -> None:
    students = load_students()

    print("\n--- Search Student ---")
    query = input("Enter Student ID or part of First Name : ").strip().lower()

    results = [
        student for student in students
        if query in student["student_id"] or query in student["first_name"].lower()
    ]

    if not results:
        print("\nNo matching Students found.")
    else:
        print(f"\n{'Student ID':<12}{'First Name'}")
        print("-"*25)
        for student in results:
            print(f"{student['student_id']:<12}{student['first_name']}")


#Student Menu
def student_menu():
    while True:
        print("\n=== Student Management ===")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("0. Back to Main Menu")
        choice = input("Select option: ").strip()


        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_students()
        elif choice == "0":
            break
        else: print("Invalid option. try again.")