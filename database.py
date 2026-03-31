import mysql.connector

def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Isaiah21',
        database='job_tracker'
    )