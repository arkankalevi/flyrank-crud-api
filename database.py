import sqlite3


DATABASE_NAME = "tasks.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM tasks")
    task_count = cursor.fetchone()[0]

    if task_count == 0:
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Learn FastAPI", 0),
                ("Build CRUD API", 0),
                ("Read FlyRank assignment", 1),
            ]
        )

    connection.commit()
    connection.close()