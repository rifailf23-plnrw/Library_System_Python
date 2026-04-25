import csv
import os
import re
from datetime import datetime

from Book import load_books, save_books, find_book, validate_book_id
from Student import load_students, find_student, validate_student_id

TRANSACTION_FILE = "transactions.csv"

#Date Validation
def validate_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False


#Transaction CSV Helpers
def load_transaction() -> list[dict]:
    if not os.path.exists(TRANSACTION_FILE):
        return []
    with open(TRANSACTION_FILE, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def save_transaction(date: str, book_id: str, student_id: str, t_type: str) -> None:
    file_exists = os.path.exists(TRANSACTION_FILE)
    with open(TRANSACTION_FILE, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["date", "book_id", "student_id", "type"])
        if not file_exists or os.stat(TRANSACTION_FILE).st_size == 0:
            writer.writeheader()
        writer.writerow({
            "date":date,
            "book_id":book_id,
            "student_id":student_id,
            "type":str(t_type)
        })


#Issue Logic Helpers
def is_book_issued_to_student(transactions: list[dict], book_id: str, student_id: str) -> bool:
    # Filter transactions for this book+student pair, in order
    relevant = [
        transaction for transaction in transactions
        if transaction["book_id"].upper() == book_id.upper()
           and transaction["student_id"] == student_id
    ]
    # Walk through: track whether student currently holds the book
    holding = False
    for transaction in relevant:
        if transaction["type"] == "1":
            holding = True
        elif transaction["type"] == "2":
            holding = False
    return holding


def count_active_issues(transactions: list[dict], book_id: str) -> int:
    issued = 0
    # Track per-student holding status for this book
    student_holdings: dict[str, bool] = {}
    for transaction in transactions:
        if transaction["book_id"].upper() != book_id.upper():
            continue
        sid = transaction["student_id"]
        if transaction["type"] == "1":
            student_holdings[sid] = True
        elif transaction["type"] == "2":
            student_holdings[sid] = False
    issued = sum(1 for held in student_holdings.values() if held)
    return issued

#Issue Book
def issue_book() -> None:
    books = load_books()
    students = load_students()
    transactions = load_transaction()

    print("\n--- Issue Book ---")

    # Book ID input
    while True:
        book_id = input("Enter Book ID: ").strip().upper()
        if not validate_book_id(book_id):
            print("  Invalid Book ID format.")
            continue
        book = find_book(books, book_id)
        if not book:
            print(f"  Book ID '{book_id}' not found in the library.")
            continue
        break

    # Check availability BEFORE asking for student ID
    availability = int(book["availability"])
    if availability <= 0:
        print(f"  Sorry, '{book['title']}' has no available copies.")
        return

    # Student ID input
    while True:
        student_id = input("Enter Student ID: ").strip()
        if not validate_student_id(student_id):
            print(" Invalid Student ID format.")
            continue
        student = find_student(students, student_id)
        if not student:
            print(f" Student ID '{student_id}' not found.")
            continue
        break

    # Check: student doesn't already hold a copy of this book
    if is_book_issued_to_student(transactions, book_id, student_id):
        print(f" Student '{student['first_name']}' already has a copy of '{book['title']}' on loan.")
        print("    Multiple copies of the same book cannot be issued to the same student.")
        return

    # Date input
    while True:
        date_str = input("Enter Issue Date (DD/MM/YYYY): ").strip()
        if not validate_date(date_str):
            print(" Invalid date.")
        else:
            break

    # All checks passed — update availability and save transaction
    book["availability"] = str(availability - 1)
    save_books(books)
    save_transaction(date_str, book_id, student_id, "1")

    print(f"\n  Book issued successfully!")
    print(f"    Book    : {book['title']} ({book_id})")
    print(f"    Student : {student['first_name']} ({student_id})")
    print(f"    Date    : {date_str}")
    print(f"    Copies remaining: {book['availability']}")


#Return Book
def return_book() -> None:
    books = load_books()
    students = load_students()
    transaction = load_transaction()

    print("\n--- Return Book ---")

    #Book ID Input
    while True:
        book_id = input("Enter Book ID: ").strip().upper()
        if not validate_book_id(book_id):
            print("Invalid Book ID.")
            continue
        book = find_book(books, book_id)
        if not book:
            print(f" Book ID '{book_id}' not found in the library.")
            continue
        break

    #Student ID Input
    while True:
        student_id = input("Enter Student ID: ").strip()
        if not validate_student_id(student_id):
            print("Invalid Student ID.")
            continue
        student = find_student(students, student_id)
        if not student:
            print(f" Student ID '{student_id}' not found.")
            continue
        break


    #Check: student actually has this book on loan
    if not is_book_issued_to_student(transaction, book_id, student_id):
        print(f" Student '{student['first_name']}' doesn't have '{book['title']} on loan.")
        print(" The book may have already been returned.")
        return



    #Date input
    while True:
        date_str = input("Enter Book Date (DD/MM/YYYY): ").strip()
        if not validate_date(date_str):
            print("Invalid Date (DD/MM/YYYY).")
        else:
            break



    #All checks passed - update availability (cannot exceed copies)
    copies = int(book["copies"])
    availability = int(book["availability"])
    new_availability = min(availability + 1, copies) #safety cap
    book["availability"] = str(new_availability)
    save_books(books)
    save_transaction(date_str, book_id, student_id, "2")

    print(f"\n Book returned successfully!")
    print(f"Book : {book['title']} ({book_id})")
    print(f"Student : {student['first_name']} ({student_id})")
    print(f"    Copies now available: {book['availability']}")


#Issue / Return Menu
def transaction_menu() -> None:
    while True:
        print("\n=== Issue / Return Books ===")
        print("  1. Issue Book")
        print("  2. Return Book")
        print("  0. Back to Main Menu")
        choice = input("Select option: ").strip()

        if choice == "1":
            issue_book()
        elif choice == "2":
            return_book()
        elif choice == "0":
            break
        else:
            print("Invalid Selection.")
