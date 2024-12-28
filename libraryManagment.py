import json
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

# Console instance
console = Console()

# Models
class Book:
    def __init__(self, isbn, title, author, genre, stock):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.genre = genre
        self.stock = stock

    def update_stock(self, count):
        self.stock += count

    def to_dict(self):
        return {
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "stock": self.stock,
        }

class Member:
    def __init__(self, member_id, name, contact, membership_type):
        self.member_id = member_id
        self.name = name
        self.contact = contact
        self.membership_type = membership_type
        self.borrowed_books = []

    def borrow_book(self, book):
        if book.stock > 0:
            self.borrowed_books.append((book, datetime.now()))
            book.update_stock(-1)
            return True
        return False

    def return_book(self, isbn):
        for book, borrowed_date in self.borrowed_books:
            if book.isbn == isbn:
                self.borrowed_books.remove((book, borrowed_date))
                book.update_stock(1)
                overdue_days = max(0, (datetime.now() - borrowed_date).days - 14)
                return overdue_days
        return None

    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "contact": self.contact,
            "membership_type": self.membership_type,
            "borrowed_books": [
                {"isbn": book[0].isbn, "borrowed_date": book[1].isoformat()} #YYYY-MM-DD
                for book in self.borrowed_books
            ],
        }

class Library:
    def __init__(self):
        self.books = []
        self.members = []
        self.transactions = []

    def add_book(self, book):
        self.books.append(book)

    def delete_book(self, isbn):
        self.books = [book for book in self.books if book.isbn != isbn]

    def register_member(self, member):
        self.members.append(member)

    def remove_member(self, member_id):
        self.members = [member for member in self.members if member.member_id != member_id]

    def issue_book(self, member_id, isbn):
        member = next((m for m in self.members if m.member_id == member_id), None)
        book = next((b for b in self.books if b.isbn == isbn), None)

        if member and book and member.borrow_book(book):
            self.transactions.append(f"{member.name} borrowed [bright_blue]{book.title}[/bright_blue] on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return True
        return False

    def return_book(self, member_id, isbn):
        member = next((m for m in self.members if m.member_id == member_id), None)
        book = next((b for b in self.books if b.isbn == isbn), None)

        if member and book:
            overdue_days = member.return_book(isbn)
            if overdue_days is not None:
                self.transactions.append(f"{member.name} returned {book.title} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                return overdue_days
        return None

    def save_data(self):
        with open('library_data.json', 'w') as file:
            data = {
                "books": [book.to_dict() for book in self.books],
                "members": [member.to_dict() for member in self.members],
                "transactions": self.transactions,
            }
            json.dump(data, file, indent=4)

    def load_data(self):
        try:
            with open('library_data.json', 'r') as file:
                data = json.load(file)
                self.books = [Book(**book) for book in data.get("books", [])]
                self.members = []
                for member_data in data.get("members", []):
                    member = Member(
                        member_id=member_data["member_id"],
                        name=member_data["name"],
                        contact=member_data["contact"],
                        membership_type=member_data["membership_type"],
                    )
                    for borrowed in member_data.get("borrowed_books", []):
                        book = next((b for b in self.books if b.isbn == borrowed["isbn"]), None)
                        if book:
                            borrowed_date = datetime.fromisoformat(borrowed["borrowed_date"])
                            member.borrowed_books.append((book, borrowed_date))
                    self.members.append(member)
                self.transactions = data.get("transactions", [])
        except FileNotFoundError:
            pass

# Main function
def main():
    library = Library()
    library.load_data()

    while True:
        console.print(Panel.fit(
            "[bold yellow]Library Management System[/bold yellow]\n"
            "1. Add Book\n"
            "2. Delete Book\n"
            "3. Register Member\n"
            "4. Remove Member\n"
            "5. Issue Book\n"
            "6. Return Book\n"
            "7. View Transactions\n"
            "8. View Available Books\n"
            "9. View Registered Members\n"
            "10. Exit",
            title="Select operation", style="bright_yellow"))

        choice = Prompt.ask("Enter your choice", choices=[str(i) for i in range(1, 11)])

        if choice == '1':
            isbn = Prompt.ask("Enter ISBN")
            title = Prompt.ask("Enter Title")
            author = Prompt.ask("Enter Author")
            genre = Prompt.ask("Enter Genre")
            stock = int(Prompt.ask("Enter Stock"))
            library.add_book(Book(isbn, title, author, genre, stock))
            console.print("[bold green]Book added successfully![/bold green]")

        elif choice == '2':
            isbn = Prompt.ask("Enter ISBN of the book to delete")
            library.delete_book(isbn)
            console.print("[bold green]Book deleted successfully![/bold green]")

        elif choice == '3':
            member_id = Prompt.ask("Enter Member ID")
            name = Prompt.ask("Enter Name")
            contact = Prompt.ask("Enter Contact")
            membership_type = Prompt.ask("Enter Membership Type")
            library.register_member(Member(member_id, name, contact, membership_type))
            console.print("[bold green]Member registered successfully![/bold green]")

        elif choice == '4':
            member_id = Prompt.ask("Enter Member ID to remove")
            library.remove_member(member_id)
            console.print("[bold green]Member removed successfully![/bold green]")

        elif choice == '5':
            member_id = Prompt.ask("Enter Member ID")
            isbn = Prompt.ask("Enter Book ISBN")
            if library.issue_book(member_id, isbn):
                console.print("[bold green]Book issued successfully![/bold green]")
            else:
                console.print("[bold red]Issue failed. Check member ID or book availability.[/bold red]")

        elif choice == '6':
            member_id = Prompt.ask("Enter Member ID")
            isbn = Prompt.ask("Enter Book ISBN")
            overdue_days = library.return_book(member_id, isbn)
            if overdue_days is not None:
                console.print(f"[bold green]Book returned successfully! Overdue by {overdue_days} days.[/bold green]")
            else:
                console.print("[bold red]Return failed. Check member ID or book details.[/bold red]")

        elif choice == '7':
            console.print("\n[bold cyan]Transactions:[/bold cyan]")
            if library.transactions:
                for transaction in library.transactions:
                    console.print(transaction)
            else:
                console.print("[bold yellow]No transactions recorded yet.[/bold yellow]")

        elif choice == '8':
            console.print("\n[bold cyan]Available Books:[/bold cyan]")
            if library.books:
                table = Table(title="Available Books")
                table.add_column("ISBN", style="cyan")
                table.add_column("Title", style="bright_yellow")
                table.add_column("Author", style="yellow")
                table.add_column("Genre", style="green")
                table.add_column("Stock", justify="right", style="red")

                for book in library.books:
                    table.add_row(book.isbn, book.title, book.author, book.genre, str(book.stock))
                console.print(table)
            else:
                console.print("[bold yellow]No books are available in the library.[/bold yellow]")

        elif choice == '9':
            console.print("\n[bold cyan]Registered Members:[/bold cyan]")
            if library.members:
                table = Table(title="Registered Members")
                table.add_column("Member ID", style="cyan")
                table.add_column("Name", style="magenta")
                table.add_column("Contact", style="yellow")
                table.add_column("Membership Type", style="green")
                table.add_column("Borrowed Books", style="red")

                for member in library.members:
                    member_details = member.to_dict()
                    borrowed_books = ', '.join(book['isbn'] for book in member_details['borrowed_books']) if member_details['borrowed_books'] else 'None'
                    table.add_row(member_details['member_id'], member_details['name'], member_details['contact'], member_details['membership_type'], borrowed_books)
                console.print(table)
            else:
                console.print("[bold yellow]No members are registered in the library.[/bold yellow]")

        elif choice == '10':
            library.save_data()
            console.print("[bold green]Data saved. Goodbye![/bold green]")
            break

if __name__ == "__main__":
    main()
