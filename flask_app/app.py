# docker-compose build
# docker-compose up -d postgres
# docker-compose up -d flask_app


import psycopg2
from flask import Flask

app = Flask(__name__)

# Define a route that connects to PostgreSQL
@app.route('/query_db')
def query_db():
    try:
        connection = psycopg2.connect(
            database="mydatabase",
            user="myuser",
            password="mypassword",
            host="postgres",  # Use the Docker service name
            port="5432"  # Use the PostgreSQL container port
        )
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM your_table_name")
        records = cursor.fetchall()

        # Process records here

    except (Exception, psycopg2.Error) as error:
        print("Error:", error)

    finally:
        if connection:
            cursor.close()
            connection.close()

    return "Query result here"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
