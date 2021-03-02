# fileuploader-rmq-docker-ocr
This project aims to demonstrate the structure of a semi-complete system.
Everything starts with an HTTP POST request with a file and the user credentials in it.
The system accepts the request, authenticate the user, then stores the file and registers the job 
in RMQ. Preprocesses it, then proceed it to the OCR (Tesseract), where the graphical information gets
extracted. 

The fileserver is just an Ubuntu server image, running as a VM.

![flowchart](https://user-images.githubusercontent.com/23174259/109699923-72b6f780-7b91-11eb-9ff5-5f199c8635be.jpg)
