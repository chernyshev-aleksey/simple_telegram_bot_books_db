import psycopg2


def create_databases() -> None:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="alex",
        password="1234",
        dbname="postgres"
    )

    with conn.cursor() as cursor:
        cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
	id serial PRIMARY KEY,
    name varchar(500) NOT NULL,
	author varchar(500)
 );   
        """)

    conn.commit()
    conn.close()


def save_data(name: str, author: str):
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="alex",
        password="1234",
        dbname="postgres"
    )

    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO books (name, author) VALUES ((%s), (%s));", (name, author))

    conn.commit()
    conn.close()


def get_books_from_db() -> list:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="alex",
        password="1234",
        dbname="postgres"
    )

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM books")

        result = cursor.fetchall()

    conn.commit()
    conn.close()

    return result


if __name__ == "__main__":
    get_books_from_db()
