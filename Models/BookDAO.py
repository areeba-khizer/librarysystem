class BookDAO:
    def __init__(self, DAO):
        self.db = DAO
        self.db.table = "books"

    # ✅ Delete a book
    def delete(self, book_id):
        query = "DELETE FROM books WHERE id=%s;"
        self.db.query(query, (book_id,))
        self.db.commit()
        return "Book deleted successfully"

    # ✅ Reserve a book for a user
    def reserve(self, user_id, book_id):
        if not self.available(book_id):
            return "err_out"  # Book not available

        query = "INSERT INTO reserve (user_id, book_id) VALUES (%s, %s);"
        self.db.query(query, (user_id, book_id))
        
        # Decrease count of available books
        self.db.query("UPDATE books SET count = count - 1 WHERE id=%s;", (book_id,))
        self.db.commit()
        return "Book reserved successfully"

    # ✅ Get all books reserved by a user
    def getBooksByUser(self, user_id):
        query = """
        SELECT books.* FROM books 
        JOIN reserve ON reserve.book_id = books.id 
        WHERE reserve.user_id=%s;
        """
        return self.db.query(query, (user_id,)).fetchall()

    # ✅ Get count of books reserved by a user
    def getBooksCountByUser(self, user_id):
        query = """
        SELECT COUNT(reserve.book_id) AS books_count 
        FROM reserve 
        WHERE reserve.user_id=%s;
        """
        return self.db.query(query, (user_id,)).fetchone()

    # ✅ Get details of a single book by ID
    def getBook(self, book_id):
        query = "SELECT * FROM books WHERE id=%s;"
        return self.db.query(query, (book_id,)).fetchone()

    # ✅ Check if a book is available (count > 0)
    def available(self, book_id):
        book = self.getBook(book_id)
        return book and book.get('count', 0) > 0

    # ✅ List all available books
    def list(self, availability=1):
        query = "SELECT * FROM books"
        if availability == 1:
            query += " WHERE availability=%s"
            return self.db.query(query, (availability,)).fetchall()
        return self.db.query(query).fetchall()

    # ✅ Get reserved book IDs for a user
    def getReserverdBooksByUser(self, user_id):
        query="select concat(book_id,',') as user_books from reserve WHERE user_id={}".format(user_id)
        books = self.db.query(query)
        books = books.fetchone()
        return books

    # ✅ Search for books by name
    def search_book(self, name, availability=1):
        query = "SELECT * FROM books WHERE name LIKE %s"
        values = ("%{}%".format(name),)
        if availability == 1:
            query += " AND availability=%s"
            values += (availability,)
        return self.db.query(query, values).fetchall()

    # ✅ Add a new book
    def add_book(self, book_data):
        query = """
        INSERT INTO books (name, count, availability, `desc`, author, edition) 
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        values = (
            book_data['name'],  
            book_data['count'],  
            book_data['availability'],  
            book_data['desc'],  
            book_data['author'],  
            book_data['edition']  
        )
        self.db.query(query, values)
        self.db.commit()
        return "Book added successfully"

    # ✅ Update book details
    def update_book(self, book_id, book_data):
        # Ensure 'name' is not None or empty
        if not book_data.get('name'):
            return "Error: Book name cannot be empty"

        query = """
        UPDATE books 
        SET name=%s, count=%s, availability=%s, `desc`=%s, author=%s, edition=%s
        WHERE id=%s;
        """
        values = (
            book_data.get('name'),  
            book_data.get('count', 0),  # Default to 0 if missing
            book_data.get('availability', 1),  # Default to 1 if missing
            book_data.get('desc', ''),  # Default to empty string
            book_data.get('author', ''),  # Default to empty string
            book_data.get('edition', ''),  # Default to empty string
            book_id  
        )
        
        self.db.query(query, values)
        self.db.commit()
        return "Book updated successfully"

    # ✅ Increase book count when returned
    def return_book(self, book_id, user_id):
        # Check if book was actually reserved
        reserved_check = "SELECT * FROM reserve WHERE book_id=%s AND user_id=%s;"
        reservation = self.db.query(reserved_check, (book_id, user_id)).fetchone()
        if not reservation:
            return "No reservation found"

        # Remove reservation
        query = "DELETE FROM reserve WHERE book_id=%s AND user_id=%s;"
        self.db.query(query, (book_id, user_id))

        # Increase count in books table
        self.db.query("UPDATE books SET count = count + 1 WHERE id=%s;", (book_id,))
        self.db.commit()
        return "Book returned successfully"
