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
    cursor = db.cursor()

    print("\n-- DISPLAYING Studio RECORDS --")
    cursor.execute("SELECT studio_id, studio_name FROM studio;")
    for studio_id, studio_name in cursor.fetchall():
        print(f"Studio ID: {studio_id}\nStudio Name: {studio_name}\n")

    print("\n-- DISPLAYING Genre RECORDS --")
    cursor.execute("SELECT genre_id, genre_name FROM genre;")
    for genre_id, genre_name in cursor.fetchall():
        print(f"Genre ID: {genre_id}\nGenre Name: {genre_name}\n")

    print("\n-- DISPLAYING Short Film RECORDS --")
    cursor.execute("SELECT movie_name, runtime FROM movies WHERE runtime < 120;")
    for movie_name, runtime in cursor.fetchall():
        print(f"Film Name: {movie_name}\nRuntime: {runtime}\n")

    print("\n-- DISPLAYING Director RECORDS in Order --")
    cursor.execute("SELECT movie_name, director FROM movies  ORDER BY director ASC, runtime DESC;")
    for movie_name, director in cursor.fetchall():
        print(f"Film Name: {movie_name}\nDirector: {director}\n")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist")
    else:
        print(err)
finally:
    db.close()

