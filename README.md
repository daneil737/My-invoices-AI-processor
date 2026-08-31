## My invoices AI processor

This project is an invoice-processing tool that reads PDF/JPG invoices scans, sends each file to Google Gemini AI model (using google-genai free tier client) to extract structured fields (invoice number, seller, buyer, issue date, total) and provides a simple Flask endpoint to store validated invoice records into a MySQL database.
