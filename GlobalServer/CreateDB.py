#!/usr/bin/python

import sqlite3



def initDatabase():
    conn = sqlite3.connect('securedropbox.db')
    print("Opened database successfully")

    conn.execute('''CREATE TABLE IF NOT EXISTS USER
             (USERNAME TEXT PRIMARY KEY     NOT NULL,
             PUBLICKEY           TEXT    NOT NULL,
             IP            TEXT     ,
             OTP        TEXT,
             OTPDATE         REAL  ,
             IPDATE          REAL  );''')
    print("Table created successfully")

    conn.execute('''CREATE TABLE IF NOT EXISTS DEVICE
             (ID INTEGER PRIMARY KEY    AUTOINCREMENT,
             USERNAME           TEXT    NOT NULL,
             PUBLICKEY            TEXT     NOT NULL);''')
    print("Table created successfully")

    conn.close()
