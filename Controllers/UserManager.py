from App.User import User

class UserManager:
    def __init__(self, DAO):
        self.db = DAO.db  # Explicitly define db
        self.user = User(self.db.user)  # Pass db reference
        self.book = self.db.book
        self.dao = self.user.dao  # Assign dao for user operations

    def getById(self, id):
        return self.dao.getById(id)  # Use dao to fetch user

    def delete(self, id):
        return self.dao.delete(id)  # Ensure delete function exists in DAO

    def list(self):
        user_list = self.dao.list()
        return user_list  # Ensure proper indentation

    def signin(self, email, password):
        user = self.dao.getByEmail(email)
        if user is None:
            return False

        user_pass = user['password']  # Retrieve stored password
        if user_pass != password:
            return False

        return user  # Return user object if authentication is successful

    def signout(self):
        self.user.signout()  # Ensure `signout()` method exists in `User`

    def get(self, id):
        return self.dao.getById(id)  # Fetch user by ID

    def signup(self, name, email, password):
        user = self.dao.getByEmail(email)
        if user is not None:
            return "already_exists"

        user_info = {"name": name, "email": email, "password": password}
        new_user = self.dao.add(user_info)

        return new_user  # Return newly created user

    def update(self, name, email, password, bio, id):
        user_info = {"name": name, "email": email, "password": password, "bio": bio}
        updated_user = self.dao.update(user_info, id)
        return updated_user  # Return updated user

    def getBooksList(self, id):
        return self.book.getBooksByUser(id)  # Fetch books linked to a user

    def getUsersByBook(self, book_id):
        return self.dao.getUsersByBook(book_id)  # Fetch users associated with a book
