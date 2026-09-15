import sqlite3


connection = sqlite3.connect('warnings.db')

cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS warnings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        reason TEXT NOT NULL
    )
""")

connection.commit()
connection.close()


def add_warning(user_id, reason):
    connection = sqlite3.connect('warnings.db')
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO warnings (user_id, reason) VALUES (?, ?)",
        (user_id, reason)
    )

    connection.commit()
    connection.close()


def get_warnings(user_id):
    connection = sqlite3.connect('warnings.db')
    cursor = connection.cursor()

    cursor.execute(
        "SELECT reason FROM warnings WHERE user_id = ?",
        (user_id,)
    )

    results = cursor.fetchall()

    connection.close()

    return results

def remove_warning(user_id):
    connection = sqlite3.connect('warnings.db')
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM warnings
        WHERE id = (
            SELECT id
            FROM warnings
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 1
        )
        """,
        (user_id,)
    )

    removed = cursor.rowcount

    connection.commit()
    connection.close()

    return removed