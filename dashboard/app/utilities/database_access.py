import cryptography
import sqlalchemy
import pymysql

def construct_string(**kwargs):
    connector_type = kwargs.get('db')
    if kwargs.get('python_lib') is not None:
        connector_type  += '+' + kwargs.get('python_lib')

    credential = kwargs.get('username')
    if kwargs.get('password') is not None:
        credential += ':' + kwargs.get('password')
    
    database = kwargs.get('host') + ':' + str(kwargs.get('port')) + '/' + kwargs.get('db_name')
    connection_string = f'{connector_type}://{credential}@{database}'
    return connection_string

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        connection_string = construct_string(**kwargs)
        if connection_string not in cls._instances:
            cls._instances[connection_string] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[connection_string]


class Connector(metaclass=Singleton):
    
    def  __init__(self, db_name, username='root', password=None, db='mysql', host='localhost', port=3306, engine='pymysql'):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.python_lib = engine
        self.db = db
        self.engine = None
    
    @property
    def db_engine(self):
        if self.engine is None:
            connector_type = self.db
            if self.python_lib is not None:
                connector_type  += '+' + self.python_lib

            credential = self.username
            if self.password is not None:
                credential += ':' + self.password
            
            database = self.host + ':' + str(self.port) + '/' + self.db_name
            connection_string = f'{connector_type}://{credential}@{database}'
            self.engine = sqlalchemy.create_engine(connection_string)
    
        return self.engine