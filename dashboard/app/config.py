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

IMG_URLS = {
    'moonahoshinova': 'https://hololive.hololivepro.com/wp-content/uploads/2022/04/%E3%83%A0%E3%83%BC%E3%83%8A-1.png',
    'kureijiollie': 'https://hololive.hololivepro.com/wp-content/uploads/2021/11/kureiji_ollie_thumb-2.png.png',
    'kobokanaeru': 'https://hololive.hololivepro.com/wp-content/uploads/2022/03/3_%E3%81%93%E3%81%BC%E3%83%BB%E3%81%8B%E3%81%AA%E3%81%88%E3%82%8B.png'
}