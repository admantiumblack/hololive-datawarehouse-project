import os

DB_PARAM = {
    'db_name': os.environ['DB_NAME'], 
    'username': os.environ['DB_USER'],
    'password': os.environ['DB_PASS'],
    'db': os.environ['DB'],
    'host': os.environ['DB_HOST'],
    'port': os.environ['DB_PORT'],
    'engine': os.environ['DB_ENGINE']
}