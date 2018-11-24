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
             (ID TEXT PRIMARY KEY     NOT NULL,
             USERNAME           TEXT    NOT NULL,
             PUBLICKEY            TEXT     NOT NULL);''')
    print("Table created successfully")

    conn.close()
