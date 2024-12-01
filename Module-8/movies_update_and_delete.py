#Jose Franco
#11/27/2024
#Assignment 8.2 - Movies: Update & Deletes.

import mysql.connector
from dotenv import dotenv_values

# Load environment variables
secrets = dotenv_values(".env")

# Database configuration
config = {
    'user': secrets["USER"],
    'password': secrets["PASSWORD"],
    'host': secrets["HOST"],
    'database': secrets["DATABASE"],
    'raise_on_warnings': secrets["RAISE_ON_WARNINGS"] == "TRUE",
}

# Function to display films
def show_films(cursor, title):
# Displays the films with details.
    cursor.execute("""
        SELECT 
            film.film_name AS Name, 
            film.film_director AS Director, 
            genre.genre_name AS Genre, 
            studio.studio_name AS Studio 
        FROM 
            film
        INNER JOIN genre ON film.genre_id = genre.genre_id
        INNER JOIN studio ON film.studio_id = studio.studio_id;
    """)
    films = cursor.fetchall()

    print(f"\n-- {title} --")
    for film in films:
        print(f"Film Name: {film[0]}\nDirector: {film[1]}\nGenre: {film[2]}\nStudio: {film[3]}\n")

# Main program
try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    # Reset database tables
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    cursor.execute("TRUNCATE TABLE film;")
    cursor.execute("TRUNCATE TABLE genre;")
    cursor.execute("TRUNCATE TABLE studio;")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    # Recreate genre and studio data
    cursor.execute("INSERT INTO genre (genre_name) VALUES ('Drama'), ('Horror'), ('SciFi');")
    cursor.execute("INSERT INTO studio (studio_name) VALUES ('Universal Pictures'), ('20th Century Fox'), ('Blumhouse Productions');")
    db.commit()

    # Insert clean film data without release date
    cursor.execute("""
        INSERT INTO film (film_name, film_director, genre_id, studio_id)
        VALUES 
        ('Gladiator', 'Ridley Scott', (SELECT genre_id FROM genre WHERE genre_name = 'Drama'), (SELECT studio_id FROM studio WHERE studio_name = 'Universal Pictures')),
        ('Alien', 'Ridley Scott', (SELECT genre_id FROM genre WHERE genre_name = 'SciFi'), (SELECT studio_id FROM studio WHERE studio_name = '20th Century Fox')),
        ('Get Out', 'Jordan Peele', (SELECT genre_id FROM genre WHERE genre_name = 'Horror'), (SELECT studio_id FROM studio WHERE studio_name = 'Blumhouse Productions'));
    """)
    db.commit()

    # Display initial films
    show_films(cursor, "DISPLAYING FILMS")

    # Insert a new film
    cursor.execute("""
        INSERT INTO film (film_name, film_director, genre_id, studio_id)
        VALUES ('Inception', 'Christopher Nolan', 
                (SELECT genre_id FROM genre WHERE genre_name = 'SciFi'), 
                (SELECT studio_id FROM studio WHERE studio_name = 'Universal Pictures'));
    """)
    db.commit()
    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")
    # Update Alien's genre
    cursor.execute("""
        UPDATE film
        SET genre_id = (SELECT genre_id FROM genre WHERE genre_name = 'Horror')
        WHERE film_name = 'Alien';
    """)
    db.commit()
    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE - Change Alien to Horror")

    # Delete Gladiator
    cursor.execute("DELETE FROM film WHERE film_name = 'Gladiator';")
    db.commit()
    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if cursor:
        cursor.close()
    if db:
        db.close()
