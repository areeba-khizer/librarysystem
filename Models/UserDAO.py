class UserDAO():
    def __init__(self, DAO):
        self.db = DAO
        self.db.table = "users"

    def list(self):
        users = self.db.query(
            "SELECT @table.id, @table.name, @table.email, @table.bio, @table.mob, @table.lock, "
            "@table.created_at, COUNT(reserve.book_id) AS books_owned "
            "FROM @table "
            "LEFT JOIN reserve ON reserve.user_id = @table.id "
            "GROUP BY @table.id, @table.name, @table.email, @table.bio, @table.mob, "
            "@table.lock, @table.created_at"
        ).fetchall()
        return users

    def getById(self, id):
        q = self.db.query("SELECT * FROM @table WHERE id='{}'".format(id))
        return q.fetchone()

    def getUsersByBook(self, book_id):
        q = self.db.query(
            "SELECT * FROM @table LEFT JOIN reserve ON reserve.user_id = @table.id "
            "WHERE reserve.book_id={}".format(book_id)
        )
        return q.fetchall()

    def getByEmail(self, email):
        q = self.db.query("SELECT * FROM @table WHERE email='{}'".format(email))
        return q.fetchone()

    def add(self, user):
        name = user['name']
        email = user['email']
        password = user['password']
        
        q = self.db.query(
            "INSERT INTO @table (name, email, password, bio, mob, `lock`) VALUES('{}', '{}', '{}', '', '', 0)".format(name, email, password)
        )
        self.db.commit()
        return q

    def update(self, user, _id):
        name = user['name']
        email = user['email']
        password = user['password']
        bio = user['bio']
        
        q = self.db.query(
            "UPDATE @table SET name='{}', email='{}', password='{}', bio='{}' WHERE id={}".format(
                name, email, password, bio, _id
            )
        )
        self.db.commit()
        return q

    def delete(self, user_id):
        q = self.db.query("DELETE FROM @table WHERE id={}".format(user_id))
        self.db.commit()
        return q
