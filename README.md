# Library Management System: Detailed Explanation

## Overview
The Library Management System is a Python program designed to manage books, members, and transactions in a library. It allows users to perform operations such as adding/deleting books, registering/removing members, issuing/returning books, and viewing transactions and available books.

This explanation details every component of the code, including classes, methods, and logic used in the system.

---

## Libraries and Modules Used

### 1. `json`
Used to save and load data to/from a file in JSON format. This ensures data persistence across program runs.

### 2. `datetime`
Provides functionality to handle dates and times, specifically for tracking when books are borrowed and calculating overdue days.

### 3. `rich`
Used for a visually appealing console interface. Includes:
   - `Console`: Prints styled text to the console.
   - `Table`: Displays data in tabular format.
   - `Panel`: Displays bordered panels for messages.
   - `Prompt`: Takes user input with specific options.

---

## Classes and Methods

### 1. **`Book` Class**
Represents a book in the library.

#### Attributes:
- `isbn`: The book's unique identifier (string).
- `title`: Title of the book (string).
- `author`: Author's name (string).
- `genre`: Book's genre (string).
- `stock`: Number of copies available (integer).

#### Methods:
- **`__init__(isbn, title, author, genre, stock)`**: Constructor to initialize book details.
- **`update_stock(count)`**: Updates the stock of the book by adding/subtracting a given count.
- **`to_dict()`**: Converts book details to a dictionary for JSON serialization.

---

### 2. **`Member` Class**
Represents a library member.

#### Attributes:
- `member_id`: Unique identifier for the member (string).
- `name`: Member's name (string).
- `contact`: Member's contact information (string).
- `membership_type`: Membership type (string).
- `borrowed_books`: List of tuples containing borrowed books and their borrow dates.

#### Methods:
- **`__init__(member_id, name, contact, membership_type)`**: Constructor to initialize member details.
- **`borrow_book(book)`**:
  - Adds the book to the member's borrowed books list if it is in stock.
  - Decreases the book's stock.
  - Returns `True` if successful, `False` otherwise.
- **`return_book(isbn)`**:
  - Removes a book from the member's borrowed books list.
  - Increases the book's stock.
  - Calculates overdue days if the book is returned late (beyond 14 days).
  - Returns `None` if the book is not found.
- **`to_dict()`**: Converts member details to a dictionary for JSON serialization.

---

### 3. **`Library` Class**
Handles the core functionality of the library system.

#### Attributes:
- `books`: List of `Book` objects in the library.
- `members`: List of `Member` objects.
- `transactions`: List of transaction logs (strings).

#### Methods:
- **`__init__()`**: Initializes empty lists for books, members, and transactions.

- **`add_book(book)`**: Adds a `Book` object to the library.

- **`delete_book(isbn)`**: Removes a book from the library based on its ISBN.

- **`register_member(member)`**: Adds a `Member` object to the library.

- **`remove_member(member_id)`**: Removes a member from the library based on their member ID.

- **`issue_book(member_id, isbn)`**:
  - Finds the member and book by their IDs.
  - Allows the member to borrow the book if available.
  - Logs the transaction.
  - Returns `True` if successful, `False` otherwise.

- **`return_book(member_id, isbn)`**:
  - Finds the member and book by their IDs.
  - Allows the member to return the book.
  - Logs the transaction.
  - Calculates overdue days if applicable.
  - Returns `None` if the operation fails.

- **`save_data()`**:
  - Saves books, members, and transactions to a JSON file (`library_data.json`).
  - Uses `to_dict()` methods of `Book` and `Member` classes for serialization.

- **`load_data()`**:
  - Loads books, members, and transactions from a JSON file (`library_data.json`).
  - Reconstructs `Book` and `Member` objects from the saved data.

---

## Main Program Logic
The program provides a menu-driven interface for users to interact with the library system.

### Menu Options
1. **Add Book**: Prompts the user to enter book details and adds the book to the library.
2. **Delete Book**: Deletes a book based on its ISBN.
3. **Register Member**: Prompts the user to enter member details and registers the member.
4. **Remove Member**: Removes a member based on their member ID.
5. **Issue Book**: Issues a book to a member if it is available.
6. **Return Book**: Processes a book return and calculates overdue days if applicable.
7. **View Transactions**: Displays a list of all transactions.
8. **View Available Books**: Displays all books currently in the library.
9. **View Registered Members**: Displays all registered members and their borrowed books.
10. **Exit**: Saves data to the JSON file and exits the program.

---

## Input and Output
- **Input**: User provides data via prompts.
- **Output**: Styled messages and tables using `rich` library.

### Example Execution
#### Adding a Book:
1. User selects option `1`.
2. Enters details (ISBN, title, author, genre, stock).
3. The book is added, and a success message is displayed.

#### Viewing Books:
1. User selects option `8`.
2. A table of available books is displayed.

---

## Data Persistence
The program uses `library_data.json` to save and load data. This ensures that books, members, and transactions persist across program runs.

---

## Key Features
1. **Data Persistence**: Saves and loads data automatically.
2. **Dynamic Menu**: Provides user-friendly choices.
3. **Rich Library**: Enhances console output.
4. **Overdue Calculation**: Tracks overdue days for returned books.
5. **Error Handling**: Prevents invalid operations like issuing unavailable books.

---

## How to Run the Program
1. Save the code to a file (e.g., `libraryManager.py`).
2. Ensure the `rich` library is installed (`pip install rich`).
3. Run the script using Python (`python libraryManager.py`).

---

## Future Improvements
1. Add authentication for users.
2. Implement search functionality for books and members.
3. Enhance overdue fine calculations.
4. Add graphical user interface (GUI).

