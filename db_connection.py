import sqlite3

class db_connection:
    '''Provides an interface to a given sqlite3 database.
    
    Note that this is intended only to extract data - not to modify the db.'''
    def __init__(self,database_reference):
        self.db = sqlite3.connect(database_reference)
        self.cursor = self.db.cursor()
    
    def query(self,sql_query,parameters):
        self.cursor.execute(sql_query,parameters)
        result = self.cursor.fetchall()
        return result