from flask import Flask
from dao_instance import initialize_dao
from Misc.functions import ago

application = Flask(__name__)
application.secret_key = '#$ab9&^BB00_.'

initialize_dao(application)
from routes.user import user_view  # noqa: E402
from routes.book import book_view  # noqa: E402
from routes.admin import admin_view  # noqa: E402


# Registering custom functions to be used within templates
application.jinja_env.globals.update(
ago=ago,
str=str,
)

# Registering blueprints
application.register_blueprint(user_view)
application.register_blueprint(book_view)
application.register_blueprint(admin_view)

if __name__ == "__main__":
    application.debug = True
    application.run()
