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


def get_books_from_db(category: str = None) -> list:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="alex",
        password="1234",
        dbname="postgres"
    )

    with conn.cursor() as cursor:
        if not category:
            cursor.execute("""
                        SELECT books.title as book_title, categories.title, authors.name FROM books
            JOIN books_categories on books_categories.book_id = books.id
            JOIN categories on categories.id = books_categories.categories_id
            JOIN authors on authors.id = books.author_id
                        """)

            result = cursor.fetchall()
        else:
            cursor.execute("""
            SELECT books.title as book_title, categories.title, authors.name FROM books
JOIN books_categories on books_categories.book_id = books.id
JOIN categories on categories.id = books_categories.categories_id
JOIN authors on authors.id = books.author_id
WHERE lower(categories.title) = lower(%s)
            """, (category, ))

            result = cursor.fetchall()

    conn.close()

    return result


def get_all_categories():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="alex",
        password="1234",
        dbname="postgres"
    )

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM categories")

        result = cursor.fetchall()

    conn.close()

    return result


def save_book(title, author, category):
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="alex",
        password="1234",
        dbname="postgres"
    )

    # Проверка и получение автора
    with conn.cursor() as cursor:
        cursor.execute("SELECT * from authors WHERE name = (%s)", (author, ))

        result = cursor.fetchone()

        if result:
            author_id = result[0]
        else:
            cursor.execute("INSERT INTO authors (name) VALUES (%s)", (author,))

            cursor.execute("SELECT * from authors WHERE name = (%s)", (author,))
            result = cursor.fetchone()
            author_id = result[0]

    # Проверка и получение жанра
    with conn.cursor() as cursor:
        cursor.execute("SELECT * from categories WHERE title = (%s)", (category, ))

        result = cursor.fetchone()

        if result:
            category_id = result[0]
        else:
            cursor.execute("INSERT INTO categories (title) VALUES (%s)", (category, ))

            cursor.execute("SELECT * from categories WHERE title = (%s)", (category,))
            result = cursor.fetchone()
            category_id = result[0]

    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO books (title, author_id) VALUES (%s, %s)", (title, author_id))

        cursor.execute("SELECT * from books WHERE title = (%s) and author_id = (%s)", (title, author_id))

        result = cursor.fetchone()

        book_id = result[0]

        cursor.execute("INSERT INTO books_categories (book_id, categories_id) VALUES (%s, %s)", (book_id, category_id))

    conn.commit()
    conn.close()

    return book_id


def add_category_to_book(book_id, category):
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="alex",
        password="1234",
        dbname="postgres"
    )

    # Проверка и получение жанра
    with conn.cursor() as cursor:
        cursor.execute("SELECT * from categories WHERE title = (%s)", (category, ))

        result = cursor.fetchone()

        if result:
            category_id = result[0]
        else:
            cursor.execute("INSERT INTO categories (title) VALUES (%s)", (category,))

            cursor.execute("SELECT * from categories WHERE title = (%s)", (category,))
            result = cursor.fetchone()
            category_id = result[0]

    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO books_categories (book_id, categories_id) VALUES (%s, %s)", (book_id, category_id))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    get_books_from_db()
