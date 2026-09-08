#!/usr/bin/python

import os
from google import genai
import base64

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


def main():
    gemini_client = create_gemini_client()
    for file in os.listdir("invoices/"):
        invoice_ai_analysis = request_invoice_details(gemini_client, f"invoices/{file}")
        print(invoice_ai_analysis)
        if not validate_ai_response(invoice_ai_analysis): print(f"issue detected with file {file}")


if __name__ == "__main__":
    main()
