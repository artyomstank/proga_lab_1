import json
import os


class Author:
    def __init__(self, name, birthdate):
        self.name = name
        self.birthdate = birthdate

    def to_dict(self):
        return {"name": self.name, "birthdate": self.birthdate}

    @staticmethod
    def from_dict(data):
        return Author(data["name"], data["birthdate"])

    def __str__(self):
        return f"{self.name} (born {self.birthdate})"


class Book:
    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

    def to_dict(self):
        return {"title": self.title, "author": self.author.name, "price": self.price}

    @staticmethod
    def from_dict(data, authors):
        author = next((a for a in authors if a.name == data["author"]), None)
        return Book(data["title"], author, data["price"]) if author else None

    def __str__(self):
        return f"'{self.title}' by {self.author.name}, ${self.price}"


class User:
    def __init__(self, username):
        self.username = username
        self.purchased_books = []

    def purchase_book(self, book):
        self.purchased_books.append(book)

    def list_purchased_books(self):
        if not self.purchased_books:
            return "No purchased books yet."
        return "\n".join([str(book) for book in self.purchased_books])

    def to_dict(self):
        return {
            "username": self.username,
            "purchased_books": [book.title for book in self.purchased_books],
        }

    @staticmethod
    def from_dict(data, books):
        user = User(data["username"])
        user.purchased_books = [b for b in books if b.title in data["purchased_books"]]
        return user

    def __str__(self):
        return self.username


class Order:
    def __init__(self, user, book):
        self.user = user
        self.book = book

    def to_dict(self):
        return {"user": self.user.username, "book": self.book.title}

    @staticmethod
    def from_dict(data, users, books):
        user = next((u for u in users if u.username == data["user"]), None)
        book = next((b for b in books if b.title == data["book"]), None)
        return Order(user, book) if user and book else None

    def __str__(self):
        return f"Order of '{self.book.title}' by {self.user.username}"


# База данных
authors = []
books = []
users = []
orders = []

# Файлы для хранения данных
DATA_FILES = {
    "authors": "authors.json",
    "books": "books.json",
    "users": "users.json",
    "orders": "orders.json",
}


def save_data():
    with open(DATA_FILES["authors"], "w") as f:
        json.dump([author.to_dict() for author in authors], f)

    with open(DATA_FILES["books"], "w") as f:
        json.dump([book.to_dict() for book in books], f)

    with open(DATA_FILES["users"], "w") as f:
        json.dump([user.to_dict() for user in users], f)

    with open(DATA_FILES["orders"], "w") as f:
        json.dump([order.to_dict() for order in orders], f)

    print("Data saved to files.")


def load_data():
    global authors, books, users, orders

    def load_json(filename):
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            with open(filename, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    print(f"Error: Could not decode JSON from {filename}. File might be corrupted.")
                    return []
        return []

    authors_data = load_json(DATA_FILES["authors"])
    books_data = load_json(DATA_FILES["books"])
    users_data = load_json(DATA_FILES["users"])
    orders_data = load_json(DATA_FILES["orders"])

    authors = [Author.from_dict(data) for data in authors_data]
    books = [Book.from_dict(data, authors) for data in books_data if Book.from_dict(data, authors)]
    users = [User.from_dict(data, books) for data in users_data]
    orders = [Order.from_dict(data, users, books) for data in orders_data]

    print("Data loaded from files.")

def add_author():
    name = input("Enter author name: ")
    birthdate = input("Enter author birthdate: ")
    author = Author(name, birthdate)
    authors.append(author)
    print(f"Author '{name}' added.")


def add_book():
    if not authors:
        print("No authors available. Add an author first.")
        return
    title = input("Enter book title: ")
    author_name = input("Enter author name: ")
    price = float(input("Enter book price: "))

    author = next((a for a in authors if a.name == author_name), None)
    if author is None:
        print("Author not found.")
        return

    book = Book(title, author, price)
    books.append(book)
    print(f"Book '{title}' added.")


def add_user():
    username = input("Enter username: ")
    user = User(username)
    users.append(user)
    print(f"User '{username}' added.")


def purchase_book():
    username = input("Enter username: ")
    user = next((u for u in users if u.username == username), None)
    if user is None:
        print("User not found.")
        return

    book_title = input("Enter book title: ")
    book = next((b for b in books if b.title == book_title), None)
    if book is None:
        print("Book not found.")
        return

    user.purchase_book(book)
    order = Order(user, book)
    orders.append(order)
    print(f"Book '{book.title}' purchased by {user.username}.")


def main_menu():
    load_data()
    while True:
        print("\nMain Menu:")
        print("1. Add Author")
        print("2. Add Book")
        print("3. Add User")
        print("4. Purchase Book")
        print("5. Save Data")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_author()
        elif choice == "2":
            add_book()
        elif choice == "3":
            add_user()
        elif choice == "4":
            purchase_book()
        elif choice == "5":
            save_data()
        elif choice == "6":
            save_data()
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
