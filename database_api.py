#!/usr/bin/python

from flask import Flask, request
import mysql.connector
import os

app = Flask(__name__)


my_database_connector = mysql.connector.connect(
    host="localhost",
    user="mysql",
    password=os.environ["MYSQL_USER_DB_PASSWORD"],
    database="accounting"
)
my_database_cursor = my_database_connector.cursor()


@app.route("/add-invoice", methods=["POST"])
def default_route():
    incoming_payload = request.get_json()
    if request.method == "POST":
        if (incoming_payload["invoice_number"] and
        incoming_payload["seller"] and
        incoming_payload["buyer"] and 
        incoming_payload["issue_date"] and 
        incoming_payload["total_amount"]):
            sql_query="INSERT INTO invoices (invoice_id, seller, buyer, issued_date, total_amount) VALUES (%s, %s, %s, %s, %s)"
            values = tuple(incoming_payload.values())
            my_database_cursor.execute(sql_query, values)
            my_database_connector.commit()
            return "record added to the database", 200
        else: return "bad request", 400


if __name__ == "__main__":
    app.run(host="localhost", port="5000", debug=False)