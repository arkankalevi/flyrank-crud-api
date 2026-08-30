import os

import psycopg
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg.connect(DATABASE_URL)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT FALSE
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM tasks")
    task_count = cursor.fetchone()[0]

    if task_count == 0:
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (%s, %s)",
            [
                ("Learn FastAPI", False),
                ("Build CRUD API", False),
                ("Read FlyRank assignment", True),
            ]
        )

    connection.commit()
    cursor.close()
    connection.close()


def get_all_tasks():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "done": bool(row[2])
        }
        for row in rows
    ]


def get_task_by_id(task_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "title": row[1],
        "done": bool(row[2])
    }


def create_task(title):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id",
        (title, False)
    )

    task_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return {
        "id": task_id,
        "title": title,
        "done": False
    }


def update_task(task_id, title=None, done=None):
    connection = get_connection()
    cursor = connection.cursor()

    if title is not None and done is not None:
        cursor.execute(
            "UPDATE tasks SET title = %s, done = %s WHERE id = %s",
            (title, done, task_id)
        )
    elif title is not None:
        cursor.execute(
            "UPDATE tasks SET title = %s WHERE id = %s",
            (title, task_id)
        )
    elif done is not None:
        cursor.execute(
            "UPDATE tasks SET done = %s WHERE id = %s",
            (done, task_id)
        )

    if cursor.rowcount == 0:
        cursor.close()
        connection.close()
        return None

    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )

    row = cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    return {
        "id": row[0],
        "title": row[1],
        "done": bool(row[2])
    }


def delete_task(task_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = %s",
        (task_id,)
    )

    if cursor.rowcount == 0:
        connection.close()
        return False

    connection.commit()
    cursor.close()
    connection.close()

    return True