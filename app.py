from flask import Flask, render_template, request
import mysql.connector
from num2words import num2words
import os

app = Flask(__name__)


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "number_project"),
        port=3306
    )
    


@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        number = int(request.form["number"])

        # Convert number into words
        result = num2words(number).title().replace("-", " ")  +    "  Only "

        # Save number and words into MySQL
        db = get_connection()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO number_words (number_value, word_value) VALUES (%s, %s)",
            (number, result)
        )

        db.commit()

        cursor.close()
        db.close()

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)