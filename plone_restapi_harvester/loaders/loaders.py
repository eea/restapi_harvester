import os


class Loader:
    def read(self, identifier):
        raise NotImplemented


class FSLoader(Loader):
    def read(self, identifier):
        with open(identifier) as f:
            return f.read()


class PostgresLoader(Loader):
    def read(self, identifier):
        """
        Details about document storage needed to set the correct the SQL sentence
        """
        try:
            import psycopg2
        except:
            raise Exception("Install python-psycopg2")
        DB_HOST = os.get("DB_HOST")
        DB_PORT = os.get("DB_PORT", 5432)
        DB_DOCUMENT_TABLENAME = os.get("DB_DOCUMENT_TABLENAME")
        DB_NAME = os.get("DB_NAME")
        DB_USERNAME = os.get("DB_USERNAME")
        DB_PASSWORD = os.get("DB_PASSWORD")
        try:
            conn = psycopg2.connect(
                database=DB_NAME,
                user=DB_USERNAME,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
            )
        except:
            raise Exception("Can't connect to database. Review settings")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM %s WHERE id=%s", (DB_DOCUMENT_TABLENAME, identifier)
        )
        return cursor.fetchone()
