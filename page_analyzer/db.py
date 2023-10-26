import psycopg2
import psycopg2.extras


def create_connection(db_url):
    return psycopg2.connect(db_url)


def close_connection(connection):
    connection.close()


def get_url_by_name(connection, name):
    with connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM urls WHERE name = %s', (name,))
        return cursor.fetchone()


def add_url(connection, name, current_date):
    with connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s)',
                       (name, current_date))
        connection.commit()


def get_url(connection, id):
    with connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute('SELECT * FROM urls WHERE id = %s', (id,))
        return cursor.fetchone()


def get_url_checks(connection, id):
    with connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute(
            'SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC',
            (id,))
        return cursor.fetchall()


def get_urls(connection):
    with connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute(
            '''SELECT DISTINCT ON (urls.id) urls.id, name,
            url_checks.created_at, url_checks.status_code
            FROM urls
            LEFT JOIN url_checks ON urls.id = url_checks.url_id
            ORDER BY urls.id DESC, url_checks.id DESC;''')
        return cursor.fetchall()


def add_url_check(connection, id, status_code, h1, title, description,
                  current_date):
    with connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor) as cursor:
        cursor.execute(
            '''INSERT INTO url_checks (url_id, status_code, h1,
            title, description, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)''',
            (id, status_code,
             h1.string if h1 else None,
             title.string if title else None,
             description['content'] if description else None,
             current_date))
        connection.commit()
