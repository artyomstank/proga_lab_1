class Author:
    def __init__(self, name, birthdate):
        self.name = name
        self.birthdate = birthdate

    def __str__(self):
        return f"{self.name} (born {self.birthdate})"


class Book:
    def __init__(self, title, author, price):
        self.title = title
        self.author = author  # объект класса Author
        self.price = price

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

    def __str__(self):
        return self.username


class Order:
    def __init__(self, user, book):
        self.user = user
        self.book = book

    def __str__(self):
        return f"Order of '{self.book.title}' by {self.user.username}"


# База данных
authors = []
books = []
users = []
orders = []


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


def list_books():
    if not books:
        print("No books available.")
        return
    for book in books:
        print(book)


def list_users():
    if not users:
        print("No users available.")
        return
    for user in users:
        print(user)


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


def list_purchased_books():
    username = input("Enter username: ")
    user = next((u for u in users if u.username == username), None)
    if user is None:
        print("User not found.")
        return

    print(f"Purchased books by {user.username}:")
    print(user.list_purchased_books())


def list_orders():
    if not orders:
        print("No orders placed yet.")
        return
    for order in orders:
        print(order)


def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Add Author")
        print("2. Add Book")
        print("3. Add User")
        print("4. List Books")
        print("5. List Users")
        print("6. Purchase Book")
        print("7. List Purchased Books")
        print("8. List Orders")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_author()
        elif choice == "2":
            add_book()
        elif choice == "3":
            add_user()
        elif choice == "4":
            list_books()
        elif choice == "5":
            list_users()
        elif choice == "6":
            purchase_book()
        elif choice == "7":
            list_purchased_books()
        elif choice == "8":
            list_orders()
        elif choice == "9":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
