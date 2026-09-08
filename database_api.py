#!/usr/bin/python

from flask import Flask, request
import mysql.connector
import os
import re

app = Flask(__name__)

# Connection to MySql database
my_database_connector = mysql.connector.connect(
    host="localhost",
    user="mysql",
    password=os.environ["MYSQL_USER_DB_PASSWORD"],
    database="accounting"
)
my_database_cursor = my_database_connector.cursor()

# Incoming data validation
# invoice numbers, seller, buyer and total amount have to be strings with correct lenghts
# issued date must be in correct format, also it must have correct values
def validate_invoice_data(invoice_data):
    issue_year, issue_month, issue_day = invoice_data["issued_date"].split("-")
    return ((len(invoice_data["invoice_number"]) > 0 and len(invoice_data["invoice_number"]) < 20) and
        (len(invoice_data["seller"]) > 0 and len(invoice_data["seller"]) < 50) and
        (len(invoice_data["buyer"]) > 0 and len(invoice_data["buyer"]) < 50) and
        (re.search("\\d{4}-\\d{2}-\\d{2}", invoice_data["issued_date"]) is not None and
        (int(issue_year) > 1990 and int(issue_year) < 2050) and
        (int(issue_month) > 0 and int(issue_month) < 13) and
        (int(issue_day) > 0 and int(issue_month) < 32)) and
        (len(invoice_data["total_amount"]) > 0 and len(invoice_data["total_amount"]) < 130))


# Handling adding invoice
# the request must have request "/add-invoice" path and use POST request
@app.route("/add-invoice", methods=["POST"])
def default_route():
    incoming_payload = request.get_json()
    if request.method == "POST":
        if validate_invoice_data(incoming_payload):
            sql_query="INSERT INTO invoices (invoice_id, seller, buyer, issued_date, total_amount) VALUES (%s, %s, %s, %s, %s)"
            values = tuple(incoming_payload.values())
            try:
                my_database_cursor.execute(sql_query, values)
                my_database_connector.commit()
            except mysql.connector.IntegrityError:
                return "bad request", 400
            return "record added to the database", 200
        else: return "bad request", 400


if __name__ == "__main__":
    app.run(host="localhost", port="5000", debug=False)
