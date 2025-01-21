import pyodbc

def db_connection():
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=(localdb)\\MSSQLLocalDB;'
        'DATABASE=Restaurant;'
        'Trusted_Connection=yes;'
    )
    return connection
