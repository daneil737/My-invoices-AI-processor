#!/usr/bin/python

import os
from google import genai
import base64
import requests
from datetime import datetime
import logging


# Creates file containing logs from script run
def create_script_logger():
	logger = logging.getLogger(__name__)
	time = datetime.now().strftime("%d.%m.%y_%H:%M")
	logging.basicConfig(filename=f'logs/invoice_processor_{time}.log', level=logging.INFO)
	logger.info('Logging started')
	return logger


# Creation of Google Gemini client
def create_gemini_client():
    return genai.Client(api_key=os.environ["GEMINI_API_KEY"])


# File is read and encoded, later it will be sent with prompt to Gemini
def encode_invoice_file(invoice_file_name):
    with open(invoice_file_name, "rb") as file:
        invoice_file = file.read()
    invoice_b64 = base64.b64encode(invoice_file).decode("utf-8")
    return invoice_b64


# Prompt with encoded file are sent to Gemini
def request_invoice_details(gemini_client_object, invoice_file_name):
    invoice_to_read = encode_invoice_file(invoice_file_name)
    
    # Program works with both pdf and jpg files
    if ".jpg" in invoice_file_name:
        file_type = {"type": "image", "mime_type": "image/jpeg"}
    elif ".pdf" in invoice_file_name:
        file_type = {"type": "document", "mime_type": "application/pdf"}
    else:
        raise TypeError("Unsupported file type")


    prompt_text = '''
    Extract following data from the attached invoice: invoice number, the seller,
    the buyer (or the issuer), when was it issued and what is the total price. Return the output
    in given order with values separated by commas. The date format should be yyyy-mm-dd. The 
    people/companies which issue and who receive the invoice are never the same ones.
    The price must not contain any spaces, the decimal point has to be a dot.
    '''
    
    interaction = gemini_client_object.interactions.create(
        model = "gemini-3.5-flash-lite",
        input = [
            {
                "type": "text",
                "text": prompt_text
            },{
                "type": file_type["type"],
                "data": invoice_to_read,
                "mime_type": file_type["mime_type"]
            }
        ]
    )

    return interaction.output_text


# Validation of response, some field may not be read by Gemini or it may be missing
# in invoice. Function converts response to list of bools and if any of these is False
# (ie. empty value) then the function returns False.
def validate_ai_response(ai_response):
    return (False not in [(x != " ") for x in ai_response.split(",")])


# Posting invoice data to database
def send_invoice_data_to_database(invoice_data):
    invoice_data_list = [data.strip() for data in invoice_data.split(",")]
    payload = {
	    "invoice_number" : invoice_data_list[0], 
	    "seller" : invoice_data_list[1], 
	    "buyer" : invoice_data_list[2], 
	    "issued_date" : invoice_data_list[3], 
	    "total_amount" : invoice_data_list[4]
    }

    sql_server_path = "http://127.0.0.1:5000/add-invoice"

    request_response = requests.post(sql_server_path, json=payload)
    return request_response


# This function is responsible for whole invoice processing ie. reading invoice
# data with Gemini AI, validating data and sending the data to database, it prints out
# the result
def process_invoice(invoice_file_name):
    invoice_ai_analysis = request_invoice_details(gemini_client, f"invoices/{invoice_file_name}")
    if not validate_ai_response(invoice_ai_analysis):
        script_logger.error(f"failed to process invoice: {invoice_file_name} correctly, invoice data: {invoice_ai_analysis}")
    else:
        send_invoice_response = send_invoice_data_to_database(invoice_ai_analysis)
        if send_invoice_response.status_code == 200:
            script_logger.info(f"invoice {invoice_file_name} added successfully to the database")
        else:
            script_logger.error(f"invoice {invoice_file_name} was not added to the database: {send_invoice_response.text}")
            

# Processing all invoices in given path
def process_all_invoices(invoices_directory_path):
    for file in os.listdir(invoices_directory_path):
        process_invoice(file)


def main():
    global gemini_client
    gemini_client = create_gemini_client()

    global script_logger
    script_logger = create_script_logger()

    process_all_invoices("invoices/")

if __name__ == "__main__":
    main()
