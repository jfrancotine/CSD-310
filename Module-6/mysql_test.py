import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values


secrets = dotenv_values(".env")

# Database configuration
config = {
    'user': secrets["USER"],     
    'password': secrets["PASSWORD"],
    'host': secrets["HOST"],
    'database': secrets["DATABASE"],
    'raise_on_warnings': secrets["RAISE_ON_WARNINGS"] == "TRUE",
}

try:
    # Establish connection
    db = mysql.connector.connect(**config)

    print("\n Database user {} connected to MySQL on host {} with database {}" .format(secrets["USER"], secrets["HOST"], secrets["DATABASE"]))

    input("\n\n Press any key to continue...")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist")

    else:
        print(err)

finally:
    db.close()
