from Models.DAO import DAO as dao

# Initialize DAO
DAO = None


def initialize_dao(application):
    global DAO
    if DAO is None:
        DAO = dao(application)
    return DAO