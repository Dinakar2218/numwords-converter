from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from num2words import num2words
import os

app = Flask(__name__)


# MySQL Connection
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "number_project")
    )


@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    entered_number = None

    # Convert Number
    if request.method == "POST":

        entered_number = int(request.form["number"])

        result = (
            num2words(entered_number)
            .title()
            .replace("-", " ")
            + " Only"
        )

        # Save into MySQL
        db = get_connection()
        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO number_words
            (number_value, word_value)
            VALUES (%s, %s)
            """,
            (entered_number, result)
        )

        db.commit()
        cursor.close()
        db.close()

    # Get conversion history
    db = get_connection()
    cursor = db.cursor()

    cursor.execute(
        """
        SELECT id, number_value, word_value
        FROM number_words
        ORDER BY id DESC
        """
    )

    history = cursor.fetchall()

    # Total conversions
    total = len(history)

    cursor.close()
    db.close()

    return render_template(
        "index.html",
        result=result,
        entered_number=entered_number,
        history=history,
        total=total
    )


# Clear History
@app.route("/clear", methods=["POST"])
def clear_history():

    db = get_connection()
    cursor = db.cursor()

    cursor.execute("DELETE FROM number_words")

    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)