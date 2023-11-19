import sqlite3
import os


class Database:
    def __init__(self, db_name: str | None, temp_db_name: str = "bot_test"):
        cwd = os.getcwd()

        os.makedirs(f"{cwd}/database/db", exist_ok=True)

        if db_name is None or db_name == "":
            self.db_path = f"{cwd}/database/db/{temp_db_name}.db"
        else:
            self.db_path = f"{cwd}/database/db/{db_name}.db"

        self.get_connection = lambda: sqlite3.connect(self.db_path)
