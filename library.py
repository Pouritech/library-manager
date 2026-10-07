import json
import os
from datetime import date, timedelta

FILE_NAME = "books.json"
LOAN_DAYS = 14
MEMBERS_FILE = "members.json"

FILE_NAME = "books.json"


def load_books():
    """خواندن کتاب‌ها از فایل"""
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)


def save_books(books):
    """ذخیره کتاب‌ها در فایل"""
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)


def load_members():
    if not os.path.exists(MEMBERS_FILE):
        return []
    with open(MEMBERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_members(members):
    with open(MEMBERS_FILE, "w", encoding="utf-8") as f:
        json.dump(members, f, ensure_ascii=False, indent=2)

def add_book(books):
    title = input("Book title: ").strip()
    author = input("Author: ").strip()
    if not title or not author:
        print("Title and author cannot be empty.")
        return
    book_id = max([b["id"] for b in books], default=0) + 1
    books.append(
        {
            "id": book_id,
            "title": title,
            "author": author,
            "available": True,
            "due_date": None,
            "borrowed_by": None,
        }
    )
    save_books(books)
    print(f"Book added with ID {book_id}.")


def list_books(books, members=None):
    if not books:
        print("No books in the library.")
        return
    print("\nID | Title | Author | Status")
    print("-" * 60)
    for b in books:
        if b["available"]:
            status = "Available"
        else:
            name = "Unknown"
            if members:
                m = find_member(members, b.get("borrowed_by"))
                if m:
                    name = m["name"]
            status = f'Borrowed by {name} (due {b.get("due_date")})'
        print(f'{b["id"]} | {b["title"]} | {b["author"]} | {status}')


def search_books(books):
    keyword = input("Search by title or author: ").strip().lower()
    results = [
        b
        for b in books
        if keyword in b["title"].lower() or keyword in b["author"].lower()
    ]
    if not results:
        print("No matching books found.")
        return
    list_books(results)


def borrow_book(books, members):
    try:
        book_id = int(input("Book ID to borrow: "))
        member_id = int(input("Member ID: "))
    except ValueError:
        print("Please enter valid numbers.")
        return

    member = find_member(members, member_id)
    if member is None:
        print("Member not found.")
        return

    for b in books:
        if b["id"] == book_id:
            if b["available"]:
                b["available"] = False
                b["borrowed_by"] = member_id
                b["due_date"] = (date.today() + timedelta(days=LOAN_DAYS)).isoformat()
                save_books(books)
                print(f'Book borrowed by {member["name"]}. Due date: {b["due_date"]}')
            else:
                print("This book is already borrowed.")
            return
    print("Book not found.")


def return_book(books):
    try:
        book_id = int(input("Book ID to return: "))
    except ValueError:
        print("Please enter a valid number.")
        return
    for b in books:
        if b["id"] == book_id:
            if not b["available"]:
                b["available"] = True
                b["due_date"] = None
                b["borrowed_by"] = None
                save_books(books)
                print("Book returned.")
            else:
                print("This book was not borrowed.")
            return
    print("Book not found.")


def delete_book(books):
    try:
        book_id = int(input("Book ID to delete: "))
    except ValueError:
        print("Please enter a valid number.")
        return
    for b in books:
        if b["id"] == book_id:
            books.remove(b)
            save_books(books)
            print("Book deleted.")
            return
    print("Book not found.")


def list_overdue(books):
    today = date.today().isoformat()
    overdue = [
        b
        for b in books
        if not b["available"] and b.get("due_date") and b["due_date"] < today
    ]
    if not overdue:
        print("No overdue books.")
        return
    print("\nOverdue books:")
    for b in overdue:
        print(f'{b["id"]} | {b["title"]} | due {b["due_date"]}')


def add_member(members):
    name = input("Member name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    member_id = max([m["id"] for m in members], default=0) + 1
    members.append({"id": member_id, "name": name})
    save_members(members)
    print(f"Member added with ID {member_id}.")


def list_members(members):
    if not members:
        print("No members yet.")
        return
    print("\nID | Name")
    print("-" * 30)
    for m in members:
        print(f'{m["id"]} | {m["name"]}')


def find_member(members, member_id):
    for m in members:
        if m["id"] == member_id:
            return m
    return None


def main():
    books = load_books()
    members = load_members()
    while True:
        print("\n=== Library Manager ===")
        print("1. Add book")
        print("2. List books")
        print("3. Search books")
        print("4. Borrow book")
        print("5. Return book")
        print("6. Delete book")
        print("7. Show overdue books")
        print("8. Add member")
        print("9. List members")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_book(books)
        elif choice == "2":
            list_books(books, members)
        elif choice == "3":
            search_books(books)
        elif choice == "4":
            borrow_book(books, members)
        elif choice == "5":
            return_book(books)
        elif choice == "6":
            delete_book(books)
        elif choice == "7":
            list_overdue(books)
        elif choice == "8":
            add_member(members)
        elif choice == "9":
            list_members(members)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
