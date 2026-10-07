import json
import os

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


def add_book(books):
    title = input("Book title: ").strip()
    author = input("Author: ").strip()
    if not title or not author:
        print("Title and author cannot be empty.")
        return
    book_id = max([b["id"] for b in books], default=0) + 1
    books.append({
        "id": book_id,
        "title": title,
        "author": author,
        "available": True,
    })
    save_books(books)
    print(f"Book added with ID {book_id}.")


def list_books(books):
    if not books:
        print("No books in the library.")
        return
    print("\nID | Title | Author | Status")
    print("-" * 40)
    for b in books:
        status = "Available" if b["available"] else "Borrowed"
        print(f'{b["id"]} | {b["title"]} | {b["author"]} | {status}')


def search_books(books):
    keyword = input("Search by title or author: ").strip().lower()
    results = [
        b for b in books
        if keyword in b["title"].lower() or keyword in b["author"].lower()
    ]
    if not results:
        print("No matching books found.")
        return
    list_books(results)


def borrow_book(books):
    try:
        book_id = int(input("Book ID to borrow: "))
    except ValueError:
        print("Please enter a valid number.")
        return
    for b in books:
        if b["id"] == book_id:
            if b["available"]:
                b["available"] = False
                save_books(books)
                print("Book borrowed.")
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


def main():
    books = load_books()
    while True:
        print("\n=== Library Manager ===")
        print("1. Add book")
        print("2. List books")
        print("3. Search books")
        print("4. Borrow book")
        print("5. Return book")
        print("6. Delete book")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_book(books)
        elif choice == "2":
            list_books(books)
        elif choice == "3":
            search_books(books)
        elif choice == "4":
            borrow_book(books)
        elif choice == "5":
            return_book(books)
        elif choice == "6":
            delete_book(books)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()