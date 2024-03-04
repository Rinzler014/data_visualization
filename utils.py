import pymssql as msql


def get_connection():
    
    #Create connection to the database
    connection = msql.connect(
            server="animals014.database.windows.net",
            user="ricardo_gonzalez",
            password="Peluche343@",
            database="AnimalsDBL",
    )

    cur = connection.cursor()
    
    return cur