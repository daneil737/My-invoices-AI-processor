# My invoices AI processor

This project is an invoice-processing tool that reads PDF/JPG invoices scans, sends each file to Google Gemini AI model (using google-genai free tier client) to extract structured fields (invoice number, seller, buyer, issue date, total) and provides a simple Flask endpoint to store validated invoice records into a MySQL database.

This script uses a set of both exemplary and real invoices. Exemplary invoices were downloaded from repositories https://github.com/femstac/Sample-Pdf-invoices and https://github.com/mouadhamri/invoice_dataset, while the real invoices were issued to me (I changed the address on them however).

Below is a video showing how the invoice processor works.

[![Watch the video](https://img.youtube.com/vi/jo3Q1GJ5JgI/0.jpg)](https://www.youtube.com/watch?v=jo3Q1GJ5JgI)

## Running the script
### Client side
```
./main.py
```
or
```
python3 main.py
```
### Server side
```
./database_api.py
```
or
```
python3 database_api.py
```
The database needs to have user with password created (in this case it is user mysql).
```
mariadb -u mysql -p -h localhost

```
All invoices files have to be placed in "invoices" directory.
Project was created in Linux-based environment (EndeavourOS).
MariaDB is MySQL database port adapted to Arch-based Linux distributions.

## Script features
- searches folder for invoices in both jpg and pdf format
- converts read file into base64 encoded format
- attaches encoded file to prompt which is sent to Google Gemini
- validates all fields - checks if all data were read correctly
- sends data into database using POST request with all fields being stored in JSON format
- server validates incoming data (eg. if data is in correct format and if string data are not longer than maximum allowed length in database) and responds with error code if needed
- script creates logs which can be traced if script starts failing

## Requirements
- google
- logging
- base64
- flask
- mysql
