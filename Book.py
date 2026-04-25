import csv
import os
import re

BOOK_FILE = "book.csv"

#ISBN-13 Check Digit Validation
def validate_isbn13(isbn: str) -> bool:
    isbn = isbn.replace("-", "").replace(" ", "")
    if not isbn.isdigit() or len(isbn) != 13:
        return False
    total = 0
    for i, digit in enumerate(isbn):
        weight = 1 if i % 2 == 0 else 3
        total += int(digit) * weight
    return total % 10 == 0

#Book ID Validation
def validate_book_id(book_id: str) -> bool:
    return bool(re.match(r"^[A-Za-z]{2}\d{2}", book_id))

#CSV Helpers
def load_books() -> list[dict]:
    if not os.path.exists(BOOK_FILE):
        return []
    with open(BOOK_FILE, "r", newline="", encoding="utf-8") as book_file:
        reader = csv.DictReader(book_file)
        return list(reader)

def save_books(books: list[dict]) -> None:
    fieldnames = ["book_id", "title", "isbn13", "author", "copies", "availability", "price"]
    with open(BOOK_FILE, "w", newline="", encoding="utf-8") as book_file:
        writer = csv.DictWriter(book_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)

def find_book(books: list[dict], book_id: str) -> dict | None:
    return next(
        (b for b in books if b["book_id"].upper() == book_id.upper()), None
    )


#Add Book
def add_book() -> None:
    books = load_books()

    print(f"\n ---Add Book---")

    #Book ID
    while True:
        book_id = input("Enter Book ID (2 letters + 2 digits, e.g. AB12): ").strip().upper()
        if not validate_book_id(book_id):
            print("Invalid Book ID.")
        elif find_book(books, book_id):
            print("Book ID is already in use.")
        else:
            break

    #ISBN-13
    while True:
        isbn = input("Enter ISBN: ").strip()
        if not validate_isbn13(isbn):
            print("Invalid ISBN.")
        else:
            break

    #Title
    while True:
        title = input("Enter Title: ").strip()
        if not re.fullmatch(r"[A-Za-z ]{1,20}", title):
            print("Invalid Title.")
        else:
            break

    #Author
    author = input("Enter Author: ").strip()

    #Copies
    while True:
        copies_str = input("Enter copies: ").strip()
        if copies_str in ("1", "2"):
            copies = int(copies_str)
            break
        print("Copies must be 1 or 2.")


    #Price
    while True:
        price_str = input("Enter Price: ").strip()
        try:
            price = round(float(price_str), 2)
            if price <= 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid Price. Enter a positive number with up to 2 decimals.")


    new_book = {
        "book_id": book_id,
        "title": title,
        "isbn13":isbn.replace("-", "").replace(" ", ""),
        "author": author,
        "copies": copies,
        "availability": copies,
        "price": price,
    }
    books.append(new_book)
    save_books(books)
    print(f"Book '{title}' added successfully.")

#View All Books

def view_books() -> None:
    books = load_books()
    if not books:
        print("\n No books found.")
        return

    print(f"\n ---Book List---")
    print(f"{'ID':<6} {'Title':<22} {'ISBN-13':<15} {'Author':<20} {'Copies':<7} {'Avail':<6} {'Price'}")
    print("-" * 85)
    for book in books:
        print(f"{book['book_id']:<6} {book['title']:<22} {book['isbn13']:<15} {book['author']:<20} {book['copies']:<7} {book['copies']:<7} {book['availability']:<6} {book.get('price', 'N/A')}")

#Search Book

def search_book() -> None:
    books = load_books()
    print(f"\n ---Search Books---")
    query = input("Enter Search Query: ").strip().lower()

    results = [
        book for book in books
        if query in book["book_id"].lower() or query in book["title"].lower()
    ]

    if not results:
        print("\n No matching books found.")

    else:
        print(f"\n{'ID':<6} {'Title':<22} {'ISBN-13':<15} {'Author':<20} {'Copies':<7} {'Avail'}")
        print("-" * 72)
        for book in results:
            print(f"{book['book_id']:<6} {book['title']:<22} {book['isbn13']:<15} {book['author']:<20} {book['availability']}")

#Edit Book
def edit_book() -> None:
    books = load_books()
    print(f"\n ---Edit Books---")
    book_id = input("Enter Book ID to edit: ").strip().upper()

    book = find_book(books, book_id)
    if not book:
        print("Book not found.")
        return

    print(f" Editing: {book['title']} (press Enter to keep current value")

    #Title
    new_title = input(f" Title [{book['title']}]: ").strip()
    if new_title:
        if not re.fullmatch(r"[A-Za-z]{1,20}", new_title):
            print("Invalid Title. Keeping Original")
        else:
            book["title"] = new_title


    #Author
    new_author = input(f" Author [{book['author']}]:  ").strip()
    if new_author:
        book["author"] = new_author

    #Copies
    new_copies = input(f" Copies [{book['copies']}]: ").strip()
    if new_copies:
        if new_copies in ("1", "2"):
            book["copies"] = int(new_copies)
            book["availability"] = int(new_copies)
        else:
            print("Invalid Copies. Enter 1 or 2.")

    #Price
    new_price = input(f" Price [{book.get('price', 'N/A')}]: ").strip()
    if new_price:
        try:
            book["price"] = round(float(new_price), 2)
        except ValueError:
            print("Invalid Price. Enter a positive number with up to 2 decimals.")



    save_books(books)
    print(" Book updated successfully.")

#Book Menu
def book_menu() -> None:
    while True:
        print("\n=== Book Management ===")
        print("1. Add Book")
        print("2. View All Books")
        print("3. Search Book")
        print("4. Edit Book")
        print("0. Back to Main Menu")
        choice = input("select option: ").strip()

        if choice == "1":
            add_book()
        elif choice == "2":
            view_books()
        elif choice == "3":
            search_book()
        elif choice == "4":
            edit_book()
        elif choice == "0":
            break
        else:
            print("Invalid Choice. Try again.")

