import sqlite3

class db_connection:
    '''Provides an interface to a given sqlite3 database'''
    def __init__(self,database_reference):
        self.db = sqlite3.connect(database_reference)
        self.cursor = self.db.cursor()
    
    def query(self,sql_query,parameters):
        self.cursor.execute(sql_query,parameters)
        result = self.cursor.fetchall()
        return result

sql_query = """SELECT locus_id FROM gene_lists WHERE list_name=?;"""
database_file="GeneListDB.db"
db = db_connection(database_file)
l = db.query(sql_query,['blasing2005_rhythmic'])