#!/usr/bin/python

import os
from google import genai
import base64


def create_gemini_client():
    return genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def encode_invoice_file(invoice_file_name):
    with open(invoice_file_name, "rb") as file:
        invoice_file = file.read()
    invoice_b64 = base64.b64encode(invoice_file).decode("utf-8")
    return invoice_b64


def request_invoice_details(gemini_client_object, invoice_file_name):
    invoice_to_read = encode_invoice_file(invoice_file_name)
    if ".jpg" in invoice_file_name:
        file_type = {"type": "image", "mime_type": "image/jpeg"}
    elif ".pdf" in invoice_file_name:
        file_type = {"type": "document", "mime_type": "application/pdf"}
    else:
        raise TypeError("Unsupported file type")


    prompt_text = '''
    Extract following data from the attached invoice: invoice number, the seller,
    the buyer (or the issuer), when was it issued and what is the total price. Return the output
    in given order with values separated by commas. The date format should be dd.mm.yyyy. The 
    people/companies which issue and who receive the invoice are never the same ones.
    The price should not contain any commas or any spaces.
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


def main():
    gemini_client = create_gemini_client()
    for file in os.listdir("invoices/"):
        print(request_invoice_details(gemini_client, f"invoices/{file}"))


if __name__ == "__main__":
    main()