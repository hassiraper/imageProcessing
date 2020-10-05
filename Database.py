import sys
import sqlite3
import jsonpickle
from flask import Flask, request, Response, make_response
import requests
import json

class Database:
    dataBase_name = 'Data.db'

    def __init__(self):
        print('In Database class')

        pass

    def check_time(self, name):
        try:
            record = []
            conn = sqlite3.connect(self.dataBase_name)
            sql = 'SELECT * from userdb WHERE name = ?'
            cur = conn.cursor()
            cur.execute(sql,[(name)])
            rows = cur.fetchall()
            for row in rows:
                record.append(row)
            print(record)
            conn.commit()
            cur.close()
            conn.close()
            return  record
        except Exception as error:
            print('Error in fetching Users {}'.format(error))

    def Updatetime(self, name, hour, min, day, mon, year ):
        try:
            conn = sqlite3.connect(self.dataBase_name)
            cursor = conn.cursor()
            cursor.execute(""" UPDATE userdb SET _hour = ?, _min = ? , date_day = ?, date_month = ?, date_year = ? WHERE  name = ? 
                                       """, (hour, min, day, mon, year, name))
            conn.commit()
            cursor.close()
            conn.close()
            return True
            pass
        except Exception as error:
            print('ERROR in UPDATING  : {}'.format(error))
            return False
        pass

    def Insertuser(self,name):
        try:
            str_name = str(name)
            hour = 0
            min = 0
            day = 0
            mon = 0
            year = 0


            conn = sqlite3.connect(self.dataBase_name)
            cursor = conn.cursor()

            cursor.execute("""
                               CREATE TABLE IF NOT EXISTS userdb
                               (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                               name TEXT, 
                               _hour INTEGER ,
                               _min INTEGER,
                               date_day INTEGER,
                               date_month INTEGER,
                               date_year INTEGER
                                )""")

            cursor.execute(""" INSERT INTO userdb 
                               (name, _hour, _min, date_day, date_month, date_year)
                           VALUES 
                           (?,?,?,?,?,?)
                           """, (str_name, hour, min, day, mon, year))

            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as ex:
            print('Error in Data base: Inserting Student Values {}'.format(ex))
            return False






