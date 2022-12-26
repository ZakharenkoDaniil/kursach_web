from utils.db_utils import create_tables, fill_words
from web_server import app

if __name__ == "__main__":
    create_tables()
    #fill_words()
    app.run()
