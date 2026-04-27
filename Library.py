from Book import book_menu
from Student import student_menu
from Transaction import issue_book
from Transaction import return_book
from Graph import graph_menu
# Main Menu

def main():
    print("=" * 40)
    print("Library Management System")
    print("=" * 40)

    while True:
        print("\n---Main Menu---")
        print("1. Book Management")
        print("2. Student Management")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. View trend Graph")
        print("0. Exit")

        choice = input("Select option: ").strip()

        if choice == "1":
            book_menu()
        elif choice == "2":
            student_menu()
        elif choice == "3":
            issue_book()
        elif choice == "4":
            return_book()
        elif choice in ("5",):
            graph_menu()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. try again.")

if __name__ == "__main__":
    main()