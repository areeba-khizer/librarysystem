from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

class DB(object):
    """Initialize MySQL database"""
    host = "localhost"
    user = "root"
    password = "root123"
    db = "lms"
    table = ""

    def __init__(self, app):
        app.config["MYSQL_DATABASE_HOST"] = self.host
        app.config["MYSQL_DATABASE_USER"] = self.user
        app.config["MYSQL_DATABASE_PASSWORD"] = self.password
        app.config["MYSQL_DATABASE_DB"] = self.db

        self.mysql = MySQL(app, cursorclass=DictCursor)

    def cur(self):
        """Returns a new database cursor."""
        return self.mysql.get_db().cursor()

    def query(self, q, params=None):
        """
        Executes a SQL query.
        :param q: SQL query string
        :param params: Optional query parameters (tuple/list/dict)
        :return: Cursor object
        """
        h = self.cur()
        
        if self.table:
            q = q.replace("@table", self.table)

        # Execute query with parameters if provided
        if params:
            h.execute(q, params)
        else:
            h.execute(q)

        return h

    def commit(self):
        """Commits the current transaction."""
        self.query("COMMIT;")
