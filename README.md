## My invoices AI processor

This project is an invoice-processing tool that reads PDF/JPG invoices scans, sends each file to Google Gemini AI model (using google-genai free tier client) to extract structured fields (invoice number, seller, buyer, issue date, total) and provides a simple Flask endpoint to store validated invoice records into a MySQL database.

This script uses a set of both exemplary and real invoices. Exemplary invoices were downloaded from repositories https://github.com/femstac/Sample-Pdf-invoices and https://github.com/mouadhamri/invoice_dataset, while the real invoices were issued to me (I changed the address on them however).

Below is a video showing how the invoice processor works.

[![Watch the video](https://img.youtube.com/vi/jo3Q1GJ5JgI/0.jpg)](https://www.youtube.com/watch?v=_jo3Q1GJ5JgI)
